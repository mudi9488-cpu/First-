"""Baukasten für die Community-Serie (Format „Ihr entscheidet“, 1080x1920, HyperFrames).

Liefert: HUD (Folge, Countdown, Kasse), Untertitel (2–4 Wörter, Versalien, gelbe Schlüsselwörter),
Lautmalerei-Pops, Abstimmungs- und Ergebniskarten, Messenger-UI, Projekt-Schreiber.
Siehe .claude/skills/tiktok-community-serie/.
"""
import json
import re
from pathlib import Path

from simkit import W, H, fmt, audio_len, load_timings  # noqa: F401

INK = "#1B1530"
YEL = "#FFE14A"
RED = "#FF4D5E"
GRN = "#4BE08A"
HL = {"y": YEL, "r": RED, "g": GRN, "b": "#6FA8FF"}

FONT = "'Inter', sans-serif"

BASE_CSS = f"""
#root {{ position:absolute; inset:0; overflow:hidden; font-family:{FONT}; color:#fff; }}
.abs {{ position:absolute; }}
.fig {{ position:absolute; }}
.pop {{ position:absolute; font-family:{FONT}; font-weight:900; text-transform:uppercase; white-space:nowrap;
  -webkit-text-stroke:12px {INK}; paint-order:stroke fill; letter-spacing:0.01em; text-shadow:0 6px 0 {INK}; }}
.bubble {{ position:absolute; background:#fff; color:{INK}; font-weight:800; border:6px solid {INK};
  border-radius:34px; padding:18px 30px; font-size:40px; white-space:nowrap; }}
.card {{ position:absolute; background:#fff; color:{INK}; border:7px solid {INK}; border-radius:30px; }}
"""


def _scope(sid, css, body, js):
    """Alle IDs einer Szene mit der Szenen-ID präfixen (Figuren-IDs wie #k kommen in vielen Szenen vor)."""
    ids = set(re.findall(r'id="([^"]+)"', body))

    def ren(m):
        x = m.group(1)
        return "#" + (f"{sid}-{x}" if x in ids else x)
    body = re.sub(r'id="([^"]+)"', lambda m: f'id="{sid}-{m.group(1)}"', body)
    body = re.sub(r'url\(#([\w-]+)\)', lambda m: f"url({ren(m)})", body)
    return re.sub(r'#([\w-]+)', ren, css), body, re.sub(r'#([\w-]+)', ren, js)


def scene(sid, css, body, js, bg="#9ED8F5"):
    css, body, js = _scope(sid, css, body, js)
    return f"""<template>
  <style>
{BASE_CSS}
#root {{ background:{bg}; }}
{css}
  </style>
  <div id="root" data-composition-id="{sid}" data-width="{W}" data-height="{H}">
{body}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{js}
    window.__timelines["{sid}"] = tl;
  </script>
</template>
"""


# ---------------------------------------------------------------- kleine Animations-Helfer (JS-Zeilen)

def pop_in(sel, at, scale=1.0, rot=0, dur=0.32):
    return (f'tl.fromTo("{sel}",{{scale:0,opacity:0,rotation:{rot - 12}}},'
            f'{{scale:{scale},opacity:1,rotation:{rot},duration:{dur},ease:"back.out(2.6)"}},{fmt(at)});\n')


def pop_out(sel, at, dur=0.18):
    return f'tl.to("{sel}",{{scale:0,opacity:0,duration:{dur},ease:"back.in(2)"}},{fmt(at)});\n'


def hide(sel, at=0):
    return f'tl.set("{sel}",{{opacity:0}},{fmt(at)});\n'


def show(sel, at):
    return f'tl.set("{sel}",{{opacity:1}},{fmt(at)});\n'


def shake(sel, at, n=6, amp=10, dur=0.05):
    return (f'tl.fromTo("{sel}",{{x:-{amp}}},{{x:{amp},duration:{dur},ease:"sine.inOut",yoyo:true,repeat:{n * 2 - 1}}},{fmt(at)});\n'
            f'tl.set("{sel}",{{x:0}},{fmt(at + dur * n * 2)});\n')


