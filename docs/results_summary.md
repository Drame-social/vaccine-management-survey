# Results Summary: Synthetic Vaccine Management Survey Analytics

## Data validation

All major validation checks passed. See `outputs/validation_results.csv`.

Key validation counts:

| Item | Count |
|---|---:|
| Synthetic awardees | 64 |
| Vaccine types | 28 |
| Awardee-vaccine rows | 1,792 |
| Incident-category rows | 640 |

## Main synthetic findings

| Metric | Result |
|---|---:|
| Total synthetic doses ordered | 12,954,807 |
| Total synthetic doses wasted | 573,251 |
| Overall synthetic vaccine loss percentage | 4.43% |
| Synthetic loss percentage excluding COVID-19 and influenza | 3.24% |
| Synthetic awardees requiring vaccine replacement | 82.8% |
| Synthetic total staff training completion | 83.1% |
| Awardees needing reconciliation review | 6 |

## Highest synthetic vaccine-loss ratios by vaccine type

| Vaccine type | Doses ordered | Doses wasted | Loss % |
|---|---:|---:|---:|
| Influenza | 1,338,571 | 147,188 | 11.0 |
| COVID-19 | 685,742 | 71,814 | 10.5 |
| Mpox | 5,767 | 484 | 8.4 |
| Dengue | 13,425 | 1,025 | 7.6 |
| Nirsevimab | 392,009 | 23,524 | 6.0 |
| RSV Maternal | 140,797 | 7,405 | 5.3 |
| MenABCWY | 50,822 | 2,644 | 5.2 |
| HepA-HepB | 69,255 | 3,001 | 4.3 |
| MMRV | 160,295 | 6,936 | 4.3 |
| Td | 94,219 | 4,059 | 4.3 |

## Interpretation

The synthetic data concentrate the highest waste-to-order ratios in seasonal and newer products (influenza, COVID-19, Mpox, dengue, RSV/nirsevimab), where ordering is harder to match to actual uptake. Volume alone does not explain the pattern — influenza carries both the largest order volume and the highest loss ratio — so the driver here is product type and demand predictability, not order size. The synthetic standard analysis excluding COVID-19 and influenza produces a lower vaccine-loss percentage than the all-vaccine estimate, which is expected because those two products were generated with higher synthetic waste-rate assumptions.

The reconciliation flag identifies synthetic awardees where the Section IV-style order/waste total does not equal the Section V-style incident-category total. In a real workflow, those records would require program follow-up, source-system review, or documentation of timing/source differences.

## Files produced

- `outputs/validation_results.csv`
- `outputs/missingness_report.csv`
- `outputs/top_10_awardees_by_loss_pct.csv`
- `outputs/vaccine_loss_by_vaccine_type.csv`
- `outputs/region_staff_and_policy_summary.csv`
- `outputs/top_vaccine_loss_ratios.png`
- `outputs/awardee_loss_distribution.png`

## Caution

These are synthetic findings only. They are not real CDC, VFC, awardee, provider, or patient findings.
