# Synthetic Data Generation Specification — v2

## Governance rule
No operational KPI outcome is hard-coded into generated final records.

Targets such as 14 failures/year, 41 excursions/year, or 132 h/year are **not**
deterministic output requirements. They may be used only as calibration references when
selecting stochastic-process parameters. Actual event counts and downtime totals emerge from
the seeded stochastic process.

## Reproducibility
Random seed: `20260912`.

Re-running the generator with the same seed must reproduce identical raw records.
Changing the seed must change the event realization while preserving the statistical character
of the scenario.

## Failure generation
Failures follow a non-homogeneous Poisson process approximation:
- annual base rate baseline: 14 events/year;
- annual base rate post: 6 events/year;
- daily hazard is multiplied by a load-dependent factor;
- realized annual count is random.

For each failure:
- asset is sampled from eligible assets with criticality weights;
- downtime is lognormal;
- repair duration is conditionally related to downtime but is not equal to it;
- failure mode is sampled from a categorical distribution.

No scaling step is permitted to force annual downtime totals.

## Temperature excursions
Excursions use a load-sensitive Poisson process:
- annual rate baseline: 41/year;
- annual rate post: 8/year;
- realized event count is random.

No exact count assertion is allowed.

## Alarm process
Daily alarms use a Gamma-Poisson mixture (negative-binomial behavior) to create
overdispersion. Rate increases on high-load days and failure days.

## Preventive maintenance
Completion is Bernoulli by scheduled order, with period-specific completion probability.

## COP and energy
Cooling demand includes seasonality and Gaussian noise. COP depends on period, load, and
random variation. Post-project improvement is probabilistic, not constant.

## Data imperfections
The generator intentionally introduces:
- controlled missing telemetry;
- duplicate telemetry rows;
- timestamp jitter;
- rare plausible outliers.

Imperfections are introduced only in raw telemetry and must not invalidate the ability to
reconstruct acceptance-period KPIs after documented cleaning.

## Validation philosophy
Validation checks:
- schema and referential integrity;
- physical plausibility;
- reproducibility;
- missingness/duplicate/outlier ranges;
- event counts within broad probabilistic tolerance bands.

Validation must never assert that realized KPIs equal desired project targets.


## O&M cost generation
O&M cost is derived from simulated monthly components rather than assigned as a final KPI:
- electrical-energy cost = generated electrical kWh × configured tariff;
- labor cost = preventive + corrective labor hours × configured labor rate;
- parts cost = stochastic event-driven part cost;
- emergency-parts cost = probabilistic premium on a subset of failure-related parts;
- service-contract cost = configured monthly fixed component.

The annual O&M KPI is the downstream sum of monthly generated costs. Values such as
EUR 284k or EUR 218k are not forced into the data generator.


## Parameter governance
All material scenario parameters must exist in `data_generation_config.json` and be listed in
`docs/PARAMETER_REGISTER.csv`. Hard-coded scenario assumptions in generation logic are prohibited.
