# Outputs

This folder contains all analysis outputs — figures and CSV tables — produced by the analysis pipeline.

## Figures

| File | Description |
|---|---|
| `top_vaccine_loss_ratios.png` | Bar chart — top 12 vaccine types by synthetic waste-to-order ratio |
| `awardee_loss_distribution.png` | Histogram — distribution of awardee-level vaccine loss percentages |

## CSV Tables

| File | Description |
|---|---|
| `awardee_vaccine_loss_summary.csv` | Per-awardee aggregate: doses ordered/wasted, loss %, standard loss %, incident total, reconciliation flag |
| `top_10_awardees_by_loss_pct.csv` | Top 10 awardees by overall synthetic vaccine loss percentage |
| `vaccine_loss_by_vaccine_type.csv` | Loss percentage by vaccine type |
| `region_staff_and_policy_summary.csv` | Regional staffing, training completion, and policy summary |
| `validation_results.csv` | Quality check results — all checks should be `PASS` |
| `missingness_report.csv` | Missing value rates by column in `core_survey.csv` |

## Notes

All outputs are derived from synthetic data and are not factual findings. Re-running `03_analyze/descriptive_analysis.py` regenerates these files deterministically from the same seeded dataset.
