#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"; cd "$ROOT"
echo '===================================================='
echo 'NDC-01 ENGINEERING CASE - FULL VALIDATION'
echo '===================================================='
./scripts/run_python_pipeline.sh
if ! command -v psql >/dev/null 2>&1; then
  echo 'PostgreSQL/psql not found: Python evidence is valid, but FULL E2E validation is incomplete.'
  echo 'Install/start PostgreSQL and rerun this command before tagging public v1.0.0.'
  exit 2
fi
./scripts/run_postgres_pipeline.sh
python scripts/generate_validation_manifest.py
echo '===================================================='
echo 'VALIDATION STATUS: PASS'
echo '===================================================='
