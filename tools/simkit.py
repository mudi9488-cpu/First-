"""Baukasten für Simulations-Videos im Stil der Referenzen (HyperFrames, 1080x1920).

Ein Video-Projekt hat eine build.py, die dieses Modul importiert, die Szenen als
HTML-Strings beschreibt und `write_project(...)` aufruft. Erzeugt werden:
index.html, compositions/<szene>.html, compositions/hud.html, compositions/captions.html.
Alle Zeiten kommen aus assets/timings.json (tools/tts.py).
"""
import json
import random
import re
from pathlib import Path

W, H = 1080, 1920

# Farbrollen aus den Referenzen (siehe .claude/skills/tiktok-sim-video/references/style.md)
C = {
    "bg": "#0E1524",
    "bg2": "#18223A",
    "card": "#121A2B",
    "line": "#2A3652",
    "ink": "#FFFFFF",
    "mute": "#8A94A6",
    "dim": "#5B6478",
    "gold": "#F5B83D",
    "red": "#FF4D5E",
    "teal": "#3CC6BE",
    "coral": "#F2604F",
    "green": "#3DDC84",
    "blue": "#4F7CFF",
}
HL = {"y": C["gold"], "r": C["red"], "g": C["green"], "b": C["blue"], "t": C["teal"]}

FONT_DISPLAY = "Inter"
FONT_MONO = "JetBrains Mono"

BASE_CSS = """
#root { position:absolute; inset:0; overflow:hidden; font-family:'Inter',sans-serif; color:#fff; }
.bg { position:absolute; inset:0; background:radial-gradient(ellipse 90% 60% at 50% 42%, %BG2% 0%, %BG% 70%); }
.mono { font-family:'JetBrains Mono',monospace; letter-spacing:0.12em; text-transform:uppercase; }
.hudcard { position:absolute; left:50%; width:620px; margin-left:-310px; top:300px; padding:22px 32px 24px;
  background:%CARD%; border:3px solid %LINE%; border-radius:22px; text-align:left; }
.hudcard .lab { font-family:'JetBrains Mono',monospace; font-size:28px; letter-spacing:0.14em; color:%MUTE%; font-weight:700; text-transform:uppercase; }
.hudcard .val { font-family:'Inter',sans-serif; font-weight:900; font-size:84px; line-height:1.05;
  font-variant-numeric:tabular-nums; margin-top:6px; }
.hudcard .unit { font-size:40px; color:%MUTE%; font-weight:700; margin-left:10px; }
.bar { height:16px; border-radius:8px; background:#232D45; margin-top:14px; overflow:hidden; }
.bar > i { display:block; height:100%; width:100%; border-radius:8px; transform-origin:left center; }
.pill { position:absolute; font-family:'Inter',sans-serif; font-weight:900; font-size:34px; padding:10px 26px;
  border-radius:999px; text-transform:uppercase; letter-spacing:0.02em; white-space:nowrap; }
"""
for k, v in C.items():
    BASE_CSS = BASE_CSS.replace("%" + k.upper() + "%", v)


def rng(seed):
    return random.Random(seed)


def plain(show):
    return re.sub(r"\{\w:([^}]*)\}", r"\1", show)


def audio_len(path):
    import subprocess
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True, check=True).stdout
    return float(out)


def load_timings(project: Path):
    return json.loads((project / "assets" / "timings.json").read_text())


def fmt(x):
    return f"{x:.3f}".rstrip("0").rstrip(".")


# ---------------------------------------------------------------- Szenen

def scene_html(sid, css, body, js):
    """Eine Szene als Sub-Composition. `js` bekommt eine Timeline `tl`."""
    return f"""<template>
  <style>
{BASE_CSS}
{css}
  </style>
  <div id="root" data-composition-id="{sid}" data-width="{W}" data-height="{H}">
    <div class="bg"></div>
{body}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{js}
    window.__timelines["{sid}"] = tl;
  </script>
</template>
"""


def hud_card(cid, label, value, unit="", color=C["ink"], bar=None, top=300, width=560, size=72):
    """Datenkarte oben (wie 'WASSER 31 mL' / 'FRAUEN AUF DER ERDE')."""
    b = f'<div class="bar"><i id="{cid}-bar" style="background:{bar}"></i></div>' if bar else ""
    u = f'<span class="unit">{unit}</span>' if unit else ""
    return (f'<div class="hudcard" id="{cid}" style="top:{top}px;width:{width}px;margin-left:{-width // 2}px">'
            f'<div class="lab">{label}</div>'
            f'<div class="val" style="color:{color};font-size:{size}px"><span id="{cid}-num">{value}</span>{u}</div>{b}</div>')


