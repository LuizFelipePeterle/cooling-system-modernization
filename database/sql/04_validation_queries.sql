SELECT * FROM ndc.vw_kpi ORDER BY period;
SELECT period, COUNT(*) intervals,
       SUM(CASE WHEN capacity_margin_kw<0 AND service_available THEN 1 ELSE 0 END) semantic_errors
FROM ndc.capacity_state GROUP BY period;
SELECT COUNT(*) stakeholder_needs FROM ndc.stakeholder_need;
SELECT COUNT(*) requirements FROM ndc.system_requirement;
SELECT COUNT(*) verification_records FROM ndc.verification_record;
SELECT status, COUNT(*) FROM ndc.verification_record GROUP BY status ORDER BY status;
SELECT * FROM ndc.vw_project_evm ORDER BY week;
SELECT * FROM ndc.vw_benefit_realization;
