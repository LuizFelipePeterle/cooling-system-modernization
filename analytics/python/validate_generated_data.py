from pathlib import Path
import pandas as pd, numpy as np
ROOT=Path(__file__).resolve().parents[2]; D=ROOT/'data'/'generated'
perf=pd.read_csv(D/'performance_telemetry_raw.csv'); fail=pd.read_csv(D/'failures.csv'); cap=pd.read_csv(D/'cooling_capacity_state.csv'); pm=pd.read_csv(D/'maintenance_orders.csv'); costs=pd.read_csv(D/'om_costs.csv'); mon=pd.read_csv(D/'monitoring_completeness_daily.csv')
assert set(perf.period)=={'baseline','post'} and set(cap.period)=={'baseline','post'}
assert (cap.available_chillers.between(0,3)).all(); assert (cap.available_cooling_capacity_kw>=0).all()
assert ((cap.capacity_margin_kw>=0)==cap.service_available).all()
assert perf.pue.dropna().between(1,3).all(); assert perf.cop.dropna().between(2,4.5).all()
assert costs.total_om_cost_eur.gt(0).all(); assert np.allclose(costs[['energy_cost_eur','labor_cost_eur','parts_cost_eur','emergency_parts_cost_eur','service_contract_cost_eur']].sum(axis=1),costs.total_om_cost_eur,atol=.05)
assert mon.completeness_pct.between(95,100).all()
for p in ['baseline','post']:
 assert len(cap[cap.period==p]) in (35040,35136)
print('V6 validation checks passed.')
