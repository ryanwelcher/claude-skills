#!/usr/bin/env python3
"""Grade one eval run. Usage: check.py <case> <workdir> <run.jsonl> <fixtures_dir> -> JSON on stdout.

Every metric is deterministic (regex, hashes, diffs, the tool-call trace). Voice quality itself is not
graded here; read the run-N.out/ documents for that.
"""
import difflib, json, os, re, sys
from collections import Counter

case, work, jsonl, fx = sys.argv[1:5]


def read(p):
    try:
        return open(p, encoding="utf-8").read()
    except OSError:
        return None


FENCE = re.compile(r"^[ \t]*```[^\n]*\n(.*?)^[ \t]*```", re.S | re.M)
STEP = re.compile(r"^\s*\d+\.\s+(.+)$", re.M)
ADMON = re.compile(r"\*\*(WARNING|CAUTION|NOTE):\*\*", re.I)
SWAPS = re.compile(r"\b(choose|choosing|pick|display|displays|ensure|verify|allow|allows|update|modify|retrieve|utilize|leverage|numerous|in order to|prior to|via)\b", re.I)
BANS = re.compile(r"\b(dive in|delve|unleash|supercharge|game-changer|robust|seamless|without further ado|let's get started|buckle up|real talk|let's get real|near and dear|genuinely|honestly|this one's for you|you're in the right place|asterisk|voodoo magic)\b", re.I)


def fences(t):
    return [re.sub(r"(?m)^[ \t]+", "", m.group(1)) for m in FENCE.finditer(t or "")]


def prose(t):
    return FENCE.sub("", t or "")


def no_code(s):
    return re.sub(r"`[^`]*`", "X", s)


def step_metrics(t):
    steps = [no_code(s) for s in STEP.findall(prose(t))]
    n = len(steps)
    le20 = sum(1 for s in steps if len(s.split()) <= 20)
    p = prose(t)
    return dict(
        steps=n,
        steps_le20_pct=round(100 * le20 / n) if n else None,
        step_swap_words=sum(len(SWAPS.findall(s)) for s in steps),
        admonitions=len(ADMON.findall(p)),
        make_sure=len(re.findall(r"make sure", p, re.I)),
    )


