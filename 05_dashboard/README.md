# 05 — Power BI Dashboard

## Purpose

`powerbi_measures.dax` contains all DAX calculated measures for a six-page Power BI dashboard built on the synthetic processed data tables.

## How to Connect

1. Open Power BI Desktop
2. **Get Data → Text/CSV** — import these three tables:
   - `data/processed/vaccine_order_waste_long.csv` → rename to `vaccine_order_waste_long_synthetic`
   - `data/raw/core_survey.csv` → rename to `core_survey_synthetic`
   - `data/raw/vaccine_incidents.csv` → rename to `vaccine_incidents_synthetic`
3. In the Model view, create relationships:
   - `vaccine_order_waste_long_synthetic[awardee_id]` → `core_survey_synthetic[awardee_id]`
   - `vaccine_incidents_synthetic[awardee_id]` → `core_survey_synthetic[awardee_id]`
4. Create a new measure for each entry in `powerbi_measures.dax`

## Dashboard Pages

| Page | Key Visuals |
|---|---|
| **Executive Summary** | KPI cards: total doses, loss %, standard loss %, awardee count, training completion |
| **Staffing & Training** | Bar chart by region — staff count vs. trained count; training gap map |
| **Policy & Deputization** | Donut charts — supply policy distribution; deputized entity counts |
| **Vaccine Loss & Waste** | Ranked bar chart — loss % by vaccine type; scatter: ordered vs. wasted |
| **Incident Reconciliation** | Table of reconciliation-flagged awardees; incident category breakdown |
| **Replacement Policy** | Stacked bar — replacement method by awardee type; repayment timeline |

## Key Measures

```dax
Vaccine Loss % = DIVIDE([Total Doses Wasted], [Total Doses Ordered])

Standard Vaccine Loss % =
DIVIDE(
    CALCULATE([Total Doses Wasted], vaccine_order_waste_long_synthetic[included_in_standard_analysis] = 1),
    CALCULATE([Total Doses Ordered], vaccine_order_waste_long_synthetic[included_in_standard_analysis] = 1)
)

Training Completion % = DIVIDE([Total Trained Staff], [Total Staff])

Reconciliation Status =
IF(ABS([Waste-Incident Difference]) = 0, "Matched", "Review discrepancy")
```

## Design Notes

- All KPI cards should display the synthetic data notice in a subtitle or tooltip
- Slicers recommended: Region, Awardee Type, Vaccine Type, Replacement Policy
- Conditional formatting on the reconciliation table: red rows where `Reconciliation Status = "Review discrepancy"`
- The standard loss measure (excluding COVID-19 and Influenza) should be displayed alongside the all-vaccine measure to demonstrate sensitivity analysis
