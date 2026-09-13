from pathlib import Path
import hashlib, csv, datetime
ROOT=Path(__file__).resolve().parents[1]
files=[
 'data/generated/performance_telemetry_raw.csv','data/generated/cooling_capacity_state.csv',
 'data/generated/failures.csv','data/generated/maintenance_orders.csv','data/generated/om_costs.csv',
 'data/generated/monitoring_completeness_daily.csv','data/generated/python_kpi_crosscheck.csv',
 'results/verification_results.csv','results/benefit_realization.csv','results/monte_carlo_schedule.txt',
 'results/sql_kpi_crosscheck.csv','results/e2e_crosscheck_report.csv','results/sql_requirement_verification.csv'
]
rows=[]; now=datetime.datetime.now(datetime.timezone.utc).isoformat()
for rel in files:
 p=ROOT/rel
 if p.exists():
  rows.append({'artifact':rel,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'generated_at_utc':now,'status':'PRESENT'})
 else:
  rows.append({'artifact':rel,'sha256':'','generated_at_utc':now,'status':'NOT GENERATED IN THIS ENVIRONMENT'})
out=ROOT/'results'/'VALIDATION_MANIFEST.csv'; out.parent.mkdir(exist_ok=True)
with out.open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['artifact','sha256','generated_at_utc','status']); w.writeheader(); w.writerows(rows)
print(f'Validation manifest written: {out}')
