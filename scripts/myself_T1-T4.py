from __future__ import annotations

from pathlib import Path
import warnings

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


def run_t1(data: pd.DataFrame):
    df = data.copy()
    treated = df[df["treated"] == 1].copy()
    mean = treated["managerial_capability"].mean()
    sd = treated["managerial_capability"].std(ddof=0)
    df["digital_intensity"] = 0.0
    df.loc[df["treated"] == 1, "digital_intensity"] = (df.loc[df["treated"] == 1, "managerial_capability"] - mean) / sd
    result = fit_model(df, "log_tfp ~ digital_intensity + capital_intensity + export_share + soe + C(firm_id) + C(year)")
    beta = float(result.params["digital_intensity"])
    se = float(result.bse["digital_intensity"])
    p = float(result.pvalues["digital_intensity"])
    md = f'''# 稳健性检验：T1 处理变量的测量方式（连续强度替代）

## 检验目的
用数字化强度替代二值处理变量，检验制度化的数字化程度提升是否能解释更高的生产率。

## Prompt（四要素）
【目标】构造数字化强度变量并重新估计主回归，解释强度变化对生产率的边际影响。\n【边界】仅用已有数据构造强度变量，不引入外部数据；控制组记为 0，处理组按 managerial_capability 标准化。\n【验证】输出强度变量系数、标准误和 p 值；若显著为正且量级合理则支持连续强度解释。\n【汇报】说明强度每增加一个标准差，生产率变化多少，并判定是否仍支持主结论。

## 结果摘要
- 数字化强度系数：{beta:.4f}
- 标准误：{se:.4f}
- p 值：{p:.4f}

## 我的观察
- 结果判断：{'支持连续强度解释，说明数字化程度越高，生产率提升越明显。' if beta > 0 and p < 0.10 else '强度变量不显著，说明二值处理变量可能更稳定或强度测度不足。'}
- 若强度效应显著，则说明数字化转型的收益并非简单门槛效应，而是存在强度层面的边际增益。
'''
    return {"check": "T1", "estimate": beta, "se": se, "p": p, "note": "支持强度解释" if beta > 0 and p < 0.10 else "需要谨慎", "judge": "稳健" if beta > 0 and p < 0.10 else "需谨慎", "md": md}


def run_t2(data: pd.DataFrame):
    groups = {
        "industry_electronics": data[data["industry"] == "electronics"],
        "industry_other": data[data["industry"] != "electronics"],
        "soe": data[data["soe"] == 1],
        "non_soe": data[data["soe"] == 0],
        "large_firms": data[data["firm_size"] >= data["firm_size"].median()],
        "small_firms": data[data["firm_size"] < data["firm_size"].median()],
    }
    output = {}
    for name, subset in groups.items():
        res = fit_model(subset, "log_tfp ~ digital + capital_intensity + export_share + soe + C(firm_id) + C(year)")
        output[name] = {"estimate": float(res.params["digital"]), "se": float(res.bse["digital"]), "p": float(res.pvalues["digital"]), "nobs": int(res.nobs)}
    md = '''# 稳健性检验：T2 异质性检验（分组回归）

## 检验目的
检测数字化转型效应是否在不同企业类型中存在异质性，判断是否存在“高能力企业更受益”或“特定行业更受益”的结构性差异。

## Prompt（四要素）
【目标】按行业、所有制与规模分组后分别估计 DID，观察效应差异并进行组间比较。\n【边界】分组样本必须满足足够规模，必要时合并类别；保留固定效应和聚类标准误。\n【验证】输出每组系数、标准误和 p 值，并说明组间差异是否显著。\n【汇报】总结哪些组更强，并讨论理论预期是否一致。

## 结果摘要
'''
    for name, res in output.items():
        md += f"- {name}: estimate={res['estimate']:.4f}, se={res['se']:.4f}, p={res['p']:.4f}, n={res['nobs']}\n"
    md += '\n## 我的观察\n- 若高能力、规模更大或特定行业组的效应更强，说明数字化转型在特定企业群体中更能发挥作用。\n- 如果分组后结果相近，则说明效应较为普遍，并非由某一群体单独驱动。\n'
    return {"check": "T2", "groups": output, "note": "存在异质性" if any(v['estimate'] > 0 and v['p'] < 0.10 for v in output.values()) else "无明显异质性", "judge": "稳健" if any(v['estimate'] > 0 and v['p'] < 0.10 for v in output.values()) else "需谨慎", "md": md}


def run_t3(data: pd.DataFrame):
    df = data.copy()
    df["managerial_centered"] = df["managerial_capability"] - df["managerial_capability"].mean()
    result = fit_model(df, "log_tfp ~ digital + managerial_centered + digital:managerial_centered + capital_intensity + export_share + soe + C(firm_id) + C(year)")
    beta_int = float(result.params["digital:managerial_centered"])
    se_int = float(result.bse["digital:managerial_centered"])
    p_int = float(result.pvalues["digital:managerial_centered"])
    md = f'''# 稳健性检验：T3 机制检验（能力互补性）

## 检验目的
检验数字化转型效应是否随着管理能力上升而增强，判断是否存在“高能力企业从数字化中获益更多”的互补机制。

## Prompt（四要素）
【目标】在主回归中加入 digital × managerial_capability 交互项，考察能力互补性。\n【边界】只增加交互项，不改变其他设定；对 managerial_capability 做中心化处理以降低共线性。\n【验证】输出交互项系数、标准误和 p 值；显著为正则支持互补机制。\n【汇报】说明是否支持能力互补假说，并判断机制可信度。

## 结果摘要
- 交互项系数：{beta_int:.4f}
- 标准误：{se_int:.4f}
- p 值：{p_int:.4f}

## 我的观察
- 结果判断：{'支持能力互补性机制，说明高能力企业更能从数字化转型中获益。' if beta_int > 0 and p_int < 0.10 else '交互项不显著，说明当前数据并不支持明显的能力互补机制。'}
- 若交互项显著，则说明数字化转型并非单一技术投入，而是与管理能力共同发挥作用。
'''
    return {"check": "T3", "estimate": beta_int, "se": se_int, "p": p_int, "note": "支持互补性" if beta_int > 0 and p_int < 0.10 else "未发现明显机制", "judge": "稳健" if beta_int > 0 and p_int < 0.10 else "需谨慎", "md": md}


