#!/usr/bin/env bash
set -euo pipefail

echo "=== Python code quality: Ruff ==="
ruff check python scripts tests

echo "=== Automated tests: Pytest ==="
pytest -v

echo "=== Ansible playbook quality: Ansible Lint ==="
ansible-lint ansible/

echo "=== Validation successful ==="