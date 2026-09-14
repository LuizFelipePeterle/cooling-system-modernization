# Executive Case Study
## Industrial Cooling System Reliability & Energy Efficiency Modernization

**Independent simulated engineering portfolio case.**

### Challenge
A fictional 1,200 kW industrial cooling system is modeled with reliability, maintainability, energy-performance and operational-visibility challenges. The project is framed from quantified information needs rather than a predetermined technology.

### Engineering approach
The case integrates Project Management and Systems Engineering: stakeholder needs, verifiable requirements, trade study, architecture/interfaces, WBS, deterministic schedule and critical path, cost/risk/EVM, controlled change, staged integration, V&V, transition and benefit realization.

### Evidence approach
Operational evidence is generated stochastically from externalized assumptions. Realized failure counts, downtime, excursions and costs are not forced to match target values. A fixed seed provides a reproducible reference realization; PostgreSQL produces the final analytical evidence layer.

### Current reference realization
Availability: 98.9557% -> 99.6844%  
Downtime: 91.48 h -> 27.72 h  
MTBF: 722.38 h -> 2,189.07 h  
Mean repair time: 5.68 h -> 4.53 h  
PM compliance: 77.78% -> 97.22%  
Temperature excursions: 37 -> 5  
O&M: EUR 425,432.79 -> EUR 357,924.84

Annual O&M reduction: 15.87%. Simple payback on O&M savings only: 5.33 years.

### Project-control scenario
At Week 20, PV=EUR210k, EV=EUR195k and AC=EUR205k (SPI 0.929; CPI 0.951). A simulated VFD procurement delay affects a zero-float critical-path activity. CR-004 evaluates recovery alternatives and adopts a qualified temporary-drive strategy with mandatory regression testing.

### Technical integrity
The portfolio includes automated tests, parameter governance, leap-year-aware measurement periods, event-derived O&M costs, decision gates, requirement traceability, acceptance criteria and an explicit PostgreSQL E2E publication gate.

### Portfolio message
The case demonstrates the ability to connect project execution and systems-engineering discipline to measurable operational evidence rather than treating them as separate bodies of knowledge.
