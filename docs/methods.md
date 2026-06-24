# Methods: Synthetic Vaccine Management Survey Analytics

## 1. Analytic scope

This project analyzes synthetic awardee-level survey data modeled after a Vaccine Management Survey workflow. It covers six domains:

1. Staffing and trained staff
2. Vaccine supply policy
3. Deputization and reporting practices
4. Vaccine orders, waste, and loss
5. Vaccine storage and handling incident categories
6. Vaccine replacement policy

## 2. Dataset strategy

A live search was performed for a public row-level Vaccine Management Survey or VFC awardee vaccine management dataset. A suitable public row-level dataset was not identified. CDC public materials describe VFC vaccine management, storage/handling, PEAR oversight, and vaccine price lists, but the row-level survey and oversight data needed for this analysis are not public.

Because public data are insufficient, the project uses synthetic data. The synthetic dataset is safe for GitHub because it contains no real CDC data, no PEAR data, no VTrckS data, no patient-level data, no provider identifiers, and no real awardee names.

## 3. Synthetic data generation

The generator creates 64 synthetic awardees and 28 vaccine types. The core survey table includes staffing, policy, deputization, incident-source, and replacement-policy variables. Vaccine order and waste records are generated using a size index, vaccine-specific expected demand, and vaccine-specific waste-rate assumptions.

Waste rates are intentionally higher for vaccines that often require more complex seasonal or demand management in the synthetic scenario, such as influenza, COVID-19, mpox, nirsevimab, and RSV maternal products. This is not a factual estimate; it is a synthetic demonstration assumption.

## 4. Descriptive analysis

The analysis computes:

- Staff totals and training gaps
- Staffing model frequencies
- Vaccine supply policy frequencies
- Deputization practices
- Dose-reporting frequency
- Total ordered doses
- Total wasted doses
- Overall vaccine loss percentage
- Vaccine loss percentage excluding COVID-19 and influenza
- Vaccine loss by vaccine type
- Vaccine loss by awardee and region
- Incident-category totals
- Waste-to-incident reconciliation differences
- Vaccine replacement policy frequencies

## 5. Data quality checks

Validation checks include:

- Core awardee row count equals 64
- `awardee_id` uniqueness
- Referential integrity from vaccine and incident tables to core awardee table
- No negative ordered or wasted doses
- Wasted doses do not exceed ordered doses
- `calculated_loss_pct` equals `100 * doses_wasted / doses_ordered`
- Synthetic data notice exists on every row
- Missingness report generated for all columns

## 6. SQL plan

SQL scripts are included for schema creation, data-quality checks, and analytic summaries:

- `scripts/sql/01_create_schema.sql`
- `scripts/sql/02_quality_checks.sql`
- `scripts/sql/03_analysis_queries.sql`

The SQL analysis reproduces overall loss, standard loss excluding COVID-19 and influenza, vaccine-type loss, awardee loss, and reconciliation checks.

## 7. SAS plan

The SAS script mirrors the original SAS-style survey analysis:

- Import core, vaccine long, and incident data
- Use `PROC MEANS` for staffing and vaccine-loss summaries
- Use `PROC FREQ` for policy, deputization, reporting, and replacement variables
- Use `PROC SUMMARY` for vaccine-type and incident-category rollups
- Reconcile order/waste totals against incident-category totals

SAS file: `scripts/sas/analysis_vaccine_management_survey.sas`

## 8. Python pipeline steps

1. Generate deterministic synthetic data.
2. Save raw synthetic wide tables and normalized long table.
3. Validate row counts, IDs, logic checks, and formulas.
4. Produce processed summaries.
5. Export CSV outputs and PNG figures.

Scripts:

- `scripts/python/generate_synthetic_data.py`
- `scripts/python/validate_synthetic_data.py`
- `scripts/python/run_analysis.py`

## 9. Dashboard metrics

Recommended dashboard metrics:

- Total doses ordered
- Total doses wasted
- Vaccine loss percentage
- Standard loss percentage excluding COVID-19 and influenza
- Awardee count
- Staff training completion percentage
- Staff training gap
- Replacement policy percentage
- Incident dose total
- Waste-incident reconciliation difference

DAX measures are saved in `scripts/powerbi/vms_powerbi_measures.dax`.

## 10. Interpretation plan

Interpretation should focus on synthetic program-monitoring questions:

- Which synthetic awardees have high vaccine loss percentages?
- Are loss percentages concentrated in seasonal or newer vaccine categories?
- Do staffing/training gaps align with higher waste-to-order ratios?
- Are storage/handling incident totals consistent with order/waste totals?
- How common are replacement policies, tiered replacement rules, and repayment options?

No result should be interpreted as a real CDC, VFC, awardee, provider, or patient finding.
