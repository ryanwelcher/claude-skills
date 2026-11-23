"""Cut matching stretches from Ryan's Premiere render and from the raw OBS
file (through the voice chain), measure both, and write a blind A/B page.

  python3 compare.py --raw <raw.mp4> --reference <render.mp4> --offset 344.555 \
      --chain chain.json --out <dir> [--force] 300:150 [2400:150 ...]

Stretches are <render start s>:<seconds>. Raw time = render time + offset."""
import argparse
import html
import json
import os
import random
import re
import sys

import audio_chain
import measure

HERE = os.path.dirname(os.path.abspath(__file__))


def parse_stretch(text):
    """'300:150' -> (300.0, 150.0). Rejects mm:ss-looking input like '5:00',
    which would otherwise read as a 0 s stretch."""
    start, sep, length = text.partition(":")
    if not sep or re.fullmatch(r"0\d+(\.\d*)?", length):
        raise ValueError(f"stretch must be <start s>:<seconds>, got {text!r}")
    start, length = float(start), float(length)
    if start < 0 or length <= 0:
        raise ValueError(f"bad stretch {text!r}")
    return start, length


OWN_FILES = re.compile(r"(ref|ours)-\d+\.wav|report\.json|index\.html")
SILENT_DB = -90  # OBS writes digital silence on the mic during Starting Soon
MIN_LOUDNESS = -70  # a cut quieter than this is treated as silence


def mic_peak_db(raw, start_s, seconds):
    """Loudest sample (dB) on the mic track over the given raw stretch."""
    err = measure.run_ffmpeg(["-ss", str(start_s), "-t", str(seconds), "-i", raw,
                              "-map", f"0:a:{audio_chain.TRACKS['mic'] - 1}",
                              "-af", "volumedetect", "-f", "null", "-"])
    m = re.search(r"max_volume:\s+(-?[\d.]+|-inf)", err)
    return float(m.group(1)) if m else float("-inf")


def check_inputs(raw, reference, offset, stretches):
    """Raise ValueError for anything that would give a wrong or empty
    comparison, before any output is written."""
    tracks, raw_duration, fps = audio_chain.probe(raw)
    if tracks != 6:
        raise ValueError(f"expected 6 audio tracks, found {tracks}")
    shift = audio_chain.MIC_LAG_FRAMES / fps
    _, ref_duration, _ = audio_chain.probe(reference, video=False)
    for i, (start, seconds) in enumerate(stretches, 1):
        if start + seconds > ref_duration:
            raise ValueError(f"stretch {i} runs past the end of the reference ({ref_duration:.2f} s)")
        if start + offset + seconds + shift > raw_duration:
            raise ValueError(f"stretch {i} runs past the end of the raw recording ({raw_duration:.2f} s)")
        if mic_peak_db(raw, start + offset + shift, seconds) <= SILENT_DB:
            raise ValueError(f"stretch {i}: the mic is silent here (Starting Soon? check --offset)")


def prepare_out(out, force, sources):
    """Create `out`, or with force clear only the files compare writes.
    Refuse a folder that holds the source files."""
    real = os.path.realpath(out)
    if any(os.path.dirname(os.path.realpath(p)) == real for p in sources):
        raise ValueError(f"{out} holds the raw recording or the reference, pick another --out")
    if os.path.exists(out):
        if not force:
            raise ValueError(f"{out} exists, pass --force to overwrite")
        for name in os.listdir(out):
            if OWN_FILES.fullmatch(name):
                os.remove(os.path.join(out, name))
    else:
        os.makedirs(out)


def cut_reference(reference, start_s, seconds, out_wav):
    measure.run_ffmpeg(["-ss", str(start_s), "-t", str(seconds), "-i", reference, "-vn",
                        "-af", "aresample=48000", "-ac", "2", "-c:a", "pcm_s24le", "-y", out_wav])


