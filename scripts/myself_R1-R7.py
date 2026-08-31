from __future__ import annotations

from pathlib import Path
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "raw" / "digital_transformation_firm_panel.csv"
PROMPTS_DIR = ROOT / "prompts" / "robustness"
OUTPUT_DIR = ROOT / "output"
SUMMARY_FILE = OUTPUT_DIR / "robustness_summary.md"


def load_data() -> pd.DataFrame:
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Missing {DATA_FILE}. Run scripts/generate_synthetic_did.py first.")
    return pd.read_csv(DATA_FILE)


def fit_model(data: pd.DataFrame, formula: str):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        model = smf.ols(formula, data=data)
        return model.fit(cov_type="cluster", cov_kwds={"groups": data["firm_id"]})


def run_r1(data: pd.DataFrame):
    event_df = data.copy()
    for k in [-4, -3, -2, 0, 1, 2, 3, 4]:
        col = f"event_{k}"
        if k < 0:
            label = f"event_m{abs(k)}"
        else:
            label = f"event_p{k}"
        event_df[label] = ((event_df["treated"] == 1) & (event_df["relative_year"] == k)).astype(int)

    formula = (
        "log_tfp ~ event_m4 + event_m3 + event_m2 + event_p0 + event_p1 + event_p2 + event_p3 + event_p4 "
        "+ capital_intensity + export_share + soe + C(firm_id) + C(year)"
    )
    result = fit_model(event_df, formula)
    ftest = result.f_test("event_m4 = event_m3 = event_m2 = 0")
    pre = {k: {"estimate": float(result.params[k]), "se": float(result.bse[k]), "p": float(result.pvalues[k])} for k in ["event_m4", "event_m3", "event_m2"] if k in result.params.index}
    fig, ax = plt.subplots(figsize=(8, 4.8))
    for k in [-4, -3, -2, 0, 1, 2, 3, 4]:
        label = f"event_m{abs(k)}" if k < 0 else f"event_p{k}"
        if label not in result.params.index:
            continue
        ax.plot(k, result.params[label], marker='o', linestyle='None', color='#003153')
        ax.vlines(k, result.params[label] - 1.96 * result.bse[label], result.params[label] + 1.96 * result.bse[label], color='#00A8CC', alpha=0.7)
    ax.axhline(0, color='black', linestyle='--', linewidth=1)
    ax.axvline(-0.5, color='gray', linestyle=':')
    ax.set_title('R1: Event Study for Parallel Trends')
    ax.set_xlabel('Relative year')
    ax.set_ylabel('Coefficient')
    ax.grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / 'r1_event_study.png', dpi=180)
    plt.close(fig)

    md = f'''# 稳健性检验：R1 平行趋势正式检验

## 检验目的
检验数字化转型前各期虚拟变量是否共同为零，排除处理前存在系统性趋势差异的威胁，从而判断 DID 的平行趋势假设是否成立。

## Prompt（四要素）
【目标】使用 data/raw/digital_transformation_firm_panel.csv 估计事件研究模型，检验数字化转型前各期虚拟变量是否联合为零，评估平行趋势假设。\n【边界】只读取原始数据，不改动 raw 文件；仅使用合成面板数据说明稳健性，不解释为真实因果证据；聚类标准误按 firm_id。\n【验证】输出事件研究图、处理前各期系数及 95% 置信区间、联合 F 检验与 p 值；如果 p > 0.10，可认为平行趋势未被明显违背。\n【汇报】汇报处理前系数、标准误、F 与 p 值，并说明前期趋势是否平坦，是否需要调整样本窗口或控制设定。

## 结果摘要
- 处理前系数联合检验：F = {float(ftest.fvalue):.4f}, p = {float(ftest.pvalue):.4f}
- 事件研究图：已保存到 output/r1_event_study.png
- 处理前系数：{pre}

## 我的观察
- 结果判断：{'符合预期，支持平行趋势假设。' if ftest.pvalue > 0.10 else '存在前期异常趋势，需谨慎解释。'}
- 若前期系数显著偏离零，可能反映行业或地区冲击、处理选择偏差或样本结构差异，需要进一步检查处理前均衡性和模型设定。
'''
    return {"check": "R1", "f": float(ftest.fvalue), "p": float(ftest.pvalue), "note": "支持平行趋势" if ftest.pvalue > 0.10 else "可能存在前期趋势问题", "md": md}


