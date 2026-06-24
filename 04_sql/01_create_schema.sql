-- 01_create_schema.sql
-- SQLite schema for synthetic Vaccine Management Survey portfolio data.
-- All data are synthetic and must not be interpreted as CDC, VTrckS, PEAR, provider, patient, or awardee records.

CREATE TABLE IF NOT EXISTS core_survey_synthetic (
    survey_year INTEGER NOT NULL,
    awardee_id TEXT PRIMARY KEY,
    awardee_name TEXT NOT NULL,
    awardee_type TEXT NOT NULL,
    region TEXT NOT NULL,
    program_size_index REAL,
    vfc_staff_count REAL,
    iqip_staff_count REAL,
    total_staff_count INTEGER,
    vfc_staff_trained REAL,
    iqip_staff_trained REAL,
    total_staff_trained INTEGER,
    vfc_staff_training_gap REAL,
    iqip_staff_training_gap REAL,
    total_staff_training_gap INTEGER,
    vfc_staff_model TEXT,
    iqip_staff_model TEXT,
    vaccine_supply_policy TEXT,
    policy_changed_since_prior_bp INTEGER,
    offer_all_acip_pediatric_vaccines INTEGER,
    delegate_authority INTEGER,
    reports_doses_distributed INTEGER,
    reporting_frequency_defined INTEGER,
    dose_reporting_frequency TEXT,
    vaccine_patient_type TEXT,
    esw_data_source TEXT,
    vsh_data_type TEXT,
    vsh_data_source TEXT,
    requires_vaccine_replacement INTEGER,
    replacement_method TEXT,
    synthetic_data_notice TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS vaccine_order_waste_long_synthetic (
    survey_year INTEGER NOT NULL,
    awardee_id TEXT NOT NULL,
    vaccine_type_code TEXT NOT NULL,
    vaccine_type TEXT NOT NULL,
    vaccine_patient_type TEXT,
    doses_ordered INTEGER NOT NULL,
    doses_wasted INTEGER NOT NULL,
    reported_loss_pct REAL,
    calculated_loss_pct REAL,
    reported_minus_calculated_pct REAL,
    included_in_standard_analysis INTEGER NOT NULL,
    synthetic_data_notice TEXT NOT NULL,
    FOREIGN KEY (awardee_id) REFERENCES core_survey_synthetic(awardee_id)
);

CREATE TABLE IF NOT EXISTS vaccine_incidents_synthetic (
    survey_year INTEGER NOT NULL,
    awardee_id TEXT NOT NULL,
    incident_category_code TEXT NOT NULL,
    incident_category TEXT NOT NULL,
    incident_dose_count INTEGER NOT NULL,
    incident_explanation_required INTEGER,
    incident_explanation_text TEXT,
    synthetic_data_notice TEXT NOT NULL,
    FOREIGN KEY (awardee_id) REFERENCES core_survey_synthetic(awardee_id)
);