def hop(sel, at, h=40, n=1, dur=0.16):
    return f'tl.fromTo("{sel}",{{y:0}},{{y:-{h},duration:{dur},ease:"power2.out",yoyo:true,repeat:{n * 2 - 1}}},{fmt(at)});\n'


def breathe(sel, start, end, amp=0.025, period=1.2, origin="50% 100%"):
    """Leichtes Atmen (endliche Wiederholungen, deterministisch)."""
    n = max(1, int((end - start) / period))
    return (f'tl.fromTo("{sel}",{{scaleY:1,scaleX:1}},{{scaleY:{1 + amp},scaleX:{1 - amp / 2},duration:{period / 2},'
            f'ease:"sine.inOut",yoyo:true,repeat:{n * 2 - 1},transformOrigin:"{origin}"}},{fmt(start)});\n')


def punch(sel, at, s=1.08, dur=0.12):
    return f'tl.to("{sel}",{{scale:{s},duration:{dur},ease:"power2.out",yoyo:true,repeat:1}},{fmt(at)});\n'


def walk_in(sel, at, frm, dur=0.6):
    return f'tl.fromTo("{sel}",{{x:{frm}}},{{x:0,duration:{dur},ease:"power2.out"}},{fmt(at)});\n'


def lautmalerei(pid, text, x, y, size=96, color=YEL, rot=-8):
    return (f'<div id="{pid}" class="pop" style="left:{x}px;top:{y}px;font-size:{size}px;color:{color};'
            f'transform:rotate({rot}deg);opacity:0">{text}</div>')


def red_ring(pid, x, y, r):
    return (f'<svg id="{pid}" class="abs" style="left:{x - r - 10}px;top:{y - r - 10}px;opacity:0" width="{2 * r + 20}" height="{2 * r + 20}">'
            f'<circle cx="{r + 10}" cy="{r + 10}" r="{r}" fill="none" stroke="{RED}" stroke-width="10" stroke-dasharray="26 14"/></svg>')


# ---------------------------------------------------------------- HUD

