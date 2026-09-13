
from pathlib import Path
import json
import subprocess
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/"data/generated"
CFG = json.loads((ROOT/"analytics/python/data_generation_config.json").read_text())

def setup_module():
    subprocess.run(["python", str(ROOT/"analytics/python/generate_data.py")], check=True, cwd=ROOT)

def test_post_period_is_leap_spanning_366_days():
    start = pd.Timestamp(CFG["periods"]["post"]["start"])
    end = pd.Timestamp(CFG["periods"]["post"]["end"])
    days = (end - start).days + 1
    assert days == 366
    assert days * 24 == 8784

def test_om_costs_exist_and_are_derived_components():
    c = pd.read_csv(OUT/"om_costs.csv")
    assert len(c) == 24
    reconstructed = (
        c["energy_cost_eur"]
        + c["labor_cost_eur"]
        + c["parts_cost_eur"]
        + c["emergency_parts_cost_eur"]
        + c["service_contract_cost_eur"]
    )
    assert ((reconstructed - c["total_om_cost_eur"]).abs() < 0.06).all()

def test_costs_are_not_fixed_to_story_values():
    c = pd.read_csv(OUT/"om_costs.csv")
    totals = c.groupby("period")["total_om_cost_eur"].sum()
    assert round(float(totals.get("baseline",0)), 0) != 284000
    assert round(float(totals.get("post",0)), 0) != 218000
