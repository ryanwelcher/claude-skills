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

# Variant arms load a patched copy of the installed devrel plugin instead of the installed one.
INSTALLED_DEVREL="$(python3 -c "import json,os;print(json.load(open(os.path.expanduser('~/.claude/plugins/installed_plugins.json')))['plugins']['devrel@ryan-claude-skills'][0]['installPath'])")"
extra_args_for() {
  case "$1" in
    new-haiku)
      local pd="$OUT/plugins/new-haiku"
      if [[ ! -d "$pd" ]]; then
        mkdir -p "$OUT/plugins" && cp -R "$INSTALLED_DEVREL" "$pd"
        # add model: haiku to the forked helper's frontmatter (after the context: fork line)
        sed -i '' 's/^context: fork$/context: fork\
model: haiku/' "$pd/skills/analyze-stream-recording/SKILL.md"
        grep -q '^model: haiku$' "$pd/skills/analyze-stream-recording/SKILL.md" || { echo "haiku patch failed" >&2; exit 3; }
      fi
      printf '%s\n' --plugin-dir "$pd" --settings '{"enabledPlugins":{"devrel@ryan-claude-skills":false}}'
      ;;
    repo-sonnet|repo-haiku)
      # fixed working-tree plugin with the forked helper pinned to another model
      local m="${1#repo-}" pd="$OUT/plugins/$1"
      if [[ ! -d "$pd" ]]; then
        mkdir -p "$OUT/plugins" && cp -R "$(cd "$HERE/../../devrel" && pwd)" "$pd"
        sed -i '' "s/^context: fork\$/context: fork\\
model: $m/" "$pd/skills/analyze-stream-recording/SKILL.md"
        grep -q "^model: $m\$" "$pd/skills/analyze-stream-recording/SKILL.md" || { echo "model patch failed" >&2; exit 3; }
      fi
      printf '%s\n' --plugin-dir "$pd" --settings '{"enabledPlugins":{"devrel@ryan-claude-skills":false}}'
      ;;
    repo)
      # uncommitted working-tree version of the devrel plugin, instead of the installed cache
      printf '%s\n' --plugin-dir "$(cd "$HERE/../../devrel" && pwd)" --settings '{"enabledPlugins":{"devrel@ryan-claude-skills":false}}'
      ;;
  esac
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
    extra=(); while IFS= read -r a; do [[ -n "$a" ]] && extra+=("$a"); done < <(extra_args_for "$v")
    ( cd "$work" && claude -p "$prompt" ${extra[@]+"${extra[@]}"} \
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