def trace(path):
    reads, skills, bash = [], [], []
    for line in open(path):
        try:
            o = json.loads(line)
        except Exception:
            continue
        if o.get("type") != "assistant":
            continue
        for b in (o.get("message") or {}).get("content") or []:
            if b.get("type") != "tool_use":
                continue
            i = b.get("input") or {}
            if b["name"] == "Read":
                reads.append(i.get("file_path", ""))
            elif b["name"] == "Skill":
                skills.append(i.get("skill") or i.get("command") or "")
            elif b["name"] == "Bash":
                bash.append(i.get("command", ""))
    touched = reads + [w for c in bash for w in re.findall(r"[^\s;'\"|&()<>]*/skills/[^\s;'\"|&()<>]+", c)]
    refs = sorted({p for p in touched if "/skills/" in p and os.path.isfile(p)})
    return dict(
        skills_invoked=skills,
        ref_files_read=len(refs),
        ref_tokens_read=sum(os.path.getsize(p) // 4 for p in refs),
        full_transcript_read=any(re.search(r"voice-samples/[^/]+\.txt$", p) for p in refs),
        ste_card_read=any(p.endswith("ste-card.md") for p in refs),
        refs=[p.split("/skills/")[-1] for p in refs],
    )


def unchanged(name):
    return read(os.path.join(fx, name)) == read(os.path.join(work, "fixtures", name))


def code_identical(name):
    return Counter(fences(read(os.path.join(fx, name)))) == Counter(fences(read(os.path.join(work, "fixtures", name))))


def classify_lines(text):
    """Map line index -> 'action' | 'voice' | None (code, headings, blanks)."""
    out, in_fence = [], False
    for line in (text or "").splitlines():
        s = line.strip()
        if s.startswith("```"):
            in_fence = not in_fence
            out.append(None)
            continue
        if in_fence or not s or s.startswith("#"):
            out.append(None)
        elif re.match(r"\d+\.\s", s) or s.startswith("|") or ADMON.search(s) or re.match(r"[-*]\s", s) or s.startswith("**Requirements"):
            out.append("action")
        else:
            out.append("voice")
    return out


def zone_diff(name):
    a = (read(os.path.join(fx, name)) or "").splitlines()
    b = (read(os.path.join(work, "fixtures", name)) or "").splitlines()
    ca, cb = classify_lines("\n".join(a)), classify_lines("\n".join(b))
    counts = Counter()
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag == "equal":
            continue
        zones = [ca[i] for i in range(i1, i2)] if tag != "insert" else [cb[j] for j in range(j1, j2)]
        for z in zones:
            if z:
                counts[z] += 1
    return dict(action_lines_changed=counts["action"], voice_lines_changed=counts["voice"])


def result_text():
    last = ""
    for line in open(jsonl):
        try:
            o = json.loads(line)
        except Exception:
            continue
        if o.get("type") == "result":
            last = o.get("result") or ""
    return last


def doc(name):
    return read(os.path.join(work, name)) or ""


m = trace(jsonl)
out = result_text()

if case == "ste-audit":
    m.update(
        fixture_unchanged=unchanged("meme-generator.md"),
        findings=len(STEP.findall(out)),
        has_zone_map=bool(re.search(r"zone", out, re.I)),
        caught_choose=bool(re.search(r"\bchoose\b", out, re.I)),
        caught_ui_path=bool(re.search(r"Site Editor|Style section|Appearance", out)),
        caught_fetch_loop=bool(re.search(r"crash|infinite|A LOT of messages|many requests|loop", out, re.I)),
    )
elif case == "ste-apply":
    new = read(os.path.join(work, "fixtures", "meme-generator.md")) or ""
    m.update(step_metrics(new))
    m.update(
        fixture_changed=not unchanged("meme-generator.md"),
        code_identical=code_identical("meme-generator.md"),
        overview_voice_kept=bool(re.search(r"spatula|whipping up|spice up", new, re.I)),
    )
elif case == "voice-pass":
    m.update(zone_diff("meme-generator-hybrid.md"))
    m.update(code_identical=code_identical("meme-generator-hybrid.md"))
elif case in ("article-devblog", "article-p2"):
    d = doc("draft.md") or out
    m.update(step_metrics(d))
    # voice signal outside action zones: first-person/"let's" per 100 words of non-step prose
    voice_prose = "\n".join(l for l in prose(d).splitlines() if l.strip() and not STEP.match(l) and not l.lstrip().startswith(("#", "|", "-", "*")) and not ADMON.search(l))
    vw = len(voice_prose.split())
    m.update(
        draft_saved=bool(doc("draft.md")),
        words=len(prose(d).split()),
        voice_bans=len(BANS.findall(prose(d))),
        first_person_per_100w=round(100 * len(re.findall(r"\b(I|I'm|I've|I'd|my|let's)\b", voice_prose)) / vw, 1) if vw else None,
    )
elif case == "ste-quick":
    m.update(
        findings=len(STEP.findall(out)),
        lint_used=any(r.endswith("ste-lint.py") for r in m["refs"]),
        helper_used=any("ste-audit" in s for s in m["skills_invoked"]),
        caught_choose=bool(re.search(r"\bchoose\b", out, re.I)),
        caught_doubled_word=bool(re.search(r"completed completed", out, re.I)),
    )
elif case == "trigger":
    m.update(
        ste_pass_invoked=any("ste-pass" in s for s in m["skills_invoked"]),
        fixture_unchanged=unchanged("meme-generator.md"),
    )
elif case == "youtube-script":
    d = doc("script.md") or out
    m.update(
        script_saved=bool(doc("script.md")),
        words=len(d.split()),
        voice_bans=len(BANS.findall(d)),
        next_one_signoff=bool(re.search(r"see you in the next one", d, re.I)),
    )
elif case == "wnd-script":
    d = doc("teleprompter.md") or out
    m.update(
        teleprompter_saved=bool(doc("teleprompter.md")),
        words=len(d.split()),
        voice_bans=len(BANS.findall(d)),
        branded_greeting=bool(re.search(r"what's new for developers", d[:1500], re.I)),
        have_a_good_one=bool(re.search(r"have a good one", d, re.I)),
        samples_read=sum(1 for r in m["refs"] if "wnd-voice-samples/" in r and r.endswith(".txt")),
    )

print(json.dumps(m))