def delta(ours, ref):
    d = {k: round(ours[k] - ref[k], 2) for k in ("I", "LRA", "TP")}
    d["bands"] = {hz: round(ours["bands"][hz] - ref["bands"][hz], 2) for hz in ours["bands"]}
    return d


def section(i, start, seconds, order):
    files = {"ours": f"ours-{i}.wav", "ref": f"ref-{i}.wav"}
    rows = "".join(
        f'<span class="label">{label}</span><audio controls preload="none" src="{files[who]}"></audio>'
        for label, who in zip("AB", order))
    ours_label = "AB"[order.index("ours")]
    mins, secs = divmod(int(start), 60)
    return (f"<section><h2>Stretch {i + 1}: {mins}:{secs:02d} into the render, {int(seconds)} s</h2>"
            f'<div class="pair">{rows}</div>'
            f'<p class="answer">{ours_label} is the ffmpeg chain.</p></section>'), ours_label


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--raw", required=True)
    ap.add_argument("--reference", required=True)
    ap.add_argument("--offset", type=float, required=True)
    ap.add_argument("--chain", default=os.path.join(HERE, "chain.json"))
    ap.add_argument("--out", required=True)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("stretches", nargs="+")
    a = ap.parse_args(argv)

    try:
        stretches = [parse_stretch(s) for s in a.stretches]
        chain = audio_chain.load_chain(a.chain)
        audio_chain.build_filtergraph(chain, {r: "x" for r in audio_chain.ROLES}, 0)
        if os.path.exists(a.out) and not a.force:
            raise ValueError(f"{a.out} exists, pass --force to overwrite")
        check_inputs(a.raw, a.reference, a.offset, stretches)
        prepare_out(a.out, a.force, [a.raw, a.reference])
    except KeyError as e:
        print(f"ERROR: chain settings missing key {e}", file=sys.stderr)
        return 1
    except (ValueError, RuntimeError, OSError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    report = {"raw": a.raw, "reference": a.reference, "offset": a.offset,
              "chain": chain, "stretches": [], "answer": []}
    sections = []
    for i, (start, seconds) in enumerate(stretches):
        ref_wav = os.path.join(a.out, f"ref-{i}.wav")
        ours_wav = os.path.join(a.out, f"ours-{i}.wav")
        try:
            cut_reference(a.reference, start, seconds, ref_wav)
            audio_chain.render_stretch(a.raw, start + a.offset, seconds, chain, ours_wav)
        except (ValueError, RuntimeError) as e:
            print(f"ERROR: stretch {i + 1}: {e}", file=sys.stderr)
            return 1
        ref_m, ours_m = measure.measure(ref_wav), measure.measure(ours_wav)
        if min(ref_m["I"], ours_m["I"]) <= MIN_LOUDNESS:
            print(f"ERROR: stretch {i + 1} is silent in the reference or ours", file=sys.stderr)
            return 1
        report["stretches"].append({"start": start, "seconds": seconds, "reference": ref_m,
                                    "ours": ours_m, "delta": delta(ours_m, ref_m)})
        order = random.sample(["ours", "ref"], 2)
        text, ours_label = section(i, start, seconds, order)
        sections.append(text)
        report["answer"].append(ours_label)
        print(f"stretch {i + 1}: ΔI {report['stretches'][-1]['delta']['I']:+} LU, "
              f"ΔLRA {report['stretches'][-1]['delta']['LRA']:+} LU")

    with open(os.path.join(HERE, "ab.html")) as f:
        page = f.read()
    page = page.replace("__TITLE__", html.escape(os.path.basename(a.reference)))
    page = page.replace("__SECTIONS__", "\n".join(sections))
    with open(os.path.join(a.out, "index.html"), "w") as f:
        f.write(page)
    with open(os.path.join(a.out, "report.json"), "w") as f:
        json.dump(report, f, indent=2)
    print(f"wrote {os.path.join(a.out, 'index.html')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
