/* analysis_vaccine_management_survey.sas
   Synthetic Vaccine Management Survey analysis.
   Data are synthetic portfolio data only: no real CDC, PEAR, VTrckS, provider, patient, or awardee data. */

%let root=.;

proc import datafile="&root./data/raw/core_survey_.csv"
    out=core dbms=csv replace;
    guessingrows=max;
run;

proc import datafile="&root./data/processed/vaccine_order_waste_long_.csv"
    out=vaccine_long dbms=csv replace;
    guessingrows=max;
run;

proc import datafile="&root./data/raw/vaccine_incidents_.csv"
    out=incidents dbms=csv replace;
    guessingrows=max;
run;

/* Section I: Staff counts and training gaps */
proc means data=core n mean median q1 q3 min max;
    var vfc_staff_count iqip_staff_count total_staff_count
        vfc_staff_trained iqip_staff_trained total_staff_trained
        vfc_staff_training_gap iqip_staff_training_gap total_staff_training_gap;
run;

proc freq data=core;
    tables vfc_staff_model iqip_staff_model / missing;
run;

/* Section II: Vaccine supply policy */
proc freq data=core;
    tables vaccine_supply_policy policy_changed_since_prior_bp offer_all_acip_pediatric_vaccines / missing;
run;

/* Section III: Deputization and reporting */
proc freq data=core;
    tables delegate_authority deputized_visit_model reports_doses_distributed reporting_frequency_defined dose_reporting_frequency / missing;
run;

proc means data=core n mean median min max;
    where delegate_authority=1;
    var deputized_lhd_count deputized_private_provider_count deputized_pharmacy_count deputized_birthing_hospital_count deputized_other_count;
run;

/* Section IV: Orders, waste, and calculated vaccine loss */
data vaccine_long;
    set vaccine_long;
    if doses_ordered > 0 then sas_calculated_loss_pct = round((doses_wasted / doses_ordered) * 100, .001);
run;

proc means data=vaccine_long n sum mean median min max;
    var doses_ordered doses_wasted calculated_loss_pct;
run;

proc summary data=vaccine_long nway;
    class vaccine_type;
    var doses_ordered doses_wasted;
    output out=vaccine_type_summary sum=;
run;

data vaccine_type_summary;
    set vaccine_type_summary;
    loss_pct = round((doses_wasted / doses_ordered) * 100, .01);
run;

proc sort data=vaccine_type_summary;
    by descending loss_pct;
run;

proc print data=vaccine_type_summary;
    var vaccine_type doses_ordered doses_wasted loss_pct;
run;

/* Standard analysis excluding COVID-19 and influenza */
proc summary data=vaccine_long nway;
    where included_in_standard_analysis=1;
    var doses_ordered doses_wasted;
    output out=standard_loss sum=;
run;

data standard_loss;
    set standard_loss;
    loss_pct_excluding_covid_flu = round((doses_wasted / doses_ordered) * 100, .01);
run;

proc print data=standard_loss;
run;

/* Section V: Storage and handling incident categories */
proc summary data=incidents nway;
    class incident_category;
    var incident_dose_count;
    output out=incident_summary sum=;
run;

proc sort data=incident_summary;
    by descending incident_dose_count;
run;

proc print data=incident_summary;
run;

/* Reconciliation of reported waste and incident-category total */
proc summary data=vaccine_long nway;
    class awardee_id;
    var doses_wasted;
    output out=waste_total sum=total_doses_wasted;
run;

proc summary data=incidents nway;
    class awardee_id;
    var incident_dose_count;
    output out=incident_total sum=incident_dose_grand_total;
run;

proc sort data=waste_total; by awardee_id; run;
proc sort data=incident_total; by awardee_id; run;

data reconciliation;
    merge waste_total incident_total;
    by awardee_id;
    difference = total_doses_wasted - incident_dose_grand_total;
run;

proc print data=reconciliation;
    where difference ne 0;
run;

/* Section VI: Vaccine replacement policy */
proc freq data=core;
    tables requires_vaccine_replacement replacement_applies_vfc replacement_applies_317
           replacement_applies_state_funded replacement_applies_chip
           replacement_policies_differ_by_fund_type tiered_replacement_policy
           repayment_over_time_allowed shipments_continue_during_replacement replacement_method
           replacement_cap_exists / missing;
run;
