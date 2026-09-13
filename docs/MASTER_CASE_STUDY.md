# Master Case Study v6.1 - NDC-01 Mission-Critical Data Center Cooling Modernization

## Executive narrative
NovaTech Data Centers (NDC), a fictional mid-sized colocation provider, operates NDC-01 continuously for approximately 80 enterprise customers. The facility contains 420 installed racks, approximately 350 occupied racks and a modeled critical IT load up to 800 kW. Its cooling plant consists of three 400 kW chillers, six pumps, PLC control, legacy BMS/SCADA and associated instrumentation.

The case begins with deterioration, not a predetermined solution. During the 2026 baseline, Facilities Engineering observes recurring equipment failures, maintenance backlog, thermal events, degraded redundancy, energy inefficiency and increasing O&M burden. The seeded reference realization records 13 equipment failures, 121.75 equipment-downtime hours, 66.75 hours outside intended N+1 redundancy, 4.75 hours in cooling-capacity deficit, 72.22% PM compliance, weighted COP 2.809, modeled PUE 1.551 and EUR 425,432.79 cooling O&M.

Asset downtime is deliberately separated from mission impact. A failed chiller does not automatically mean a data-center outage. The mission-level question is whether remaining cooling capacity can satisfy defined cooling demand and margin. This distinction is central to v6.

## Phase 1 - Operational observation
The organization identifies a pattern of progressive deterioration. No single catastrophic event is required to justify assessment. Repeated equipment events reduce redundancy, consume maintenance capacity, increase the probability of coincident exposure and worsen operating economics.

## Phase 2 - Engineering assessment
Management authorizes an engineering assessment before authorizing a capital project. The assessment establishes the baseline, stakeholder needs, system requirements, measurement plan, alternatives and risk exposure.

## Phase 3 - Stakeholder needs and requirements
Operations requires sufficient cooling capacity and visibility of redundancy/thermal margin. Maintenance requires earlier degradation detection and defined restoration performance. Engineering requires reliable data. Finance requires measurable lifecycle value. Service Management requires protection of customer-facing IT services. Cybersecurity requires appropriate separation and least privilege across control, supervisory and analytics functions.

Requirements convert these needs into measurable acceptance criteria for cooling-service availability, redundancy visibility, PM compliance, weighted COP, modeled PUE, monitoring completeness and cybersecurity review.

## Phase 4 - Alternatives analysis
Four alternatives are evaluated: continue as-is; full plant replacement; controls/instrumentation only; targeted modernization. Targeted modernization is selected as the balanced alternative, with EUR 360k authorized funding and a 32-week planned duration.

## Phase 5 - Integrated PM + SE planning
Project Management creates the charter, scope/WBS, schedule, cost baseline, procurement strategy, risk register, change process, EVM structure and decision gates. Systems Engineering maintains needs-to-requirements traceability, architecture, interfaces, integration logic, verification methods and validation intent. Neither discipline replaces the other.

## Phase 6 - Solution architecture
Field sensors, meters and VFDs feed PLC control; BMS/SCADA provides supervision; historian/data services retain evidence; condition-monitoring logic and engineering dashboards provide decision support; maintenance processes translate information into action. Cybersecurity controls apply across these interfaces.

## Phase 7 - Execution and control
Design, procurement, installation, controls, data integration and maintenance-process changes proceed under project governance. A VFD supplier delay materializes as an issue. CR-004 documents assessment, alternatives, approval and regression-test protection rather than an ungoverned workaround. At week 20, PV=EUR210k, EV=EUR195k and AC=EUR205k, producing SPI 0.929 and CPI 0.951.

## Phase 8 - Integration, verification and validation
Integration progresses from field devices to control, supervisory, data and analytics layers. Verification asks whether each requirement is satisfied by evidence. Validation asks whether the resulting solution meets stakeholder needs and intended operational use. A failed criterion remains failed; seed or evidence is not changed to force acceptance.

## Phase 9 - Transition and benefit realization
After commissioning and transition, the post-modernization observation period is 1 Sep 2027 through 31 Aug 2028. The seeded reference realization records 5 failures, 20.08 equipment-downtime hours, 15.25 hours outside intended N+1 redundancy, 0.50 hours of cooling-capacity deficit, 98.61% PM compliance, weighted COP 3.361, modeled PUE 1.489 and EUR 357,924.84 cooling O&M.

Direct O&M saving is EUR 67,507.95/year (15.87%). Simple payback on direct O&M saving only is 5.33 years. Avoided customer outage value is not monetized. Operational-risk reduction is reported separately through redundancy and capacity-deficit exposure.

## Why v6 is materially stronger
v6 does not merely rename the facility as a data center. It changes the engineering semantics. Cooling capacity is compared with time-varying demand; asset downtime is separated from service availability; redundancy exposure is measurable; 15-minute performance telemetry supports COP/PUE; 1-minute monitoring completeness supports monitoring requirements; direct economics are separated from unmonetized service-risk reduction; and independent random streams reduce accidental coupling among subsystems.

## Evidence chain
Business concern -> baseline evidence -> stakeholder needs -> system requirements -> alternatives -> selected architecture -> PM delivery controls -> integration -> verification -> validation -> post evidence -> benefit realization.


## Evidence-integrity architecture
The v6.1 revision treats evidence generation as a pipeline rather than a collection of prepackaged outputs. The generator writes raw simulated evidence; `calculate_python_kpis.py` regenerates KPI evidence from those current files; the complete pytest suite checks semantics and governance; requirement verification and benefit realization are then derived; PostgreSQL independently recalculates the mapped KPIs and reloads PM+SE reference entities.

Weighted COP uses only paired, deduplicated 15-minute observations with both cooling-energy channels present. The seeded reference realization therefore produces baseline weighted COP **2.8087** from **34,744 paired observations (99.155%)** and post weighted COP **3.3607** from **34,864 paired observations (99.226%)**.

The integrated PostgreSQL model contains governed reporting periods, stakeholder needs, system requirements, verification records, risks, change requests, schedule activities, EVM progress and decision gates. Reporting-period master data does not drive cooling-service availability; availability remains interval-evidence based.
