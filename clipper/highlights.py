"""Find highlight moments in a stream recording from chat activity + audio loudness.

usage: python3 -I highlights.py <rec.ts> <rec_start_epoch_file> <chat.jsonl> <out.json> [n]
"""
import json, subprocess, sys
import numpy as np

rec, start_file, chat_file, out = sys.argv[1:5]
N = int(sys.argv[5]) if len(sys.argv) > 5 else 8
rec_start = float(open(start_file).read().strip())

# --- audio loudness per second -------------------------------------------
SR = 8000
raw = subprocess.run(
    ["ffmpeg", "-loglevel", "error", "-i", rec, "-vn", "-ac", "1", "-ar", str(SR),
     "-f", "s16le", "-"], capture_output=True).stdout
a = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
secs = len(a) // SR
rms = np.sqrt((a[: secs * SR].reshape(secs, SR) ** 2).mean(axis=1) + 1e-9)
db = 20 * np.log10(rms)

# --- chat activity per second --------------------------------------------
HYPE = ["lul", "kekw", "omegalul", "lmao", "lmfao", "icant", "😂", "🤣", "lol",
        "w ", "ww", "clip", "omg", "bro", "no way", "nah", "wtf", "holy", "pog",
        "!!!", "💀", "😭", "insane", "crazy"]
chat = np.zeros(secs)
hype = np.zeros(secs)
for line in open(chat_file):
    try:
        d = json.loads(line)
    except ValueError:
        continue
    s = int(d["t"] - rec_start)
    if 0 <= s < secs:
        chat[s] += 1
        m = d["m"].lower() + " "
        hype[s] += sum(1 for k in HYPE if k in m)

def smooth(x, w):
    return np.convolve(x, np.ones(w) / w, mode="same")

def z(x):
    return (x - np.median(x)) / (x.std() + 1e-9)

# Chat reacts ~3-12 s after the moment: look ahead.
ahead = 10
chat_s = smooth(chat + 2 * hype, 8)
chat_ahead = np.concatenate([chat_s[ahead:], np.zeros(ahead)])
audio_s = smooth(db, 3)
score = 1.0 * z(chat_ahead) + 0.8 * z(audio_s)

# --- pick top peaks, non-overlapping --------------------------------------
order = np.argsort(-score)
picked = []
for t in order:
    t = int(t)
    if t < 25 or t > secs - 10:
        continue
    if all(abs(t - p) > 60 for p in picked):
        picked.append(t)
    if len(picked) >= N:
        break

res = [{"peak": t, "start": max(0, t - 22), "end": min(secs, t + 10),
        "score": round(float(score[t]), 2),
        "chat_msgs_next_15s": int(chat[t:t + 15].sum()),
        "loud_db": round(float(audio_s[t]), 1)} for t in sorted(picked, key=lambda t: -score[t])]
json.dump(res, open(out, "w"), indent=1)
print(json.dumps(res, indent=1))
print("recording seconds:", secs, "chat msgs:", int(chat.sum()))
