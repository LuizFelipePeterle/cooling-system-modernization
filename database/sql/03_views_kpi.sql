CREATE OR REPLACE VIEW ndc.vw_kpi AS
WITH perf_dedup AS (
  SELECT DISTINCT ON(period,timestamp) *
  FROM ndc.performance_telemetry
  ORDER BY period,timestamp
),
perf AS (
  SELECT period,
    -- Paired-observation methodology: both channels must exist on the SAME interval.
    SUM(cooling_energy_kwh) FILTER (WHERE cooling_energy_kwh IS NOT NULL AND cooling_electrical_energy_kwh IS NOT NULL)
      / NULLIF(SUM(cooling_electrical_energy_kwh) FILTER (WHERE cooling_energy_kwh IS NOT NULL AND cooling_electrical_energy_kwh IS NOT NULL),0) AS weighted_cop,
    COUNT(*) FILTER (WHERE cooling_energy_kwh IS NOT NULL AND cooling_electrical_energy_kwh IS NOT NULL) AS paired_cop_observations,
    100.0 * COUNT(*) FILTER (WHERE cooling_energy_kwh IS NOT NULL AND cooling_electrical_energy_kwh IS NOT NULL) / NULLIF(COUNT(*),0) AS paired_cop_observation_pct,
    SUM(facility_energy_kwh) FILTER (WHERE facility_energy_kwh IS NOT NULL AND it_energy_kwh IS NOT NULL)
      / NULLIF(SUM(it_energy_kwh) FILTER (WHERE facility_energy_kwh IS NOT NULL AND it_energy_kwh IS NOT NULL),0) AS pue
  FROM perf_dedup GROUP BY period
),
cap AS (
  SELECT period,
    100.0*AVG(CASE WHEN service_available THEN 1 ELSE 0 END) AS cooling_service_availability_pct,
    0.25*SUM(CASE WHEN redundancy_state<>'N+1' THEN 1 ELSE 0 END) AS degraded_redundancy_h,
    0.25*SUM(CASE WHEN redundancy_state='capacity deficit' THEN 1 ELSE 0 END) AS capacity_deficit_h
  FROM ndc.capacity_state GROUP BY period
),
f AS (
  SELECT period,COUNT(*) AS failures,COALESCE(SUM(downtime_hours),0) AS equipment_downtime_h
  FROM ndc.failures GROUP BY period
),
pm AS (
  SELECT period,100.0*AVG(CASE WHEN completed THEN 1 ELSE 0 END) AS pm_compliance_pct
  FROM ndc.maintenance GROUP BY period
),
c AS (
  SELECT period,SUM(total_om_cost_eur) AS om_cost_eur FROM ndc.om_costs GROUP BY period
)
SELECT cap.period,f.failures,f.equipment_downtime_h,
       cap.cooling_service_availability_pct,cap.degraded_redundancy_h,
       cap.capacity_deficit_h,perf.weighted_cop,perf.paired_cop_observations,
       perf.paired_cop_observation_pct,perf.pue,pm.pm_compliance_pct,c.om_cost_eur
FROM cap
JOIN perf USING(period)
JOIN f USING(period)
JOIN pm USING(period)
JOIN c USING(period);

CREATE OR REPLACE VIEW ndc.vw_requirement_verification AS
SELECT r.requirement_id,r.requirement,r.acceptance_criterion,r.target_kpi,
       v.measured_result,v.status,v.evidence_source
FROM ndc.system_requirement r
LEFT JOIN ndc.verification_record v USING(requirement_id)
ORDER BY r.requirement_id;

CREATE OR REPLACE VIEW ndc.vw_project_evm AS
SELECT week,planned_value_eur,earned_value_eur,actual_cost_eur,
       earned_value_eur/NULLIF(planned_value_eur,0) AS spi,
       earned_value_eur/NULLIF(actual_cost_eur,0) AS cpi,
       planned_progress_pct,actual_progress_pct
FROM ndc.project_progress;

CREATE OR REPLACE VIEW ndc.vw_benefit_realization AS
WITH k AS (SELECT * FROM ndc.vw_kpi),
b AS (SELECT om_cost_eur baseline_om_cost_eur FROM k WHERE period='baseline'),
p AS (SELECT om_cost_eur post_om_cost_eur FROM k WHERE period='post')
SELECT b.baseline_om_cost_eur,
       p.post_om_cost_eur,
       b.baseline_om_cost_eur-p.post_om_cost_eur AS annual_direct_om_savings_eur,
       100.0*(b.baseline_om_cost_eur-p.post_om_cost_eur)/NULLIF(b.baseline_om_cost_eur,0) AS om_reduction_pct,
       360000.0::numeric AS authorized_capex_eur,
       360000.0/NULLIF(b.baseline_om_cost_eur-p.post_om_cost_eur,0) AS simple_payback_years,
       false AS avoided_customer_outage_value_included
FROM b CROSS JOIN p;
