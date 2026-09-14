# Power BI Build Guide

## Data source
For the public portfolio, use exported PostgreSQL views when the E2E gate has passed. Until then, use the CSVs only for development and label the dashboard as draft.

Recommended imports:
- `results/sql_kpi_crosscheck.csv`
- `results/sql_benefit_realization.csv`
- `data/generated/failures.csv`
- `data/generated/maintenance_orders.csv`
- `data/generated/alarms.csv`
- `data/generated/temperature_excursions.csv`
- `data/generated/om_costs.csv`
- `project_management/project_progress.csv`
- `project_management/risk_register.csv`
- `engineering/requirements_traceability.csv`

## Page 1 - Executive
Cards: Availability, Downtime, Outside N+1 state, Capacity deficit, COP, O&M Cost.
Use Baseline/Post labels and target lines where requirements exist. Add a prominent SIMULATED CASE STUDY subtitle.

## Page 2 - Reliability & Maintenance
Visuals: failure count by mode, downtime by mode/asset, restoration-time distribution, PM compliance, temperature excursions.

## Page 3 - Energy & Operations
Visuals: monthly energy cost, COP by period/load band, alarm rate, excursions. Keep raw-vs-clean data distinction documented in tooltip/notes.

## Page 4 - Project & Systems
Cards: SPI, CPI, P50/P80/P90. Visuals: critical-path timeline, risk heatmap, gate status, requirements-to-verification progress.

## Model rules
- Do not combine project KPIs and system KPIs into one unlabeled score.
- Do not display early illustrative values as realized results.
- Final public numbers must come from the SQL E2E output.
- Keep units explicit.
- Use target status only when the acceptance rule is defined.
