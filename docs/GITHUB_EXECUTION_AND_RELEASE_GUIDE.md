# GitHub Execution & Release Guide

## 1. Create the repository
Recommended public name: `industrial-engineering-systems-case-study`.

From the extracted project folder:
```bash
git init
git branch -M main
git add README.md DISCLAIMER.md docs/MASTER_CASE_STUDY.md
git commit -m "Initial case study structure and problem definition"
```
Create an empty repository on GitHub, then:
```bash
git remote add origin https://github.com/<username>/industrial-engineering-systems-case-study.git
git push -u origin main
```

## 2. Progressive evidence commits
```bash
git add engineering/
git commit -m "Add stakeholder needs requirements and traceability"

git add project_management/
git commit -m "Add schedule risk EVM change control and decision gates"

git add analytics/ tests/ requirements.txt
git commit -m "Add governed stochastic data generator and automated tests"

git add database/
git commit -m "Add integrated PostgreSQL evidence model and KPI views"

git add docs/ portfolio/ linkedin/ scripts/
git commit -m "Add V&V business case execution and publication pack"

git push
```

## 3. Run the Python evidence gate
```bash
./scripts/run_python_pipeline.sh
```
Expected: raw evidence is regenerated, validation passes, `python_kpi_crosscheck.csv` is recalculated from current evidence, the complete pytest suite passes, requirements and benefits are evaluated, Monte Carlo runs, charts are regenerated and a validation manifest is written.

## 4. Run the full E2E gate
PostgreSQL 16 is recommended. With `psql` available, use the single public release command:

```bash
./scripts/run_full_validation.sh
```

For troubleshooting, the SQL-only stage can still be run with `./scripts/run_postgres_pipeline.sh` after the Python gate.
Expected outputs:
- `results/postgres_validation.txt`
- `results/sql_kpi_crosscheck.csv`
- `results/sql_benefit_realization.csv`
- `results/sql_requirement_verification.csv`
- `results/sql_project_evm.csv`
- `results/e2e_crosscheck_report.csv`
- `results/VALIDATION_MANIFEST.csv`

The SQL crosscheck must state `E2E crosscheck PASSED for mapped v6 KPIs.` and the full script must finish with `VALIDATION STATUS: PASS`.

## 5. Freeze evidence
Record environment information:
```bash
python --version > results/environment.txt
psql --version >> results/environment.txt
git rev-parse HEAD >> results/environment.txt
```
Do not change seed, distributions, economic assumptions, KPI formulas, acceptance thresholds or measurement periods without a documented model/change revision.

## 6. Tag v1.0 only after E2E passes
```bash
git add results/ docs/POSTGRES_E2E_VALIDATION_REPORT.md
git commit -m "Record PostgreSQL E2E validation evidence"
git tag -a v1.0 -m "Validated simulated engineering case study v1.0"
git push origin main --tags
```

## 7. GitHub repository description
`Simulated engineering case integrating project management, systems engineering, stochastic operational data, PostgreSQL, V&V and measurable benefit realization.`

## 8. Suggested GitHub topics
`systems-engineering`, `project-management`, `engineering-management`, `reliability`, `maintenance`, `postgresql`, `python`, `verification-validation`, `industrial-engineering`, `data-governance`.

## 9. What not to upload
Do not upload INCOSE/PMI copyrighted training PDFs, copied figures, screenshots of protected reference material, employer data or real sensitive engineering information.

## 10. Evidence freeze sequence
The public release sequence is:

`configuration/model freeze -> clean stale derived outputs -> raw evidence generation -> complete tests -> Python KPI generation -> requirement verification -> benefit calculation -> PostgreSQL load -> SQL KPI calculation -> Python/SQL crosscheck -> validation manifest -> report/dashboard publication`.

Do not carry `python_kpi_crosscheck.csv`, SQL crosschecks or verification outputs from an earlier model run into a new evidence freeze.
