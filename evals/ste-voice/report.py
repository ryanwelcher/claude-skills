#!/usr/bin/env python3
"""Summarize a results folder into summary.md: token usage from the stream-json trace plus check.py metrics.

peak_main_ctx = largest prompt the main thread sent (input + cache_read + cache_creation)
total_in/out  = result.usage across every thread
ref_tokens    = estimated tokens (bytes/4) of skill files the run actually read
"""
import json, os, statistics, sys
from collections import defaultdict

root = sys.argv[1]


def ctx(u):
    return u.get("input_tokens", 0) + u.get("cache_read_input_tokens", 0) + u.get("cache_creation_input_tokens", 0)


def parse(path):
    main, res = [], None
    for line in open(path):
        try:
            o = json.loads(line)
        except Exception:
            continue
        if o.get("type") == "assistant" and not o.get("parent_tool_use_id"):
            main.append(ctx((o.get("message") or {}).get("usage") or {}))
        elif o.get("type") == "result":
            res = o
    if res is None:
        return None
    u = res.get("usage", {})
    return dict(
        ok=res.get("subtype") == "success" and not res.get("is_error"),
        peak_main_ctx=max(main) if main else 0,
        total_in=ctx(u),
        total_out=u.get("output_tokens", 0),
        cost_usd=res.get("total_cost_usd", 0.0),
        turns=res.get("num_turns", 0),
        duration_s=res.get("duration_ms", 0) / 1000,
        models="+".join(sorted(m.replace("claude-", "").split("-2")[0] for m in (res.get("modelUsage") or {}))),
    )


runs = defaultdict(list)
for case in sorted(os.listdir(root)):
    cdir = os.path.join(root, case)
    if case in ("work", "plugins") or not os.path.isdir(cdir):
        continue
    for arm in sorted(os.listdir(cdir)):
        adir = os.path.join(cdir, arm)
        for f in sorted(os.listdir(adir)):
            if not f.endswith(".jsonl"):
                continue
            m = parse(os.path.join(adir, f))
            if not m:
                continue
            ck = os.path.join(adir, f[:-6] + ".check.json")
            try:
                m.update(json.load(open(ck)))
            except Exception:
                pass
            runs[(case, arm)].append((f[:-6], m))

TOK = ["peak_main_ctx", "total_in", "total_out", "cost_usd", "turns", "duration_s", "ref_tokens_read"]
SKIP = set(TOK) | {"ok", "models", "refs", "skills_invoked"}
ORDER = ["baseline", "ste", "optimized", "final"]


def arm_key(a):
    b = a.split("-")[0]
    return (ORDER.index(b) if b in ORDER else 99, a)


def fmt(k, v):
    if v is None:
        return "-"
    if isinstance(v, bool):
        return "yes" if v else "no"
    if k == "cost_usd":
        return f"{v:.3f}"
    if isinstance(v, float) and not v.is_integer():
        return f"{v:,.1f}"
    return f"{v:,.0f}"


def mean(vals):
    vals = [v for v in vals if v is not None and not isinstance(v, (list, dict, str))]
    if not vals:
        return None
    if all(isinstance(v, bool) for v in vals):
        return f"{sum(vals)}/{len(vals)}"
    return statistics.mean(vals)


meta = open(os.path.join(root, "meta.txt")).read() if os.path.exists(os.path.join(root, "meta.txt")) else ""
out = [f"# STE + efficiency eval — {os.path.basename(root)}", "", "```", meta.strip(), "```", ""]
for case in sorted({c for c, _ in runs}):
    arms = sorted((a for c, a in runs if c == case), key=arm_key)
    qual = sorted({k for a in arms for _, m in runs[(case, a)] for k in m if k not in SKIP})
    out += [f"## {case}", "", "Mean per arm (booleans as passes/runs).", ""]
    cols = TOK + qual
    out += ["| arm | n | ok | " + " | ".join(cols) + " | models |", "|" + "---|" * (len(cols) + 4)]
    base = None
    for a in arms:
        ms = [m for _, m in runs[(case, a)]]
        row = {c: mean([m.get(c) for m in ms]) for c in cols}
        base = base or row
        cells = [(v if isinstance(v, str) else fmt(c, v)) for c, v in row.items()]
        out.append(f"| {a} | {len(ms)} | {sum(m['ok'] for m in ms)} | " + " | ".join(cells) + f" | {ms[0]['models']} |")
    first = arms[0]
    if len(arms) > 1:
        out += ["", f"Delta vs `{first}`:", "", "| arm | peak_main_ctx | total_in | cost_usd | ref_tokens_read |", "|---|---|---|---|---|"]
        b = {c: mean([m.get(c) for _, m in runs[(case, first)]]) for c in TOK}
        for a in arms[1:]:
            t = {c: mean([m.get(c) for _, m in runs[(case, a)]]) for c in TOK}
            cells = []
            for c in ["peak_main_ctx", "total_in", "cost_usd", "ref_tokens_read"]:
                x, y = b[c], t[c]
                cells.append(f"{fmt(c, y - x)} ({(y - x) / x * 100:+.0f}%)" if x and y is not None else "-")
            out.append(f"| {a} | " + " | ".join(cells) + " |")
    out += ["", "<details><summary>Per run</summary>", "", "| arm | run | ok | " + " | ".join(TOK) + " | skills read |", "|" + "---|" * (len(TOK) + 4)]
    for a in arms:
        for rep, m in runs[(case, a)]:
            out.append(f"| {a} | {rep} | {'y' if m['ok'] else 'N'} | " + " | ".join(fmt(c, m.get(c)) for c in TOK) + f" | {', '.join(m.get('refs') or [])} |")
    out += ["", "</details>", ""]

text = "\n".join(out)
open(os.path.join(root, "summary.md"), "w").write(text)
print(text)
