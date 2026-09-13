# Evolution and Concepts - v1 to v6.1

## v1 - Narrative-forced outcomes
Early versions forced selected failure, excursion and downtime totals. This was useful for storytelling but weak as evidence.

## v2 - Stochastic outcomes
Failure and excursion counts became stochastic and validators checked plausibility rather than exact desired totals.

## v3 - Dynamic calendar and event-derived economics
Calendar handling and O&M economics became more explicit and reproducible.

## v4 - Model freeze and authoritative periods
Material assumptions moved to configuration, project periods became authoritative and benefit calculations avoided double counting.

## v5 - Portfolio release candidate
PM and SE artifacts, GitHub execution, publication assets, parameter register and Python/PostgreSQL crosscheck design were packaged professionally.

## v6 - Mission-critical data-center semantics
The case is re-engineered as NDC-01, a fictional colocation data center. Key corrections:
1. 800 kW critical IT load is coherent with a 3 x 400 kW cooling plant under the defined N+1 design condition.
2. Equipment downtime is no longer labeled system/IT outage.
3. Cooling-service availability is derived from available capacity versus required cooling demand.
4. Redundancy exposure and capacity-deficit hours are explicit.
5. PUE is added with a declared modeled facility-energy boundary.
6. Performance telemetry is 15-minute; monitoring completeness is based on 1-minute evidence.
7. Independent RNG streams improve change isolation.
8. Direct O&M savings remain separate from unmonetized IT-service risk reduction.

## Core concepts
**Asset reliability** concerns failures, repair and equipment downtime.

**Service availability** concerns whether the system can perform its mission despite asset failures.

**Redundancy exposure** measures time outside the intended redundant state even when service remains available.

**Capacity deficit** occurs when available cooling capacity is below defined cooling demand plus margin.

**Weighted COP** is total cooling energy divided by total cooling electrical energy over the evaluation period; it is preferred to a simple average of interval COPs for the public KPI.

**PUE** is modeled facility energy divided by IT energy within the declared boundary. It is not presented as a measurement from a real data center.

**Verification** evaluates requirements. **Validation** evaluates stakeholder needs and intended use.

**Project performance** (SPI/CPI/schedule/risk) is distinct from **system performance** (availability/COP/PUE/redundancy/maintenance).

## v6.1 evidence-integrity corrections

The v6.1 revision closes several audit findings without changing the core NDC-01 scenario.

1. **Paired weighted COP.** Weighted COP is calculated only from 15-minute observations for which both `cooling_energy_kwh` and `cooling_electrical_energy_kwh` are present. Numerator and denominator therefore use the same time windows. The paired observation count and percentage are published as first-class evidence.
2. **Generated Python KPI evidence.** `python_kpi_crosscheck.csv` is no longer a static packaged artifact. It is deleted and regenerated from current raw evidence on every Python pipeline run.
3. **Complete test suite.** The public pipeline runs `pytest` across the entire `tests/` directory. Legacy tests were updated to v6 semantics rather than bypassed.
4. **Governed reporting periods.** `project_period` is restored as master data for reporting boundaries and annualization, while cooling-service availability remains independently derived from 15-minute `capacity_state` observations. This preserves the leap-year-safe v6 availability design.
5. **Integrated PM + SE database model.** Stakeholder needs, requirements, verification records, risks, changes, schedule, EVM progress and decision gates are again loaded into PostgreSQL as first-class entities.
6. **Dead-file removal.** The legacy `telemetry_raw.csv` is removed. `performance_telemetry_raw.csv` is the authoritative v6 performance dataset.
7. **Evidence freeze discipline.** Configuration/model freeze precedes evidence generation. Derived KPI, verification, benefit and SQL crosscheck artifacts are generated after the frozen model is executed, not carried forward from an older run.

The release criterion is intentionally stricter: a clean clone must run the complete Python suite successfully; public `v1.0.0` additionally requires PostgreSQL E2E execution and Python-SQL KPI agreement.
