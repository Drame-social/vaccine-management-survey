# 03 — Descriptive Analysis

## Purpose

This folder contains the core analysis scripts that produce all summary outputs, figures, and interpretable findings. Two implementations are provided: Python (primary) and SAS (reference/validation).

## Files

| File | Description |
|---|---|
| `descriptive_analysis.py` | Python pipeline — produces all CSV outputs and PNG figures |
| `sas_analysis.sas` | SAS script — PROC MEANS / PROC FREQ / PROC SUMMARY equivalents |

## How to Run

```bash
# Python (from repository root)
python 03_analyze/descriptive_analysis.py
```

```sas
/* SAS — set libname/path to repository root */
%let root=.;
%include "03_analyze/sas_analysis.sas";
```

## Outputs Produced

| Output | Description |
|---|---|
| `outputs/awardee_vaccine_loss_summary.csv` | Per-awardee total ordered, wasted, loss %, standard loss %, incident total, reconciliation flag |
| `outputs/top_10_awardees_by_loss_pct.csv` | Top 10 awardees by overall vaccine loss percentage |
| `outputs/vaccine_loss_by_vaccine_type.csv` | Loss percentage by vaccine type, ordered and wasted doses |
| `outputs/region_staff_and_policy_summary.csv` | Regional breakdown: staffing, training completion, replacement policy |
| `outputs/top_vaccine_loss_ratios.png` | Bar chart of top 12 vaccine waste-to-order ratios |
| `outputs/awardee_loss_distribution.png` | Histogram of awardee loss percentages |

## Analysis Domains

### 1. Staffing and Training Gaps
Calculates total VFC and IQIP staff counts, trained staff, and training gaps per awardee and region. Identifies programs where staffing model (Centralized / Regionalized / Hybrid) may relate to training completion rates.

### 2. Vaccine Supply Policy
Frequencies of supply policy categories: offering all ACIP-recommended vaccines vs. awardee-defined menus vs. provider-specific ordering policies.

### 3. Deputization and Reporting
Counts of deputized LHDs, private providers, pharmacies, and birthing hospitals. Frequencies of dose-distribution reporting and reporting frequency.

### 4. Vaccine Orders, Waste, and Loss

```python
# Overall loss
total_wasted / total_ordered × 100 = 4.43%

# Standard analysis (excluding COVID-19 and Influenza)
standard_wasted / standard_ordered × 100 = 3.24%
```

### 5. Incident Reconciliation

```python
# Reconciliation flag logic
waste_vs_incident_difference = total_doses_wasted − incident_dose_grand_total
flag = "Review discrepancy" if abs(difference) > 0 else "Matched"
```

### 6. Replacement Policy
Frequencies of replacement requirement, replacement method, tiered policy rules, repayment-over-time allowance, and replacement caps.

## SAS Equivalents

The `sas_analysis.sas` script uses:
- `PROC MEANS` for staffing and loss statistics
- `PROC FREQ` for policy, deputization, and replacement frequencies
- `PROC SUMMARY` with `CLASS` for vaccine-type and awardee-region rollups
- `DATA` step logic to recalculate `sas_calculated_loss_pct` and compare to reported values
