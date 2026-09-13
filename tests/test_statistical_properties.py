from pathlib import Path
import subprocess
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'data/generated'

def setup_module():
    subprocess.run(['python', str(ROOT/'analytics/python/generate_data.py')], check=True, cwd=ROOT)

def test_failure_counts_not_asserted_exact():
    f = pd.read_csv(OUT/'failures.csv')
    for label, rate in [('baseline',14),('post',6)]:
        n = (f.period==label).sum()
        lo = max(0, int(rate-3*np.sqrt(rate)))
        hi = int(rate+3*np.sqrt(rate)+1)
        assert lo <= n <= hi

def test_imperfections_exist_in_v6_performance_evidence():
    t = pd.read_csv(OUT/'performance_telemetry_raw.csv')
    assert t[['it_load_kw','cooling_demand_kw','cooling_electrical_energy_kwh','cop','pue']].isna().sum().sum() > 0
    assert t.duplicated(['period','timestamp']).any()
