# Publication Checklist

- [ ] Python generator executed from clean environment.
- [ ] Validator passes.
- [ ] `pytest` passes across the complete `tests/` directory (no selective test invocation).
- [ ] Reproducibility hashes confirmed if desired.
- [ ] Monte Carlo output recorded.
- [ ] PostgreSQL 16 E2E pipeline passes and integrated PM+SE reference entities load successfully.
- [ ] `python_kpi_crosscheck.csv` is regenerated from current evidence and SQL/Python crosscheck passes within documented tolerance.
- [ ] `POSTGRES_E2E_VALIDATION_REPORT.md` updated with real environment/commit/results.
- [ ] Weighted COP uses paired observations in Python and SQL; paired-observation count/coverage are recorded.
- [ ] No early illustrative EUR284k/EUR218k or 132h/38h values remain as realized evidence.
- [ ] Parameter Register shared/global column reviewed.
- [ ] All public diagrams are original.
- [ ] No INCOSE/PMI copyrighted PDFs, screenshots or copied tables/figures included.
- [ ] README clearly says simulated.
- [ ] Executive Case Study exported to PDF.
- [ ] Power BI dashboard uses final E2E outputs.
- [ ] GitHub tag v1.0 created only after E2E pass.
- [ ] LinkedIn Post 9 published only after final E2E evidence is frozen.

- [ ] No legacy `data/generated/telemetry_raw.csv` exists.
- [ ] `results/VALIDATION_MANIFEST.csv` regenerated after final E2E run.
- [ ] `./scripts/run_full_validation.sh` completes with `VALIDATION STATUS: PASS`.
