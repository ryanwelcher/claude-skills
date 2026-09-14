#!/usr/bin/env python3
"""Static context cost per skill, per snapshot: what each skill's instructions tell it to load before writing.

Free and deterministic (no model calls). Tokens are estimates: bytes / 4.
Usage: static-cost.py baseline ste optimized > static.md
"""
import glob, os, re, statistics, sys

HERE = os.path.dirname(os.path.abspath(__file__))


def tok(path):
    return os.path.getsize(path) // 4 if os.path.exists(path) else 0


def skill_text(snap, skill):
    p = os.path.join(snap, "skills", skill, "SKILL.md")
    return open(p).read() if os.path.exists(p) else ""


def profile(snap):
    s = lambda rel: os.path.join(snap, "skills", rel)
    have = lambda rel: os.path.exists(s(rel))
    f = lambda *rels: sum(tok(s(r)) for r in rels)
    yt_txt = [tok(p) for p in glob.glob(s("youtube-script/references/voice-samples/*.txt"))]
    wnd_txt = [tok(p) for p in glob.glob(s("wnd-script/references/wnd-voice-samples/*.txt"))]
    card = "ste-pass/references/ste-card.md"
    rows = {}
    rows["write-article: tutorial"] = f("write-article/SKILL.md", "write-article/references/writing-style.md") + (f(card) if have(card) else 0)
    rows["write-article: P2 post"] = f("write-article/SKILL.md", "write-article/references/writing-style.md")
    rows["ste-pass"] = f("ste-pass/SKILL.md", card) if have("ste-pass/SKILL.md") else None
    rows["sounds-like-me: written draft"] = f("sounds-like-me/SKILL.md", "youtube-script/references/style-card.md") + (f(card) if have(card) else 0)
    rows["sounds-like-me: WND teleprompter"] = f("sounds-like-me/SKILL.md", "youtube-script/references/style-card.md", "wnd-script/references/wnd-series-card.md")
    yt = f("youtube-script/SKILL.md", "youtube-script/references/style-card.md", "youtube-script/references/format-template.md", "youtube-script/references/voice-samples/excerpts.md")
    rows["youtube-script: write"] = yt
    deep = re.search(r"full transcript", skill_text(snap, "youtube-script"), re.I) and not re.search(r"never read a full transcript", skill_text(snap, "youtube-script"), re.I)
    rows["youtube-script: write + deep soak (worst case)"] = yt + max(yt_txt) if deep and yt_txt else yt
    wnd = f("wnd-script/SKILL.md", "youtube-script/references/style-card.md", "wnd-script/references/wnd-series-card.md", "wnd-script/references/wnd-format.md")
    ex = "wnd-script/references/wnd-voice-samples/excerpts.md"
    rows["wnd-script (typical: one sample)"] = wnd + (f(ex) if have(ex) else round(statistics.mean(wnd_txt)))
    rows["wp-workshop-scaffold: create"] = f("wp-workshop-scaffold/SKILL.md")
    rows["wp-workshop-scaffold: audit"] = f("wp-workshop-scaffold/SKILL.md") + f("wp-workshop-scaffold/references/mode-audit.md")
    rows["wp-workshop-scaffold: reformat"] = f("wp-workshop-scaffold/SKILL.md") + f("wp-workshop-scaffold/references/mode-reformat.md", "wp-workshop-scaffold/references/mode-audit.md")
    desc = 0
    for p in glob.glob(os.path.join(snap, "skills", "*", "SKILL.md")):
        fm = open(p).read().split("---")[1]
        m = re.search(r"^description:(.*?)(?=^\S|\Z)", fm, re.S | re.M)
        desc += len(m.group(1)) // 4 if m else 0
    rows["all devrel skill descriptions (every session)"] = desc
    return rows


snaps = sys.argv[1:] or ["baseline", "ste", "optimized"]
data = {n: profile(os.path.join(HERE, "snapshots", n)) for n in snaps if os.path.isdir(os.path.join(HERE, "snapshots", n))}
names = list(data)
keys = list(next(iter(data.values())))
print("# Static context cost (estimated tokens loaded before writing)\n")
print("| skill / path | " + " | ".join(names) + (f" | {names[0]} → {names[-1]} |" if len(names) > 1 else " |"))
print("|---|" + "---|" * (len(names) + (1 if len(names) > 1 else 0)))
for k in keys:
    vals = [data[n][k] for n in names]
    cells = ["-" if v is None else f"{v:,}" for v in vals]
    delta = ""
    if len(names) > 1:
        a, b = vals[0], vals[-1]
        delta = " | new" if a is None and b is not None else (f" | {b - a:+,} ({(b - a) / a * 100:+.0f}%)" if a else " | -")
    print(f"| {k} | " + " | ".join(cells) + delta + " |")
