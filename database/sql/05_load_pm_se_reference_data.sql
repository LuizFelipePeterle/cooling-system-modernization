-- Reporting period master data: governance only, not service-availability arithmetic.
INSERT INTO ndc.project_period(period,start_date,end_date,required_hours) VALUES
 ('baseline','2026-01-01','2026-12-31',8760),
 ('post','2027-09-01','2028-08-31',8784);

\copy ndc.stakeholder_need FROM 'engineering/stakeholder_needs.csv' CSV HEADER;
\copy ndc.system_requirement FROM 'engineering/requirements_traceability.csv' CSV HEADER;
\copy ndc.project_risk FROM 'project_management/risk_register.csv' CSV HEADER;
\copy ndc.change_request FROM 'project_management/change_log.csv' CSV HEADER;
\copy ndc.schedule_activity FROM 'project_management/schedule_activities.csv' CSV HEADER NULL '';
\copy ndc.project_progress FROM 'project_management/project_progress.csv' CSV HEADER;
\copy ndc.decision_gate FROM 'project_management/decision_gates.csv' CSV HEADER;
\copy ndc.verification_record FROM 'results/verification_results.csv' CSV HEADER;

SELECT 'Integrated PM/SE reference model loaded' AS status,
       (SELECT count(*) FROM ndc.stakeholder_need) AS needs,
       (SELECT count(*) FROM ndc.system_requirement) AS requirements,
       (SELECT count(*) FROM ndc.verification_record) AS verification_records,
       (SELECT count(*) FROM ndc.project_risk) AS risks,
       (SELECT count(*) FROM ndc.decision_gate) AS gates;
