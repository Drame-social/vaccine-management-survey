# 04 — SQL Analysis

## Purpose

These SQL scripts demonstrate the full data workflow using SQLite — from schema creation through quality checks to analytic queries. They reproduce the same findings as the Python pipeline and can be run against any SQLite database loaded with the processed CSVs.

## Files

| File | Description |
|---|---|
| `01_create_schema.sql` | DDL — table definitions with primary keys, foreign keys, and NOT NULL constraints |
| `02_quality_checks.sql` | QA queries — row counts, uniqueness, referential integrity, logic checks, formula verification |
| `03_analysis_queries.sql` | Analytic queries — overall loss, standard loss, loss by vaccine type, loss by awardee/region, reconciliation |

## How to Load and Run

```bash
# Load data into SQLite and run all scripts
python3 - <<'EOF'
import sqlite3, pandas as pd
from pathlib import Path

ROOT = Path(".")
conn = sqlite3.connect("outputs/vms_analysis.sqlite")

pd.read_csv(ROOT/"data/raw/core_survey.csv").to_sql(
    "core_survey_synthetic", conn, if_exists="replace", index=False)
pd.read_csv(ROOT/"data/processed/vaccine_order_waste_long.csv").to_sql(
    "vaccine_order_waste_long_synthetic", conn, if_exists="replace", index=False)
pd.read_csv(ROOT/"data/raw/vaccine_incidents.csv").to_sql(
    "vaccine_incidents_synthetic", conn, if_exists="replace", index=False)

for script in ["04_sql/01_create_schema.sql",
               "04_sql/02_quality_checks.sql",
               "04_sql/03_analysis_queries.sql"]:
    sql = open(script).read()
    for stmt in sql.split(";"):
        s = stmt.strip()
        if s:
            try:
                print(conn.execute(s).fetchall()[:5])
            except Exception as e:
                pass

conn.close()
EOF
```

## Key Queries

### Overall vaccine loss

```sql
SELECT SUM(doses_ordered)  AS total_doses_ordered,
       SUM(doses_wasted)   AS total_doses_wasted,
       ROUND(100.0 * SUM(doses_wasted) / NULLIF(SUM(doses_ordered), 0), 2) AS loss_pct
FROM vaccine_order_waste_long_synthetic;
-- Result: 4.43%
```

### Loss excluding COVID-19 and Influenza

```sql
SELECT ROUND(100.0 * SUM(doses_wasted) / NULLIF(SUM(doses_ordered), 0), 2) AS standard_loss_pct
FROM vaccine_order_waste_long_synthetic
WHERE included_in_standard_analysis = 1;
-- Result: 3.24%
```

### Loss by vaccine type

```sql
SELECT vaccine_type,
       SUM(doses_ordered)  AS total_ordered,
       SUM(doses_wasted)   AS total_wasted,
       ROUND(100.0 * SUM(doses_wasted) / NULLIF(SUM(doses_ordered), 0), 2) AS loss_pct
FROM vaccine_order_waste_long_synthetic
GROUP BY vaccine_type
ORDER BY loss_pct DESC;
```

### Reconciliation: waste vs. incident totals

```sql
WITH waste AS (
  SELECT awardee_id, SUM(doses_wasted) AS total_waste
  FROM vaccine_order_waste_long_synthetic GROUP BY awardee_id
),
incidents AS (
  SELECT awardee_id, SUM(incident_dose_count) AS incident_total
  FROM vaccine_incidents_synthetic GROUP BY awardee_id
)
SELECT w.awardee_id,
       w.total_waste,
       i.incident_total,
       w.total_waste - i.incident_total AS difference
FROM waste w JOIN incidents i ON w.awardee_id = i.awardee_id
WHERE w.total_waste <> i.incident_total
ORDER BY ABS(w.total_waste - i.incident_total) DESC;
```

## Schema Design

The three core tables model a normalized survey schema:

```
core_survey_synthetic          (PK: awardee_id)
        |
        ├── vaccine_order_waste_long_synthetic  (FK: awardee_id)
        └── vaccine_incidents_synthetic         (FK: awardee_id)
```

This structure supports flexible GROUP BY analysis across awardee, vaccine type, region, and incident category without data redundancy.
