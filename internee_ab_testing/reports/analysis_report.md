# A/B Test Analysis Report

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
| Sessions | 1200 | 1200 |
| Engaged sessions | 646 | 746 |
| Bounce rate | 46.17% | 37.83% |
| Conversion rate | 7.50% | 9.25% |

## Statistical test
- Conversion-rate difference (B - A): 1.75% (1.75 percentage points)
- 95% confidence interval: [-0.47%, 3.97%]
- z statistic: 1.547
- p-value: 0.1218
- Statistically significant at 5%: No

## Interpretation
Variant B has the higher observed conversion rate.
The observed difference is not statistically significant at the 5% level; do not claim a proven winner.
The observed bounce-rate difference (B - A) is -8.33%. A negative value means Variant B has a lower bounce rate.

## Recommendation
Treat the result as a demonstration only. For a real decision, run the experiment on live traffic with random, persistent assignment; keep variants active concurrently; define the conversion event before launch; avoid changing other page elements during the test; and continue until the pre-defined sample size and test duration are reached. Check results by device and traffic source as secondary diagnostics, not as a reason to repeatedly peek and stop early.

## Limitations
- Synthetic data cannot establish how real Internee.pk visitors behave.
- The z-test assumes independent sessions and a properly randomized split.
- Session-level conversion is used here; use a consistent user/session definition in the real GA4 export.
- This simple analysis does not adjust for multiple comparisons or repeated testing.
