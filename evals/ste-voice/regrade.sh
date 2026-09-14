#!/usr/bin/env bash
# Re-run check.py over every finished run in a results folder (after a grader fix), then rebuild summary.md.
# Needs the gitignored work/ dirs from the original runs.
# Usage: bash regrade.sh [results-name]   (default: main)
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
OUT="$HERE/results/${1:-main}"
n=0
for jsonl in "$OUT"/*/*/run-*.jsonl; do
  rel="${jsonl#"$OUT"/}"; case="${rel%%/*}"; rest="${rel#*/}"; arm="${rest%%/*}"
  rep="$(basename "$jsonl" .jsonl)"; rep="${rep#run-}"
  work="$OUT/work/$case-$arm-$rep"
  [[ -d "$work" ]] || { echo "skip $rel (no work dir)"; continue; }
  python3 "$HERE/check.py" "$case" "$work" "$jsonl" "$HERE/fixtures" > "${jsonl%.jsonl}.check.json"
  n=$((n + 1))
done
python3 "$HERE/report.py" "$OUT" > /dev/null
echo "regraded $n runs -> $OUT/summary.md"
