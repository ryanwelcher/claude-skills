# youtube-stream-description A/B eval

Headless before/after measurement of the legacy (in-context transcript) vs forked (`analyze-stream-recording`) version. The legacy skill was removed in devrel 1.20.0 after measurement; restore it from commit d835b26 to rerun the baseline. Built because `claude plugin eval` is still early access; the layout mirrors its `evals/<case>/prompt.md` shape so cases can move over later.

## Run

```bash
# 1. fixture: an 8-minute mid-stream clip (fixtures/ is gitignored)
ffmpeg -ss 00:05:00 -t 00:08:00 -i /path/to/recording.mp4 -c copy fixtures/clip.mp4

# 2. smoke, then real
bash run.sh --clip fixtures/clip.mp4 --reps 1
bash run.sh --clip fixtures/clip.mp4 --reps 3 --model opus
```

Both versions are invoked by explicit slash command with the intake answers pre-supplied, so triggering and questions are not variables. Runs are sequential (mlx_whisper shares the GPU). Plugin is loaded from the installed cache: make sure `~/.claude/plugins/installed_plugins.json` `gitCommitSha` for `devrel@ryan-claude-skills` matches `git rev-parse HEAD`, or run `/plugin marketplace update ryan-claude-skills` first.

## Output

`results/<timestamp>/summary.md` plus per-run `run-N.jsonl` (raw stream-json, gitignored) and `run-N.md` (the description the model produced; read these for quality parity).

| column | meaning |
|---|---|
| peak_main_ctx | largest prompt the main thread sent (input + cache read + cache creation) |
| final_main_ctx | same on the last main-thread turn; what `/context` shows at session end |
| fork_tokens | tokens spent inside the forked helper (subagent messages) |
| total_in / total_out | whole-session totals from the result event, all threads |
| cost_usd, turns, subagents, duration_s | from the result event |
| words | transcript word count printed by `transcribe-file.sh`, to scale expectations |
