DROP SCHEMA IF EXISTS ndc CASCADE;
CREATE SCHEMA ndc;

-- Governed reporting-period master data. Availability itself is NOT derived from
-- calendar hours; it is derived from 15-minute capacity-state evidence.
CREATE TABLE ndc.project_period(
  period text PRIMARY KEY,
  start_date date NOT NULL,
  end_date date NOT NULL,
  required_hours numeric NOT NULL
);

CREATE TABLE ndc.performance_telemetry(
  period text,timestamp timestamp,it_load_kw numeric,cooling_demand_kw numeric,
  cooling_energy_kwh numeric,cooling_electrical_power_kw numeric,
  cooling_electrical_energy_kwh numeric,cop numeric,facility_power_kw numeric,
  facility_energy_kwh numeric,it_energy_kwh numeric,pue numeric
);
CREATE TABLE ndc.capacity_state(
  period text,timestamp timestamp,available_chillers int,
  available_cooling_capacity_kw numeric,required_cooling_capacity_kw numeric,
  capacity_margin_kw numeric,service_available boolean,redundancy_state text
);
CREATE TABLE ndc.failures(
  period text,failure_id text PRIMARY KEY,asset_code text,start_timestamp timestamp,
  end_timestamp timestamp,downtime_hours numeric,repair_hours numeric,failure_mode text
);
CREATE TABLE ndc.maintenance(
  period text,work_order_id text PRIMARY KEY,asset_code text,planned_date date,
  completed_date date,completed boolean
);
CREATE TABLE ndc.om_costs(
  period text,month text,energy_cost_eur numeric,labor_cost_eur numeric,
  parts_cost_eur numeric,emergency_parts_cost_eur numeric,
  service_contract_cost_eur numeric,total_om_cost_eur numeric
);

-- Integrated PM + SE evidence model.
CREATE TABLE ndc.stakeholder_need(
  need_id text PRIMARY KEY, stakeholder text, need_statement text, rationale text
);
CREATE TABLE ndc.system_requirement(
  requirement_id text PRIMARY KEY, source_need text REFERENCES ndc.stakeholder_need(need_id),
  requirement text, architecture_element text, verification_method text,
  acceptance_criterion text, target_kpi text
);
CREATE TABLE ndc.verification_record(
  requirement_id text PRIMARY KEY REFERENCES ndc.system_requirement(requirement_id),
  target_kpi text, acceptance_criterion text, measured_result text,
  status text, evidence_source text
);
CREATE TABLE ndc.project_risk(
  risk_id text PRIMARY KEY,risk_statement text,probability numeric,impact numeric,
  exposure numeric,severity text,trigger text,response text,owner text,status text
);
CREATE TABLE ndc.change_request(
  change_id text PRIMARY KEY,title text,week integer,status text,cost_impact_eur numeric,
  schedule_impact_weeks numeric,decision text,verification_consequence text
);
CREATE TABLE ndc.schedule_activity(
  activity_id text PRIMARY KEY,activity_name text,duration_weeks numeric,
  predecessor_id text,baseline_start_week numeric,baseline_finish_week numeric,
  total_float_weeks numeric,critical boolean
);
CREATE TABLE ndc.project_progress(
  week integer PRIMARY KEY,planned_value_eur numeric,earned_value_eur numeric,
  actual_cost_eur numeric,planned_progress_pct numeric,actual_progress_pct numeric
);
CREATE TABLE ndc.decision_gate(
  gate_id text PRIMARY KEY,gate_name text,entry_criteria text,exit_criteria text,status text
);
