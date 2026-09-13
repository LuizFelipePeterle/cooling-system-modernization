# Verification & Acceptance Criteria

## SYS-AVL-001 Availability
- 90 consecutive days after stabilization.
- Planned maintenance excluded only if pre-approved and recorded.
- Acceptance: >=99.50%, no unplanned outage >8 h, no unresolved Severity-1 defect.

## SYS-ENE-001 COP
- >=30 valid operating days.
- >=500 paired 15-minute measurements.
- Acceptance load range: 60-90% nominal demand.
- Calibration/verification status valid.
- Mean COP >=3.30.
- Lower 95% CI of daily mean COP >=3.20.
- <=10% of valid days below daily COP 3.00.

## SYS-MNT-001 MTTR
- Include all corrective events during demonstration.
- Clock definition fixed before test.
- Mean <=5.0 h; median <=4.5 h; P90 <=8.0 h.

## SYS-MON-001 Data availability
- Nominal interval <=60 s.
- >=99% expected timestamps over 30 days.
- No gap >10 min without documented cause.

## SYS-ALM-001 Alarm performance
- Normalized per 720 operating hours.
- Same priority taxonomy before/after.
- High-priority nuisance alarm reduction >=60%.
- No safety/protection alarm may be suppressed merely to meet the metric.
