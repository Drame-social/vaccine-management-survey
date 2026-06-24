"""Validate synthetic Vaccine Management Survey data."""
from pathlib import Path
import pandas as pd
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
NOTICE = 'SYNTHETIC_PORTFOLIO_DATA_NOT_REAL_CDC_OR_AWARDEE_DATA'
core = pd.read_csv(ROOT/'data/raw/core_survey.csv')
vax = pd.read_csv(ROOT/'data/processed/vaccine_order_waste_long.csv')
inc = pd.read_csv(ROOT/'data/raw/vaccine_incidents.csv')
awardee_summary = pd.read_csv(ROOT/'data/processed/awardee_vaccine_loss_summary.csv')
vaccine_summary = pd.read_csv(ROOT/'data/processed/vaccine_type_loss_summary.csv')
checks=[]
def check(name, ok, detail):
    checks.append({'check_name':name,'status':'PASS' if ok else 'FAIL','detail':detail,'checked_at_utc':datetime.now(timezone.utc).isoformat(timespec='seconds')})
check('Core awardee count', len(core)==64, f'{len(core)} awardees generated; expected 64')
check('Vaccine long row count', len(vax)==64*28, f'{len(vax)} rows generated; expected 1,792')
check('Incident long row count', len(inc)==64*10, f'{len(inc)} rows generated; expected 640')
check('awardee_id unique', core['awardee_id'].is_unique, 'Core awardee IDs are unique')
check('Vaccine rows have matching awardees', set(vax.awardee_id).issubset(set(core.awardee_id)), 'All vaccine rows map to core')
check('Incident rows have matching awardees', set(inc.awardee_id).issubset(set(core.awardee_id)), 'All incident rows map to core')
check('No negative ordered doses', (vax.doses_ordered>=0).all(), 'All ordered doses >= 0')
check('No negative wasted doses', (vax.doses_wasted>=0).all(), 'All wasted doses >= 0')
check('Wasted doses <= ordered doses', (vax.doses_wasted<=vax.doses_ordered).all(), 'All waste values are logically possible')
calc = vax[vax.doses_ordered>0].copy()
max_diff = (calc.calculated_loss_pct - (calc.doses_wasted/calc.doses_ordered*100).round(3)).abs().max()
check('Calculated loss formula', max_diff < 0.002, f'max abs rounded diff={max_diff}')
check('Awardee summary row count', len(awardee_summary)==64, f'{len(awardee_summary)} summary rows; expected 64')
check('Vaccine type summary row count', len(vaccine_summary)==28, f'{len(vaccine_summary)} summary rows; expected 28')
for name, df in [('core',core),('vaccine_long',vax),('incidents',inc),('awardee_summary',awardee_summary),('vaccine_summary',vaccine_summary)]:
    check(f'Synthetic notice present: {name}', df.synthetic_data_notice.eq(NOTICE).all(), 'All rows labeled synthetic')
ROOT.joinpath('outputs').mkdir(exist_ok=True)
pd.DataFrame(checks).to_csv(ROOT/'outputs/validation_results.csv', index=False)
print(pd.DataFrame(checks).to_string(index=False))
if any(c['status']=='FAIL' for c in checks):
    raise SystemExit(1)
