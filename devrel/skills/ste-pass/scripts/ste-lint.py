#!/usr/bin/env python3
"""Mechanical STE checks for action zones. Prints only violations, so the model doesn't count words by hand.

Usage: ste-lint.py <file.md> [--lines 12-40,88-120] [--strict]
  default  checks action-zone lines: numbered steps, bullets, WARNING/CAUTION/NOTE blocks, table rows
  --lines  also checks prose inside these line ranges (action zones written as prose, from the zone map)
  --strict also checks all prose paragraphs (voice zones)
Code fences, inline code, and headings are always skipped. Judgment calls (zones, vague UI paths,
prose that belongs in a table) are left to the model.
"""
import re
import sys

MAX_HITS = 60
SWAPS = {
    "choose": "select", "pick": "select", "display": "show", "render": "show", "ensure": "make sure",
    "verify": "make sure", "allow": "let", "allows": "lets", "update": "change", "modify": "change",
    "retrieve": "get", "utilize": "use", "leverage": "use", "generate": "make", "execute": "run",
    "trigger": "start", "numerous": "many", "a lot of": "many", "in order to": "to", "prior to": "before",
    "via": "through / with", "e.g.": "for example", "i.e.": "that is",
}
PHRASAL = ["set up", "spin up", "find out", "go back", "check out", "fill in", "look into", "hook up", "carry out"]
HEDGES = ["just", "simply", "feel free", "you might want", "you may want", "you should", "let's", "basically"]
SWAP_RE = re.compile(r"(?<![\w-])(" + "|".join(re.escape(w) for w in sorted(SWAPS, key=len, reverse=True)) + r")(?![\w-])", re.I)
PHRASAL_RE = re.compile(r"\b(" + "|".join(PHRASAL) + r")\b", re.I)
HEDGE_RE = re.compile(r"\b(" + "|".join(re.escape(h) for h in HEDGES) + r")\b", re.I)
EMOJI_RE = re.compile("[\U0001F300-\U0001FAFF☀-➿]")
ADMON_RE = re.compile(r"\*\*(WARNING|CAUTION|NOTE):\*\*", re.I)
STEP_RE = re.compile(r"^\s*\d+\.\s+")
UI_RE = re.compile(r"\*\*[^*]+\*\*")  # bold = UI label, exempt from word swaps


def kind(s):
    if STEP_RE.match(s):
        return "step"
    if ADMON_RE.search(s):
        return "admonition"
    if s.startswith("|") and not re.match(r"^\|[\s:|-]+\|$", s):
        return "table"
    if re.match(r"[-*]\s", s):
        return "bullet"
    return "prose"


def main():
    argv = sys.argv[1:]
    ranges = []
    if "--lines" in argv:
        i = argv.index("--lines")
        for part in argv[i + 1].split(","):
            a, _, b = part.partition("-")
            ranges.append((int(a), int(b or a)))
        del argv[i:i + 2]
    args = [a for a in argv if not a.startswith("--")]
    strict = "--strict" in argv
    in_ranges = lambda n: any(a <= n <= b for a, b in ranges)
    if not args:
        sys.exit(__doc__)
    lines = open(args[0], encoding="utf-8").read().splitlines()

    items, in_fence = [], False  # (lineno, kind, text)
    for n, raw in enumerate(lines, 1):
        s = raw.strip()
        if s.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or not s or s.startswith("#"):
            continue
        items.append((n, kind(s), s))

    hits = []
    def hit(n, rule, text):
        hits.append(f"L{n} [{rule}] {text[:90]}")

    for idx, (n, k, s) in enumerate(items):
        if k == "prose" and not (strict or in_ranges(n)):
            continue
        plain = re.sub(r"`[^`]*`", "X", s)
        checkable = UI_RE.sub("X", plain)
        body = STEP_RE.sub("", plain)
        limit = 20 if k in ("step", "admonition") else 25
        for sentence in re.split(r"(?<=[.!?])\s+", body):
            wc = len(sentence.split())
            if wc > limit:
                hit(n, f"R1 {wc} words > {limit}", sentence)
        if k == "step" and len(re.findall(r"[.!?](\s|$)", body.strip())) > 1:
            hit(n, "R2 more than one sentence in a step", s)
        for m in SWAP_RE.finditer(checkable):
            hit(n, f"swap '{m.group(1)}' -> '{SWAPS[m.group(1).lower()]}'", s)
        for m in PHRASAL_RE.finditer(checkable):
            hit(n, f"R9 phrasal verb '{m.group(1)}'", s)
        for m in HEDGE_RE.finditer(checkable):
            hit(n, f"R13 hedge '{m.group(1)}'", s)
        if EMOJI_RE.search(s):
            hit(n, "R8 emoji", s)
        if k == "admonition" and re.match(r"\*\*(WARNING|CAUTION):", s, re.I):
            prev = items[idx - 1][1] if idx else None
            nxt = items[idx + 1][1] if idx + 1 < len(items) else None
            if prev == "step" and nxt != "step":
                hit(n, "R6 warning/caution may come after its step", s)

    # R7: each run of numbered steps should end with a check
    run = []
    for n, k, s in items + [(0, "end", "")]:
        if k == "step":
            run.append((n, s))
            continue
        if k in ("admonition",) and run:
            continue
        if len(run) >= 2 and not re.search(r"make sure", run[-1][1], re.I):
            hit(run[-1][0], "R7 procedure does not end with a 'make sure' check", run[-1][1])
        run = []

    steps = sum(1 for _, k, _ in items if k == "step")
    scope = "strict" if strict else ("marked lines + ranges " + ",".join(f"{a}-{b}" for a, b in ranges) if ranges else "marked action lines only")
    print(f"ste-lint: {len(hits)} hits in {args[0]} ({steps} numbered steps; {scope})")
    for h in hits[:MAX_HITS]:
        print(h)
    if len(hits) > MAX_HITS:
        print(f"... {len(hits) - MAX_HITS} more hits not shown (fix these, then re-run)")


if __name__ == "__main__":
    main()
