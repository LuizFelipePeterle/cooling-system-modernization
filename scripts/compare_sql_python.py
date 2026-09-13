from pathlib import Path
import pandas as pd, numpy as np
R=Path(__file__).resolve().parents[1]; py=pd.read_csv(R/'data/generated/python_kpi_crosscheck.csv').sort_values('period').reset_index(drop=True); sql=pd.read_csv(R/'results/sql_kpi_crosscheck.csv').sort_values('period').reset_index(drop=True)
cols=['failures','equipment_downtime_h','cooling_service_availability_pct','degraded_redundancy_h','capacity_deficit_h','weighted_cop','paired_cop_observations','paired_cop_observation_pct','pue','pm_compliance_pct','om_cost_eur']; rows=[]
for i,p in enumerate(py.period):
 for c in cols:
  a=float(py.loc[i,c]); b=float(sql.loc[i,c]); ok=np.isclose(a,b,rtol=1e-6,atol=1e-4); rows.append({'period':p,'metric':c,'python':a,'sql':b,'pass':bool(ok)})
out=pd.DataFrame(rows); out.to_csv(R/'results/e2e_crosscheck_report.csv',index=False)
if not out['pass'].all(): raise SystemExit('E2E crosscheck FAILED. See results/e2e_crosscheck_report.csv')
print('E2E crosscheck PASSED for mapped v6 KPIs.')
