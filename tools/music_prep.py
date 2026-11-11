#!/usr/bin/env python3
"""Hintergrundmusik vorbereiten: Stille am Anfang abschneiden, Pfeif-Stellen leiser machen.

Nutzung: python3 tools/music_prep.py <eingabe.mp3> <ausgabe.wav> [dip_db]

- schneidet die leere Stelle am Anfang ab (alles unter -45 dB)
- erkennt Pfeifen (tonale Spitze 900-3500 Hz) in 0,25-s-Fenstern und senkt dort die Lautstärke
  um dip_db (Standard 6 dB), mit weichen Übergängen (~0,3 s)
Das Wiederholen (Loop) auf Videolänge macht build.py.
"""
import subprocess
import sys

import numpy as np

src, dst = sys.argv[1], sys.argv[2]
dip_db = float(sys.argv[3]) if len(sys.argv) > 3 else 6.0
SR = 44100

raw = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                     capture_output=True, check=True).stdout
x = np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).copy()
m = x.mean(1)

# 1) Stille am Anfang/Ende abschneiden
thr = 10 ** (-45 / 20)
loud = np.where(np.abs(m) > thr)[0]
a, b = loud[0], loud[-1] + 1
x, m = x[a:b], m[a:b]

# 2) Pfeifen erkennen
h = SR // 4
n = len(m) // h
fr = np.fft.rfftfreq(h, 1 / SR)
band = (fr > 900) & (fr < 3500)
low = (fr > 60) & (fr < 900)
tonal = np.zeros(n)
ratio = np.zeros(n)
win = np.hanning(h)
for i in range(n):
    X = np.abs(np.fft.rfft(m[i * h:(i + 1) * h] * win))
    bb = X[band]
    tonal[i] = bb.max() / (np.median(bb) + 1e-9)
    ratio[i] = (bb ** 2).sum() / ((X[low] ** 2).sum() + 1e-9)
mask = ((tonal > np.percentile(tonal, 75)) & (ratio > np.median(ratio))).astype(float)
# kleine Lücken schließen (Pfeif-Phrasen zusammenhängend behandeln)
k = np.ones(3)
mask = (np.convolve(mask, k, "same") > 0).astype(float)

# 3) Gain-Kurve glätten und anwenden
g_win = 1 - (1 - 10 ** (-dip_db / 20)) * mask
gain = np.repeat(g_win, h)
gain = np.concatenate([gain, np.full(len(m) - len(gain), gain[-1] if len(gain) else 1.0)])
sm = int(SR * 0.3)
kern = np.hanning(sm)
kern /= kern.sum()
gain = np.convolve(np.pad(gain, (sm, sm), mode="edge"), kern, "same")[sm:-sm]
x *= gain[:, None]

# kurze Fades an den Schnittkanten (Loop ohne Knacksen)
f = int(SR * 0.02)
x[:f] *= np.linspace(0, 1, f)[:, None]
x[-f:] *= np.linspace(1, 0, f)[:, None]

subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", dst],
               input=x.astype(np.float32).tobytes(), check=True)
print(f"{dst}: {len(x) / SR:.2f}s, Stille vorne {a / SR:.2f}s entfernt, Pfeifen {mask.mean() * 100:.0f}% der Zeit um {dip_db} dB leiser")