def js_count(target, frm, to, at, dur, decimals=0, sep=".", dec=",", ease="power2.inOut"):
    """Zähler, der im Takt der Timeline läuft (deterministisch)."""
    return (f"""    (function(){{ const o={{v:{frm}}}; const el=document.getElementById("{target}");
      const f=(v)=>{{ let s=v.toFixed({decimals}); let [a,b]=s.split("."); a=a.replace(/\\B(?=(\\d{{3}})+(?!\\d))/g,"{sep}"); return b?a+"{dec}"+b:a; }};
      tl.fromTo(o,{{v:{frm}}},{{v:{to},duration:{dur},ease:"{ease}",onUpdate:()=>{{el.textContent=f(o.v);}}}},{at}); }})();
""")


# ---------------------------------------------------------------- HUD (Kapitel-Label + Checkliste)

def hud_html(timings, checklist, total, check_end=None):
    """Kapitel-Label oben Mitte (wechselt pro Beat) und Checkliste oben links.
    checklist: [(abs_time, text, color)]; check_end: Zeit, ab der die Checkliste weg ist."""
    check_end = check_end or total
    beats = timings["beats"]
    labels, js = [], []
    for i, b in enumerate(beats):
        start = 0 if i == 0 else b["start"]
        end = beats[i + 1]["start"] if i + 1 < len(beats) else total
        lid = f"hud-l{i}"
        labels.append(f'<div id="{lid}" class="clip lab" data-start="{fmt(start)}" data-duration="{fmt(end - start)}" '
                      f'data-track-index="1"><span>{b["label"]}</span></div>')
        if i > 0:
            js.append(f'    tl.fromTo("#{lid} span",{{opacity:0,filter:"blur(8px)"}},{{opacity:1,filter:"blur(0px)",duration:0.18,ease:"power4.out"}},{fmt(start)});')
    items = []
    for j, (t, text, col) in enumerate(checklist):
        iid = f"hud-c{j}"
        items.append(f'<div id="{iid}" class="clip chk" data-start="{fmt(t)}" data-duration="{fmt(check_end - t)}" '
                     f'data-track-index="2" style="top:{288 + j * 58}px"><span style="color:{col};border-color:{col}">{text}</span></div>')
        js.append(f'    tl.fromTo("#{iid} span",{{x:-30,opacity:0}},{{x:0,opacity:1,duration:0.35,ease:"expo.out"}},{fmt(t)});')
    css = f"""
#root {{ position:absolute; inset:0; }}
.lab {{ position:absolute; top:176px; left:0; width:100%; text-align:center; }}
.lab span {{ display:inline-block; font-family:'JetBrains Mono',monospace; font-weight:700; font-size:30px; letter-spacing:0.16em;
  color:{C['gold']}; padding:10px 28px; border:3px solid {C['gold']}; border-radius:12px; background:rgba(14,21,36,0.85); }}
.chk {{ position:absolute; left:48px; }}
.chk span {{ display:inline-block; font-family:'JetBrains Mono',monospace; font-weight:700; font-size:28px; letter-spacing:0.08em;
  padding:6px 14px; border:2px solid; border-radius:8px; background:rgba(14,21,36,0.85); }}
"""
    return f"""<template>
  <style>{css}</style>
  <div id="root" data-composition-id="hud" data-width="{W}" data-height="{H}" data-layout-allow-overlap>
    {chr(10).join('    ' + l for l in labels)}
    {chr(10).join('    ' + l for l in items)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
    window.__timelines["hud"] = tl;
  </script>
</template>
"""


# ---------------------------------------------------------------- Karaoke-Untertitel

