from pathlib import Path
import subprocess
import pandas as pd
import numpy as np
ROOT=Path(__file__).resolve().parents[1]; D=ROOT/'data'/'generated'

def setup_module():
    subprocess.run(['python', str(ROOT/'analytics/python/generate_data.py')], check=True, cwd=ROOT)
    subprocess.run(['python', str(ROOT/'analytics/python/calculate_python_kpis.py')], check=True, cwd=ROOT)

def test_capacity_state_semantics():
    d=pd.read_csv(D/'cooling_capacity_state.csv'); assert ((d.capacity_margin_kw>=0)==d.service_available).all()

def test_post_redundancy_exposure_improves_seeded_reference():
    d=pd.read_csv(D/'cooling_capacity_state.csv'); h=lambda p:(d[d.period==p].redundancy_state!='N+1').sum()*.25
    assert h('post') < h('baseline')

def test_energy_boundaries():
    d=pd.read_csv(D/'performance_telemetry_raw.csv'); assert (d.pue.dropna()>1).all(); assert (d.cop.dropna()>1).all()

def test_monitoring_interval_evidence():
    d=pd.read_csv(D/'monitoring_completeness_daily.csv'); assert (d.expected_1min_samples==1440).all()

def test_weighted_cop_uses_paired_observations_only():
    t=pd.read_csv(D/'performance_telemetry_raw.csv').sort_values(['period','timestamp']).drop_duplicates(['period','timestamp'])
    k=pd.read_csv(D/'python_kpi_crosscheck.csv').set_index('period')
    for p in ('baseline','post'):
        x=t[t.period==p][['cooling_energy_kwh','cooling_electrical_energy_kwh']].dropna()
        expected=x.cooling_energy_kwh.sum()/x.cooling_electrical_energy_kwh.sum()
        assert np.isclose(expected,float(k.loc[p,'weighted_cop']),rtol=1e-12,atol=1e-12)
        assert int(k.loc[p,'paired_cop_observations'])==len(x)

def test_python_kpi_crosscheck_is_recalculable_from_current_evidence():
    before=pd.read_csv(D/'python_kpi_crosscheck.csv')
    subprocess.run(['python', str(ROOT/'analytics/python/calculate_python_kpis.py')], check=True, cwd=ROOT)
    after=pd.read_csv(D/'python_kpi_crosscheck.csv')
    pd.testing.assert_frame_equal(before,after)
