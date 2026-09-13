from pathlib import Path
from kpi_calculations import calculate_kpis
ROOT=Path(__file__).resolve().parents[2]
D=ROOT/'data'/'generated'
out=calculate_kpis(D)
out.to_csv(D/'python_kpi_crosscheck.csv',index=False)
print('Python KPI crosscheck generated from current evidence.')
for _,r in out.iterrows():
    print(r['period'],
          'failures=',int(r['failures']),
          'equipment_downtime_h=',round(r['equipment_downtime_h'],1),
          'service_availability_pct=',round(r['cooling_service_availability_pct'],5),
          'degraded_h=',round(r['degraded_redundancy_h'],2),
          'paired_weighted_COP=',round(r['weighted_cop'],4),
          'paired_COP_obs=',int(r['paired_cop_observations']),
          'paired_COP_pct=',round(r['paired_cop_observation_pct'],3),
          'PUE=',round(r['pue'],4),
          'PM=',round(r['pm_compliance_pct'],2),
          'O&M=',round(r['om_cost_eur'],2))
