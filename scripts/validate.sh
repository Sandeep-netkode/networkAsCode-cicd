#!/usr/bin/env bash
set -euo pipefail

echo "=== Python code quality: Ruff ==="
ruff check python tests

echo "=== Automated tests: Pytest ==="
pytest -v

echo "=== Validation successful ==="
