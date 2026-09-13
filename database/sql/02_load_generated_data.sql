\copy ndc.performance_telemetry FROM 'data/generated/performance_telemetry_raw.csv' CSV HEADER;
\copy ndc.capacity_state FROM 'data/generated/cooling_capacity_state.csv' CSV HEADER;
\copy ndc.failures FROM 'data/generated/failures.csv' CSV HEADER;
\copy ndc.maintenance FROM 'data/generated/maintenance_orders.csv' CSV HEADER NULL '';
\copy ndc.om_costs FROM 'data/generated/om_costs.csv' CSV HEADER;
