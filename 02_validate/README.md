# 02 — Data Quality Validation

## Purpose

This folder contains data quality scripts that verify the synthetic dataset before analysis runs. All checks must pass before proceeding to `03_analyze/`.

## Files

| File | Description |
|---|---|
| `validate_data.py` | Python validation script — row counts, uniqueness, referential integrity, logic checks |
| `sql_quality_checks.sql` | SQL equivalents of the same checks for SQLite |

## How to Run

```bash
# From the repository root
python 02_validate/validate_data.py
```

All checks should return `PASS`. Results are written to `outputs/validation_results.csv`.

## Checks Performed

| Check | What it verifies |
|---|---|
| Core awardee count | Exactly 64 synthetic awardees |
| Vaccine long row count | Exactly 1,792 rows (64 awardees × 28 vaccines) |
| Incident long row count | Exactly 640 rows (64 awardees × 10 incident categories) |
| `awardee_id` uniqueness | No duplicate awardee IDs in core table |
| Vaccine referential integrity | All vaccine rows have a matching awardee in core |
| Incident referential integrity | All incident rows have a matching awardee in core |
| No negative ordered doses | `doses_ordered ≥ 0` for all rows |
| No negative wasted doses | `doses_wasted ≥ 0` for all rows |
| Wasted ≤ ordered | `doses_wasted ≤ doses_ordered` for all rows |
| Calculated loss formula | `calculated_loss_pct = round(doses_wasted / doses_ordered × 100, 3)` |
| Awardee summary row count | 64 summary rows |
| Vaccine type summary row count | 28 summary rows |
| Synthetic notice on all tables | Every row carries the required `synthetic_data_notice` label |

## Example Output

```
                         check_name status                              detail
                  Core awardee count   PASS              64 awardees generated; expected 64
            Vaccine long row count   PASS           1792 rows generated; expected 1,792
           Incident long row count   PASS             640 rows generated; expected 640
                   awardee_id unique   PASS                  Core awardee IDs are unique
       Vaccine rows have matching awardees   PASS           All vaccine rows map to core
      Incident rows have matching awardees   PASS          All incident rows map to core
           No negative ordered doses   PASS                All ordered doses >= 0
            No negative wasted doses   PASS                 All wasted doses >= 0
         Wasted doses <= ordered doses   PASS  All waste values are logically possible
             Calculated loss formula   PASS              max abs rounded diff=0.0
```

## Key Concepts

**Referential integrity:** Every row in `vaccine_order_waste_long.csv` and `vaccine_incidents.csv` must have a matching `awardee_id` in `core_survey.csv`. This mirrors the foreign key constraints defined in `04_sql/01_create_schema.sql`.

**Loss formula check:** The validation recalculates `doses_wasted / doses_ordered × 100` independently and confirms it matches `calculated_loss_pct` to within 0.002 — catching any floating-point rounding issues.

**Missingness report:** `outputs/missingness_report.csv` documents actual missing-value rates for each column in `core_survey.csv`. Conditional missingness (e.g., `repayment_months_allowed` is missing when `repayment_over_time_allowed = 0`) is expected and documented in `docs/data_dictionary.md`.
