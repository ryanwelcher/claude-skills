#!/usr/bin/env python3
"""Summarize stream-json runs into results/<ts>/summary.md.

peak_main_ctx  = largest prompt the main thread ever sent (input + cache_read + cache_creation)
final_main_ctx = same measure on the main thread's last assistant message (what /context would show)
fork_tokens    = input+output summed over messages that carry a parent_tool_use_id (subagent/fork)
total_in/out   = result.usage, covers every thread
coverage       = COVERAGE line printed by transcribe-file.sh (share of the recording not lost to Whisper loops or silence)
"""
import json, os, re, statistics, sys
from collections import defaultdict

root = sys.argv[1]
meta = {}
mp = os.path.join(root, "meta.txt")
if os.path.exists(mp):
    for l in open(mp):
        if "=" in l: k, v = l.strip().split("=", 1); meta[k] = v

def ctx(u): return (u.get("input_tokens", 0) + u.get("cache_read_input_tokens", 0) + u.get("cache_creation_input_tokens", 0))

def parse(path):
    main_ctx, fork_in, fork_out, res, words, coverage, fork_msgs = [], 0, 0, None, None, None, 0
    for line in open(path):
        if words is None:
            mw = re.search(r"WORDS: (\d+)", line)
            if mw: words = int(mw.group(1))
        if coverage is None:
            mc = re.search(r"COVERAGE: (\d+)%", line)
            if mc: coverage = int(mc.group(1))
        try: o = json.loads(line)
        except Exception: continue
        t = o.get("type")
        if t == "assistant":
            u = (o.get("message") or {}).get("usage") or {}
            if o.get("parent_tool_use_id"):
                fork_msgs += 1; fork_in += ctx(u); fork_out += u.get("output_tokens", 0)
            else:
                main_ctx.append(ctx(u))
        elif t == "result":
            res = o
    if res is None: return None
    u = res.get("usage", {})
    return dict(
        peak_main_ctx=max(main_ctx) if main_ctx else 0,
        final_main_ctx=main_ctx[-1] if main_ctx else 0,
        fork_tokens=fork_in + fork_out,
        total_in=u.get("input_tokens", 0) + u.get("cache_read_input_tokens", 0) + u.get("cache_creation_input_tokens", 0),
        total_out=u.get("output_tokens", 0),
        cache_create=u.get("cache_creation_input_tokens", 0),
        cost_usd=res.get("total_cost_usd", 0.0),
        turns=res.get("num_turns", 0),
        subagents=1 if fork_msgs else (res.get("subagent_stats") or {}).get("spawned", 0),
        duration_s=res.get("duration_ms", 0) / 1000,
        transcript_words=words,
        coverage=coverage,
        ok=(res.get("subtype") == "success" and not res.get("is_error")),
        models="+".join(sorted(m.replace("claude-", "").split("-2")[0] for m in (res.get("modelUsage") or {}))),
    )

runs = defaultdict(list)  # (scenario, version) -> [(rep, metrics)]
for scenario in sorted(os.listdir(root)):
    sdir = os.path.join(root, scenario)
    if not os.path.isdir(sdir) or scenario == "work": continue
    for version in sorted(os.listdir(sdir)):
        vdir = os.path.join(sdir, version)
        for f in sorted(os.listdir(vdir)):
            if f.endswith(".jsonl"):
                m = parse(os.path.join(vdir, f))
                if m: runs[(scenario, version)].append((f[:-6], m))

cols = ["peak_main_ctx", "final_main_ctx", "fork_tokens", "total_in", "total_out", "cache_create", "cost_usd", "turns", "subagents", "duration_s"]
def fmt(k, v):
    if v is None: return "-"
    if k == "cost_usd": return f"{v:.3f}"
    if k == "duration_s": return f"{v:.0f}"
    return f"{v:,.0f}" if isinstance(v, float) else f"{v:,}"

out = [f"# Summary — {os.path.basename(root)}", "", " · ".join(f"{k}={v}" for k, v in meta.items()), ""]
out += ["## Per run", "", "| scenario | version | run | ok | " + " | ".join(cols) + " | words | coverage | models |", "|" + "---|" * (len(cols) + 7)]
for (sc, ver), lst in sorted(runs.items()):
    for rep, m in lst:
        out.append(f"| {sc} | {ver} | {rep} | {'y' if m['ok'] else 'N'} | " + " | ".join(fmt(c, m[c]) for c in cols) + f" | {m['transcript_words'] or '-'} | {str(m['coverage']) + '%' if m['coverage'] is not None else '-'} | {m['models']} |")

out += ["", "## Mean (min–max) per version", "", "| scenario | version | n | " + " | ".join(cols) + " |", "|" + "---|" * (len(cols) + 3)]
means = {}
for (sc, ver), lst in sorted(runs.items()):
    ok = [m for _, m in lst if m["ok"]] or [m for _, m in lst]
    row = []
    for c in cols:
        vals = [m[c] for m in ok]
        mu = statistics.mean(vals); means[(sc, ver, c)] = mu
        row.append(f"{fmt(c, mu)} ({fmt(c, min(vals))}–{fmt(c, max(vals))})")
    out.append(f"| {sc} | {ver} | {len(ok)} | " + " | ".join(row) + " |")

out += ["", "## Delta vs legacy (mean)", "", "| scenario | version | metric | legacy | this | delta | % |", "|---|---|---|---|---|---|---|"]
for sc in sorted({s for s, _ in runs}):
    if (sc, "legacy") not in runs: continue
    for ver in sorted(v for s2, v in runs if s2 == sc and v != "legacy"):
        for c in ["peak_main_ctx", "final_main_ctx", "fork_tokens", "total_in", "total_out", "cost_usd", "turns", "duration_s"]:
            a, b = means[(sc, "legacy", c)], means[(sc, ver, c)]
            pct = f"{(b - a) / a * 100:+.0f}%" if a else "n/a"
            out.append(f"| {sc} | {ver} | {c} | {fmt(c, a)} | {fmt(c, b)} | {fmt(c, b - a)} | {pct} |")
out += ["", "_final_main_ctx is the number `/context` would show at the end of an interactive session. Negative delta = the new version is cheaper._", ""]
text = "\n".join(out)
open(os.path.join(root, "summary.md"), "w").write(text)
print(text)
