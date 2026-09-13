from __future__ import annotations
from pathlib import Path
import pandas as pd

KPI_COLUMNS = [
    'period','failures','equipment_downtime_h','cooling_service_availability_pct',
    'degraded_redundancy_h','capacity_deficit_h','weighted_cop',
    'paired_cop_observations','paired_cop_observation_pct','pue',
    'pm_compliance_pct','om_cost_eur'
]

def _dedupe_perf(perf: pd.DataFrame) -> pd.DataFrame:
    x = perf.copy()
    x['timestamp'] = pd.to_datetime(x['timestamp'])
    return x.sort_values(['period','timestamp']).drop_duplicates(['period','timestamp'], keep='first')

def calculate_kpis(data_dir: Path) -> pd.DataFrame:
    perf = _dedupe_perf(pd.read_csv(data_dir/'performance_telemetry_raw.csv'))
    fail = pd.read_csv(data_dir/'failures.csv')
    cap = pd.read_csv(data_dir/'cooling_capacity_state.csv')
    pm = pd.read_csv(data_dir/'maintenance_orders.csv')
    costs = pd.read_csv(data_dir/'om_costs.csv')
    rows=[]
    for period in sorted(cap['period'].unique()):
        pp=perf[perf.period==period]
        pc=cap[cap.period==period]
        pf=fail[fail.period==period]
        ppm=pm[pm.period==period]
        po=costs[costs.period==period]

        # Methodological rule: weighted COP uses only paired 15-minute observations
        # where both cooling energy and cooling electrical energy are present.
        cop_pair = pp[['cooling_energy_kwh','cooling_electrical_energy_kwh']].dropna()
        weighted_cop = cop_pair.cooling_energy_kwh.sum()/cop_pair.cooling_electrical_energy_kwh.sum()
        paired_count = len(cop_pair)
        paired_pct = 100.0*paired_count/len(pp) if len(pp) else float('nan')

        # PUE is likewise evaluated over paired facility/IT energy observations.
        pue_pair = pp[['facility_energy_kwh','it_energy_kwh']].dropna()
        pue = pue_pair.facility_energy_kwh.sum()/pue_pair.it_energy_kwh.sum()

        rows.append({
            'period':period,
            'failures':int(len(pf)),
            'equipment_downtime_h':float(pf.downtime_hours.sum()),
            'cooling_service_availability_pct':100.0*pc.service_available.astype(bool).mean(),
            'degraded_redundancy_h':0.25*(pc.redundancy_state!='N+1').sum(),
            'capacity_deficit_h':0.25*(pc.redundancy_state=='capacity deficit').sum(),
            'weighted_cop':float(weighted_cop),
            'paired_cop_observations':int(paired_count),
            'paired_cop_observation_pct':float(paired_pct),
            'pue':float(pue),
            'pm_compliance_pct':100.0*ppm.completed.astype(bool).mean(),
            'om_cost_eur':float(po.total_om_cost_eur.sum()),
        })
    return pd.DataFrame(rows, columns=KPI_COLUMNS)
