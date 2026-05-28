#!/usr/bin/env bash
set -euo pipefail

# Syntax-check every PlantUML source in the repo root.
# Fails with non-zero exit code if any file has a syntax error.

cd "$(dirname "$0")/.."

shopt -s nullglob
files=( *.puml )
if (( ${#files[@]} == 0 )); then
  echo "No .puml files found."
  exit 1
fi

echo "Checking ${#files[@]} diagram source(s):"
printf '  %s\n' "${files[@]}"
echo

plantuml -failfast2 -checkonly "${files[@]}"
echo "All diagrams pass syntax check."
