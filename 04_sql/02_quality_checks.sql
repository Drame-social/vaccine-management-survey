-- 02_quality_checks.sql
-- Data quality checks for synthetic Vaccine Management Survey data.

-- 1. Row counts
SELECT 'core_survey_synthetic' AS table_name, COUNT(*) AS row_count FROM core_survey_synthetic
UNION ALL
SELECT 'vaccine_order_waste_long_synthetic', COUNT(*) FROM vaccine_order_waste_long_synthetic
UNION ALL
SELECT 'vaccine_incidents_synthetic', COUNT(*) FROM vaccine_incidents_synthetic;

-- 2. Awardee ID uniqueness
SELECT awardee_id, COUNT(*) AS n
FROM core_survey_synthetic
GROUP BY awardee_id
HAVING COUNT(*) > 1;

-- 3. Referential integrity gaps
SELECT v.awardee_id
FROM vaccine_order_waste_long_synthetic v
LEFT JOIN core_survey_synthetic c ON v.awardee_id = c.awardee_id
WHERE c.awardee_id IS NULL;

-- 4. Logic checks: waste cannot exceed ordered doses
SELECT awardee_id, vaccine_type_code, doses_ordered, doses_wasted
FROM vaccine_order_waste_long_synthetic
WHERE doses_wasted > doses_ordered OR doses_ordered < 0 OR doses_wasted < 0;

-- 5. Recalculate vaccine loss percentage
SELECT awardee_id, vaccine_type_code, doses_ordered, doses_wasted, calculated_loss_pct,
       ROUND(100.0*doses_wasted/NULLIF(doses_ordered,0),3) AS sql_calculated_loss_pct
FROM vaccine_order_waste_long_synthetic
WHERE doses_ordered > 0
  AND ABS(calculated_loss_pct - ROUND(100.0*doses_wasted/NULLIF(doses_ordered,0),3)) > 0.01;

-- 6. Synthetic notice check
SELECT synthetic_data_notice, COUNT(*) AS n
FROM vaccine_order_waste_long_synthetic
GROUP BY synthetic_data_notice;
