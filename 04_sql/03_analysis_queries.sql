-- 03_analysis_queries.sql
-- Analysis queries for synthetic Vaccine Management Survey data.

-- Overall vaccine waste-to-order ratio
SELECT SUM(doses_ordered) AS total_doses_ordered,
       SUM(doses_wasted) AS total_doses_wasted,
       ROUND(100.0 * SUM(doses_wasted) / NULLIF(SUM(doses_ordered),0), 2) AS loss_pct_all_vaccines
FROM vaccine_order_waste_long_synthetic;

-- Overall vaccine waste-to-order ratio excluding COVID-19 and influenza
SELECT SUM(doses_ordered) AS total_doses_ordered,
       SUM(doses_wasted) AS total_doses_wasted,
       ROUND(100.0 * SUM(doses_wasted) / NULLIF(SUM(doses_ordered),0), 2) AS loss_pct_excluding_covid_flu
FROM vaccine_order_waste_long_synthetic
WHERE included_in_standard_analysis = 1;

-- Loss by vaccine type
SELECT vaccine_type,
       SUM(doses_ordered) AS total_ordered,
       SUM(doses_wasted) AS total_wasted,
       ROUND(100.0 * SUM(doses_wasted) / NULLIF(SUM(doses_ordered),0), 2) AS loss_pct
FROM vaccine_order_waste_long_synthetic
GROUP BY vaccine_type
ORDER BY loss_pct DESC;

-- Loss by awardee and region
SELECT c.region, c.awardee_type, v.awardee_id,
       SUM(v.doses_ordered) AS total_ordered,
       SUM(v.doses_wasted) AS total_wasted,
       ROUND(100.0 * SUM(v.doses_wasted) / NULLIF(SUM(v.doses_ordered),0), 2) AS loss_pct
FROM vaccine_order_waste_long_synthetic v
JOIN core_survey_synthetic c ON v.awardee_id = c.awardee_id
GROUP BY c.region, c.awardee_type, v.awardee_id
ORDER BY loss_pct DESC;

-- Reconciliation: Section IV order/waste vs Section V incident categories
WITH waste AS (
  SELECT awardee_id, SUM(doses_wasted) AS total_waste
  FROM vaccine_order_waste_long_synthetic
  GROUP BY awardee_id
), incidents AS (
  SELECT awardee_id, SUM(incident_dose_count) AS incident_total
  FROM vaccine_incidents_synthetic
  GROUP BY awardee_id
)
SELECT w.awardee_id, w.total_waste, i.incident_total, w.total_waste - i.incident_total AS difference
FROM waste w JOIN incidents i ON w.awardee_id = i.awardee_id
WHERE w.total_waste <> i.incident_total
ORDER BY ABS(w.total_waste - i.incident_total) DESC;
