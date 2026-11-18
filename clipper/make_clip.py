"""Cut one TikTok clip (1080x1920) from a 1280x720 stream recording.

Facecam (top-left box) goes on top, center gameplay below, word-by-word subtitles.
usage: python3 -I make_clip.py <rec.ts> <start_s> <end_s> <out.mp4> <lang en|de> [hook text]
"""
import os, subprocess, sys, tempfile
import whisper

rec, start, end, out, lang = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4], sys.argv[5]
hook = sys.argv[6] if len(sys.argv) > 6 else ""
dur = end - start
tmp = tempfile.mkdtemp()
wav = os.path.join(tmp, "a.wav")
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(start), "-i", rec, "-t", str(dur),
                "-vn", "-ac", "1", "-ar", "16000", wav], check=True)

model = whisper.load_model("small")
r = model.transcribe(wav, language=lang, word_timestamps=True, fp16=False)
words = [w for s in r["segments"] for w in s.get("words", [])]

def ts(t):
    t = max(0.0, t)
    return "%d:%02d:%02d.%02d" % (t // 3600, t % 3600 // 60, int(t % 60), int(t * 100) % 100)

def esc(s):
    return s.replace("{", "(").replace("}", ")").replace("\\", "")

# ASS subtitles: 3-word groups, current word in yellow.
ass = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: 1080", "PlayResY: 1920", "",
       "[V4+ Styles]",
       "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
       "Style: Sub,DejaVu Sans,78,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,7,3,5,60,60,0,1",
       "Style: Hook,DejaVu Sans,84,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,8,4,8,50,50,90,1",
       "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
if hook:
    # Pop-in (scale 70% -> 100%) and fade out, line breaks via "|".
    pop = "{\\fad(0,300)\\fscx70\\fscy70\\t(0,180,\\fscx105\\fscy105)\\t(180,300,\\fscx100\\fscy100)}"
    ass.append("Dialogue: 1,%s,%s,Hook,,0,0,0,,%s%s" % (ts(0), ts(min(dur, 6.0)), pop, esc(hook).replace("|", "\\N")))
groups = [words[i:i + 3] for i in range(0, len(words), 3)]
for g in groups:
    for j, w in enumerate(g):
        w_end = g[j + 1]["start"] if j + 1 < len(g) else w["end"]
        parts = []
        for k, x in enumerate(g):
            word = esc(x["word"].strip().upper())
            parts.append("{\\c&H00E6FF&}%s{\\c&HFFFFFF&}" % word if k == j else word)
        ass.append("Dialogue: 0,%s,%s,Sub,,0,0,0,,{\\pos(540,1150)}%s" % (ts(w["start"]), ts(max(w_end, w["start"] + 0.08)), " ".join(parts)))
assf = os.path.join(tmp, "s.ass")
open(assf, "w").write("\n".join(ass) + "\n")

# Layout: facecam box (x:y:w:h in the 1280x720 source) on top, gameplay crop below.
cx, cy, cw, ch = (int(v) for v in (sys.argv[7] if len(sys.argv) > 7 else "0:0:330:186").split(":"))
cam_h = round(1080 * ch / cw / 2) * 2
game_h = 1920 - cam_h
game_w = round(720 * 1080 / game_h / 2) * 2
gx = int(sys.argv[8]) if len(sys.argv) > 8 else (1280 - game_w) // 2
fc = ("[0:v]split[a][b];"
      "[a]crop=%d:%d:%d:%d,scale=1080:%d[cam];"
      "[b]crop=%d:720:%d:0,scale=1080:%d[game];" % (cw, ch, cx, cy, cam_h, game_w, gx, game_h) +
      "[cam][game]vstack,format=yuv420p,ass=%s[v]" % assf)
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(start), "-i", rec, "-t", str(dur),
                "-filter_complex", fc, "-map", "[v]", "-map", "0:a",
                "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-r", "30",
                "-c:a", "aac", "-b:a", "160k", "-af", "loudnorm=I=-14:TP=-1.5",
                "-movflags", "+faststart", out], check=True)
print("TRANSCRIPT:", r["text"].strip())
print("wrote", out)