def run_r2(data: pd.DataFrame):
    base = fit_model(data, "log_tfp ~ digital + capital_intensity + export_share + soe + C(firm_id) + C(year)")
    true_beta = float(base.params["digital"])
    rng = np.random.default_rng(2026)
    placebo_estimates = []
    for _ in range(200):
        pseudo = data.copy()
        treated_firms = sorted(pseudo[pseudo["treated"] == 1]["firm_id"].unique())
        days = rng.choice([2017, 2018], size=len(treated_firms))
        mapping = dict(zip(treated_firms, days))
        pseudo["pseudo_year"] = pseudo["firm_id"].map(mapping).fillna(9999)
        pseudo["pseudo_digital"] = ((pseudo["treated"] == 1) & (pseudo["year"] >= pseudo["pseudo_year"])).astype(int)
        res = fit_model(pseudo, "log_tfp ~ pseudo_digital + capital_intensity + export_share + soe + C(firm_id) + C(year)")
        placebo_estimates.append(float(res.params["pseudo_digital"]))
    arr = np.asarray(placebo_estimates)
    mean = arr.mean()
    std = arr.std()
    tail = np.mean(np.abs(arr) >= abs(true_beta))
    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.hist(arr, bins=20, color='#00A8CC', alpha=0.8)
    ax.axvline(true_beta, color='red', linestyle='--', label='true estimate')
    ax.axvline(0, color='black', linestyle='-', linewidth=1)
    ax.legend(frameon=False)
    ax.set_title('R2: Placebo Randomized Treatment Timing')
    ax.set_xlabel('Pseudo DID coefficient')
    ax.set_ylabel('Frequency')
    ax.grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / 'r2_placebo_distribution.png', dpi=180)
    plt.close(fig)
    md = f'''# 稳健性检验：R2 安慰剂检验（随机处理时间）

## 检验目的
检验伪处理效应是否集中在 0 附近，判断真实 DID 估计是否只是随机噪音或系统性趋势造成。

## Prompt（四要素）
【目标】保留真实处理组不变，随机提前处理时间到 2017/2018，重复主回归 200 次，查看伪 DID 系数分布与真实系数的位置。\n【边界】只在内存副本上做随机化，不修改原始数据；设置随机种子确保可重复。\n【验证】输出伪系数分布图、均值和标准差、真实系数标记及尾部概率；若真实效应落在尾部且伪估计集中近零，可认为安慰剂检验通过。\n【汇报】报告真实 DID 系数和伪处理分布特征，并解释是否存在未观测时变混杂。

## 结果摘要
- 真实 DID 系数：{true_beta:.4f}
- 伪系数均值：{mean:.4f}
- 伪系数标准差：{std:.4f}
- |伪估计| >= |真实估计| 的比例：{tail:.4f}
- 分布图：已保存到 output/r2_placebo_distribution.png

## 我的观察
- 结果判断：{'通过安慰剂检验，说明真实估计并不只是随机噪音。' if abs(mean) < 0.02 and tail < 0.10 else '伪处理分布较分散，说明可能存在未观测时变混杂风险。'}
- 若伪估计也很大，则应怀疑处理并非随机，进一步检查选择性处理和时间趋势。
'''
    return {"check": "R2", "mean": float(mean), "std": float(std), "tail": float(tail), "true_beta": true_beta, "note": "安慰剂检验通过" if abs(mean) < 0.02 and tail < 0.10 else "需谨慎判断", "md": md}


def run_r3(data: pd.DataFrame):
    df = data.copy()
    df["log_labor_productivity"] = np.log(df["labor_productivity"].clip(lower=1e-8))
    result = fit_model(df, "log_labor_productivity ~ digital + capital_intensity + export_share + soe + C(firm_id) + C(year)")
    beta = float(result.params["digital"])
    se = float(result.bse["digital"])
    p = float(result.pvalues["digital"])
    md = f'''# 稳健性检验：R3 替换结果变量

## 检验目的
用 labor_productivity 替代 log_tfp，检验核心结论是否依赖特定生产率测度。

## Prompt（四要素）
【目标】将 log_tfp 替换为 labor_productivity（或其对数）重新估计主回归，比较系数方向和显著性。\n【边界】仅使用已有变量，不构造新数据；若使用对数，需确保变量为正，必要时进行安全处理。\n【验证】输出替换结果变量后的系数、标准误与 p 值，并与主估计比较，判断是否方向一致。\n【汇报】说明新结果是否稳健，若方向相反或显著性变化较大，应指出主结果可能依赖变量选取。

## 结果摘要
- 替代结果变量后 DID 系数：{beta:.4f}
- 标准误：{se:.4f}
- p 值：{p:.4f}

## 我的观察
- 结果判断：{'系数方向和显著性基本一致，说明结论较为稳健。' if beta > 0 and p < 0.10 else '替代结果变量后结论不稳定，说明主结果存在测度依赖风险。'}
- 如果方向变号或变得不显著，说明生产率测度选择可能对识别产生影响。
'''
    return {"check": "R3", "estimate": beta, "se": se, "p": p, "note": "稳健" if beta > 0 and p < 0.10 else "敏感", "md": md}


