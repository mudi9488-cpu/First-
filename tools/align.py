#!/usr/bin/env python3
"""Eine fertige Sprachaufnahme (eigene Stimme, ElevenLabs …) auf script.json ausrichten.

Usage: python3 tools/align.py <projekt-ordner> <aufnahme.mp3|wav>

Schreibt <projekt>/assets/voice.wav (−16 LUFS, 44.1 kHz) und <projekt>/assets/timings.json
im selben Format wie tools/tts.py – danach einfach `python3 build.py` laufen lassen.

Ohne Spracherkennung: Die Pausen der Aufnahme (ffmpeg silencedetect) werden per dynamischer
Programmierung den Zeilenenden zugeordnet, die im Skript auf ein Satzzeichen enden. Die Länge
jedes Abschnitts wird an der Buchstabenzahl des gesprochenen Texts gemessen. Zeilen ohne eigene
Pause werden innerhalb ihres Abschnitts nach Buchstaben aufgeteilt.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from tts import plain, word_times  # noqa: E402

SILENCE_DB = -38
SILENCE_MIN = 0.12
MISS_STRONG = 3.0   # Satzende (. ? ! :) ohne Pause
MISS_WEAK = 0.4     # Komma ohne Pause
GAP_UNUSED = 2.0    # Pause, die keinem Zeilenende zugeordnet ist (Atmer mitten im Satz)
GAP_ODD = 1.0       # Pause an einem Zeilenende ohne Satzzeichen


def silences(path):
    out = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path), "-af",
                          f"silencedetect=n={SILENCE_DB}dB:d={SILENCE_MIN}", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", out)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", out)]
    dur = float(re.search(r"Duration: (\d+):(\d+):([\d.]+)", out).group(3)) + \
        60 * float(re.search(r"Duration: (\d+):(\d+):", out).group(2))
    return list(zip(starts, ends + [dur] * (len(starts) - len(ends)))), dur


def weight(text):
    """Sprechdauer-Schätzung: Silben (Vokalgruppen) – genauer als Buchstaben."""
    t = text.lower()
    for a, b in (("ei", "a"), ("eu", "a"), ("au", "a"), ("ie", "i"), ("äu", "a")):
        t = t.replace(a, b)
    return len(re.findall(r"[aeiouäöüy]+", t)) + 0.5


def main(project: Path, audio: Path):
    script = json.loads((project / "script.json").read_text())
    lines = [(bi, l) for bi, b in enumerate(script["beats"]) for l in b["lines"]]
    say = [l.get("say", plain(l["show"])) for _, l in lines]
    wts = [weight(s) for s in say]
    kind = []  # Art des Zeilenendes
    for s in say:
        c = s.rstrip()[-1]
        kind.append("strong" if c in ".?!:" else "weak" if c in ",;" else "none")

    sil, dur = silences(audio)
    head = sil[0][1] if sil and sil[0][0] < 0.05 else 0.0
    tail = sil[-1][0] if sil and sil[-1][1] >= dur - 0.05 else dur
    gaps = [g for g in sil if g[0] > head + 0.05 and g[1] < tail - 0.05]
    speech = (tail - head) - sum(e - s for s, e in gaps)
    rate = speech / sum(wts)  # Sekunden pro Gewichtseinheit

    n, m = len(lines), len(gaps)
    # Anker: (Zeilenende-Index, Pausen-Index); Start-Anker (-1, -1), End-Anker (n-1, m)
    def t_end(j):   # Zeit, an der die Sprache vor Pause j endet
        return tail if j == m else gaps[j][0]

    def t_start(j):  # Zeit, an der es nach Pause j weitergeht
        return head if j == -1 else gaps[j][1]

    pre = [0]
    for x in wts:
        pre.append(pre[-1] + x)

    def seg_cost(i1, j1, i2, j2):
        actual = t_end(j2) - t_start(j1)
        # Pausen dazwischen, die nicht zugeordnet sind, gehören zur Sprechzeit nicht dazu
        inner = sum(gaps[k][1] - gaps[k][0] for k in range(j1 + 1, j2))
        exp = (pre[i2 + 1] - pre[i1 + 1]) * rate
        c = ((actual - inner) - exp) ** 2 / max(exp, 0.3)
        # kurze Pausen (Atmer, < 0,2 s) dürfen fast kostenlos übersprungen werden
        c += sum(GAP_UNUSED * min(1.0, max(0.0, (gaps[k][1] - gaps[k][0] - 0.1) / 0.3)) for k in range(j1 + 1, j2))
        for k in range(i1 + 1, i2):
            c += MISS_STRONG if kind[k] == "strong" else MISS_WEAK if kind[k] == "weak" else 0
        return c

    INF = float("inf")
    best = {(-1, -1): (0.0, None)}
    order = [(i, j) for i in range(n - 1) for j in range(m)] + [(n - 1, m)]
    for i2, j2 in order:
        cands = []
        for (i1, j1), (c1, _) in best.items():
            if i1 < i2 and j1 < j2:
                c = c1 + seg_cost(i1, j1, i2, j2)
                if i2 < n - 1 and kind[i2] == "none":
                    c += GAP_ODD
                cands.append((c, (i1, j1)))
        if cands:
            best[(i2, j2)] = min(cands)
    path, node = [], (n - 1, m)
    while node is not None:
        path.append(node)
        node = best[node][1]
    path.reverse()

    # Zeiten je Zeile: zwischen zwei Ankern nach Gewicht verteilen
    starts, ends = [0.0] * n, [0.0] * n
    for (i1, j1), (i2, j2) in zip(path, path[1:]):
        a, b = t_start(j1), t_end(j2)
        inner = [gaps[k] for k in range(j1 + 1, j2)]
        span_w = pre[i2 + 1] - pre[i1 + 1]
        speak = (b - a) - sum(e - s for s, e in inner)
        t = a
        for k in range(i1 + 1, i2 + 1):
            d = speak * wts[k] / span_w
            # nicht zugeordnete Pausen (Atmer) überspringen
            st = t
            for gs, ge in inner:
                if st >= gs - 1e-3 and st < ge:
                    st = ge
            starts[k] = st
            en = st + d
            for gs, ge in inner:
                if st < gs < en:
                    en += ge - gs
            ends[k] = en
            t = en

    beats_out, li = [], 0
    for b in script["beats"]:
        bo = {"id": b["id"], "label": b["label"], "lines": []}
        for l in b["lines"]:
            bo["lines"].append({"show": l["show"], "start": round(starts[li], 3), "end": round(ends[li], 3),
                                "words": word_times(plain(l["show"]), starts[li], ends[li])})
            li += 1
        bo["start"] = bo["lines"][0]["start"]
        bo["end"] = bo["lines"][-1]["end"]
        beats_out.append(bo)

    assets = project / "assets"
    assets.mkdir(exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(audio), "-af",
                    "loudnorm=I=-16:TP=-1.5:LRA=9,aresample=44100", "-ar", "44100", "-ac", "1",
                    str(assets / "voice.wav")], check=True)
    (assets / "timings.json").write_text(json.dumps(
        {"duration": round(dur, 3), "source": audio.name, "beats": beats_out}, ensure_ascii=False, indent=1))
    used = sum(1 for _, j in path if 0 <= j < m)
    print(f"voice.wav {dur:.2f}s · {used}/{m} Pausen zugeordnet")
    for bo in beats_out:
        print(f"  {bo['id']:8s} {bo['start']:6.2f} – {bo['end']:6.2f}")
        for l in bo["lines"]:
            print(f"      {l['start']:6.2f}–{l['end']:6.2f}  {plain(l['show'])}")


if __name__ == "__main__":
    main(Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve())
