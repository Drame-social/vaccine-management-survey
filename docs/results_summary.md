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

| vaccine_type   |   total_doses_ordered |   total_doses_wasted |   loss_pct |
|:---------------|----------------------:|---------------------:|-----------:|
| Influenza      |               1338571 |               147188 |     10.996 |
| COVID-19       |                685742 |                71814 |     10.472 |
| Mpox           |                  5767 |                  484 |      8.393 |
| Dengue         |                 13425 |                 1025 |      7.635 |
| Nirsevimab     |                392009 |                23524 |      6.001 |
| RSV Maternal   |                140797 |                 7405 |      5.259 |
| MenABCWY       |                 50822 |                 2644 |      5.202 |
| HepA-HepB      |                 69255 |                 3001 |      4.333 |
| MMRV           |                160295 |                 6936 |      4.327 |
| Td             |                 94219 |                 4059 |      4.308 |

## Interpretation

The synthetic data show a coherent pattern: higher waste-to-order ratios are concentrated in vaccine categories with lower or more variable ordering volumes and in seasonal/newer products. The synthetic standard analysis excluding COVID-19 and influenza produces a lower vaccine-loss percentage than the all-vaccine estimate, which is expected because those two products were generated with higher synthetic waste-rate assumptions.

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