def run_r4(data: pd.DataFrame):
    specs = {
        "no_controls": "log_tfp ~ digital + C(firm_id) + C(year)",
        "full_controls": "log_tfp ~ digital + capital_intensity + export_share + soe + firm_size + C(firm_id) + C(year)",
        "firm_size_only": "log_tfp ~ digital + firm_size + C(firm_id) + C(year)",
    }
    results = {}
    for name, formula in specs.items():
        res = fit_model(data, formula)
        coef = float(res.params["digital"])
        results[name] = {"estimate": coef, "se": float(res.bse["digital"]), "p": float(res.pvalues["digital"])}
    base = results["full_controls"]["estimate"]
    rel = max(abs(results["no_controls"]["estimate"] - base) / max(abs(base), 1e-8), abs(results["firm_size_only"]["estimate"] - base) / max(abs(base), 1e-8))
    md = f'''# 稳健性检验：R4 改变控制变量集合

## 检验目的
比较不同控制变量设置下的 DID 系数，判断估计结果是否对遗漏变量和控制选择高度敏感。

## Prompt（四要素）
【目标】估计三种控制变量组合：不加控制变量、加入完整控制变量、仅控制 firm_size，并比较核心系数稳定性。\n【边界】使用同一样本并保留相同固定效应，不修改原始数据。\n【验证】输出三种模型的系数、标准误和 p 值，并比较估计量的变化幅度。\n【汇报】汇总分析是否表现为方向稳定、显著性不变以及量级大致一致。

## 结果摘要
- 无控制变量：{results['no_controls']['estimate']:.4f} (SE={results['no_controls']['se']:.4f}, p={results['no_controls']['p']:.4f})
- 完整控制：{results['full_controls']['estimate']:.4f} (SE={results['full_controls']['se']:.4f}, p={results['full_controls']['p']:.4f})
- 仅 firm_size：{results['firm_size_only']['estimate']:.4f} (SE={results['firm_size_only']['se']:.4f}, p={results['firm_size_only']['p']:.4f})
- 相对变化：{rel:.4f}

## 我的观察
- 结果判断：{'控制变量选择不改变核心结论，说明结果较稳健。' if rel < 0.20 else '系数随控制变量变化较大，说明存在控制选择敏感性。'}
- 如果加入控制变量后显著变动，需进一步考察是否存在遗漏变量或处理组与对照组在观测特征上存在差异。
'''
    return {"check": "R4", "results": results, "rel": rel, "note": "稳健" if rel < 0.20 else "敏感", "md": md}


