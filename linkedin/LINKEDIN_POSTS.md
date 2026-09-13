# LinkedIn Publication Pack

All posts refer to an independent simulated case study. Replace `[GitHub link]` only after the relevant evidence is public.

## Post 1 - Engineering starts with the problem, not the solution
I have started developing an independent simulated engineering case study to explore how Project Management and Systems Engineering can be integrated around a measurable operational problem.

The case involves an industrial cooling system modeled with reliability, maintainability, energy-performance and operational-visibility challenges.

Rather than starting with a technology, I began with the information needed for decisions: operating periods, failure events, downtime, maintenance performance, energy behavior, alarms and cost.

An important design rule is that the simulated KPI outcomes are not hard-coded. The model generates operational evidence first; performance is calculated afterward.

The next step is to translate the operational problem into stakeholder needs and verifiable engineering requirements.

This is an independent simulated case study. All organizations, assets, data and results are fictional.

Visual: Problem -> Measurement -> Needs -> Requirements.

## Post 2 - From operational need to verifiable requirement
A KPI becomes much more useful when it is connected to an engineering decision.

In my simulated cooling-system case, the chain for operational continuity is:

Operational need -> Stakeholder need -> System requirement -> Architecture -> Verification evidence -> Operational KPI.

For example, the need for continuous cooling service is translated into a measurable availability requirement rather than a vague statement such as "improve reliability."

The important part is traceability: if a requirement cannot be connected to a need, design decision and verification method, it becomes difficult to justify and difficult to accept objectively.

This case is fully simulated and developed for professional learning.

Visual: SN-01 -> SYS-AVL-001 -> architecture -> test -> availability.

## Post 3 - Choosing a solution is an engineering decision
A solution should be the result of a decision process, not the starting assumption.

For the simulated cooling modernization I compared four conceptual alternatives: do nothing, full replacement, controls/instrumentation only, and targeted modernization.

The selected concept balances investment, reliability benefit, energy performance, integration risk, shutdown burden and lifecycle value.

The exercise reinforced a simple point: the most technically extensive option is not automatically the best system decision.

Visual: original trade-study matrix. Do not use third-party figures.

## Post 4 - Breaking an engineering objective into manageable work
A system objective is not yet an executable project plan.

I decomposed the simulated modernization into seven workstreams: Project Management, Engineering, Procurement, Implementation, Software/Data, Integration & V&V, and Transition.

The WBS creates the bridge between engineering scope and project control. Requirements describe what the system must achieve; work packages organize the effort required to deliver and prove it.

Visual: WBS tree.

## Post 5 - Risk becomes useful when it changes a decision
A risk register should do more than assign colors.

In the simulated case, probability and impact are explicitly scored, but each material risk also has a trigger, owner and response strategy.

The highest initial exposure is a long-lead VFD procurement risk on a zero-float critical-path activity. That connection matters: the same risk score would have a different project consequence if the activity had substantial float.

Visual: risk heatmap plus critical-path highlight.

## Post 6 - When a risk becomes an issue
In the simulated execution, the VFD supplier reports a three-week delay.

The response is not "expedite immediately." The sequence is: assess the schedule network, identify the affected critical path, evaluate alternatives, quantify cost/verification consequences, raise a change request, obtain approval and update controlled baselines/evidence.

The selected simulated response uses qualified temporary equivalent drives for commissioning and installs the final units during the planned shutdown, with mandatory regression testing. The approved cost impact is EUR 7,500.

The important lesson is that a schedule recovery action can create a verification obligation. Project change and engineering evidence cannot be managed separately.

## Post 7 - Project performance is not system performance
At Week 20 of the simulated project:

PV = EUR 210k
EV = EUR 195k
AC = EUR 205k
SPI = 0.929
CPI = 0.951

Those metrics describe project execution. They do not tell me whether the delivered cooling system will achieve availability, maintainability or energy-performance requirements.

A project can be on time and on budget and still deliver a poor system. A technically excellent system delivered through uncontrolled execution is also not a desirable outcome.

That is why I keep project, system, technical and business metrics as separate layers connected by traceability.

Visual: Project KPIs | System KPIs | Business Outcomes.

## Post 8 - Verification is not validation
Verification asks whether the engineered entity satisfies its specified requirements.

Validation asks whether the integrated solution satisfies stakeholder needs and intended use in its operational context.

In the simulated case, a COP test can verify an energy-performance requirement, while operational validation considers whether the complete solution provides the reliability, maintainability and visibility that justified the modernization.

Keeping the two questions separate makes acceptance evidence clearer.

Visual: Requirement -> Design -> Verification; Stakeholder Need -> Operational Use -> Validation.

## Post 9 - Did the project actually improve performance?
A project is not successful simply because planned deliverables were completed.

The more important question is whether the delivered system improved the operational outcomes that justified the investment.

For the current reproducible reference realization of my simulated case:

- Availability: 98.9557% -> 99.6844%
- Unplanned downtime: 91.48 h -> 27.72 h
- MTBF: 722.38 h -> 2,189.07 h
- Mean repair time: 5.68 h -> 4.53 h
- PM compliance: 77.78% -> 97.22%
- Temperature excursions: 37 -> 5
- O&M cost: EUR 496,827.73 -> EUR 413,914.64

These values are not manually inserted into the generator. They emerge from a fixed, reproducible stochastic scenario and are calculated downstream.

The resulting simulated O&M reduction is 16.69%, with a simple payback of 4.34 years using O&M savings only.

Measurements should exist because they support decisions - not because dashboards need more metrics.

This is an independent simulated case study; all data and results are fictional.

Visual: Before/Post dashboard. Publish only after the PostgreSQL E2E gate passes; replace raw COP with final SQL-cleaned KPI.

## Post 10 - The system was delivered. The learning should remain.
Five lessons from building this simulated engineering case:

1. Define the problem and information needs before selecting technology.
2. Requirements should be measurable and linked to verification evidence.
3. Interfaces and integration need to be planned early.
4. Project KPIs, system KPIs and business outcomes answer different questions.
5. Project closure is not the end of benefit realization.

A sixth lesson emerged while developing the model: if the evidence contradicts the original story, change the story - not the evidence.

That principle changed this case substantially. Early illustrative values were replaced by stochastic, reproducible outcomes and an event-derived business case.

Repository: [GitHub link]