def run_t4(data: pd.DataFrame):
    df = data.copy()
    res1 = fit_model(df, "log_tfp ~ digital + capital_intensity + export_share + soe + C(firm_id) + C(year) + C(industry):C(year)")
    res2 = fit_model(df, "log_tfp ~ digital + capital_intensity + export_share + soe + C(firm_id) + C(year) + C(province):C(year)")
    base = fit_model(df, "log_tfp ~ digital + capital_intensity + export_share + soe + C(firm_id) + C(year)")
    beta_base = float(base.params["digital"])
    beta1 = float(res1.params["digital"])
    beta2 = float(res2.params["digital"])
    md = f'''# 稳健性检验：T4 排除竞争性解释（行业-年份固定效应）

## 检验目的
吸收行业或地区层面的共同时间冲击，排除行业/地区特定变化被误认为数字化效应的可能性。

## Prompt（四要素）
【目标】分别加入 industry × year 和 province × year 固定效应，估计是否仍能观察到数字化效应。\n【边界】仅增加高维固定效应，保持解释变量和样本一致，以排除竞争性解释。\n【验证】输出加入固定效应后的系数和标准误，并与基准模型比较。\n【汇报】若系数仍显著且变化不大，可说明结果不主要由行业或地区冲击驱动。

## 结果摘要
- 基准 DID 系数：{beta_base:.4f}
- 加入 industry × year：{beta1:.4f}
- 加入 province × year：{beta2:.4f}

## 我的观察
- 结果判断：{'结果较稳健，说明行业或地区时间冲击并非主要解释。' if abs(beta1 - beta_base) / max(abs(beta_base), 1e-8) < 0.30 or abs(beta2 - beta_base) / max(abs(beta_base), 1e-8) < 0.30 else '加入高维固定效应后系数明显缩小，说明存在竞争性解释风险。'}
- 若系数显著下降，则说明数字化转型可能部分反映行业/地区的共同冲击，而不是单独处理效应。
'''
    return {"check": "T4", "base": beta_base, "industry_year": beta1, "province_year": beta2, "note": "稳健" if (abs(beta1 - beta_base)/max(abs(beta_base),1e-8) < 0.30 or abs(beta2 - beta_base)/max(abs(beta_base),1e-8) < 0.30) else "敏感", "judge": "稳健" if (abs(beta1 - beta_base)/max(abs(beta_base),1e-8) < 0.30 or abs(beta2 - beta_base)/max(abs(beta_base),1e-8) < 0.30) else "需谨慎", "md": md}


def write_markdown(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')


def append_summary(summary: dict, key: str, note: str, comment: str):
    summary[key] = {"note": note, "comment": comment}


def build_summary_table(results: dict):
    rows = []
    for key in list(results.keys()):
        val = results[key]
        rows.append(f"| {key} | {val['note']} | {val.get('comment', '无')} | {val.get('judge', '待判断')} |")
    return "\n".join(rows)


def build_ordered_summary(all_results: dict):
    order = [f"R{i}" for i in range(1, 8)] + [f"T{i}" for i in range(1, 5)]
    ordered = {k: all_results[k] for k in order if k in all_results}
    for key, val in all_results.items():
        if key not in ordered:
            ordered[key] = val
    return ordered


def main():
    data = load_data()
    r_script = ROOT / "scripts" / "myself_R1-R7.py"
    r_results = {}
    if r_script.exists():
        import importlib.util
        spec = importlib.util.spec_from_file_location("myself_r1_r7", r_script)
        rmod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(rmod)
        for fn in [rmod.run_r1, rmod.run_r2, rmod.run_r3, rmod.run_r4, rmod.run_r5, rmod.run_r6, rmod.run_r7]:
            result = fn(data)
            r_results[result['check']] = {
                "note": result.get('note', '待评估'),
                "comment": result.get('comment', '无'),
                "judge": result.get('judge', '待判断'),
            }

    t_results = {}
    for fn in [run_t1, run_t2, run_t3, run_t4]:
        result = fn(data)
        write_markdown(PROMPTS_DIR / f"{result['check']}.md", result['md'])
        t_results[result['check']] = {
            "note": result.get('note', '待评估'),
            "comment": result.get('judge', '待评估'),
            "judge": result.get('judge', '待评估'),
        }

    combined = {**r_results, **t_results}
    summary_md = "# R1-R7 与 T1-T4 稳健性检验汇总\n\n| 检验 | 结论是否稳健 | 观察 | 判断 |\n|---|---|---|---|\n"
    for key, val in build_ordered_summary(combined).items():
        summary_md += f"| {key} | {val['note']} | {val.get('comment', '无')} | {val.get('judge', '待判断')} |\n"
    summary_md += "\n"
    SUMMARY_FILE.write_text(summary_md, encoding='utf-8')
    print(f"Generated {PROMPTS_DIR}/*.md and {SUMMARY_FILE}")


if __name__ == "__main__":
    main()
