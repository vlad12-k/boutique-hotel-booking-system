#!/usr/bin/env bash

printf '\n=== PROJECT TREE ===\n'
find . -maxdepth 3 -type f \
  ! -path './.git/*' \
  ! -path './venv/*' \
  ! -path './.venv/*' \
  ! -path './__pycache__/*' \
  | sort

printf '\n=== FLASK ROUTES ===\n'
grep -nE '@app\.(route|get|post|put|delete)|@.*_bp\.(route|get|post|put|delete)' app.py || true

printf '\n=== SCREENSHOTS ===\n'
find screenshots -maxdepth 1 -type f | sort

printf '\n=== TELEGRAM COMMANDS ===\n'
grep -RInE '/help|/status|/cleaning|/available|/ready|/maintenance|/notifications' \
  telegram_bot_worker.py services tests || true

printf '\n=== ENVIRONMENT VARIABLES USED IN CODE ===\n'
python - <<'PY'
from pathlib import Path
import re

files = [Path("app.py"), Path("telegram_bot_worker.py")]
files.extend(Path("services").glob("*.py"))

patterns = [
    re.compile(r'''(?:os\.)?getenv\(\s*["']([A-Z0-9_]+)["']'''),
    re.compile(r'''os\.environ\.get\(\s*["']([A-Z0-9_]+)["']'''),
    re.compile(r'''os\.environ\[\s*["']([A-Z0-9_]+)["']\s*\]'''),
]

variables = set()

for file in files:
    if not file.exists():
        continue

    text = file.read_text(encoding="utf-8", errors="ignore")

    for pattern in patterns:
        variables.update(pattern.findall(text))

for variable in sorted(variables):
    print(variable)
PY

printf '\n=== ENV EXAMPLE VARIABLES ===\n'
awk -F= '/^[A-Z0-9_]+=/ {print $1}' .env.example 2>/dev/null | sort -u

printf '\n=== AUTOMATED TESTS ===\n'
python -m pytest -q

printf '\n=== OLD TEST IDS IN CORE DOCUMENTS ===\n'
grep -RInE '(^|[^A-Za-z0-9_])T(0[1-9]|1[0-9]|2[0-5])([^A-Za-z0-9_]|$)' \
  README.md \
  docs/requirements.md \
  docs/design-diagrams.md \
  docs/testing-plan.md \
  docs/test-results-template.md \
  docs/traceability-matrix.md \
  docs/user-guide.md || true

printf '\n=== GIT STATUS ===\n'
git status --short

printf '\n=== SENSITIVE OR UNWANTED TRACKED FILES ===\n'
git ls-files \
  | grep -E '(^|/)\.env$|\.DS_Store$|(^|/)instance/|\.sqlite3?$|\.db$' \
  || true
