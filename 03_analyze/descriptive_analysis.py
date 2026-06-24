"""Run analysis for the synthetic Vaccine Management Survey project."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

NOTICE = "All data are synthetic and generated solely for portfolio demonstration purposes."

ROOT = Path(__file__).resolve().parents[1]
core = pd.read_csv(ROOT/'data/raw/core_survey.csv')
vax = pd.read_csv(ROOT/'data/processed/vaccine_order_waste_long.csv')
inc = pd.read_csv(ROOT/'data/raw/vaccine_incidents.csv')
outputs = ROOT/'outputs'
outputs.mkdir(exist_ok=True)

awardee = vax.groupby('awardee_id', as_index=False).agg(total_doses_ordered=('doses_ordered','sum'), total_doses_wasted=('doses_wasted','sum'))
awardee['loss_pct_all_vaccines'] = (awardee.total_doses_wasted/awardee.total_doses_ordered*100).round(3)
standard = vax.query('included_in_standard_analysis == 1').groupby('awardee_id', as_index=False).agg(standard_doses_ordered=('doses_ordered','sum'), standard_doses_wasted=('doses_wasted','sum'))
standard['loss_pct_excluding_covid_flu'] = (standard.standard_doses_wasted/standard.standard_doses_ordered*100).round(3)
inc_total = inc.groupby('awardee_id', as_index=False).agg(incident_dose_grand_total=('incident_dose_count','sum'))
awardee = awardee.merge(standard,on='awardee_id').merge(inc_total,on='awardee_id').merge(core[['awardee_id','awardee_name','awardee_type','region','total_staff_count','total_staff_trained','total_staff_training_gap','requires_vaccine_replacement','replacement_method','esw_data_source','vsh_data_source']], on='awardee_id')
awardee['waste_vs_incident_dose_difference'] = awardee.total_doses_wasted - awardee.incident_dose_grand_total
awardee['reconciliation_flag'] = awardee.waste_vs_incident_dose_difference.abs().map(lambda x: 'Matched' if x==0 else 'Review discrepancy')
awardee["synthetic_data_notice"] = NOTICE
awardee.to_csv(outputs/'awardee_vaccine_loss_summary.csv', index=False)
top10 = awardee.sort_values('loss_pct_all_vaccines', ascending=False).head(10).copy()
top10["synthetic_data_notice"] = NOTICE
top10.to_csv(outputs/'top_10_awardees_by_loss_pct.csv', index=False)

vaccine = vax.groupby(['vaccine_type_code','vaccine_type','included_in_standard_analysis'], as_index=False).agg(total_doses_ordered=('doses_ordered','sum'), total_doses_wasted=('doses_wasted','sum'), awardees_with_orders=('doses_ordered', lambda s: int((s>0).sum())), median_awardee_loss_pct=('calculated_loss_pct','median'))
vaccine['loss_pct'] = (vaccine.total_doses_wasted/vaccine.total_doses_ordered*100).round(3)
vaccine["synthetic_data_notice"] = NOTICE
vaccine.to_csv(outputs/'vaccine_loss_by_vaccine_type.csv', index=False)

plt.figure(figsize=(9,5))
vaccine.sort_values('loss_pct', ascending=False).head(12).plot(kind='bar', x='vaccine_type', y='loss_pct', legend=False)
plt.ylabel('Waste-to-order ratio (%)')
plt.xlabel('Vaccine type')
plt.title('Top Synthetic Vaccine Waste-to-Order Ratios')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(outputs/'top_vaccine_loss_ratios.png', dpi=150)
plt.close()
print('Analysis complete. Outputs saved to outputs/.')
