# Project Execution Guide v2

1. Freeze business problem and system boundary.
2. Freeze KPI definitions and acceptance criteria.
3. Freeze risk scales.
4. Freeze schedule network and critical path.
5. Freeze synthetic-data statistical model.
6. Generate raw data.
7. Validate raw data independently of project targets.
8. Load database.
9. Calculate KPIs downstream.
10. Compare realized KPI outcomes with requirements.
11. Execute Monte Carlo schedule analysis.
12. Run decision gates G0-G6.
13. Produce project-controls and V&V evidence.
14. Publish only after all tests pass.

## Publication rule
Never describe stochastic calibration parameters as realized outcomes.
Never claim simulated results as real operational achievements.


## Calendar-time rule
Never use a fixed 8,760-hour denominator for arbitrary annual windows.
Required operating hours must be derived from the exact inclusive calendar span of the
measurement period. Leap-day inclusion must therefore be reflected automatically.

## Cost rule
O&M benefit claims may be published only if the cost table has been generated, loaded,
reconciled, and aggregated through the database. Story values must never substitute for
calculated values.


## v4 model-freeze rule
Use `docs/MODEL_FREEZE_V4.md` as the controlled scenario baseline.
Use `docs/BUSINESS_CASE.md` for current economic results.
Earlier illustrative figures are superseded.
