from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "raw"
OUTPUT_FILE = DATA_DIR / "digital_transformation_firm_panel.csv"


def build_panel(seed: int = 2026) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    n_firms = 360
    years = np.arange(2016, 2025)
    industries = np.array(["electronics", "machinery", "textile", "chemicals"])
    provinces = np.array(["coastal", "central", "western"])

    industry = rng.choice(industries, size=n_firms, p=[0.30, 0.28, 0.22, 0.20])
    province = rng.choice(provinces, size=n_firms, p=[0.45, 0.35, 0.20])
    managerial_capability = rng.normal(0, 1, n_firms)
    baseline_size = rng.lognormal(mean=3.2, sigma=0.45, size=n_firms)
    export_share = np.clip(rng.beta(2.0, 5.0, size=n_firms), 0, 1)
    soe = rng.binomial(1, 0.18, n_firms)

    adoption_score = (
        0.55 * managerial_capability
        + 0.35 * np.log(baseline_size)
        + 0.45 * export_share
        + rng.normal(0, 0.75, n_firms)
    )
    treated = (adoption_score > np.quantile(adoption_score, 0.58)).astype(int)
    adoption_year = np.where(treated == 1, 2020, 9999)

    industry_effect = {
        "electronics": 0.18,
        "machinery": 0.08,
        "textile": -0.10,
        "chemicals": 0.03,
    }
    province_effect = {"coastal": 0.12, "central": 0.00, "western": -0.08}

    rows = []
    for firm_index in range(n_firms):
        firm_fixed_effect = rng.normal(0, 0.22)
        for year in years:
            relative_year = year - adoption_year[firm_index]
            post = int(year >= 2020)
            digital = int(treated[firm_index] == 1 and year >= adoption_year[firm_index])
            pre_digitization = 0.08 * treated[firm_index] * (year - 2016)
            common_trend = 0.035 * (year - 2016)
            demand_cycle = 0.025 * np.sin((year - 2016) / 1.7)
            dynamic_effect = 0.0
            if digital:
                dynamic_effect = 0.045 + 0.035 * min(relative_year, 4)
            log_tfp = (
                1.45
                + firm_fixed_effect
                + industry_effect[industry[firm_index]]
                + province_effect[province[firm_index]]
                + 0.07 * managerial_capability[firm_index]
                + 0.035 * np.log(baseline_size[firm_index])
                + 0.06 * export_share[firm_index]
                - 0.035 * soe[firm_index]
                + common_trend
                + demand_cycle
                + pre_digitization * 0.01
                + dynamic_effect
                + rng.normal(0, 0.06)
            )
            labor_productivity = np.exp(log_tfp + rng.normal(0, 0.03))
            rows.append(
                {
                    "firm_id": firm_index + 1,
                    "year": year,
                    "industry": industry[firm_index],
                    "province": province[firm_index],
                    "treated": treated[firm_index],
                    "post": post,
                    "digital": digital,
                    "treated_post": treated[firm_index] * post,
                    "adoption_year": adoption_year[firm_index],
                    "relative_year": relative_year if treated[firm_index] else -99,
                    "firm_size": baseline_size[firm_index]
                    * np.exp(0.04 * (year - 2016)),
                    "capital_intensity": 0.55
                    + 0.08 * managerial_capability[firm_index]
                    + rng.normal(0, 0.08),
                    "export_share": export_share[firm_index],
                    "soe": soe[firm_index],
                    "managerial_capability": managerial_capability[firm_index],
                    "log_tfp": log_tfp,
                    "labor_productivity": labor_productivity,
                }
            )

    return pd.DataFrame(rows)


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    panel = build_panel()
    panel.to_csv(OUTPUT_FILE, index=False)
    print(f"Wrote {OUTPUT_FILE.relative_to(ROOT)} with {len(panel):,} rows")


if __name__ == "__main__":
    main()
