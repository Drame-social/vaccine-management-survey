# 01 — Synthetic Data Generation

## Purpose

`generate_data.py` creates all synthetic datasets needed for this project. It produces a deterministic set of 64 awardees, 28 vaccine types, and 10 incident categories — a total of 2,432 rows across raw and normalized tables.

No real CDC, VFC, PEAR, VTrckS, awardee, provider, or patient records are used or reproduced.

## How to Run

```bash
# From the repository root
python 01_generate_data/generate_data.py
```

Expected output:
```
Synthetic data generated successfully.
Awardees: 64 | Vaccine rows: 1792 | Incident rows: 640
```

## Files Produced

| Output | Location | Description |
|---|---|---|
| `core_survey.csv` | `data/raw/` | Core awardee survey table (staffing, policy, deputization, replacement) |
| `vaccine_orders_wide.csv` | `data/raw/` | Wide-format ordered doses — one column per vaccine type |
| `vaccine_waste_wide.csv` | `data/raw/` | Wide-format wasted doses |
| `vaccine_loss_reported_wide.csv` | `data/raw/` | Wide-format self-reported loss percentages |
| `vaccine_incidents.csv` | `data/raw/` | Incident category dose counts |
| `vaccine_order_waste_long.csv` | `data/processed/` | Normalized long table — one row per awardee × vaccine |
| `awardee_vaccine_loss_summary.csv` | `data/processed/` | Awardee-level aggregated loss and reconciliation flag |
| `vaccine_type_loss_summary.csv` | `data/processed/` | Vaccine-type loss summary |
| `staff_training_gap_summary.csv` | `data/processed/` | Staff training totals |

## Key Design Decisions

**Awardee types:** 50 State Programs, 6 Large City Programs, 8 Territorial Programs — proportional to real VFC program counts.

**Vaccine waste rates:** Synthetic waste rates are intentionally higher for seasonal and newer products (Influenza: 9.5%, COVID-19: 8.5%, Mpox: 7.0%) to demonstrate analytic differentiation. These are not factual estimates.

**Reconciliation discrepancies:** For approximately 15% of awardees, the synthetic incident-category dose total is allowed to differ from the waste total, simulating the real-world program-monitoring need for reconciliation follow-up.

**Seed:** `SEED = 20260618` — fully deterministic; re-running always produces the same dataset.

## Key Concepts

- **Waste-to-order ratio:** `doses_wasted / doses_ordered × 100`
- **Standard analysis:** Excludes COVID-19 and Influenza (field `included_in_standard_analysis`)
- **Reconciliation flag:** Set to `"Review discrepancy"` when `abs(total_doses_wasted − incident_dose_grand_total) > 0`

## Example

```python
from pathlib import Path
import pandas as pd

ROOT = Path(".")
core = pd.read_csv(ROOT / "data/raw/core_survey.csv")
print(core[["awardee_id", "awardee_type", "region", "total_staff_count",
            "total_staff_training_gap", "requires_vaccine_replacement"]].head())
```

```
  awardee_id               awardee_type    region  total_staff_count  total_staff_training_gap  requires_vaccine_replacement
0  SYN-AWD-001  State Immunization Program     South                 38                         4                             1
1  SYN-AWD-002  State Immunization Program  Midwest                 27                         3                             1
2  SYN-AWD-003  State Immunization Program     West                 19                         2                             0
```
