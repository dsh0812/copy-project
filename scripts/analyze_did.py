from pathlib import Path
import warnings

import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "output"
DATA_FILE = ROOT / "data" / "raw" / "digital_transformation_firm_panel.csv"
RESULTS_FILE = OUTPUT_DIR / "python_did_results.csv"
STATA_RESULTS_FILE = OUTPUT_DIR / "stata_did_results.csv"
EVENT_COEFFICIENTS_FILE = OUTPUT_DIR / "stata_event_study.csv"
PLACEBO_FILE = OUTPUT_DIR / "stata_placebo_results.csv"
PRETREND_FILE = OUTPUT_DIR / "pretrend_means.csv"
FIGURE_FILE = OUTPUT_DIR / "digital_parallel_trends.png"
EVENT_FIGURE_FILE = OUTPUT_DIR / "digital_event_study.png"
SUMMARY_FILE = OUTPUT_DIR / "demo_summary.md"


def load_data() -> pd.DataFrame:
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Missing {DATA_FILE}. Run scripts/generate_synthetic_did.py first."
        )
    return pd.read_csv(DATA_FILE)


def estimate_did(data: pd.DataFrame):
    model = smf.ols(
        "log_tfp ~ digital + capital_intensity + export_share + soe + C(firm_id) + C(year)",
        data=data,
    )
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            message="invalid value encountered in sqrt",
            category=RuntimeWarning,
        )
        return model.fit(cov_type="cluster", cov_kwds={"groups": data["firm_id"]})


def build_pretrend(data: pd.DataFrame) -> pd.DataFrame:
    grouped = (
        data.groupby(["year", "treated"], as_index=False)["log_tfp"]
        .mean()
        .pivot(index="year", columns="treated", values="log_tfp")
        .rename(columns={0: "control", 1: "treated"})
    )
    grouped["gap"] = grouped["treated"] - grouped["control"]
    pre_gap = grouped.loc[grouped.index < 2020, "gap"].mean()
    grouped["did_relative"] = grouped["gap"] - pre_gap
    return grouped.reset_index()


def load_optional_csv(path: Path) -> pd.DataFrame | None:
    if path.exists():
        return pd.read_csv(path)
    return None


def save_results(result, pretrend: pd.DataFrame) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            message="invalid value encountered in sqrt",
            category=RuntimeWarning,
        )
        digital_estimate = result.params["digital"]
        digital_std_error = result.bse["digital"]
        digital_t_value = result.tvalues["digital"]
        digital_p_value = result.pvalues["digital"]
    table = pd.DataFrame(
        [
            {
                "term": "digital",
                "estimate": digital_estimate,
                "std_error_cluster_firm": digital_std_error,
                "t_value": digital_t_value,
                "p_value": digital_p_value,
                "n_obs": int(result.nobs),
            }
        ]
    )
    table.to_csv(RESULTS_FILE, index=False)
    pretrend.to_csv(PRETREND_FILE, index=False)

    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.axhline(0, color="#666666", linewidth=1, linestyle="--")
    ax.axvline(2019.5, color="#AE0B2A", linewidth=1.2, linestyle=":")
    ax.plot(
        pretrend["year"],
        pretrend["treated"],
        marker="o",
        color="#003153",
        linewidth=2,
        label="Treated firms",
    )
    ax.plot(
        pretrend["year"],
        pretrend["control"],
        marker="o",
        color="#00A8CC",
        linewidth=2,
        label="Control firms",
    )
    ax.set_title("Digital Transformation Demo: Parallel-Trend Check")
    ax.set_xlabel("Year")
    ax.set_ylabel("Mean log TFP")
    ax.legend(frameon=False)
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIGURE_FILE, dpi=180)
    plt.close(fig)

    event_coefficients = load_optional_csv(EVENT_COEFFICIENTS_FILE)
    if event_coefficients is not None:
        event_coefficients = event_coefficients.sort_values("relative_year").copy()
        event_coefficients["ci_low"] = (
            event_coefficients["estimate"] - 1.96 * event_coefficients["std_error"]
        )
        event_coefficients["ci_high"] = (
            event_coefficients["estimate"] + 1.96 * event_coefficients["std_error"]
        )
        fig, ax = plt.subplots(figsize=(8, 4.8))
        ax.axhline(0, color="#666666", linewidth=1, linestyle="--")
        ax.axvline(-0.5, color="#AE0B2A", linewidth=1.2, linestyle=":")
        ax.fill_between(
            event_coefficients["relative_year"],
            event_coefficients["ci_low"],
            event_coefficients["ci_high"],
            color="#00A8CC",
            alpha=0.18,
            label="95% confidence interval",
        )
        ax.plot(
            event_coefficients["relative_year"],
            event_coefficients["estimate"],
            marker="o",
            color="#003153",
            linewidth=2,
            label="Event-study estimate",
        )
        ax.set_title("Stata Event-Study Estimates")
        ax.set_xlabel("Years Relative to Digital Adoption")
        ax.set_ylabel("Coefficient relative to year -1")
        ax.set_xticks(range(-4, 5))
        ax.legend(frameon=False)
        ax.grid(alpha=0.25)
        fig.tight_layout()
        fig.savefig(EVENT_FIGURE_FILE, dpi=180)
        plt.close(fig)

    estimate = table.loc[0, "estimate"]
    std_error = table.loc[0, "std_error_cluster_firm"]
    stata_results = load_optional_csv(STATA_RESULTS_FILE)
    placebo = load_optional_csv(PLACEBO_FILE)
    stata_line = "- Stata DID estimate: run `stata -b do scripts/run_stata_did.do` to generate this output\n"
    if stata_results is not None:
        stata_line = (
            f"- Stata DID estimate: {stata_results.loc[0, 'estimate']:.3f} "
            f"(SE {stata_results.loc[0, 'std_error']:.3f})\n"
        )
    placebo_line = "- Placebo test: run the Stata script to generate pre-period placebo output\n"
    if placebo is not None:
        placebo_line = (
            f"- Placebo estimate: {placebo.loc[0, 'estimate']:.3f} "
            f"(SE {placebo.loc[0, 'std_error']:.3f})\n"
        )
    SUMMARY_FILE.write_text(
        "# Demo Summary: Digital Transformation and Firm Productivity\n\n"
        "This synthetic workflow generated a firm-level panel dataset, estimated a two-way "
        "fixed-effect DID model, exported a parallel-trend figure, and prepared Stata/Matlab "
        "outputs for the notebooks and LaTeX draft.\n\n"
        f"- Python DID estimate: {estimate:.3f}\n"
        f"- Clustered standard error: {std_error:.3f}\n"
        f"{stata_line}"
        f"{placebo_line}"
        "- Data status: synthetic teaching data only\n",
        encoding="utf-8",
    )


def main() -> None:
    data = load_data()
    result = estimate_did(data)
    pretrend = build_pretrend(data)
    save_results(result, pretrend)
    print(f"Wrote {RESULTS_FILE.relative_to(ROOT)}")
    print(f"Wrote {FIGURE_FILE.relative_to(ROOT)}")
    if EVENT_FIGURE_FILE.exists():
        print(f"Wrote {EVENT_FIGURE_FILE.relative_to(ROOT)}")
    print(f"Wrote {SUMMARY_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
