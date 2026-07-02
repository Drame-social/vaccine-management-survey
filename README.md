# Vaccine Management Survey Analytics

*By Aly Drame, MD, MPH, MBA.* Awardee-level vaccine-management monitoring (Python / SAS / SQLite / Power BI) over a synthetic Vaccine Management Survey: staffing gaps, waste-to-order ratios, storage/handling incidents, and replacement-policy rules. No real CDC, VFC, PEAR, VTrckS, awardee, provider, or patient data are included.

---

## Overview

This project demonstrates awardee-level immunization program monitoring analytics modeled after a Vaccine Management Survey workflow. It answers the question:

> **How can an immunization program monitor vaccine management performance across awardees by assessing staffing gaps, supply policy variation, deputization practices, vaccine waste-to-order ratios, storage/handling incidents, and replacement-policy rules?**

The analysis covers 64 synthetic awardees across six program-monitoring domains:

1. Staffing and training gap assessment
2. Vaccine supply policy variation
3. Deputization and dose-distribution reporting practices
4. Vaccine orders, waste, and calculated loss percentages
5. Storage and handling incident categorization
6. Vaccine replacement policy and repayment rules

---

## Key Findings (Synthetic Data)

| Metric | Result |
|---|---:|
| Synthetic awardees analyzed | 64 |
| Vaccine types | 28 |
| Total synthetic doses ordered | 12,954,807 |
| Total synthetic doses wasted | 573,251 |
| Overall vaccine loss percentage | **4.43%** |
| Standard loss (excl. COVID-19 & Influenza) | **3.24%** |
| Awardees requiring vaccine replacement | **82.8%** |
| Staff training completion rate | **83.1%** |
| Awardees flagged for reconciliation review | **6** |

### Highest Synthetic Vaccine Loss Ratios

| Vaccine | Loss % |
|---|---:|
| Influenza | 11.0% |
| COVID-19 | 10.5% |
| Mpox | 8.4% |
| Dengue | 7.6% |
| Nirsevimab | 6.0% |

Higher loss ratios cluster in seasonal and newer products; influenza is both the largest-volume and the highest-loss product, so the pattern reflects demand predictability rather than order size.

---

## Repository Structure

```
vaccine-management-survey/
├── 01_generate_data/          # Synthetic data generation script
├── 02_validate/               # Data quality checks (Python + SQL)
├── 03_analyze/                # Descriptive analysis (Python + SAS)
├── 04_sql/                    # SQL schema and analysis queries
├── 05_dashboard/              # Power BI DAX measures
├── data/
│   ├── raw/                   # Raw synthetic survey tables
│   └── processed/             # Normalized and summarized outputs
├── docs/                      # Methods, data dictionary, results, limitations
└── outputs/                   # Figures and CSV outputs
```

---

## Analysis Workflow

```
01_generate_data/generate_data.py
         ↓ creates data/raw/ and data/processed/
02_validate/validate_data.py
         ↓ all checks pass → outputs/validation_results.csv
03_analyze/descriptive_analysis.py
         ↓ produces outputs/  (CSVs + PNGs)
04_sql/  (01_create_schema.sql → 02_quality_checks.sql → 03_analysis_queries.sql)
05_dashboard/powerbi_measures.dax
         ↓ connect processed CSVs as Power BI data source
```

---

## How to Run

```bash
git clone https://github.com/Drame-social/vaccine-management-survey.git
cd vaccine-management-survey
pip install -r requirements.txt

# Step 1: Generate synthetic data
python 01_generate_data/generate_data.py

# Step 2: Validate
python 02_validate/validate_data.py

# Step 3: Analyze
python 03_analyze/descriptive_analysis.py
```

All scripts use relative paths anchored to the repository root — no hardcoded local paths.

---

## Datasets

| File | Grain | Description |
|---|---|---|
| `data/raw/core_survey.csv` | 1 row / awardee | Staffing, policy, deputization, replacement |
| `data/raw/vaccine_incidents.csv` | 1 row / awardee × incident category | Storage/handling incident dose counts |
| `data/raw/vaccine_orders_wide.csv` | 1 row / awardee | Wide-format ordered doses by vaccine type |
| `data/raw/vaccine_waste_wide.csv` | 1 row / awardee | Wide-format wasted doses by vaccine type |
| `data/raw/vaccine_loss_reported_wide.csv` | 1 row / awardee | Wide-format reported loss percentages |
| `data/processed/vaccine_order_waste_long.csv` | 1 row / awardee × vaccine | Normalized analysis table |
| `data/processed/awardee_vaccine_loss_summary.csv` | 1 row / awardee | Aggregated awardee summary |
| `data/processed/vaccine_type_loss_summary.csv` | 1 row / vaccine type | Vaccine-level loss summary |
| `data/processed/staff_training_gap_summary.csv` | Summary metrics | Staff training totals |

---

## Tools and Skills Demonstrated

- **Python (pandas, numpy, matplotlib):** Data generation, validation, descriptive analysis, visualization
- **SAS:** PROC MEANS, PROC FREQ, PROC SUMMARY — standard immunization survey analysis style
- **SQL (SQLite):** Schema design, referential integrity checks, multi-table analysis queries
- **Power BI DAX:** Calculated measures for executive dashboard
- **Data quality:** Missingness reporting, logic validation, reconciliation flagging

---

## Disclaimer

All data are synthetic and generated solely for portfolio demonstration. They must not be interpreted as real CDC, VFC, PEAR, VTrckS, awardee, provider, or patient findings.
