#!/usr/bin/env python3
"""Wort-Zeitstempel (ElevenLabs Scribe words.json) auf script.json legen.

Usage: python3 tools/words_align.py <projekt> <aufnahme.mp3> <words.json>
Schreibt <projekt>/assets/voice.wav (−16 LUFS) und assets/timings.json (Format wie tts.py),
aber mit echten Wortzeiten statt geschätzter. Tags wie [whispers] werden übersprungen.
"""
import json, re, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from tts import plain  # noqa: E402

proj, audio, wj = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
script = json.loads((proj / "script.json").read_text())
raw = json.loads(wj.read_text())
W = raw["words"] if isinstance(raw, dict) else raw
W = [w for w in W if w.get("type", "word") == "word" and not re.fullmatch(r"\[.*\]", w["text"].strip())]
norm = lambda s: re.sub(r"[^\w]", "", s.lower())
k = 0
beats = []
for b in script["beats"]:
    bo = {"id": b["id"], "label": b.get("label", ""), "lines": []}
    for l in b["lines"]:
        ws = []
        for t in plain(l["show"]).split():
            w = W[k]
            if norm(w["text"]) != norm(t):
                print(f"WARN mismatch #{k}: script '{t}' vs audio '{w['text']}'")
            ws.append({"text": t, "start": round(w["start"], 3), "end": round(w["end"], 3)})
            k += 1
        bo["lines"].append({"show": l["show"], "start": ws[0]["start"], "end": ws[-1]["end"], "words": ws})
    bo["start"], bo["end"] = bo["lines"][0]["start"], bo["lines"][-1]["end"]
    beats.append(bo)
assert k == len(W), (k, len(W))
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(audio)], capture_output=True, text=True).stdout)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(audio), "-af", "loudnorm=I=-16:TP=-1.5:LRA=7,aresample=44100", "-ar", "44100",
                str(proj / "assets" / "voice.wav")], check=True)
(proj / "assets" / "timings.json").write_text(json.dumps({"duration": round(dur, 3), "beats": beats}, ensure_ascii=False, indent=1))
print(f"voice.wav {dur:.2f}s, {k} Wörter")
