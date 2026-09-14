#!/usr/bin/env bash
# Before/after eval for the STE + context-efficiency changes to the devrel plugin, headless.
# Arms are frozen plugin copies in snapshots/<arm> (baseline = last commit before STE, ste = STE added,
# optimized = STE + efficiency changes). Append "-sonnet" to an arm to pin ste-pass to Sonnet.
# Usage: bash run.sh --arms baseline,ste --cases all --reps 3 [--parallel 3] [--model claude-opus-5] [--out <name>]
#   --out reuses a results folder so arms run at different times land in one summary.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ARMS="baseline,ste"; CASES="all"; REPS=3; PAR=3; MODEL="claude-opus-5"; OUTNAME=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --arms) ARMS="$2"; shift 2;;
    --cases) CASES="$2"; shift 2;;
    --reps) REPS="$2"; shift 2;;
    --parallel) PAR="$2"; shift 2;;
    --model) MODEL="$2"; shift 2;;
    --out) OUTNAME="$2"; shift 2;;
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done
[[ "$CASES" == all ]] && CASES="$(cd "$HERE/cases" && ls *.md | sed 's/\.md$//' | paste -sd, -)"

OUT="$HERE/results/${OUTNAME:-$(date +%Y%m%d-%H%M%S)}"
mkdir -p "$OUT/plugins" "$OUT/work"
printf 'date=%s\narms=%s\ncases=%s\nreps=%s\nmodel=%s\nclaude=%s\n---\n' "$(date +%Y-%m-%dT%H:%M:%S)" "$ARMS" "$CASES" "$REPS" "$MODEL" "$(claude --version)" >> "$OUT/meta.txt"

# Resolve each arm to a plugin dir once, before any parallel job starts.
IFS=',' read -ra ALIST <<< "$ARMS"
for arm in "${ALIST[@]}"; do
  base="${arm%-sonnet}"; src="$HERE/snapshots/$base"
  [[ -d "$src/skills" ]] || { echo "no snapshot for arm $base at $src" >&2; exit 2; }
  pd="$src"
  if [[ "$arm" == *-sonnet ]]; then
    pd="$OUT/plugins/$arm"
    if [[ ! -d "$pd" ]]; then
      cp -R "$src" "$pd"
      sed -i '' 's/^name: ste-pass$/name: ste-pass\
model: sonnet/' "$pd/skills/ste-pass/SKILL.md"
      grep -q '^model: sonnet$' "$pd/skills/ste-pass/SKILL.md" || { echo "sonnet patch failed" >&2; exit 3; }
    fi
  fi
  echo "$pd" > "$OUT/plugins/$arm.path"
done

run_one() {
  local case="$1" arm="$2" rep="$3"
  local dir="$OUT/$case/$arm" work="$OUT/work/$case-$arm-$rep" cf="$HERE/cases/$case.md"
  mkdir -p "$dir" "$work" && cp -R "$HERE/fixtures" "$work/fixtures"
  local pd; pd="$(cat "$OUT/plugins/$arm.path")"
  local prompt; prompt="$(grep -v '^<!--' "$cf")"
  local jsonl="$dir/run-$rep.jsonl"
  echo "== [$case/$arm] rep $rep start $(date +%H:%M:%S)"
  ( cd "$work" && claude -p "$prompt" \
      --plugin-dir "$pd" --settings '{"enabledPlugins":{"devrel@ryan-claude-skills":false}}' \
      --strict-mcp-config --model "$MODEL" \
      --output-format stream-json --verbose --max-turns 40 \
      --permission-mode acceptEdits \
      --allowedTools Read Edit Write Glob Grep Skill "Bash(python3:*)" "Bash(bash:*)" "Bash(ls:*)" "Bash(cat:*)" \
      --disallowedTools AskUserQuestion WebFetch WebSearch Agent \
    ) > "$jsonl" 2> "$dir/run-$rep.err" || true
  python3 -c '
import json,sys
r=[json.loads(l) for l in open(sys.argv[1]) if l.startswith("{")]
res=[o for o in r if o.get("type")=="result"]
open(sys.argv[2],"w").write((res[-1].get("result") or "") if res else "NO RESULT\n")
' "$jsonl" "$dir/run-$rep.md"
  mkdir -p "$dir/run-$rep.out"
  # keep only what the run wrote: new root-level docs, plus fixtures it actually changed
  find "$work" -maxdepth 1 -name '*.md' -exec cp {} "$dir/run-$rep.out/" \; 2>/dev/null || true
  for f in "$work"/fixtures/*.md; do cmp -s "$f" "$HERE/fixtures/$(basename "$f")" || cp "$f" "$dir/run-$rep.out/"; done
  python3 "$HERE/check.py" "$case" "$work" "$jsonl" "$HERE/fixtures" > "$dir/run-$rep.check.json" 2>> "$dir/run-$rep.err" || echo '{}' > "$dir/run-$rep.check.json"
  echo "== [$case/$arm] rep $rep done  $(date +%H:%M:%S)"
}
export -f run_one; export OUT HERE MODEL

IFS=',' read -ra CLIST <<< "$CASES"
JOBS=()
for rep in $(seq 1 "$REPS"); do
  for case in "${CLIST[@]}"; do
    req="$(sed -n 's/^<!-- requires: \(.*\) -->$/\1/p' "$HERE/cases/$case.md")"
    for arm in "${ALIST[@]}"; do
      pd="$(cat "$OUT/plugins/$arm.path")"
      if [[ -n "$req" && ! -d "$pd/skills/$req" ]]; then continue; fi
      JOBS+=("$case $arm $rep")
    done
  done
done
echo "${#JOBS[@]} runs, parallel $PAR -> $OUT"
printf '%s\n' "${JOBS[@]}" | xargs -P "$PAR" -L 1 bash -c 'run_one "$0" "$1" "$2"'
python3 "$HERE/report.py" "$OUT" > /dev/null && echo "summary: $OUT/summary.md"
