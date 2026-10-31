#!/usr/bin/env python3
"""Deutsche Sprecherstimme + Wort-Timings aus einer script.json erzeugen.

Usage: python3 tools/tts.py <projekt-ordner>

Liest <projekt>/script.json, schreibt <projekt>/assets/voice.wav und
<projekt>/assets/timings.json. Jede Zeile wird einzeln synthetisiert, damit
Untertitel und Szenen exakt auf die Stimme getimt werden können.
"""
import json
import re
import subprocess
import sys
import urllib.request
import wave
from pathlib import Path

import numpy as np

VOICES_DIR = Path.home() / ".cache" / "piper-voices"
VOICE_URL = "https://github.com/rhasspy/piper/releases/download/v0.0.2/voice-{name}.tar.gz"

LEAD_IN = 0.15        # Stille vor dem ersten Wort
GAP_LINE = 0.06       # zwischen Zeilen ohne Satzzeichen
GAP_COMMA = 0.16      # nach Komma / Doppelpunkt
GAP_SENTENCE = 0.30   # nach . ? !
GAP_BEAT = 0.40       # zusätzlich zwischen zwei Beats
TAIL = 0.6            # Stille nach dem letzten Wort


def plain(show: str) -> str:
    """'{y:niemand} mehr' -> 'niemand mehr'"""
    return re.sub(r"\{\w:([^}]*)\}", r"\1", show)


def load_voice(name: str):
    from piper import PiperVoice
    # „thorsten-low“ (alt, deutsch) oder voller Name mit Sprache, z. B. „en-us-ryan-medium“
    full = name if name.count("-") >= 2 else f"de-{name}"
    d = VOICES_DIR / name
    model = d / f"{full}.onnx"
    if not model.exists():
        d.mkdir(parents=True, exist_ok=True)
        tgz = d / "voice.tar.gz"
        urllib.request.urlretrieve(VOICE_URL.format(name=full), tgz)
        subprocess.run(["tar", "xzf", str(tgz), "-C", str(d)], check=True)
    return PiperVoice.load(str(model))


def trim(audio: np.ndarray, sr: int, thresh: float = 0.02) -> np.ndarray:
    idx = np.where(np.abs(audio) > thresh)[0]
    if len(idx) == 0:
        return audio
    pad = int(0.02 * sr)
    return audio[max(0, idx[0] - pad): idx[-1] + pad]


def word_times(text: str, start: float, end: float):
    """Zeit einer Zeile nach Buchstaben auf die Wörter verteilen."""
    words = text.split()
    weights = [len(re.sub(r"[^\wäöüÄÖÜß]", "", w)) + 1.5 for w in words]
    total = sum(weights)
    out, t = [], start
    for w, wt in zip(words, weights):
        d = (end - start) * wt / total
        out.append({"text": w, "start": round(t, 3), "end": round(t + d, 3)})
        t += d
    return out


def main(project: Path):
    script = json.loads((project / "script.json").read_text())
    from piper import SynthesisConfig
    voice = load_voice(script.get("voice", "thorsten-low"))
    sr = voice.config.sample_rate
    cfg = SynthesisConfig(length_scale=script.get("length_scale", 0.9))

    pieces = [np.zeros(int(LEAD_IN * sr), dtype=np.float32)]
    t = LEAD_IN
    beats_out = []
    for bi, beat in enumerate(script["beats"]):
        if bi > 0:
            pieces.append(np.zeros(int(GAP_BEAT * sr), dtype=np.float32))
            t += GAP_BEAT
        beat_out = {"id": beat["id"], "label": beat["label"], "start": round(t, 3), "lines": []}
        for line in beat["lines"]:
            say = line.get("say", plain(line["show"]))
            chunks = list(voice.synthesize(say, syn_config=cfg))
            audio = np.concatenate([c.audio_float_array for c in chunks]).astype(np.float32)
            audio = trim(audio, sr)
            dur = len(audio) / sr
            shown = plain(line["show"])
            beat_out["lines"].append({
                "show": line["show"],
                "start": round(t, 3),
                "end": round(t + dur, 3),
                "words": word_times(shown, t, t + dur),
            })
            pieces.append(audio)
            t += dur
            last = say.rstrip()[-1]
            gap = GAP_SENTENCE if last in ".?!" else GAP_COMMA if last in ",:;" else GAP_LINE
            pieces.append(np.zeros(int(gap * sr), dtype=np.float32))
            t += gap
        beat_out["end"] = round(t, 3)
        beats_out.append(beat_out)
    pieces.append(np.zeros(int(TAIL * sr), dtype=np.float32))
    t += TAIL

    assets = project / "assets"
    assets.mkdir(exist_ok=True)
    raw = assets / "voice-raw.wav"
    pcm = (np.clip(np.concatenate(pieces), -1, 1) * 32767).astype(np.int16)
    with wave.open(str(raw), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(pcm.tobytes())
    # Klang: Rumpeln weg, etwas Präsenz, Kompression, -16 LUFS, 44.1 kHz
    subprocess.run([
        "ffmpeg", "-y", "-v", "error", "-i", str(raw), "-af",
        "highpass=f=90,equalizer=f=3000:t=q:w=1:g=3,"
        "acompressor=threshold=-20dB:ratio=3:attack=5:release=80,"
        "loudnorm=I=-16:TP=-1.5:LRA=7,aresample=44100",
        "-ar", "44100", str(assets / "voice.wav"),
    ], check=True)
    raw.unlink()
    (assets / "timings.json").write_text(json.dumps(
        {"duration": round(t, 3), "beats": beats_out}, ensure_ascii=False, indent=1))
    print(f"voice.wav {t:.2f}s")
    for b in beats_out:
        print(f"  {b['id']:8s} {b['start']:6.2f} – {b['end']:6.2f}")


if __name__ == "__main__":
    main(Path(sys.argv[1]).resolve())
