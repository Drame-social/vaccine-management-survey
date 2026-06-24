"""
Generate synthetic Vaccine Management Survey data.

This script creates GitHub-safe synthetic data only. It does not use or reproduce
real CDC, PEAR, VTrckS, awardee, provider, or patient records.

Run from the repository root or from any location:
    python scripts/python/generate_synthetic_data.py
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
OUTPUTS = ROOT / "outputs"
for path in [RAW, PROCESSED, OUTPUTS]:
    path.mkdir(parents=True, exist_ok=True)

NOTICE = "SYNTHETIC_PORTFOLIO_DATA_NOT_REAL_CDC_OR_AWARDEE_DATA"
SEED = 20260618
rng = np.random.default_rng(SEED)

VACCINES = [
    ("dtap", "DTaP", 9000, 0.022),
    ("dtap_ipv", "DTaP-IPV", 2700, 0.026),
    ("dtap_hepb_ipv", "DTaP-HepB-IPV", 3800, 0.024),
    ("dtap_ipv_hib", "DTaP-IPV-Hib", 1600, 0.031),
    ("hepa_pediatric", "HepA Pediatric", 7600, 0.025),
    ("hepa_hepb", "HepA-HepB", 900, 0.038),
    ("hepb_pediatric", "HepB Pediatric", 8500, 0.023),
    ("hib", "Hib", 7200, 0.027),
    ("hpv", "HPV", 9500, 0.020),
    ("mmr", "MMR", 7800, 0.029),
    ("pcv", "PCV", 9300, 0.024),
    ("ppv23", "PPSV23", 1200, 0.036),
    ("polio", "Polio", 6900, 0.022),
    ("rota", "Rotavirus", 6100, 0.034),
    ("td", "Td", 1000, 0.033),
    ("tdap", "Tdap", 8200, 0.023),
    ("varicella", "Varicella", 7200, 0.032),
    ("mmrv", "MMRV", 1700, 0.036),
    ("menb", "MenB", 3900, 0.031),
    ("dengue", "Dengue", 280, 0.060),
    ("dtap_ipv_hib_hepb", "DTaP-IPV-Hib-HepB", 2100, 0.033),
    ("menabcwy", "MenABCWY", 800, 0.041),
    ("menacwy", "MenACWY", 7800, 0.023),
    ("nirsevimab", "Nirsevimab", 4300, 0.052),
    ("mpox", "Mpox", 200, 0.070),
    ("rsv_maternal", "RSV Maternal", 2200, 0.045),
    ("covid", "COVID-19", 7600, 0.085),
    ("influenza", "Influenza", 14500, 0.095),
]
INCIDENTS = [
    ("expired_doses", "Expired doses"),
    ("cold_chain_excursion", "Cold-chain temperature excursion"),
    ("storage_unit_malfunction", "Storage unit malfunction"),
    ("open_vial_waste", "Open vial/unused doses"),
    ("shipment_issue", "Shipment or delivery issue"),
    ("inventory_discrepancy", "Inventory discrepancy"),
    ("administration_error", "Administration error"),
    ("provider_closed_or_inactive", "Provider closed/inactive"),
    ("manufacturer_recall_or_return", "Manufacturer recall/return"),
    ("other_explained", "Other explained incident"),
]


def generate_core(n_awardees: int = 64) -> pd.DataFrame:
    rows = []
    for i in range(1, n_awardees + 1):
        if i <= 50:
            awardee_type = "State Immunization Program"
        elif i <= 56:
            awardee_type = "Large City Immunization Program"
        else:
            awardee_type = "Territorial Immunization Program"
        region = rng.choice(["Northeast", "Midwest", "South", "West", "Territories"], p=[.18, .20, .28, .22, .12])
        size_index = {
            "State Immunization Program": rng.lognormal(0.4, 0.55),
            "Large City Immunization Program": rng.lognormal(0.05, 0.45),
            "Territorial Immunization Program": rng.lognormal(-0.65, 0.35),
        }[awardee_type]
        vfc_staff = int(max(2, round(rng.normal(16 * size_index, 5))))
        iqip_staff = int(max(1, round(rng.normal(7 * size_index, 3))))
        shared_staff = int(max(0, round(rng.normal(4 * size_index, 2))))
        total_staff = max(vfc_staff + iqip_staff + shared_staff, vfc_staff, iqip_staff)
        vfc_trained = int(round(vfc_staff * np.clip(rng.normal(.88, .10), .45, 1.0)))
        iqip_trained = int(round(iqip_staff * np.clip(rng.normal(.84, .12), .35, 1.0)))
        total_trained = min(total_staff, vfc_trained + iqip_trained + int(shared_staff * rng.uniform(.4, 1.0)))
        policy = rng.choice([
            "Offer all ACIP-recommended pediatric vaccines", "Awardee-defined vaccine menu",
            "Provider-specific ordering policy", "Other policy"
        ], p=[.63, .19, .13, .05])
        policy_changed = int(rng.choice([0, 1], p=[.78, .22]))
        delegate = int(rng.choice([0, 1], p=[.70, .30]))
        replacement = int(rng.choice([0, 1], p=[.18, .82]))
        repayment = int(replacement and rng.choice([0, 1], p=[.55, .45]))
        cap_exists = int(replacement and rng.choice([0, 1], p=[.64, .36]))
        freq_defined = int(rng.choice([0, 1], p=[.18, .82]))
        rows.append({
            "survey_year": 2024,
            "awardee_id": f"SYN-AWD-{i:03d}",
            "awardee_name": f"Synthetic Immunization Program {i:03d}",
            "awardee_type": awardee_type,
            "region": region,
            "program_size_index": round(size_index, 3),
            "vfc_staff_count": vfc_staff,
            "iqip_staff_count": iqip_staff,
            "total_staff_count": total_staff,
            "vfc_staff_trained": vfc_trained,
            "iqip_staff_trained": iqip_trained,
            "total_staff_trained": total_trained,
            "vfc_staff_training_gap": vfc_staff - vfc_trained,
            "iqip_staff_training_gap": iqip_staff - iqip_trained,
            "total_staff_training_gap": total_staff - total_trained,
            "vfc_staff_model": rng.choice(["Centralized", "Regionalized", "Hybrid", "Other"], p=[.30, .22, .43, .05]),
            "iqip_staff_model": rng.choice(["Centralized", "Regionalized", "Hybrid", "Other"], p=[.27, .20, .48, .05]),
            "staff_model_other_text": None,
            "vaccine_supply_policy": policy,
            "policy_text_group": policy,
            "policy_changed_since_prior_bp": policy_changed,
            "policy_change_reason": rng.choice(["Updated ACIP formulary alignment", "Inventory reconciliation improvement", "Budget period policy clarification", "Provider ordering policy refinement"]) if policy_changed else None,
            "offer_all_acip_pediatric_vaccines": 1 if policy.startswith("Offer all") else int(rng.choice([0, 1], p=[.75, .25])),
            "delegate_authority": delegate,
            "deputized_lhd_count": int(rng.poisson(12 * size_index)) if delegate else 0,
            "deputized_private_provider_count": int(rng.poisson(5 * size_index)) if delegate else 0,
            "deputized_pharmacy_count": int(rng.poisson(3 * size_index)) if delegate else 0,
            "deputized_birthing_hospital_count": int(rng.poisson(1.5 * size_index)) if delegate else 0,
            "deputized_other_count": int(rng.poisson(2 * size_index)) if delegate else 0,
            "deputized_visit_model": rng.choice(["Awardee conducts all visits", "Deputized entity conducts selected visits", "Deputized entity conducts all visits"]) if delegate else "Not applicable",
            "reports_doses_distributed": int(rng.choice([0, 1], p=[.13, .87])),
            "reporting_frequency_defined": freq_defined,
            "dose_reporting_frequency": rng.choice(["Monthly", "Quarterly", "Semiannual", "Annual", "Other"], p=[.50, .35, .07, .04, .04]) if freq_defined else None,
            "vaccine_patient_type": rng.choice(["VFC pediatric doses only", "Public pediatric doses", "All publicly funded doses", "Mixed pediatric/adult public doses"], p=[.42, .26, .24, .08]),
            "esw_data_source": rng.choice(["VTrckS extract", "IIS aggregate report", "Awardee inventory system", "Mixed/manual reconciliation"], p=[.36, .30, .18, .16]),
            "esw_data_source_detail": None,
            "vsh_data_type": rng.choice(["Dose count by incident category", "Incident count only", "Dose and incident count", "Other"], p=[.52, .12, .30, .06]),
            "vsh_data_source": rng.choice(["PEAR/VFC oversight system", "IIS or inventory system", "Awardee spreadsheet", "Mixed/manual reconciliation"], p=[.39, .25, .23, .13]),
            "vsh_data_source_detail": None,
            "requires_vaccine_replacement": replacement,
            "replacement_applies_vfc": int(replacement and rng.choice([0, 1], p=[.05, .95])),
            "replacement_applies_317": int(replacement and rng.choice([0, 1], p=[.42, .58])),
            "replacement_applies_state_funded": int(replacement and rng.choice([0, 1], p=[.63, .37])),
            "replacement_applies_chip": int(replacement and rng.choice([0, 1], p=[.76, .24])),
            "replacement_policies_differ_by_fund_type": int(replacement and rng.choice([0, 1], p=[.70, .30])),
            "replacement_policy_difference_text": None,
            "tiered_replacement_policy": int(replacement and rng.choice([0, 1], p=[.58, .42])),
            "tiered_replacement_text": None,
            "repayment_over_time_allowed": repayment,
            "repayment_months_allowed": int(rng.choice([3, 6, 9, 12, 18, 24])) if repayment else np.nan,
            "shipments_continue_during_replacement": rng.choice(["Yes", "No", "Case-by-case", "Not applicable"], p=[.50, .12, .30, .08]) if replacement else "Not applicable",
            "replacement_method": rng.choice(["Dose-for-dose replacement", "Dollar repayment", "Dose or dollar replacement", "Other"], p=[.49, .10, .36, .05]) if replacement else "Not applicable",
            "replacement_cap_exists": cap_exists,
            "replacement_cap_doses": int(rng.choice([100, 250, 500, 1000, 2500])) if cap_exists else np.nan,
            "replacement_cap_dollars": int(rng.choice([5000, 10000, 25000, 50000, 100000])) if cap_exists else np.nan,
            "replacement_cap_other_text": None,
            "replacement_tracking_system": rng.choice(["PEAR note field", "Awardee inventory system", "Spreadsheet tracker", "Other"]) if replacement else "Not applicable",
            "replacement_exception_policy": rng.choice(["Documented exception allowed", "No exception policy", "Case-by-case supervisor approval"]) if replacement else "Not applicable",
            "synthetic_data_notice": NOTICE,
        })
    return pd.DataFrame(rows)


def generate_vaccine_tables(core: pd.DataFrame) -> pd.DataFrame:
    rows = []
    zero_probs = {"dengue": .62, "mpox": .70, "rsv_maternal": .28, "menabcwy": .25, "hepa_hepb": .16}
    for _, awardee in core.iterrows():
        gap_factor = 1 + min(.50, awardee.total_staff_training_gap / max(awardee.total_staff_count, 1) * .8)
        source_factor = 1.15 if awardee.esw_data_source == "Mixed/manual reconciliation" else 1.0
        type_factor = .42 if awardee.awardee_type == "Territorial Immunization Program" else .70 if awardee.awardee_type == "Large City Immunization Program" else 1.0
        for code, label, mean_order, base_rate in VACCINES:
            if rng.random() < zero_probs.get(code, .01):
                ordered = 0
            else:
                ordered = int(rng.poisson(max(mean_order * awardee.program_size_index * type_factor * rng.lognormal(0, .12), 5)))
            rate = float(np.clip(base_rate * gap_factor * source_factor * rng.lognormal(0, .25), 0, .22))
            wasted = 0 if ordered == 0 else int(min(ordered, rng.poisson(max(ordered * rate, .2))))
            calc_loss = np.nan if ordered == 0 else wasted / ordered * 100
            reported = np.nan if ordered == 0 or rng.random() < .035 else calc_loss + rng.normal(0, .18)
            rows.append({
                "survey_year": 2024,
                "awardee_id": awardee.awardee_id,
                "vaccine_type_code": code,
                "vaccine_type": label,
                "vaccine_patient_type": awardee.vaccine_patient_type,
                "doses_ordered": ordered,
                "doses_wasted": wasted,
                "reported_loss_pct": round(reported, 3) if pd.notna(reported) else np.nan,
                "calculated_loss_pct": round(calc_loss, 3) if pd.notna(calc_loss) else np.nan,
                "reported_minus_calculated_pct": round(reported - calc_loss, 3) if pd.notna(reported) and pd.notna(calc_loss) else np.nan,
                "included_in_standard_analysis": 0 if code in ["covid", "influenza"] else 1,
                "synthetic_data_notice": NOTICE,
            })
    return pd.DataFrame(rows)


def generate_incidents(vax: pd.DataFrame) -> pd.DataFrame:
    probs = np.array([.22, .18, .14, .13, .08, .10, .05, .04, .02, .04])
    rows = []
    totals = vax.groupby("awardee_id", as_index=False).doses_wasted.sum()
    for _, row in totals.iterrows():
        total = int(row.doses_wasted)
        incident_total = total if rng.random() < .85 else max(0, int(round(total * (1 + rng.uniform(-.05, .05)))))
        counts = rng.multinomial(incident_total, probs / probs.sum()) if incident_total > 0 else np.zeros(len(INCIDENTS), dtype=int)
        for (code, label), count in zip(INCIDENTS, counts):
            rows.append({
                "survey_year": 2024,
                "awardee_id": row.awardee_id,
                "incident_category_code": code,
                "incident_category": label,
                "incident_dose_count": int(count),
                "incident_explanation_required": 1 if code == "other_explained" and count > 0 else 0,
                "incident_explanation_text": "Synthetic explanation for other incident category." if code == "other_explained" and count > 0 else None,
                "synthetic_data_notice": NOTICE,
            })
    return pd.DataFrame(rows)


def main() -> None:
    core = generate_core()
    vax = generate_vaccine_tables(core)
    incidents = generate_incidents(vax)

    core.to_csv(RAW / "core_survey.csv", index=False)
    orders = vax.pivot(index="awardee_id", columns="vaccine_type_code", values="doses_ordered").reset_index()
    waste = vax.pivot(index="awardee_id", columns="vaccine_type_code", values="doses_wasted").reset_index()
    loss = vax.pivot(index="awardee_id", columns="vaccine_type_code", values="reported_loss_pct").reset_index()
    orders = orders.rename(columns={c: f"pedVxOrder_{c}" for c in orders.columns if c != "awardee_id"})
    waste = waste.rename(columns={c: f"pedVxWaste_{c}" for c in waste.columns if c != "awardee_id"})
    loss = loss.rename(columns={c: f"pedVxLoss_{c}" for c in loss.columns if c != "awardee_id"})
    for df, filename in [(orders, "vaccine_orders_wide.csv"), (waste, "vaccine_waste_wide.csv"), (loss, "vaccine_loss_reported_wide.csv")]:
        df.insert(0, "survey_year", 2024)
        df["synthetic_data_notice"] = NOTICE
        df.to_csv(RAW / filename, index=False)
    incidents.to_csv(RAW / "vaccine_incidents.csv", index=False)
    vax.to_csv(PROCESSED / "vaccine_order_waste_long.csv", index=False)

    awardee = vax.groupby("awardee_id", as_index=False).agg(total_doses_ordered=("doses_ordered", "sum"), total_doses_wasted=("doses_wasted", "sum"))
    awardee["loss_pct_all_vaccines"] = (awardee.total_doses_wasted / awardee.total_doses_ordered * 100).round(3)
    std = vax.query("included_in_standard_analysis == 1").groupby("awardee_id", as_index=False).agg(standard_doses_ordered=("doses_ordered", "sum"), standard_doses_wasted=("doses_wasted", "sum"))
    std["loss_pct_excluding_covid_flu"] = (std.standard_doses_wasted / std.standard_doses_ordered * 100).round(3)
    inc_total = incidents.groupby("awardee_id", as_index=False).agg(incident_dose_grand_total=("incident_dose_count", "sum"))
    awardee = awardee.merge(std, on="awardee_id").merge(inc_total, on="awardee_id").merge(core[["awardee_id", "awardee_name", "awardee_type", "region", "total_staff_count", "total_staff_trained", "total_staff_training_gap", "requires_vaccine_replacement", "replacement_method", "esw_data_source", "vsh_data_source"]], on="awardee_id")
    awardee["waste_vs_incident_dose_difference"] = awardee.total_doses_wasted - awardee.incident_dose_grand_total
    awardee["reconciliation_flag"] = np.where(awardee.waste_vs_incident_dose_difference.abs() > 0, "Review discrepancy", "Matched")
    awardee["synthetic_data_notice"] = NOTICE
    awardee.to_csv(PROCESSED / "awardee_vaccine_loss_summary.csv", index=False)

    vaccine = vax.groupby(["vaccine_type_code", "vaccine_type", "included_in_standard_analysis"], as_index=False).agg(total_doses_ordered=("doses_ordered", "sum"), total_doses_wasted=("doses_wasted", "sum"), awardees_with_orders=("doses_ordered", lambda s: int((s > 0).sum())), median_awardee_loss_pct=("calculated_loss_pct", "median"))
    vaccine["loss_pct"] = (vaccine.total_doses_wasted / vaccine.total_doses_ordered * 100).round(3)
    vaccine["synthetic_data_notice"] = NOTICE
    vaccine.to_csv(PROCESSED / "vaccine_type_loss_summary.csv", index=False)

    staff = pd.DataFrame({
        "metric": ["Total staff", "Total trained", "Total training gap"],
        "value": [core.total_staff_count.sum(), core.total_staff_trained.sum(), core.total_staff_training_gap.sum()],
        "synthetic_data_notice": NOTICE,
    })
    staff.to_csv(PROCESSED / "staff_training_gap_summary.csv", index=False)
    print("Synthetic data generated successfully.")
    print(f"Awardees: {len(core)} | Vaccine rows: {len(vax)} | Incident rows: {len(incidents)}")

if __name__ == "__main__":
    main()