def captions_html(timings, total, top=1150):
    """Eine Zeile = eine Gruppe. Kommende Wörter grau, gesprochene weiß,
    {y:..}-markierte Wörter werden beim Sprechen farbig (Stil Referenz B)."""
    lines = [l for b in timings["beats"] for l in b["lines"]]
    groups, js = [], []
    for gi, line in enumerate(lines):
        start = max(0.1, line["start"] - 0.06)
        nxt = lines[gi + 1]["start"] - 0.06 if gi + 1 < len(lines) else total
        end = min(nxt, line["end"] + 0.9)
        # Wörter mit Farbe aus der {x:...}-Markierung
        colors = []
        for m in re.finditer(r"\{(\w):([^}]*)\}|([^{}\s]+)", line["show"]):
            if m.group(3):
                colors += [None] * len(m.group(3).split())
            else:
                colors += [HL[m.group(1)]] * len(m.group(2).split())
        spans = []
        for wi, (w, col) in enumerate(zip(line["words"], colors)):
            wid = f"cw{gi}-{wi}"
            spans.append(f'<span id="{wid}" class="w">{w["text"]}</span>')
            js.append(f'    tl.fromTo("#{wid}",{{color:"{C["dim"]}"}},{{color:"{col or C["ink"]}",duration:0.08,ease:"none"}},{fmt(max(w["start"], start))});')
        gid = f"cg{gi}"
        groups.append(f'<div id="{gid}" class="clip grp" data-start="{fmt(start)}" data-duration="{fmt(end - start)}" '
                      f'data-track-index="1"><div class="in">{" ".join(spans)}</div></div>')
        js.append(f'    tl.fromTo("#{gid} .in",{{scale:0.9,opacity:0}},{{scale:1,opacity:1,duration:0.12,ease:"back.out(2)"}},{fmt(start)});')
        js.append(f'    tl.set("#{gid} .in",{{opacity:0}},{fmt(end - 0.01)});')
    css = f"""
#root {{ position:absolute; inset:0; }}
.grp {{ position:absolute; left:60px; right:60px; top:{top}px; text-align:center; overflow:visible; }}
.in {{ font-family:'Inter',sans-serif; font-weight:900; font-size:84px; line-height:1.02; text-transform:uppercase;
  letter-spacing:-0.01em; -webkit-text-stroke:14px #000; paint-order:stroke fill;
  text-shadow:0 6px 0 #000, 0 0 30px rgba(0,0,0,0.6); }}
.w {{ color:{C['dim']}; }}
"""
    return f"""<template>
  <style>{css}</style>
  <div id="root" data-composition-id="captions" data-width="{W}" data-height="{H}">
{chr(10).join('    ' + g for g in groups)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
    window.__timelines["captions"] = tl;
  </script>
</template>
"""


# ---------------------------------------------------------------- Projekt schreiben

def write_project(project: Path, title, scenes, sfx, checklist, total, sfx_root=None, check_end=None):
    """scenes: [(id, start, end, html)], sfx: [(abs_time, file, volume)]"""
    timings = load_timings(project)
    comp = project / "compositions"
    comp.mkdir(exist_ok=True)
    hosts = []
    for i, (sid, start, end, html) in enumerate(scenes):
        (comp / f"{sid}.html").write_text(html)
        hosts.append(f'      <div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" '
                     f'data-start="{fmt(start)}" data-duration="{fmt(end - start)}" data-track-index="1" '
                     f'data-track-kind="graphics" data-width="{W}" data-height="{H}" style="z-index:1"></div>')
    (comp / "hud.html").write_text(hud_html(timings, checklist, total, check_end))
    (comp / "captions.html").write_text(captions_html(timings, total))
    audio = [f'      <audio id="voice" class="clip" src="assets/voice.wav" data-start="0" data-track-index="10" data-volume="1"></audio>']
    for j, (t, f, vol) in enumerate(sfx):
        dur = min(audio_len(Path(sfx_root) / f), total - t)
        audio.append(f'      <audio id="sfx{j}" class="clip" src="assets/sfx/{f}" data-start="{fmt(t)}" data-duration="{fmt(dur)}" '
                     f'data-track-index="{11 + j}" data-volume="{vol}"></audio>')
    index = f"""<!doctype html>
<html lang="de" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <title>{title}</title>
    <script src="assets/gsap.min.js"></script>
    <style>
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:{C['bg']}; }}
      #root {{ position:relative; width:100%; height:100%; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{fmt(total)}" data-width="{W}" data-height="{H}">
{chr(10).join(hosts)}
      <div id="hud" data-composition-id="hud" data-composition-src="compositions/hud.html" data-start="0" data-duration="{fmt(total)}"
        data-track-index="2" data-track-kind="graphics" data-width="{W}" data-height="{H}" style="z-index:5"></div>
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0"
        data-duration="{fmt(total)}" data-track-index="3" data-track-kind="captions" data-width="{W}" data-height="{H}" style="z-index:6"></div>
{chr(10).join(audio)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
    (project / "index.html").write_text(index)
    (project / "assets" / "gsap.min.js").write_bytes((Path(__file__).parent / "vendor" / "gsap-3.14.2.min.js").read_bytes())
    if sfx_root:
        (project / "assets" / "sfx").mkdir(parents=True, exist_ok=True)
        for _, f, _ in sfx:
            src = Path(sfx_root) / f
            dst = project / "assets" / "sfx" / f
            if not dst.exists():
                dst.write_bytes(src.read_bytes())