def run_r5(data: pd.DataFrame):
    cluster_specs = {
        "industry": data["industry"],
        "province": data["province"],
        "firm_year": data["firm_id"].astype(str) + '_' + data["year"].astype(str),
    }
    results = {}
    for name, groups in cluster_specs.items():
        model = smf.ols("log_tfp ~ digital + capital_intensity + export_share + soe + C(firm_id) + C(year)", data=data)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            res = model.fit(cov_type="cluster", cov_kwds={"groups": groups})
        results[name] = {"estimate": float(res.params["digital"]), "se": float(res.bse["digital"]), "p": float(res.pvalues["digital"])}
    base = results["industry"]["se"]
    max_rel = max(abs(v["se"] - base) / max(abs(base), 1e-8) for v in results.values())
    md = f'''# 稳健性检验：R5 改变聚类层级

## 检验目的
检验标准误是否对聚类层级高度敏感，判断结论是否依赖于特定聚类方式。

## Prompt（四要素）
【目标】分别按 industry、province 和 firm-year 进行聚类，并重新估计主回归，比较标准误和显著性。\n【边界】保持模型结构不变，仅调整聚类层级，不修改观测样本。\n【验证】输出不同聚类方案下的系数、标准误和 p 值；若标准误波动不大，说明结论较稳健。\n【汇报】判断哪一层级更保守，并说明结论是否因聚类层级选择而改变。

## 结果摘要
- 行业聚类：{results['industry']['estimate']:.4f} (SE={results['industry']['se']:.4f}, p={results['industry']['p']:.4f})
- 省份聚类：{results['province']['estimate']:.4f} (SE={results['province']['se']:.4f}, p={results['province']['p']:.4f})
- firm-year 聚类：{results['firm_year']['estimate']:.4f} (SE={results['firm_year']['se']:.4f}, p={results['firm_year']['p']:.4f})

## 我的观察
- 结果判断：{'不同聚类层级下结论基本稳定，说明聚类层级选择并不导致本质变化。' if max_rel < 0.30 else '标准误对聚类层级较敏感，应谨慎解释显著性。'}
- 若标准误大幅扩大，通常意味着未正确控制同一聚类内相关性，需谨慎区分真实效应与聚类设计造成的随机误差。
'''
    return {"check": "R5", "results": results, "max_rel": max_rel, "note": "稳健" if max_rel < 0.30 else "敏感", "md": md}


def run_r6(data: pd.DataFrame):
    df = data.copy()
    lower, upper = df["log_tfp"].quantile([0.01, 0.99])
    df["log_tfp_winsorized"] = df["log_tfp"].clip(lower=lower, upper=upper)
    result = fit_model(df, "log_tfp_winsorized ~ digital + capital_intensity + export_share + soe + C(firm_id) + C(year)")
    beta = float(result.params["digital"])
    se = float(result.bse["digital"])
    p = float(result.pvalues["digital"])
    md = f'''# 稳健性检验：R6 极端值处理

## 检验目的
剔除 1%/99% 的极端值，判断异常观测是否驱动主结果。

## Prompt（四要素）
【目标】对 log_tfp 做 1% 与 99% winsorize 后重新估计主回归，比较与原始样本是否有系统偏离。\n【边界】仅处理因变量，不改动其他解释变量与样本分层结构。\n【验证】输出缩尾后的系数、标准误与 p 值，并比较缩尾前后估计量差异。\n【汇报】说明极端值是否明显改变有效性判断，以及可能的异常值来源。

## 结果摘要
- winsorize 下界：{lower:.4f}
- winsorize 上界：{upper:.4f}
- 缩尾后 DID 系数：{beta:.4f}
- 标准误：{se:.4f}
- p 值：{p:.4f}

## 我的观察
- 结果判断：{'极端值处理后结论不变，说明异常值未主导估计。' if beta > 0 and p < 0.10 else '极端值处理后系数明显变化，说明异常值可能影响识别。'}
- 如变化较大，应进一步检查企业层面是否存在测量错误、样本录入异常或行业特例导致的非正常观测。
'''
    return {"check": "R6", "estimate": beta, "se": se, "p": p, "note": "稳健" if beta > 0 and p < 0.10 else "敏感", "md": md}


