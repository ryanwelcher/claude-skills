#!/usr/bin/env bash
# A/B runner for youtube-stream-description variants, headless.
# The legacy skill was deleted in devrel 1.20.0; its baseline numbers live in the repo README.
# To rerun it, restore devrel/skills/youtube-stream-description-legacy from git history (d835b26).
# Usage: bash run.sh --clip <file> [--reps 3] [--model opus] [--versions new,repo,repo-sonnet,repo-haiku,new-haiku] [--scenario local-recording]
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
CLIP=""; REPS=3; MODEL="claude-opus-5"; VERSIONS="new,repo"; SCENARIO="local-recording"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --clip) CLIP="$2"; shift 2;;
    --reps) REPS="$2"; shift 2;;
    --model) MODEL="$2"; shift 2;;
    --versions) VERSIONS="$2"; shift 2;;
    --scenario) SCENARIO="$2"; shift 2;;
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done
[[ -f "$CLIP" ]] || { echo "--clip <file> is required and must exist" >&2; exit 2; }
CLIP="$(cd "$(dirname "$CLIP")" && pwd)/$(basename "$CLIP")"
PROMPT_FILE="$HERE/prompts/$SCENARIO.md"
[[ -f "$PROMPT_FILE" ]] || { echo "no prompt for scenario $SCENARIO" >&2; exit 2; }

TS="$(date +%Y%m%d-%H%M%S)"
OUT="$HERE/results/$TS"
mkdir -p "$OUT/work"
printf 'model=%s\nreps=%s\nclip=%s\nscenario=%s\nclaude=%s\n' "$MODEL" "$REPS" "$CLIP" "$SCENARIO" "$(claude --version)" > "$OUT/meta.txt"

skill_for() { case "$1" in legacy) echo youtube-stream-description-legacy;; new|new-haiku|repo|repo-sonnet|repo-haiku) echo youtube-stream-description;; *) echo "bad version $1" >&2; exit 2;; esac; }

# Every arm loads its own copy of the devrel plugin with --plugin-dir, and
# --setting-sources project,local hides the user-level skills in ~/.claude/skills
# (symlinks to this repo's working tree) so they cannot shadow that copy.
#   new, new-haiku           committed HEAD (git archive)
#   repo, repo-sonnet, ...   uncommitted working tree
# A -<model> suffix pins the forked helper to that model in a patched copy.
REPO_ROOT="$(cd "$HERE/../.." && pwd)"
plugin_for() {
  local v="$1" src m pd
  case "$v" in
    new|new-haiku)
      src="$OUT/plugins/head/devrel"
      if [[ ! -d "$src" ]]; then
        mkdir -p "$OUT/plugins/head"
        git -C "$REPO_ROOT" archive HEAD devrel | tar -x -C "$OUT/plugins/head"
      fi
      ;;
    *) src="$REPO_ROOT/devrel";;
  esac
  case "$v" in
    *-haiku|*-sonnet) m="${v##*-}";;
    *) echo "$src"; return;;
  esac
  pd="$OUT/plugins/$v"
  if [[ ! -d "$pd" ]]; then
    mkdir -p "$OUT/plugins" && cp -R "$src" "$pd"
    # pin the forked helper's frontmatter model
    sed -i '' "s/^model: .*/model: $m/" "$pd/skills/analyze-stream-recording/SKILL.md"
    grep -q "^model: $m\$" "$pd/skills/analyze-stream-recording/SKILL.md" || { echo "model patch failed" >&2; exit 3; }
  fi
  echo "$pd"
}

IFS=',' read -ra VLIST <<< "$VERSIONS"
for rep in $(seq 1 "$REPS"); do
  for v in "${VLIST[@]}"; do
    skill="$(skill_for "$v")"
    dir="$OUT/$SCENARIO/$v"; mkdir -p "$dir"
    jsonl="$dir/run-$rep.jsonl"; md="$dir/run-$rep.md"
    prompt="$(sed -e "s|{{SKILL}}|$skill|g" -e "s|{{CLIP}}|$CLIP|g" "$PROMPT_FILE")"
    work="$OUT/work/$v-$rep"; mkdir -p "$work"
    echo "== [$v] rep $rep  ($(date +%H:%M:%S))"
    start=$(date +%s)
    plugin="$(plugin_for "$v")"
    ( cd "$work" && claude -p "$prompt" \
        --plugin-dir "$plugin" --setting-sources project,local \
        --model "$MODEL" \
        --output-format stream-json --verbose \
        --max-turns 40 \
        --allowedTools "Bash(bash:*)" "Bash(yt-dlp:*)" "Bash(ffmpeg:*)" "Bash(mlx_whisper:*)" "Read" "Skill" "Agent" "Glob" \
        --disallowedTools "AskUserQuestion" "Edit" "Write" \
        > "$jsonl" ) || echo "   claude exited non-zero (see $jsonl)"
    echo "   wall: $(( $(date +%s) - start ))s"
    python3 - "$jsonl" "$md" <<'PY'
import json, sys
res = None
for line in open(sys.argv[1]):
    try: o = json.loads(line)
    except Exception: continue
    if o.get("type") == "result": res = o
if res is None:
    open(sys.argv[2], "w").write("(no result event)\n")
else:
    open(sys.argv[2], "w").write(res.get("result", "") or "")
    cost = res.get("total_cost_usd", 0)
    print(f"   cost ${cost:.3f}  turns {res.get('num_turns')}  subagents {res.get('subagent_stats',{}).get('spawned')}")
    if cost > 2.0:
        print("   COST GUARD: single run exceeded $2, aborting"); sys.exit(9)
PY
  done
done
echo "results in $OUT"
python3 "$HERE/summarize.py" "$OUT"
