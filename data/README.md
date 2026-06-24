# Data

All data files in this folder are **synthetic**. They were generated programmatically by `01_generate_data/generate_data.py` and do not contain any real CDC, VFC, PEAR, VTrckS, awardee, provider, or patient records.

## raw/

Raw synthetic survey tables — one row per awardee (wide tables) or one row per awardee × category (long tables).

| File | Rows | Columns | Description |
|---|---|---|---|
| `core_survey.csv` | 64 | 55 | Core awardee survey — staffing, policy, deputization, replacement |
| `vaccine_incidents.csv` | 640 | 8 | Storage/handling incident dose counts — 10 categories × 64 awardees |
| `vaccine_orders_wide.csv` | 64 | 30 | Ordered doses — one column per vaccine type (SAS-style wide format) |
| `vaccine_waste_wide.csv` | 64 | 30 | Wasted doses — one column per vaccine type |
| `vaccine_loss_reported_wide.csv` | 64 | 30 | Self-reported loss percentages — one column per vaccine type |

## processed/

Normalized and aggregated tables ready for analysis, SQL loading, and Power BI.

| File | Rows | Columns | Description |
|---|---|---|---|
| `vaccine_order_waste_long.csv` | 1,792 | 11 | Normalized — one row per awardee × vaccine type |
| `awardee_vaccine_loss_summary.csv` | 64 | 16 | Awardee-level aggregate: loss %, standard loss %, reconciliation flag |
| `vaccine_type_loss_summary.csv` | 28 | 8 | Vaccine-type aggregate: total ordered, wasted, loss %, awardees with orders |
| `staff_training_gap_summary.csv` | 3 | 3 | Program-wide staffing totals |

## Key Column Definitions

| Column | Table | Definition |
|---|---|---|
| `awardee_id` | all | Synthetic awardee identifier — primary key (format: `SYN-AWD-001`) |
| `doses_ordered` | vaccine_order_waste_long | Synthetic doses ordered from the program in the survey year |
| `doses_wasted` | vaccine_order_waste_long | Synthetic doses reported as wasted, spoiled, or excess |
| `calculated_loss_pct` | vaccine_order_waste_long | `doses_wasted / doses_ordered × 100`, rounded to 3 decimal places |
| `included_in_standard_analysis` | vaccine_order_waste_long | 1 = include; 0 = exclude (COVID-19 and Influenza are excluded) |
| `reconciliation_flag` | awardee_vaccine_loss_summary | `"Matched"` or `"Review discrepancy"` |
| `synthetic_data_notice` | all | Required label — value: `SYNTHETIC_PORTFOLIO_DATA_NOT_REAL_CDC_OR_AWARDEE_DATA` |

Full column-level definitions are in `docs/data_dictionary.md`.