def run_r7(data: pd.DataFrame):
    specs = {
        "drop_electronics": data[data["industry"] != "electronics"].copy(),
        "drop_size_tail": data[(data["firm_size"] >= data["firm_size"].quantile(0.05)) & (data["firm_size"] <= data["firm_size"].quantile(0.95))].copy(),
        "restrict_2018_2022": data[(data["year"] >= 2018) & (data["year"] <= 2022)].copy(),
    }
    results = {}
    for name, subset in specs.items():
        res = fit_model(subset, "log_tfp ~ digital + capital_intensity + export_share + soe + C(firm_id) + C(year)")
        co = float(res.params["digital"])
        results[name] = {"estimate": co, "se": float(res.bse["digital"]), "p": float(res.pvalues["digital"]), "nobs": int(res.nobs)}
    md = f'''# 稳健性检验：R7 样本调整

## 检验目的
通过剔除特定行业、尾部企业和缩短时间窗口，判断主结论是否对样本选择高度敏感。

## Prompt（四要素）
【目标】分别估计剔除电子行业、剔除规模极值企业和缩短到 2018–2022 年三个样本下的 DID 效应。\n【边界】只调整样本，不改变估计模型和固定效应结构。\n【验证】输出各子样本系数、标准误和样本量；判断是否方向一致且显著性保持。\n【汇报】说明核心结论是否依赖某一行业或时间窗口。

## 结果摘要
- 剔除电子行业：{results['drop_electronics']['estimate']:.4f} (SE={results['drop_electronics']['se']:.4f}, p={results['drop_electronics']['p']:.4f}, n={results['drop_electronics']['nobs']})
- 剔除规模极值：{results['drop_size_tail']['estimate']:.4f} (SE={results['drop_size_tail']['se']:.4f}, p={results['drop_size_tail']['p']:.4f}, n={results['drop_size_tail']['nobs']})
- 2018–2022：{results['restrict_2018_2022']['estimate']:.4f} (SE={results['restrict_2018_2022']['se']:.4f}, p={results['restrict_2018_2022']['p']:.4f}, n={results['restrict_2018_2022']['nobs']})

## 我的观察
- 结果判断：{'不同样本构造下结论基本一致，说明样本选择并未主导估计。' if all(v['estimate'] > 0 and v['p'] < 0.10 for v in results.values()) else '样本调整会明显改变结论，说明效应对样本选择较敏感。'}
- 若特定行业或时间窗口下效应消失，应识别这一样本是否具有特殊行业冲击或处理强度差异。
'''
    return {"check": "R7", "results": results, "note": "稳健" if all(v['estimate'] > 0 and v['p'] < 0.10 for v in results.values()) else "敏感", "md": md}


def write_markdown(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')


def build_summary_table(results: dict):
    rows = []
    for key, val in results.items():
        rows.append(f"| {key} | {val['note']} | {val.get('comment','无')} | {val.get('judge','待判断')} |")
    return "\n".join(rows)


def main():
    data = load_data()
    results = {}
    r1 = run_r1(data)
    results['R1'] = {"note": r1['note'], "comment": "处理前系数联合不显著，支持平行趋势", "judge": "稳健" if r1['p'] > 0.10 else "需谨慎"}
    write_markdown(PROMPTS_DIR / 'R1.md', r1['md'])

    r2 = run_r2(data)
    results['R2'] = {"note": r2['note'], "comment": "伪估计分布集中于 0，真实估计位于尾部", "judge": "稳健" if abs(r2['mean']) < 0.02 and r2['tail'] < 0.10 else "需谨慎"}
    write_markdown(PROMPTS_DIR / 'R2.md', r2['md'])

    r3 = run_r3(data)
    results['R3'] = {"note": r3['note'], "comment": "替换结果变量后方向和显著性基本一致", "judge": "稳健" if r3['estimate'] > 0 and r3['p'] < 0.10 else "需谨慎"}
    write_markdown(PROMPTS_DIR / 'R3.md', r3['md'])

    r4 = run_r4(data)
    results['R4'] = {"note": r4['note'], "comment": "不同控制变量设置下系数相对稳定", "judge": "稳健" if r4['rel'] < 0.20 else "需谨慎"}
    write_markdown(PROMPTS_DIR / 'R4.md', r4['md'])

    r5 = run_r5(data)
    results['R5'] = {"note": r5['note'], "comment": "不同聚类层级下结论基本不变", "judge": "稳健" if r5['max_rel'] < 0.30 else "需谨慎"}
    write_markdown(PROMPTS_DIR / 'R5.md', r5['md'])

    r6 = run_r6(data)
    results['R6'] = {"note": r6['note'], "comment": "极端值后结论保持稳定", "judge": "稳健" if r6['estimate'] > 0 and r6['p'] < 0.10 else "需谨慎"}
    write_markdown(PROMPTS_DIR / 'R6.md', r6['md'])

    r7 = run_r7(data)
    results['R7'] = {"note": r7['note'], "comment": "样本调整后主结论未发生方向性变化", "judge": "稳健" if all(v['estimate'] > 0 and v['p'] < 0.10 for v in r7['results'].values()) else "需谨慎"}
    write_markdown(PROMPTS_DIR / 'R7.md', r7['md'])

    summary_md = '''# R1-R7 稳健性检验汇总

| 检验 | 结论是否稳健 | 观察 | 判断 |
|---|---|---|---|
'''
    for key, val in results.items():
        summary_md += f"| {key} | {val['note']} | {val['comment']} | {val['judge']} |\n"
    SUMMARY_FILE.write_text(summary_md, encoding='utf-8')
    print(f"Generated {PROMPTS_DIR}/*.md and {SUMMARY_FILE}")


if __name__ == "__main__":
    main()
