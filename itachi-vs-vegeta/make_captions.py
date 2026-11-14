"""Builds word-by-word captions (ASS) from voiceover pause timings."""
import re

# (start, end) speech segments from silencedetect, with the text spoken in each
SEGMENTS = [
    (0.00, 1.37, "Itachi gegen Vegeta."),
    (1.86, 2.46, "Wer gewinnt?"),
    (3.24, 8.04, "Vegeta greift sofort an – ein Galick Gun, der die halbe Straße wegfegt."),
    (8.62, 9.85, "Doch Itachi steht still."),
    (10.36, 11.53, "Das Sharingan dreht sich."),
    (12.05, 13.21, "Vegeta merkt es nicht –"),
    (13.55, 14.85, "er ist längst im Genjutsu."),
    (15.29, 18.15, "Er schlägt zu, wieder und wieder … ins Leere."),
    (18.63, 20.08, "Itachi erscheint hinter ihm."),
    (20.56, 21.50, "Amaterasu."),
    (21.81, 22.80, "Schwarze Flammen."),
    (23.18, 24.20, "Doch Vegeta schreit –"),
    (24.56, 25.80, "Super Saiyajin!"),
    (26.19, 27.87, "Die Aura sprengt die Illusion."),
    (28.31, 29.75, "Ein letzter Final Flash –"),
    (30.23, 31.78, "Itachi hebt das Susanoo."),
    (32.35, 34.38, "Die Explosion verschluckt die ganze Stadt."),
    (34.93, 36.17, "Am Ende steht nur einer …"),
    (36.56, 39.09, "Vegeta. Rohe Kraft schlägt Illusion."),
    (39.67, 40.77, "Hättest du das gedacht?"),
    (41.33, 42.60, "Schreib's in die Kommentare."),
]

HIGHLIGHT = {"ITACHI", "VEGETA", "SHARINGAN", "GENJUTSU", "AMATERASU", "SAIYAJIN", "SUSANOO", "FINAL", "FLASH", "GALICK", "GUN"}


def ts(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


lines = []
for start, end, text in SEGMENTS:
    words = [w for w in text.split() if re.search(r"\w", w)]
    weights = [len(re.sub(r"\W", "", w)) + 2 for w in words]
    total = sum(weights)
    t = start
    for i, (w, wt) in enumerate(zip(words, weights)):
        d = (end - start) * wt / total
        word_end = t + d
        # hold the last word of a phrase through the pause (max 0.4s)
        show_end = word_end + (0.35 if i == len(words) - 1 else 0)
        clean = re.sub(r"[^\w'’ßäöüÄÖÜ]", "", w).upper()
        colour = r"{\c&H00D7FF&}" if clean in HIGHLIGHT else ""
        pop = r"{\fscx80\fscy80\t(0,80,\fscx100\fscy100)}"
        lines.append(f"Dialogue: 0,{ts(t)},{ts(show_end)},Cap,,0,0,0,,{pop}{colour}{clean}")
        t = word_end

header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Inter Black,120,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,9,4,2,40,40,520,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

with open("captions.ass", "w", encoding="utf-8") as f:
    f.write(header + "\n".join(lines) + "\n")
print(len(lines), "words")
