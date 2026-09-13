# NDC-01 Mission-Critical Data Center Cooling Modernization

**Engineering Project Management + Systems Engineering + Reproducible Evidence**

> From quantified operational deterioration to requirements, engineering decision, controlled delivery, V&V and measurable benefit realization.

## Disclaimer
This is an independent, fully simulated portfolio case. NovaTech Data Centers, NDC-01, customers, assets, operational data, costs and results are fictional. No employer, client or restricted operational information is represented.

## 1. Scenario
NovaTech Data Centers (NDC) is a fictional mid-sized colocation and digital-infrastructure provider. NDC-01 is a regional facility serving approximately 80 enterprise customers, with 420 installed racks, approximately 350 occupied racks and a modeled critical IT load up to 800 kW. The facility operates 24x7x365.

The cooling plant comprises three 400 kW chillers (1.2 MW nominal capacity), six pumps, field instrumentation, PLC-based control, a legacy BMS/SCADA layer and maintenance processes. Under the defined design condition, two chillers support the critical cooling requirement while the third provides intended redundancy.

During the 2026 baseline period, Facilities Engineering identifies progressive deterioration rather than one catastrophic event. The frozen seeded realization produces 13 equipment failures, 121.75 accumulated equipment-downtime hours, 66.75 hours outside the intended N+1 state, 4.75 hours of cooling-capacity deficit, 72.22% PM compliance, weighted COP 2.809, modeled PUE 1.551 and EUR 425,432.79 annual cooling O&M.

**Equipment downtime is explicitly not treated as IT-service downtime.** Individual asset failures can be absorbed by redundancy. The engineering concern is the loss of redundancy, reduced thermal margin, capacity-deficit exposure, maintenance burden, energy performance and lifecycle cost.

## 2. Chronological narrative
Baseline evidence -> engineering assessment -> stakeholder needs -> verifiable requirements -> alternatives analysis -> business case -> project authorization -> PM + SE integrated execution -> design/procurement/implementation -> integration -> verification -> validation -> transition -> post-modernization observation -> benefit realization.

## 3. Selected modernization
The selected EUR 360k targeted modernization combines VFDs, selected instrumentation, control optimization, condition monitoring, BMS/data visibility, alarm rationalization, selected reliability interventions and maintenance-process redesign. Full plant replacement is deliberately not assumed to be the only answer.

## 4. PM and SE roles
**Project Management** governs charter, scope/WBS, schedule, cost, procurement, risk, change, EVM, decision gates and transition.

**Systems Engineering** maintains the technical evidence chain: stakeholder needs -> requirements -> architecture -> interfaces -> integration -> verification -> validation.

## 5. Mission-level semantics
The v6.1 model separates three concepts:
1. **Asset reliability:** failures and equipment downtime.
2. **Cooling-service performance:** whether available cooling capacity meets required cooling demand.
3. **IT-service consequence:** not assumed from an equipment failure; customer outage monetization is outside the base case.

## 6. Energy boundaries
15-minute performance evidence contains IT load, cooling demand, cooling electrical power/energy, COP, total modeled facility power/energy and PUE. PUE is explicitly a modeled facility-boundary indicator, not a claim about a real facility. A separate 1-minute monitoring-completeness evidence set demonstrates the monitoring requirement without creating an unnecessarily large raw sensor file.

## 7. Seeded reference realization
| KPI | Baseline | Post |
|---|---:|---:|
| Failures | 13 | 5 |
| Equipment downtime | 121.75 h | 20.08 h |
| Cooling-service availability | 99.9458% | 99.9943% |
| Outside intended N+1 state | 66.75 h | 15.25 h |
| Capacity deficit | 4.75 h | 0.50 h |
| Weighted COP | 2.809 | 3.361 |
| Modeled PUE | 1.551 | 1.489 |
| PM compliance | 72.22% | 98.61% |
| Cooling O&M | EUR 425,432.79 | EUR 357,924.84 |

Direct O&M saving = **EUR 67,507.95/year (15.87%)**. Simple payback on direct O&M savings only = **5.33 years**. No avoided IT outage is monetized.

## 8. Model governance
The project distinguishes:
- **Model baseline:** distributions, periods, engineering/economic assumptions and acceptance thresholds.
- **Seeded reference realization:** one reproducible stochastic realization using seed `20260912`.
- **Acceptance results:** PASS/FAIL produced by comparing derived evidence with predeclared criteria.

If evidence contradicts the intended story, the story changes - not the evidence.


## 8.1 Paired-observation energy methodology
Weighted COP is calculated only over deduplicated 15-minute timestamps where **both** `cooling_energy_kwh` and `cooling_electrical_energy_kwh` are present. Baseline uses 34,744 paired observations (99.155% coverage) and post uses 34,864 paired observations (99.226% coverage). This prevents numerator and denominator from representing different time windows. The same rule is implemented in Python and PostgreSQL.

`project_period` is retained as governed master data for reporting boundaries and annualization, but cooling-service availability is derived directly from 15-minute `capacity_state` observations.

## 9. Generated evidence
`performance_telemetry_raw.csv`, `cooling_capacity_state.csv`, `monitoring_completeness_daily.csv`, `failures.csv`, `maintenance_orders.csv`, `alarms.csv`, `temperature_excursions.csv`, `om_costs.csv`, `assets.csv`, and `python_kpi_crosscheck.csv`.

## 10. Run in GitHub Codespaces
```bash
chmod +x scripts/*.sh
./scripts/run_python_pipeline.sh
```
Expected Python gate: data generation, validation, regenerated KPI evidence, the complete pytest suite, requirement verification, benefit calculation, schedule Monte Carlo and chart generation.

For the final release gate, run `./scripts/run_full_validation.sh` in an environment with PostgreSQL/psql available. The PostgreSQL layer reloads operational evidence plus the integrated PM+SE model and compares SQL KPIs with freshly regenerated Python KPIs. Publish v1.0 only after the full E2E crosscheck passes.

## 11. Current release status
**v6.1 Engineering Evidence Integrity Release Candidate.** The Python pipeline passes the complete test suite and regenerates derived evidence from current raw data. PostgreSQL E2E validation remains the final gate before a validated public v1.0 tag.