def hud_html(total, folge, tage, tage_flip=None, kasse=None, ziel=3000, accent="#FF7A2F"):
    """tage_flip: (zeit, neue_tage) – Countdown springt um.
    kasse: (zeit_einblenden, betrag_text, anteil 0..1) – Kassen-Zeile erscheint (neues HUD-Element)."""
    key = ('<svg width="44" height="44" viewBox="0 0 44 44"><circle cx="14" cy="22" r="10" fill="none" stroke="#FFD23F" stroke-width="6"/>'
           '<path d="M 24 22 L 40 22 M 34 22 L 34 30 M 40 22 L 40 28" stroke="#FFD23F" stroke-width="6" stroke-linecap="round"/></svg>')
    js = [pop_in("#row1", 0.0, dur=0.4)]
    kasse_html = ""
    if kasse:
        t, txt, frac = kasse
        kasse_html = f"""
    <div id="row2" class="row" style="top:226px;width:640px;margin-left:-320px;height:66px;opacity:0">
      <div class="coin">€</div><div class="lab">KALLES KASSE</div>
      <div class="kval"><span id="kv">{txt}</span><small> / {f"{ziel:,}".replace(",", ".")} €</small></div>
      <div class="kbar"><i style="width:{max(1.5, frac * 100):.1f}%"></i></div>
    </div>"""
        js.append(pop_in("#row2", t, dur=0.4))
        js.append(punch("#kv", t + 0.45, 1.25, 0.15))
    if tage_flip:
        t, neu = tage_flip
        js.append(f'tl.to("#tg",{{scaleY:0,duration:0.12,ease:"power2.in"}},{fmt(t)});\n')
        js.append(f'tl.set("#tg",{{innerText:"{neu}"}},{fmt(t + 0.12)});\n')
        js.append(f'tl.to("#tg",{{scaleY:1,duration:0.18,ease:"back.out(3)"}},{fmt(t + 0.12)});\n')
        js.append(f'tl.fromTo("#row1",{{borderColor:"#fff"}},{{borderColor:"{RED}",duration:0.15,yoyo:true,repeat:3}},{fmt(t)});\n')
    css = f"""
#root {{ position:absolute; inset:0; font-family:{FONT}; }}
.row {{ position:absolute; left:50%; background:#1E1838; border:4px solid #fff; border-radius:999px;
  display:flex; align-items:center; gap:16px; padding:0 22px 0 10px; box-shadow:0 6px 0 rgba(0,0,0,0.25); }}
#row1 {{ top:128px; height:84px; width:720px; margin-left:-360px; }}
.folge {{ background:{accent}; color:#fff; font-weight:900; font-size:36px; border-radius:999px; padding:8px 26px; letter-spacing:0.02em; }}
.tage {{ color:#FFD23F; font-weight:900; font-size:44px; letter-spacing:0.01em; display:flex; align-items:center; gap:10px; }}
#tg {{ display:inline-block; transform-origin:50% 50%; }}
.coin {{ width:46px; height:46px; border-radius:50%; background:#FFC233; color:{INK}; font-weight:900; font-size:30px;
  display:flex; align-items:center; justify-content:center; border:3px solid {INK}; flex:none; }}
.lab {{ color:#fff; font-weight:900; font-size:26px; letter-spacing:0.06em; }}
.kval {{ margin-left:auto; color:#fff; font-weight:900; font-size:32px; white-space:nowrap; }}
.kval small {{ color:#9A94B8; font-size:22px; }}
#kv {{ display:inline-block; }}
.kbar {{ position:absolute; left:70px; right:24px; bottom:6px; height:6px; border-radius:3px; background:#3A3360; overflow:hidden; }}
.kbar i {{ display:block; height:100%; background:{GRN}; }}
"""
    return f"""<template>
  <style>{css}</style>
  <div id="root" data-composition-id="hud" data-width="{W}" data-height="{H}">
    <div id="row1" class="row"><div class="folge">FOLGE {folge}</div>
      <div class="tage">{key}<span>NOCH <span id="tg">{tage}</span> TAGE</span></div></div>{kasse_html}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{''.join(js)}
    window.__timelines["hud"] = tl;
  </script>
</template>
"""


# ---------------------------------------------------------------- Untertitel

def captions_html(timings, total, top=1400, size=80, overrides=None):
    """Eine Skriptzeile = eine Gruppe, erscheint komplett (Pop), markierte Wörter farbig.
    overrides: {zeilen_index: top_px} für Szenen, in denen Karten den Platz brauchen."""
    overrides = overrides or {}
    lines = [l for b in timings["beats"] for l in b["lines"]]
    groups, js = [], []
    for gi, line in enumerate(lines):
        start = max(0.05, line["start"] - 0.05)
        nxt = lines[gi + 1]["start"] - 0.05 if gi + 1 < len(lines) else total
        end = min(nxt, line["end"] + 0.6)
        html = []
        for m in re.finditer(r"\{(\w):([^}]*)\}|([^{}\s]+)", line["show"]):
            if m.group(3):
                html.append(m.group(3))
            else:
                html.append(f'<span style="color:{HL[m.group(1)]}">{m.group(2)}</span>')
        text = " ".join(html).replace("„", "").replace("“", "")
        gid = f"cg{gi}"
        t = overrides.get(gi, top)
        groups.append(f'<div id="{gid}" class="clip grp" data-start="{fmt(start)}" data-duration="{fmt(end - start)}" '
                      f'data-track-index="1" style="top:{t}px"><div class="in">{text}</div></div>')
        js.append(f'    tl.fromTo("#{gid} .in",{{scale:0.7,opacity:0}},{{scale:1,opacity:1,duration:0.14,ease:"back.out(2.4)"}},{fmt(start)});')
        js.append(f'    tl.set("#{gid} .in",{{opacity:0}},{fmt(end - 0.01)});')
    css = f"""
#root {{ position:absolute; inset:0; }}
.grp {{ position:absolute; left:50px; right:50px; text-align:center; overflow:visible; }}
.in {{ font-family:{FONT}; font-weight:900; font-size:{size}px; line-height:1.04; text-transform:uppercase; color:#fff;
  letter-spacing:0.005em; -webkit-text-stroke:15px #000; paint-order:stroke fill; text-shadow:0 7px 0 #000; }}
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


# ---------------------------------------------------------------- Abstimmung

VOTE_CSS = f"""
.vt {{ position:absolute; left:60px; right:60px; top:420px; text-align:center; font-weight:900; text-transform:uppercase;
  line-height:1.02; -webkit-text-stroke:10px {INK}; paint-order:stroke fill; }}
