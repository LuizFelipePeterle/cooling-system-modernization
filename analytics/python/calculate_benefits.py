from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[2]
D=ROOT/'data'/'generated'; R=ROOT/'results'; R.mkdir(exist_ok=True)
k=pd.read_csv(D/'python_kpi_crosscheck.csv').set_index('period')
b=float(k.loc['baseline','om_cost_eur']); p=float(k.loc['post','om_cost_eur'])
s=b-p; pct=100*s/b if b else float('nan'); capex=360000.0; payback=capex/s if s>0 else float('inf')
out=pd.DataFrame([{'baseline_om_cost_eur':b,'post_om_cost_eur':p,'annual_direct_om_savings_eur':s,'om_reduction_pct':pct,'authorized_capex_eur':capex,'simple_payback_years':payback,'avoided_customer_outage_value_included':False}])
out.to_csv(R/'benefit_realization.csv',index=False)
print(out.to_string(index=False))
