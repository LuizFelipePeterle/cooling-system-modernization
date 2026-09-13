# PostgreSQL E2E Validation Gate - v6.1

The Python evidence pipeline has been executed successfully with the complete test suite. PostgreSQL remains the final public-release gate in this environment.

## Required sequence

1. Run `./scripts/run_python_pipeline.sh`.
2. Start PostgreSQL and ensure `psql` is available.
3. Run `./scripts/run_postgres_pipeline.sh` or, preferably, `./scripts/run_full_validation.sh`.
4. Confirm `results/e2e_crosscheck_report.csv` contains only `pass=true` for all mapped KPIs, including paired COP observation count/coverage.
5. Confirm `results/sql_requirement_verification.csv` contains the loaded PM+SE verification evidence.
6. Regenerate `results/VALIDATION_MANIFEST.csv`.

Do not tag public `v1.0.0` until the console reports:

`E2E crosscheck PASSED for mapped v6 KPIs.`

The SQL KPI view uses the same paired-observation weighted-COP rule as Python. PostgreSQL also restores the integrated PM+SE evidence model: reporting periods, stakeholder needs, requirements, verification records, risks, change requests, schedule, project progress/EVM and decision gates.
