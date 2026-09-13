# NDC-01 v6.1 Data Dictionary

| Dataset | Granularity | Purpose | Authority |
|---|---|---|---|
| `performance_telemetry_raw.csv` | 15-minute, with controlled duplicates/missingness | IT load, cooling demand, energy, COP/PUE evidence | Authoritative raw performance evidence |
| `cooling_capacity_state.csv` | 15-minute | available cooling capacity, demand, capacity margin, service availability, redundancy state | Authoritative capacity/service evidence |
| `monitoring_completeness_daily.csv` | Daily summary of 1-minute monitoring | 1-minute monitoring completeness requirement | Authoritative monitoring-quality evidence |
| `failures.csv` | Event | Equipment reliability and downtime | Authoritative failure evidence |
| `maintenance_orders.csv` | Work order | Preventive-maintenance compliance | Authoritative maintenance evidence |
| `alarms.csv` | Event | Alarm-performance analysis | Supporting operational evidence |
| `temperature_excursions.csv` | Event | Thermal-exposure analysis | Supporting operational evidence |
| `om_costs.csv` | Monthly | Cooling O&M cost components | Authoritative direct-cost evidence |
| `assets.csv` | Asset master | Cooling asset population | Master data |
| `python_kpi_crosscheck.csv` | Period summary | Recalculated Python KPI evidence | Derived on every pipeline run |

## Paired weighted COP rule

Let `P` be the set of deduplicated 15-minute timestamps where both cooling-energy channels are present. Then:

`weighted_COP = sum(cooling_energy_kwh[t], t in P) / sum(cooling_electrical_energy_kwh[t], t in P)`.

The KPI output also publishes `paired_cop_observations` and `paired_cop_observation_pct`. Missing values from one channel can therefore never cause numerator and denominator to represent different time windows.

## Reporting periods versus service availability

`project_period` defines governed baseline/post boundaries and required calendar hours. It is **not** used to calculate cooling-service availability. Service availability is the proportion of 15-minute `capacity_state` observations whose `capacity_margin_kw >= 0`, so leap-year reporting differences cannot distort that KPI.
