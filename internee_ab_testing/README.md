# Internee.pk Homepage A/B Testing

A GitHub-ready, reproducible project for comparing two homepage design variants using bounce rate, engagement rate, and conversion rate.

## Important data transparency
The included CSV is **synthetic demonstration data**. It is not collected from Internee.pk and is not a Google Analytics export. No Internee.pk analytics credentials or private website data were provided. Do not present the sample results as real company findings. Replace the CSV with authorized analytics data to produce a genuine result.

## Experiment design
- **A (control):** Current homepage.
- **B (treatment):** Proposed homepage with a clearer headline and more prominent primary call-to-action.
- **Primary metric:** Conversion rate.
- **Secondary metrics:** Bounce rate and engagement rate.
- **Allocation:** 50/50 random split, with a persistent assignment per visitor.
- **Decision rule:** Two-sided two-proportion z-test at alpha = 0.05, alongside the effect size and 95% confidence interval.

## Dataset schema
`data/ab_test_sessions.csv` contains:
- `session_id`: unique session identifier
- `variant`: A or B
- `engaged_session`: 1 if GA4 considers the session engaged, otherwise 0
- `converted`: 1 if the chosen conversion event occurred, otherwise 0
- `device`: device category (optional diagnostic)
- `source`: traffic source category (optional diagnostic)

For real GA4 data, export one row per session with the experiment variant and these binary outcomes. Ensure each session is assigned to exactly one variant.

## Run locally
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python src/analyze_ab_test.py
```
Outputs:
- `reports/variant_summary.csv`
- `reports/ab_test_comparison.png`
- `reports/analysis_report.md`

Use a different input file:
```bash
python src/analyze_ab_test.py --input data/your_ga4_export.csv --output reports
```

## GA4 implementation notes
Google Analytics 4 does not itself serve homepage variants; use an experiment/feature-flag system to randomize and serve A/B variants. Send an exposure event when a visitor is assigned, including experiment and variant identifiers. Register those event parameters as event-scoped custom dimensions in GA4, then compare the variant cohorts in Explorations.

Example client-side exposure event (replace the experiment ID and variant with values supplied by your experiment system):
```javascript
gtag('event', 'experiment_impression', {
  experiment_id: 'internee_homepage_2026',
  variant_id: 'A'
});
```
Track the actual primary action using a GA4 recommended event where appropriate (for example `generate_lead` or `sign_up`) and mark it as a key event if it represents a meaningful business outcome. Do not fire a conversion event merely because the page loaded.

## Suggested test procedure
1. Confirm the business conversion (e.g., successful lead form submission) with the Internee.pk team.
2. Record the current homepage as A and create a single focused change for B.
3. Use a testing platform or feature-flag service to assign visitors randomly and persistently.
4. Fire an experiment exposure event and conversion event with consistent identifiers.
5. Verify events in GA4 Realtime/DebugView before starting the measurement window.
6. Run both variants concurrently and avoid editing either during the experiment.
7. Decide sample size and minimum run time before launch; include a full weekly cycle where possible.
8. Export data and run this analysis. Report effect size, confidence interval, p-value, and limitations.

## Repository structure
```text
internee_ab_testing/
├── data/
│   └── ab_test_sessions.csv
├── reports/
│   └── analysis_report.md
├── src/
│   └── analyze_ab_test.py
├── requirements.txt
└── README.md
```

## References
- Google Analytics Help — A/B testing: https://support.google.com/analytics/answer/13468470
- Google for Developers — Experiment integration with GA4: https://developers.google.com/analytics/devguides/collection/ga4/integration
- Google Analytics Help — Engagement rate and bounce rate: https://support.google.com/analytics/answer/12195621
- Google Analytics Help — Recommended events: https://support.google.com/analytics/answer/9267735