.vt .l1 {{ font-size:66px; color:#fff; }} .vt .l2 {{ font-size:88px; color:{YEL}; }}
.vc {{ position:absolute; left:110px; width:860px; height:190px; border-radius:30px; border:6px solid #fff;
  display:flex; align-items:center; gap:28px; padding:0 34px; box-shadow:0 10px 0 rgba(0,0,0,0.35); }}
.vc .bx {{ width:110px; height:110px; border-radius:50%; background:#fff; display:flex; align-items:center;
  justify-content:center; font-weight:900; font-size:72px; flex:none; }}
.vc .tx {{ flex:1; text-align:left; }}
.vc .t {{ font-weight:900; font-size:52px; color:#fff; line-height:1.05; }}
.vc .u {{ font-weight:800; font-size:34px; color:rgba(255,255,255,0.88); margin-top:6px; }}
.vc .ic {{ width:120px; height:120px; flex:none; }}
.vpill {{ position:absolute; left:50%; top:1170px; transform:translateX(-50%); background:#fff; color:{INK}; font-weight:900;
  font-size:36px; padding:16px 38px; border-radius:999px; white-space:nowrap; border:5px solid {INK}; }}
"""


def vote_cards(titel, a, b, icons, top_a=640, top_b=870, col_a="#3B6FF0", col_b="#FF4F8B"):
    """titel: [zeile1, zeile2]; a/b: {"titel","unter"}; icons: (svgA, svgB)."""
    def card(cid, letter, opt, col, top, icon):
        return (f'<div id="{cid}" class="vc" style="top:{top}px;background:{col};opacity:0">'
                f'<div class="bx" style="color:{col}">{letter}</div>'
                f'<div class="tx"><div class="t">{opt["titel"]}</div><div class="u">{opt["unter"]}</div></div>'
                f'<div class="ic">{icon}</div></div>')
    return (f'<div id="vt" class="vt" style="opacity:0"><div class="l1">{titel[0]}</div><div class="l2">{titel[1]}</div></div>'
            + card("va", "A", a, col_a, top_a, icons[0]) + card("vb", "B", b, col_b, top_b, icons[1])
            + '<div id="vpill" class="vpill" style="opacity:0">Schreib A oder B in die Kommentare!</div>')


def strahlen(cid, c1="#12333A", c2="#1C4A52", n=16):
    """Strahlen-Hintergrund (Abstimmung/Ergebnis)."""
    rays = []
    for i in range(n):
        a = 360 / n * i
        rays.append(f'<path d="M 540 1000 L {540 - 260} -1400 L {540 + 260} -1400 Z" fill="{c2}" transform="rotate({a} 540 1000)"/>')
    return (f'<svg id="{cid}" class="abs" style="left:0;top:0" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<rect width="{W}" height="{H}" fill="{c1}"/><g id="{cid}-r">{"".join(rays)}</g></svg>')


# ---------------------------------------------------------------- Messenger

def chat_phone(name, avatar_svg, bubbles, top=330):
    """bubbles: [(id, 'in'|'out', text)] – alle unsichtbar; mit pop_in einblenden."""
    items = []
    for bid, side, text in bubbles:
        al = "flex-start" if side == "in" else "flex-end"
        bg = "#EDEAF5" if side == "in" else "#7B5CF5"
        col = INK if side == "in" else "#fff"
        items.append(f'<div class="brow" style="justify-content:{al}"><div id="{bid}" class="bb" '
                     f'style="background:{bg};color:{col};opacity:0">{text}</div></div>')
    css = f"""
.phone {{ position:absolute; left:150px; top:{top}px; width:780px; height:1020px; background:#15122A; border-radius:80px;
  border:10px solid #2C2747; box-shadow:0 30px 0 rgba(0,0,0,0.25); overflow:hidden; }}
.phone .scr {{ position:absolute; inset:18px; border-radius:62px; background:#F6F4FB; overflow:hidden; }}
.phone .hd {{ height:150px; background:#24304A; display:flex; align-items:flex-end; gap:20px; padding:0 34px 22px; }}
.phone .av {{ width:84px; height:84px; border-radius:50%; background:#9AA0AE; overflow:hidden; border:4px solid #fff; flex:none; }}
.phone .nm {{ color:#fff; font-weight:900; font-size:40px; }} .phone .st {{ color:#9FE3B5; font-size:26px; font-weight:700; }}
.phone .msgs {{ padding:40px 30px; display:flex; flex-direction:column; gap:26px; }}
.brow {{ display:flex; }}
.bb {{ font-size:44px; font-weight:800; padding:22px 30px; border-radius:30px; max-width:560px; line-height:1.15; }}
.phone .typ {{ position:absolute; left:48px; bottom:150px; display:flex; gap:12px; background:#EDEAF5; padding:20px 26px; border-radius:30px; }}
.phone .typ i {{ width:18px; height:18px; border-radius:50%; background:#8A84A8; display:block; }}
.phone .inp {{ position:absolute; left:30px; right:30px; bottom:36px; height:84px; border-radius:42px; background:#fff;
  border:3px solid #DDD8EA; color:#B3ADC8; font-size:30px; display:flex; align-items:center; padding-left:34px; }}
"""
    html = (f'<div id="phone" class="phone"><div class="scr"><div class="hd"><div class="av">{avatar_svg}</div>'
            f'<div><div class="nm">{name}</div><div class="st">online</div></div></div>'
            f'<div class="msgs">{"".join(items)}</div>'
            f'<div id="typ" class="typ" style="opacity:0"><i></i><i></i><i></i></div>'
            f'<div class="inp">Nachricht</div></div></div>')
    return css, html


# ---------------------------------------------------------------- Projekt schreiben

def write_project(project: Path, title, scenes, sfx, hud, captions, total, music=None):
    """scenes: [(id, start, end, html)], sfx: [(abs_time, datei_in_assets/sfx, volume)],
    music: (datei_in_assets, volume) oder None."""
    comp = project / "compositions"
    comp.mkdir(exist_ok=True)
    for f in comp.glob("*.html"):
        f.unlink()
    hosts = []
    for sid, start, end, html in scenes:
        (comp / f"{sid}.html").write_text(html)
        hosts.append(f'      <div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" '
                     f'data-start="{fmt(start)}" data-duration="{fmt(end - start)}" data-track-index="1" '
                     f'data-track-kind="graphics" data-width="{W}" data-height="{H}" style="z-index:1"></div>')
    (comp / "hud.html").write_text(hud)
    (comp / "captions.html").write_text(captions)
    audio = ['      <audio id="voice" class="clip" src="assets/voice.wav" data-start="0" data-track-index="10" data-volume="1"></audio>']
    if music:
        f, vol = music
        audio.append(f'      <audio id="music" class="clip" src="assets/{f}" data-start="0" data-duration="{fmt(total)}" '
                     f'data-track-index="11" data-volume="{vol}"></audio>')
    for j, (t, f, vol) in enumerate(sfx):
        dur = min(audio_len(project / "assets" / "sfx" / f), total - t)
        audio.append(f'      <audio id="sfx{j}" class="clip" src="assets/sfx/{f}" data-start="{fmt(t)}" data-duration="{fmt(dur)}" '
                     f'data-track-index="{12 + j}" data-volume="{vol}"></audio>')
    index = f"""<!doctype html>
<html lang="de" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <title>{title}</title>
    <script src="assets/gsap.min.js"></script>
    <style>
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:#12333A; }}
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


# ---------------------------------------------------------------- HUD ab Folge 2 (Kasse läuft, Sterne)

def _eur(v):
    return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def hud_serie(total, folge, tage, kasse0, kasse_events=(), sterne=None, tage_flip=None, ziel=3000, accent="#FF7A2F"):
    """Wie hud_html, aber Kasse ist von Anfang an da und ändert sich.
    kasse_events: [(zeit, neuer_betrag)] – zählt hoch/runter, Delta fliegt ein (+250 € grün / −180 € rot).
    sterne: (zeit_einblenden, start, [(zeit, neuer_wert)]) – neue Zeile „KUNDEN ★“ (0–5)."""
    key = ('<svg width="44" height="44" viewBox="0 0 44 44"><circle cx="14" cy="22" r="10" fill="none" stroke="#FFD23F" stroke-width="6"/>'
           '<path d="M 24 22 L 40 22 M 34 22 L 34 30 M 40 22 L 40 28" stroke="#FFD23F" stroke-width="6" stroke-linecap="round"/></svg>')
    zs = f"{ziel:,}".replace(",", ".")
    js = [pop_in("#row1", 0.0, dur=0.4), pop_in("#row2", 0.1, dur=0.4)]
    js.append('    const fe=(v)=>{let s=v.toFixed(2).replace(".",",");let [a,b]=s.split(",");a=a.replace(/\\B(?=(\\d{3})+(?!\\d))/g,".");return a+","+b+" €";};\n')
    deltas = []
    prev = kasse0
    for i, (t, v) in enumerate(kasse_events):
        d = v - prev
        col = GRN if d >= 0 else RED
        sign = "+" if d >= 0 else "−"
        deltas.append(f'<div id="kd{i}" class="kd" style="color:{col};opacity:0">{sign}{_eur(abs(d))[:-3] if abs(d) == int(abs(d)) else _eur(abs(d))} €</div>')
        js.append(f'    (function(){{const o={{v:{prev}}};const el=document.getElementById("kv");'
                  f'tl.fromTo(o,{{v:{prev}}},{{v:{v},duration:0.8,ease:"power2.out",immediateRender:false,onUpdate:()=>{{el.textContent=fe(o.v);}}}},{fmt(t)});}})();\n')
        js.append(f'tl.to("#kbar",{{width:"{max(1.5, v / ziel * 100):.1f}%",duration:0.8,ease:"power2.out"}},{fmt(t)});\n')
        js.append(f'tl.fromTo("#kd{i}",{{y:30,opacity:0,scale:0.6}},{{y:0,opacity:1,scale:1,duration:0.3,ease:"back.out(2.5)"}},{fmt(t)});\n')
        js.append(f'tl.to("#kd{i}",{{y:-30,opacity:0,duration:0.35,ease:"power1.in"}},{fmt(t + 1.6)});\n')
        js.append(punch("#row2", t, 1.06, 0.14))
        prev = v
    sterne_html = ""
    if sterne:
        ts, s0, ev = sterne
        stars = "".join(f'<svg class="st" width="34" height="34" viewBox="0 0 24 24"><path d="M12 2l2.9 6.6 7.1.6-5.4 4.7 1.6 7-6.2-3.8-6.2 3.8 1.6-7L2 9.2l7.1-.6z" '
                        f'fill="#4A4370"/></svg>' for _ in range(5))
        sterne_html = f"""
    <div id="row3" class="row" style="top:306px;width:560px;margin-left:-280px;height:60px;opacity:0">
      <div class="lab" style="margin-left:14px">KUNDEN</div><div class="stars"><div class="sb">{stars}</div>
      <div id="sf" class="sf" style="width:{s0 / 5 * 100:.0f}%">{stars.replace('#4A4370', '#FFC233')}</div></div>
      <div id="sv" class="kval">{f"{s0:.1f}".replace(".", ",")}</div></div>"""
        js.append(pop_in("#row3", ts, dur=0.4))
        for t, v in ev:
            js.append(f'tl.to("#sf",{{width:"{v / 5 * 100:.0f}%",duration:0.7,ease:"power2.out"}},{fmt(t)});\n')
            js.append(f'tl.set("#sv",{{innerText:"{f"{v:.1f}".replace(".", ",")}"}},{fmt(t + 0.35)});\n')
            js.append(punch("#row3", t, 1.06, 0.14))
    if tage_flip:
        t, neu = tage_flip
        js.append(f'tl.to("#tg",{{scaleY:0,duration:0.12,ease:"power2.in"}},{fmt(t)});\n')
        js.append(f'tl.set("#tg",{{innerText:"{neu}"}},{fmt(t + 0.12)});\n')
        js.append(f'tl.to("#tg",{{scaleY:1,duration:0.18,ease:"back.out(3)"}},{fmt(t + 0.12)});\n')
    css = f"""
#root {{ position:absolute; inset:0; font-family:{FONT}; }}
.row {{ position:absolute; left:50%; background:#1E1838; border:4px solid #fff; border-radius:999px;
  display:flex; align-items:center; gap:16px; padding:0 22px 0 10px; box-shadow:0 6px 0 rgba(0,0,0,0.25); }}
#row1 {{ top:128px; height:84px; width:720px; margin-left:-360px; }}
.folge {{ background:{accent}; color:#fff; font-weight:900; font-size:36px; border-radius:999px; padding:8px 26px; letter-spacing:0.02em; }}
.tage {{ color:#FFD23F; font-weight:900; font-size:44px; display:flex; align-items:center; gap:10px; }}
#tg {{ display:inline-block; }}
.coin {{ width:46px; height:46px; border-radius:50%; background:#FFC233; color:{INK}; font-weight:900; font-size:30px;
  display:flex; align-items:center; justify-content:center; border:3px solid {INK}; flex:none; }}
.lab {{ color:#fff; font-weight:900; font-size:28px; letter-spacing:0.06em; }}
.kval {{ margin-left:auto; color:#fff; font-weight:900; font-size:34px; white-space:nowrap; }}
.kval small {{ color:#9A94B8; font-size:28px; }}
.kbar {{ position:absolute; left:70px; right:24px; bottom:6px; height:6px; border-radius:3px; background:#3A3360; overflow:hidden; }}
.kbar i {{ display:block; height:100%; background:{GRN}; }}
.kd {{ position:absolute; right:-150px; top:4px; font-weight:900; font-size:46px; -webkit-text-stroke:9px {INK}; paint-order:stroke fill; white-space:nowrap; }}
.stars {{ position:relative; height:34px; width:190px; }}
.sb, .sf {{ position:absolute; left:0; top:0; height:34px; display:flex; gap:4px; overflow:hidden; white-space:nowrap; }}
.st {{ flex:none; }}
"""
    return f"""<template>
  <style>{css}</style>
  <div id="root" data-composition-id="hud" data-width="{W}" data-height="{H}">
    <div id="row1" class="row"><div class="folge">FOLGE {folge}</div>
      <div class="tage">{key}<span>NOCH <span id="tg">{tage}</span> TAGE</span></div></div>
    <div id="row2" class="row" style="top:226px;width:700px;margin-left:-350px;height:66px;opacity:0">
      <div class="coin">€</div><div class="lab" style="white-space:nowrap">KALLES KASSE</div>
      <div class="kval"><span id="kv">{_eur(kasse0)} €</span><small> / {zs} €</small></div>
      <div class="kbar"><i id="kbar" style="width:{max(1.5, kasse0 / ziel * 100):.1f}%"></i></div>{''.join(deltas)}
    </div>{sterne_html}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{''.join(js)}
    window.__timelines["hud"] = tl;
  </script>
</template>
"""


# ---------------------------------------------------------------- Ergebnis der letzten Abstimmung

RESULT_CSS = f"""
.rt {{ position:absolute; left:60px; right:60px; top:420px; text-align:center; font-weight:900; text-transform:uppercase;
  line-height:1.05; -webkit-text-stroke:10px {INK}; paint-order:stroke fill; }}
.rt .l1 {{ font-size:58px; color:#fff; }} .rt .l2 {{ font-size:66px; color:{YEL}; }}
.rc {{ position:absolute; left:110px; width:860px; height:150px; border-radius:30px; background:#1E1838; border:5px solid #5A5480;
  display:flex; align-items:center; gap:24px; padding:0 30px; }}
.rc.win {{ border:7px solid #FFC233; box-shadow:0 0 0 6px rgba(255,194,51,0.25); }}
.rc .ic {{ width:90px; height:90px; border-radius:50%; display:flex; align-items:center; justify-content:center; flex:none;
  font-weight:900; font-size:52px; color:#fff; }}
.rc .mid {{ flex:1; }}
.rc .t {{ color:#fff; font-weight:900; font-size:42px; }}
.rc .bar {{ height:18px; border-radius:9px; background:#3A3360; margin-top:12px; overflow:hidden; }}
.rc .bar i {{ display:block; height:100%; width:0%; border-radius:9px; }}
.rc .pc {{ color:#fff; font-weight:900; font-size:54px; width:150px; text-align:right; font-variant-numeric:tabular-nums; }}
.badge {{ position:absolute; right:-24px; top:-34px; background:#3DDC84; color:{INK}; font-weight:900; font-size:30px; padding:8px 20px;
  border-radius:14px; border:4px solid {INK}; transform:rotate(8deg); }}
"""


def result_cards(a, b, pa, pb, col_a="#3B6FF0", col_b="#FF4F8B", top=640):
    """a/b: Titel der Optionen, pa/pb: Prozent (vom Creator!). Gewinner bekommt Goldrahmen + GEWONNEN!."""
    def card(cid, letter, txt, p, col, y, win):
        badge = f'<div id="{cid}-badge" class="badge" style="opacity:0">GEWONNEN!</div>' if win else ""
        return (f'<div id="{cid}" class="rc" style="top:{y}px;opacity:0"><div class="ic" style="background:{col}">{letter}</div>'
                f'<div class="mid"><div class="t">{txt}</div><div class="bar"><i id="{cid}-bar" style="background:{col}"></i></div></div>'
                f'<div class="pc"><span id="{cid}-p">0</span>%</div>{badge}</div>')
    return ('<div id="rt" class="rt" style="opacity:0"><div class="l1">LETZTE FOLGE</div><div class="l2">HABT IHR ENTSCHIEDEN</div></div>'
            + card("ra", "A", a, pa, col_a, top, pa >= pb) + card("rb", "B", b, pb, col_b, top + 190, pb > pa))


def result_js(at, pa, pb, dur=1.2):
    js = pop_in("#rt", at) + pop_in("#ra", at + 0.15) + pop_in("#rb", at + 0.3)
    for cid, p in (("ra", pa), ("rb", pb)):
        js += f'tl.to("#{cid}-bar",{{width:"{p}%",duration:{dur},ease:"power2.out"}},{fmt(at + 0.5)});\n'
        js += (f'(function(){{const o={{v:0}};const el=document.querySelector("#{cid}-p");'
               f'tl.fromTo(o,{{v:0}},{{v:{p},duration:{dur},ease:"power2.out",onUpdate:()=>{{el.textContent=Math.round(o.v);}}}},{fmt(at + 0.5)});}})();\n')
    win = "ra" if pa >= pb else "rb"
    js += f'tl.set("#{win}",{{className:"rc win"}},{fmt(at + 0.5 + dur)});\n' + pop_in(f"#{win}-badge", at + 0.5 + dur, rot=8)
    return js
