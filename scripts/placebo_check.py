from __future__ import annotations

import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "raw" / "digital_transformation_firm_panel.csv"
OUTPUT_DIR = ROOT / "output"
REPORT_FILE = OUTPUT_DIR / "placebo-check.md"
PLOT_FILE = OUTPUT_DIR / "placebo-check.png"


def load_data() -> pd.DataFrame:
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Missing dataset: {DATA_FILE}")
    return pd.read_csv(DATA_FILE)


def estimate_main_did(data: pd.DataFrame):
    formula = "log_tfp ~ digital + capital_intensity + export_share + soe + C(firm_id) + C(year)"
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        model = smf.ols(formula, data=data)
        return model.fit(cov_type="cluster", cov_kwds={"groups": data["firm_id"]})


def run_placebo(data: pd.DataFrame, n_iter: int = 300, seed: int = 2026):
    main_fit = estimate_main_did(data)
    true_beta = float(main_fit.params["digital"])

    rng = np.random.default_rng(seed)
    treated_firms = sorted(data[data["treated"] == 1]["firm_id"].unique())
    placebo_coefs: list[float] = []

    for _ in range(n_iter):
        d = data.copy()
        rand_year = {firm: int(rng.choice([2017, 2018])) for firm in treated_firms}
        d["pseudo_year"] = d["firm_id"].map(rand_year).fillna(9999)
        d["pseudo_digital"] = ((d["treated"] == 1) & (d["year"] >= d["pseudo_year"])).astype(int)

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            placebo_fit = smf.ols(
                "log_tfp ~ pseudo_digital + capital_intensity + export_share + soe + C(firm_id) + C(year)",
                data=d,
            ).fit(cov_type="cluster", cov_kwds={"groups": d["firm_id"]})

        placebo_coefs.append(float(placebo_fit.params["pseudo_digital"]))

    arr = np.asarray(placebo_coefs, dtype=float)
    mean = float(arr.mean())
    std = float(arr.std())
    tail_prob = float(np.mean(np.abs(arr) >= abs(true_beta)))

    return {
        "true_beta": true_beta,
        "placebo_mean": mean,
        "placebo_std": std,
        "tail_prob": tail_prob,
        "distribution": arr,
    }


def save_plot(distribution: np.ndarray, true_beta: float) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    width, height = 1200, 700
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    min_v = float(np.min(distribution))
    max_v = float(np.max(distribution))
    if np.isclose(min_v, max_v):
        min_v -= 0.01
        max_v += 0.01
    pad_left, pad_right = 80, 60
    pad_top, pad_bottom = 60, 80
    plot_w = width - pad_left - pad_right
    plot_h = height - pad_top - pad_bottom

    draw.rectangle((pad_left, pad_top, width - pad_right, height - pad_bottom), outline="black", width=2)
    draw.line((pad_left, height - pad_bottom, width - pad_right, height - pad_bottom), fill="black", width=2)
    draw.line((pad_left, pad_top, pad_left, height - pad_bottom), fill="black", width=2)

    bins = 25
    hist, bin_edges = np.histogram(distribution, bins=bins, range=(min_v, max_v))
    max_count = float(hist.max()) if hist.size else 1.0
    for i, count in enumerate(hist):
        x0 = pad_left + i * plot_w / bins
        x1 = pad_left + (i + 1) * plot_w / bins
        bar_h = (count / max_count) * plot_h
        y0 = height - pad_bottom - bar_h
        draw.rectangle((x0 + 2, y0, x1 - 2, height - pad_bottom), fill=(0, 168, 204), outline=(0, 120, 160))

    true_x = pad_left + ((true_beta - min_v) / (max_v - min_v + 1e-12)) * plot_w
    draw.line((true_x, pad_top, true_x, height - pad_bottom), fill="red", width=3)
    draw.text((true_x - 30, pad_top - 18), f"True DID\n{true_beta:.4f}", fill="red")

    draw.text((width // 2 - 170, 18), "DID Placebo Test: Randomized Treatment Timing", fill="black")
    draw.text((pad_left, height - 22), "Pseudo DID coefficient", fill="black")
    draw.text((18, height // 2 - 60), "Frequency", fill="black")

    PLOT_FILE.parent.mkdir(parents=True, exist_ok=True)
    img.save(PLOT_FILE, format="PNG")


def write_report(summary: dict) -> None:
    true_beta = summary["true_beta"]
    mean = summary["placebo_mean"]
    std = summary["placebo_std"]
    tail_prob = summary["tail_prob"]

    if abs(mean) < 0.02 and tail_prob < 0.10:
        judgement = "Placebo test passes: pseudo coefficients are centered near zero and the true estimate lies far from the placebo distribution."
        verdict = "通过"
        overlap = "较低"
    else:
        judgement = "Placebo test raises caution: pseudo estimates are sizable or overlap the true DID estimate more than expected."
        verdict = "需谨慎"
        overlap = "较高"

    md = f'''# DID 安慰剂检验（Placebo Test）

## Skill 触发
调用 `did-placebo-check` 这一 Skill，对 `data/raw/digital_transformation_firm_panel.csv` 数据执行 DID 安慰剂检验。

## 检验目的
验证真实处理效应是否只是随机噪音或时间趋势所致，而不是真实政策效应。

## 数据与模型
- 数据：`data/raw/digital_transformation_firm_panel.csv`
- 主回归：`log_tfp ~ digital + capital_intensity + export_share + soe + C(firm_id) + C(year)`
- 标准误：按 `firm_id` 聚类
- 安慰剂设计：保留真实处理组不变，随机指定处理年份为 2017 或 2018，并重复 300 次估计

## 结果摘要
- 真实 DID 系数：{true_beta:.4f}
- 伪处理系数均值：{mean:.4f}
- 伪处理系数标准差：{std:.4f}
- |伪估计| >= |真实估计| 的比例：{tail_prob:.4f}
- 图片输出：`output/placebo-check.png`

## 判断
{judgement}

## 结论
本次安慰剂检验结果为 {verdict}。真实系数与伪处理分布的重叠程度为 {overlap}，说明该 DID 估计的解释需要结合时间趋势、处理选择和未观测冲击进一步审慎评估。
'''

    REPORT_FILE.write_text(md, encoding="utf-8")


def main() -> None:
    data = load_data()
    summary = run_placebo(data)
    save_plot(summary["distribution"], summary["true_beta"])
    write_report(summary)

    print(f"True DID coefficient: {summary['true_beta']:.4f}")
    print(f"Placebo mean: {summary['placebo_mean']:.4f}")
    print(f"Placebo std: {summary['placebo_std']:.4f}")
    print(f"Tail probability: {summary['tail_prob']:.4f}")
    print(f"Saved report: {REPORT_FILE}")
    print(f"Saved plot: {PLOT_FILE}")


if __name__ == "__main__":
    main()
