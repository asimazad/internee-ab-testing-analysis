from pathlib import Path
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

REQUIRED = {"session_id", "variant", "engaged_session", "converted"}

def two_prop_test(x1, n1, x2, n2):
    """Two-sided pooled two-proportion z-test and 95% CI for p2-p1."""
    p1, p2 = x1 / n1, x2 / n2
    pooled = (x1 + x2) / (n1 + n2)
    se_pool = np.sqrt(pooled * (1 - pooled) * (1/n1 + 1/n2))
    z = (p2 - p1) / se_pool if se_pool else 0.0
    p_value = 2 * (1 - norm.cdf(abs(z)))
    se_diff = np.sqrt(p1*(1-p1)/n1 + p2*(1-p2)/n2)
    diff = p2 - p1
    ci = (diff - 1.96*se_diff, diff + 1.96*se_diff)
    return diff, z, p_value, ci

def main():
    parser = argparse.ArgumentParser(description="Analyze homepage A/B test sessions.")
    parser.add_argument("--input", default="data/ab_test_sessions.csv")
    parser.add_argument("--output", default="reports")
    args = parser.parse_args()

    data = pd.read_csv(args.input)
    missing = REQUIRED - set(data.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    data["variant"] = data["variant"].astype(str).str.upper().str.strip()
    if not set(data["variant"].unique()).issubset({"A", "B"}):
        raise ValueError("variant must contain only A and/or B.")
    for col in ["engaged_session", "converted"]:
        data[col] = pd.to_numeric(data[col], errors="raise")
        if not data[col].isin([0, 1]).all():
            raise ValueError(f"{col} must contain only 0/1 values.")

    summary = data.groupby("variant").agg(
        sessions=("session_id", "nunique"),
        engaged_sessions=("engaged_session", "sum"),
        conversions=("converted", "sum")
    )
    summary["engagement_rate"] = summary["engaged_sessions"] / summary["sessions"]
    summary["bounce_rate"] = 1 - summary["engagement_rate"]
    summary["conversion_rate"] = summary["conversions"] / summary["sessions"]
    summary.to_csv(Path(args.output) / "variant_summary.csv")

    if not {"A", "B"}.issubset(summary.index):
        raise ValueError("The dataset must contain both variants A and B.")

    a, b = summary.loc["A"], summary.loc["B"]
    diff, z, p, ci = two_prop_test(int(a.conversions), int(a.sessions),
                                   int(b.conversions), int(b.sessions))
    bounce_diff = b.bounce_rate - a.bounce_rate
    winner = "B" if diff > 0 else ("A" if diff < 0 else "No difference")
    significant = p < 0.05

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 5))
    x = np.arange(2)
    ax.bar(x - 0.18, [a.bounce_rate*100, b.bounce_rate*100], 0.36, label="Bounce rate")
    ax.bar(x + 0.18, [a.conversion_rate*100, b.conversion_rate*100], 0.36, label="Conversion rate")
    ax.set_xticks(x, ["Variant A", "Variant B"])
    ax.set_ylabel("Rate (%)")
    ax.set_title("Homepage A/B Test: Bounce and Conversion Rates")
    ax.legend()
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(out / "ab_test_comparison.png", dpi=160)
    plt.close(fig)

    report = f"""# A/B Test Analysis Report

## Data note
This run uses the **illustrative sample dataset** bundled with this repository. It is synthetic and is **not actual Internee.pk or Google Analytics data**. Replace it with an authorized GA4 export before making business decisions.

## Experiment
- Objective: Compare two homepage designs.
- Variant A: Existing/control homepage.
- Variant B: Revised homepage with clearer hero message and stronger primary call-to-action.
- Primary metric: Conversion rate = converted sessions / total sessions.
- Secondary metrics: Bounce rate = 1 - engagement rate; engagement rate = engaged sessions / total sessions.
- Significance threshold: 0.05, two-sided two-proportion z-test.

## Results

| Metric | Variant A | Variant B |
|---|---:|---:|
| Sessions | {int(a.sessions)} | {int(b.sessions)} |
| Engaged sessions | {int(a.engaged_sessions)} | {int(b.engaged_sessions)} |
| Bounce rate | {a.bounce_rate:.2%} | {b.bounce_rate:.2%} |
| Conversion rate | {a.conversion_rate:.2%} | {b.conversion_rate:.2%} |

## Statistical test
- Conversion-rate difference (B - A): {diff:.2%} ({diff*100:.2f} percentage points)
- 95% confidence interval: [{ci[0]:.2%}, {ci[1]:.2%}]
- z statistic: {z:.3f}
- p-value: {p:.4f}
- Statistically significant at 5%: {"Yes" if significant else "No"}

## Interpretation
{"Variant B has the higher observed conversion rate." if diff > 0 else "Variant A has the higher observed conversion rate." if diff < 0 else "Both variants have the same observed conversion rate."}
{"The difference is statistically significant in this illustrative dataset." if significant else "The observed difference is not statistically significant at the 5% level; do not claim a proven winner."}
The observed bounce-rate difference (B - A) is {bounce_diff:.2%}. A negative value means Variant B has a lower bounce rate.

## Recommendation
Treat the result as a demonstration only. For a real decision, run the experiment on live traffic with random, persistent assignment; keep variants active concurrently; define the conversion event before launch; avoid changing other page elements during the test; and continue until the pre-defined sample size and test duration are reached. Check results by device and traffic source as secondary diagnostics, not as a reason to repeatedly peek and stop early.

## Limitations
- Synthetic data cannot establish how real Internee.pk visitors behave.
- The z-test assumes independent sessions and a properly randomized split.
- Session-level conversion is used here; use a consistent user/session definition in the real GA4 export.
- This simple analysis does not adjust for multiple comparisons or repeated testing.
"""
    (out / "analysis_report.md").write_text(report, encoding="utf-8")
    print(summary.round(4).to_string())
    print(f"\\nConversion test: p={p:.4f}; B-A={diff:.2%}; significant={significant}")
    print(f"Report saved to {out / 'analysis_report.md'}")

if __name__ == "__main__":
    main()
