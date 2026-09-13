\copy (SELECT * FROM ndc.vw_kpi ORDER BY period) TO 'results/sql_kpi_crosscheck.csv' CSV HEADER;
\copy (SELECT * FROM ndc.vw_requirement_verification ORDER BY requirement_id) TO 'results/sql_requirement_verification.csv' CSV HEADER;
\copy (SELECT * FROM ndc.vw_project_evm ORDER BY week) TO 'results/sql_project_evm.csv' CSV HEADER;
\copy (SELECT * FROM ndc.vw_benefit_realization) TO 'results/sql_benefit_realization.csv' CSV HEADER;
