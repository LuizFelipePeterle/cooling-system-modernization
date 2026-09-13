from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
GEN = (ROOT/'analytics/python/generate_data.py').read_text()
CFG = json.loads((ROOT/'analytics/python/data_generation_config.json').read_text())

def test_cost_scenario_parameters_are_externalized():
    cm = CFG['cost_model']
    assert 'parts_cost_lognormal_median_eur' in cm
    assert 'parts_cost_lognormal_sigma' in cm
    assert 'emergency_procurement_probability' in cm
    assert 'preventive_labor_hours_per_completed_order' in cm
    assert '1800 if label' not in GEN
    assert '1400 if label' not in GEN
    assert '0.55 if label' not in GEN

def test_reporting_period_master_data_is_governed_but_not_used_for_service_availability():
    schema=(ROOT/'database/sql/01_schema.sql').read_text()
    views=(ROOT/'database/sql/03_views_kpi.sql').read_text()
    loader=(ROOT/'database/sql/05_load_pm_se_reference_data.sql').read_text()
    assert 'CREATE TABLE ndc.project_period' in schema
    assert "('baseline','2026-01-01','2026-12-31',8760)" in loader
    assert "('post','2027-09-01','2028-08-31',8784)" in loader
    # Service availability is interval-evidence based, not calendar arithmetic.
    assert 'AVG(CASE WHEN service_available THEN 1 ELSE 0 END)' in views
    assert 'required_hours-downtime' not in views
