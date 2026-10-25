#!/usr/bin/env python3
"""Baut das Video „Was wäre, wenn niemand mehr arbeiten geht?“

1. python3 ../../tools/tts.py .     (Stimme + assets/timings.json)
2. python3 build.py                 (index.html + compositions/)
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "tools"))
from simkit import C, scene_html, hud_card, js_count, load_timings, write_project, rng, fmt  # noqa: E402

SFX_ROOT = "/root/.claude/plugins/cache/hyperframes/hyperframes/0.8.197/skills/media-use/audio/assets/sfx"
T = load_timings(HERE)
TOTAL = round(T["duration"] + 1.3, 2)  # kurzer Halt am Ende für den Loop
B = {b["id"]: b for b in T["beats"]}
ORDER = [b["id"] for b in T["beats"]]
S = {bid: (0.0 if i == 0 else B[bid]["start"]) for i, bid in enumerate(ORDER)}
E = {bid: (S[ORDER[i + 1]] if i + 1 < len(ORDER) else TOTAL) for i, bid in enumerate(ORDER)}


def w(bid, li, wi=0):
    """Startzeit eines Wortes relativ zum Szenenbeginn."""
    return round(B[bid]["lines"][li]["words"][wi]["start"] - S[bid], 3)


def wa(bid, li, wi=0):
    """Absolute Startzeit eines Wortes."""
    return round(B[bid]["lines"][li]["words"][wi]["start"], 3)


# ------------------------------------------------------------------ Wecker (Hook + Loop)

def clock_svg(p, time_text):
    return f"""
    <svg id="{p}-clock" class="clock" viewBox="0 0 640 460" width="640" height="460">
      <g id="{p}-ringL" stroke="{C['gold']}" stroke-width="12" stroke-linecap="round" fill="none" opacity="0">
        <path d="M 52 160 Q 22 230 52 300"/><path d="M 14 130 Q -24 230 14 330"/></g>
      <g id="{p}-ringR" stroke="{C['gold']}" stroke-width="12" stroke-linecap="round" fill="none" opacity="0">
        <path d="M 588 160 Q 618 230 588 300"/><path d="M 626 130 Q 664 230 626 330"/></g>
      <g id="{p}-body">
        <rect x="270" y="58" width="100" height="34" rx="12" fill="{C['gold']}"/>
        <rect x="90" y="84" width="460" height="290" rx="64" fill="#1E2740" stroke="#34415F" stroke-width="8"/>
        <rect x="130" y="132" width="380" height="190" rx="26" fill="#070B14"/>
        <text id="{p}-t1" x="320" y="270" text-anchor="middle" font-family="JetBrains Mono" font-weight="700"
          font-size="128" fill="{C['red']}">{time_text}</text>
        <text id="{p}-t2" x="320" y="270" text-anchor="middle" font-family="JetBrains Mono" font-weight="700"
          font-size="128" fill="{C['red']}" opacity="0">07:00</text>
        <rect x="140" y="368" width="70" height="30" rx="10" fill="#2A3652"/>
        <rect x="430" y="368" width="70" height="30" rx="10" fill="#2A3652"/>
      </g>
    </svg>"""


def clock_ring_js(p, at):
    return f"""
    tl.set("#{p}-t1", {{opacity:0}}, {at});
    tl.set("#{p}-t2", {{opacity:1}}, {at});
    tl.fromTo("#{p}-body", {{rotation:0}}, {{rotation:4, duration:0.05, ease:"sine.inOut", yoyo:true, repeat:15,
      transformOrigin:"50% 80%"}}, {at});
    tl.fromTo(["#{p}-ringL","#{p}-ringR"], {{opacity:0, scale:0.8}}, {{opacity:1, scale:1.08, duration:0.16,
      ease:"power2.out", yoyo:true, repeat:5, transformOrigin:"50% 50%"}}, {at});
"""


TITLE_CSS = f"""
.title {{ position:absolute; left:60px; right:60px; top:300px; text-align:center; }}
.title div {{ font-weight:900; text-transform:uppercase; line-height:1.0; letter-spacing:-0.01em; }}
.title .t1 {{ font-size:56px; color:{C['mute']}; }}
.title .t2 {{ font-size:104px; color:{C['gold']}; }}
.title .t3 {{ font-size:104px; color:{C['red']}; }}
.clockwrap {{ position:absolute; left:220px; top:660px; width:640px; height:460px; }}
"""


def title_html(p):
    return (f'<div class="title" id="{p}-title"><div class="t1">Was wäre, wenn</div>'
            f'<div class="t2">niemand mehr</div><div class="t3">arbeiten geht?</div></div>')


def scene_hook():
    p = "hk"
    body = title_html(p) + f'<div class="clockwrap" id="{p}-cw">{clock_svg(p, "06:59")}</div>'
    js = clock_ring_js(p, w("hook", 1, 1))
    js += f"""
    tl.fromTo("#{p}-cw", {{scale:1}}, {{scale:1.06, duration:{E['hook'] - 0.2}, ease:"power1.inOut"}}, 0);
    tl.to("#{p}-title", {{opacity:0, filter:"blur(8px)", duration:0.2, ease:"power2.in"}}, {E['hook'] - 0.25});
"""
    return scene_html("hook", TITLE_CSS, body, js)


def scene_loop():
    p = "lp"
    at = w("loop", 2, 1)
    body = f'<div class="clockwrap" id="{p}-cw">{clock_svg(p, "06:59")}</div>' + title_html(p)
    js = clock_ring_js(p, at)
    js += f"""
    tl.fromTo("#{p}-cw", {{scale:1.12, opacity:0}}, {{scale:1, opacity:1, duration:0.5, ease:"expo.out"}}, 0);
    tl.fromTo("#{p}-title div", {{opacity:0, filter:"blur(8px)"}}, {{opacity:1, filter:"blur(0px)", duration:0.15,
      stagger:0.08, ease:"power4.out"}}, {at + 0.75});
"""
    return scene_html("loop", TITLE_CSS, body, js)


# ------------------------------------------------------------------ Globus mit Zähler

def scene_welt():
    r = rng(7)
    # Kontinente als weiche Ellipsen (wie in Referenz B)
    conts = [(-150, -120, 120, 90, -20), (-170, 90, 80, 130, 15), (60, -150, 150, 80, 5),
             (90, 40, 110, 140, -10), (230, 170, 70, 50, 20), (300, -60, 60, 120, 0), (420, -20, 90, 140, 10)]
    shapes, dots = [], []
    for cx, cy, rx, ry, rot in conts:
        shapes.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" transform="rotate({rot} {cx} {cy})"/>')
    import math
    pts = []
    while len(pts) < 170:
        cx, cy, rx, ry, rot = conts[r.randrange(len(conts))]
        a, d = r.random() * 6.283, r.random() ** 0.5
        x, y = d * rx * math.cos(a), d * ry * math.sin(a)
        t = math.radians(rot)
        pts.append((cx + x * math.cos(t) - y * math.sin(t), cy + x * math.sin(t) + y * math.cos(t)))
    r.shuffle(pts)
    for i, (x, y) in enumerate(pts):
        dots.append(f'<circle class="wd" cx="{x:.1f}" cy="{y:.1f}" r="6.5" fill="{C["gold"]}"/>')
    merid = "".join(f'<ellipse cx="0" cy="0" rx="{330 * k:.0f}" ry="330"/>' for k in (0.25, 0.55, 0.82))
    paral = "".join(f'<line x1="-330" y1="{y}" x2="330" y2="{y}"/>' for y in (-220, -110, 0, 110, 220))
    body = hud_card("wc", "Menschen bei der Arbeit", "3.600.000.000", width=720, size=76, top=290) + f"""
    <svg id="wg" viewBox="-360 -360 720 720" width="720" height="720" style="position:absolute;left:180px;top:470px">
      <defs>
        <radialGradient id="wgg" cx="35%" cy="30%" r="80%"><stop offset="0" stop-color="#3655C9"/><stop offset="1" stop-color="#16225C"/></radialGradient>
        <clipPath id="wgc"><circle r="330"/></clipPath>
      </defs>
      <circle r="352" fill="#2B3F9A" opacity="0.25"/>
      <circle r="330" fill="url(#wgg)"/>
      <g clip-path="url(#wgc)">
        <g id="wg-spin">
          <g fill="#5A74E0" opacity="0.55">{''.join(shapes)}</g>
          <g id="wg-dots">{''.join(dots)}</g>
        </g>
        <g stroke="#FFFFFF" stroke-opacity="0.14" stroke-width="2" fill="none">{merid}{paral}</g>
      </g>
    </svg>"""
    t0, t1 = w("welt", 1), w("welt", 2, 2) + 0.2
    js = js_count("wc-num", 3600000000, 0, t0 + 0.1, t1 - t0 - 0.1, ease="power2.in")
    js += f"""
    tl.fromTo("#wg", {{scale:0.9, opacity:0}}, {{scale:1, opacity:1, duration:0.6, ease:"expo.out", transformOrigin:"50% 50%"}}, 0);
    tl.fromTo("#wc", {{y:-30, opacity:0}}, {{y:0, opacity:1, duration:0.4, ease:"expo.out"}}, 0.1);
    tl.fromTo("#wg-spin", {{x:40}}, {{x:-60, duration:{E['welt'] - S['welt']}, ease:"none"}}, 0);
    tl.fromTo(".wd", {{fill:"{C['gold']}", scale:1}}, {{fill:"#2A3570", scale:0.6, duration:0.15, ease:"power2.in",
      transformOrigin:"50% 50%", stagger:{(t1 - t0 - 0.2) / len(pts):.4f}}}, {t0 + 0.1});
    tl.to("#wc-num", {{color:"{C['red']}", duration:0.1}}, {t1});
    tl.fromTo("#wc", {{borderColor:"{C['line']}"}}, {{borderColor:"{C['red']}", duration:0.1}}, {t1});
"""
    return scene_html("welt", "", body, js)


# ------------------------------------------------------------------ Abfahrtstafel

def scene_verkehr():
    rows = [("08:00", "BUS 42", C["teal"], "Hauptbahnhof", w("verkehr", 1, 1)),
            ("08:02", "S1", C["green"], "Flughafen", w("verkehr", 2, 1)),
            ("08:04", "ICE 573", "#DDE3EE", "Berlin Hbf", w("verkehr", 2, 1) + 0.25),
            ("08:10", "LH 400", C["blue"], "New York", w("verkehr", 3, 1))]
    css = f"""
#vb {{ position:absolute; left:50px; width:980px; top:400px; background:#0A0F1C; border:4px solid {C['line']}; border-radius:28px; overflow:hidden; }}
#vb .hd {{ display:flex; justify-content:space-between; padding:28px 36px; background:#141C2E; border-bottom:4px solid {C['line']};
  font-family:'JetBrains Mono',monospace; font-weight:700; font-size:36px; letter-spacing:0.14em; }}
.row {{ position:relative; display:flex; align-items:center; height:150px; padding:0 30px; border-bottom:3px solid #1A2338; }}
.row:last-child {{ border-bottom:none; }}
.row .fl {{ position:absolute; inset:0; background:{C['red']}; opacity:0; }}
.row .tm {{ position:relative; font-family:'JetBrains Mono',monospace; font-weight:700; font-size:38px; width:150px; }}
.row .ln {{ position:relative; font-weight:900; font-size:30px; color:#0A0F1C; padding:8px 14px; border-radius:10px; width:150px; text-align:center; }}
.row .ds {{ position:relative; font-weight:700; font-size:40px; margin-left:26px; flex:1; }}
.row .st {{ position:relative; width:250px; height:64px; perspective:400px; }}
.row .st span {{ position:absolute; right:0; top:0; height:64px; line-height:64px; font-family:'JetBrains Mono',monospace; font-weight:700;
  font-size:30px; letter-spacing:0.06em; padding:0 16px; border-radius:10px; white-space:nowrap; }}
.row .ok {{ color:{C['green']}; }}
.row .no {{ color:#fff; background:{C['red']}; opacity:0; }}
"""
    rh, js = [], []
    for i, (tm, ln, col, ds, at) in enumerate(rows):
        rh.append(f'<div class="row" id="vr{i}"><div class="fl"></div><div class="tm">{tm}</div>'
                  f'<div class="ln" style="background:{col}">{ln}</div><div class="ds">{ds}</div>'
                  f'<div class="st"><span class="ok">PÜNKTLICH</span><span class="no">FÄLLT AUS</span></div></div>')
        js.append(f"""    tl.fromTo("#vr{i} .ok", {{rotationX:0, opacity:1}}, {{rotationX:90, opacity:0, duration:0.1, ease:"power2.in"}}, {at});
    tl.fromTo("#vr{i} .no", {{rotationX:-90, opacity:0}}, {{rotationX:0, opacity:1, duration:0.2, ease:"expo.out"}}, {at + 0.1});
    tl.fromTo("#vr{i} .fl", {{opacity:0.45}}, {{opacity:0, duration:0.4, ease:"power2.out"}}, {at + 0.1});""")
    body = (f'<div id="vb"><div class="hd"><span style="color:{C["gold"]}">ABFAHRT</span><span>08:00</span></div>'
            + "".join(rh) + "</div>")
    js.insert(0, f'    tl.fromTo("#vb", {{y:120, opacity:0}}, {{y:0, opacity:1, duration:0.5, ease:"expo.out"}}, 0);')
    return scene_html("verkehr", css, body, "\n".join(js))


# ------------------------------------------------------------------ Skyline (Strom + Himmel)

def skyline(p, lit=True, seed=3):
    r = rng(seed)
    blds, wins = [], []
    x = -10
    while x < 1080:
        bw = r.choice([110, 130, 150, 170])
        bh = r.randint(260, 600)
        top = 1130 - bh
        blds.append(f'<rect x="{x}" y="{top}" width="{bw}" height="{bh + 20}" fill="{r.choice(["#1B2440", "#212B49", "#182038"])}"/>')
        cols = (bw - 30) // 34
        for cy in range(top + 30, 1100, 46):
            for cx in range(cols):
                if lit and r.random() < 0.7:
                    wx = x + 18 + cx * 34
                    wins.append((wx, f'<rect class="{p}-win" x="{wx}" y="{cy}" width="20" height="26" rx="3" fill="#F5C451"/>'))
                elif not lit and r.random() < 0.7:
                    wx = x + 18 + cx * 34
                    blds.append(f'<rect x="{wx}" y="{cy}" width="20" height="26" rx="3" fill="#121A2E"/>')
        x += bw + r.choice([0, 6, 12])
    wins.sort(key=lambda t: -t[0])  # rechts nach links ausgehen
    return "".join(blds), "".join(s for _, s in wins), len(wins)


def scene_strom():
    blds, wins, n = skyline("st")
    body = hud_card("sc", "Stromnetz", "100", unit="%", color=C["teal"], bar=C["teal"], top=290) + f"""
    <div id="st-sky" style="position:absolute;inset:0;background:linear-gradient(180deg,#141B33 0%,#2A2547 55%,#3A2B45 100%)"></div>
    <svg id="st-city" data-layout-allow-overflow viewBox="0 0 1080 1920" width="1080" height="1920" style="position:absolute;left:0;top:0">
      {blds}<g id="st-wins">{wins}</g>
      <rect x="0" y="1130" width="1080" height="790" fill="#0B101D"/>
    </svg>
    <div id="st-dark" style="position:absolute;inset:0;background:#000;opacity:0"></div>
    <div class="pill" id="st-pill" style="left:0;right:0;margin:0 auto;width:max-content;top:520px;background:{C['red']}">Kraftwerke: kein Personal</div>
    """
    a, b = w("strom", 1, 1), w("strom", 1, 2)
    js = js_count("sc-num", 100, 0, a - 0.2, b - a + 0.3, ease="power3.in")
    js += f"""
    tl.fromTo("#st-city", {{y:60}}, {{y:0, duration:1.2, ease:"expo.out"}}, 0);
    tl.fromTo(".st-win", {{opacity:1}}, {{opacity:0, duration:0.06, ease:"none", stagger:{(b - a + 0.1) / n:.4f}}}, {a});
    tl.fromTo("#sc-bar", {{scaleX:1}}, {{scaleX:0, duration:{b - a + 0.3}, ease:"power3.in"}}, {a - 0.2});
    tl.to("#sc-num", {{color:"{C['red']}", duration:0.1}}, {b + 0.1});
    tl.fromTo("#st-dark", {{opacity:0}}, {{opacity:0.35, duration:0.25, ease:"power2.out"}}, {b + 0.05});
    tl.fromTo("#st-pill", {{scale:1.4, opacity:0}}, {{scale:1, opacity:1, duration:0.25, ease:"expo.out"}}, {w("strom", 2)});
"""
    css = "#st-sky, #st-city, #st-dark { z-index:0; } .hudcard, .pill { z-index:3; }"
    return scene_html("strom", css, body, js)


def scene_himmel():
    blds, _, _ = skyline("hm", lit=False)
    r = rng(11)
    stars = "".join(f'<circle class="hm-s" cx="{r.randint(20, 1060)}" cy="{r.randint(480, 1000)}" r="{r.choice([2, 3, 3, 4])}" fill="#fff"/>'
                    for _ in range(70))
    body = f"""
    <div style="position:absolute;inset:0;background:linear-gradient(180deg,#071433 0%,#12306B 70%,#1E4C96 100%)"></div>
    <svg viewBox="0 0 1080 1920" width="1080" height="1920" style="position:absolute;left:0;top:0">
      <g id="hm-stars">{stars}</g>
      <circle id="hm-moon" cx="830" cy="600" r="56" fill="#F4F1E6"/>
    </svg>
    <svg data-layout-allow-overflow viewBox="0 0 1080 1920" width="1080" height="1920" style="position:absolute;left:0;top:0;z-index:2">
      <g id="hm-birds" fill="none" stroke="#F4F1E6" stroke-width="7" stroke-linecap="round" stroke-linejoin="round">
        {''.join(f'<path class="hm-b" transform="translate({x},{y})" d="M -34 -6 Q -16 -24 0 0 Q 16 -24 34 -6"/>' for x, y in ((0, 620), (90, 560), (150, 690), (230, 600), (320, 660)))}
      </g>
    </svg>
    <div id="hm-smog" style="position:absolute;inset:0;background:linear-gradient(180deg,#3B3631 0%,#5A4E40 70%,#6E5C45 100%)"></div>
    <svg data-layout-allow-overflow viewBox="0 0 1080 1920" width="1080" height="1920" style="position:absolute;left:0;top:0">
      {blds}<rect x="0" y="1130" width="1080" height="790" fill="#0B101D"/>
    </svg>
    <div class="hudcard" id="hc" style="top:290px;width:560px;margin-left:-280px">
      <div class="lab">Luft über der Stadt</div>
      <div class="val" style="font-size:72px;position:relative;height:80px">
        <span id="hc-a" style="position:absolute;left:0;color:{C['red']}">SCHLECHT</span>
        <span id="hc-b" style="position:absolute;left:0;color:{C['green']};opacity:0">SAUBER</span></div>
      <div class="bar"><i id="hc-bar" style="background:{C['red']}"></i></div>
    </div>
    """
    k = w("himmel", 2, 3)
    js = f"""
    tl.fromTo("#hm-smog", {{opacity:1}}, {{opacity:0, duration:{k - w('himmel', 1) + 0.2}, ease:"power2.inOut"}}, {w('himmel', 1) - 0.2});
    tl.fromTo(".hm-s", {{opacity:0}}, {{opacity:1, duration:0.2, stagger:0.012, ease:"power1.out"}}, {w('himmel', 2, 1)});
    tl.fromTo("#hm-moon", {{opacity:0}}, {{opacity:1, duration:0.6, ease:"power2.out"}}, {w('himmel', 2, 1)});
    tl.fromTo("#hc-bar", {{scaleX:0.2, backgroundColor:"{C['red']}"}}, {{scaleX:1, backgroundColor:"{C['green']}", duration:{k - w('himmel', 1)},
      ease:"power2.inOut"}}, {w('himmel', 1)});
    tl.set("#hc-a", {{opacity:0}}, {k});
    tl.fromTo("#hc-b", {{opacity:0, scale:1.3}}, {{opacity:1, scale:1, duration:0.25, ease:"expo.out", transformOrigin:"0% 50%"}}, {k});
    tl.fromTo("#hc", {{borderColor:"{C['line']}"}}, {{borderColor:"{C['green']}", duration:0.15}}, {k});
    tl.fromTo("#hm-birds", {{x:-420, y:60}}, {{x:860, y:-40, duration:2.2, ease:"none"}}, {w('himmel', 3, 2) - 0.4});
    tl.fromTo(".hm-b", {{scaleY:1}}, {{scaleY:-0.6, duration:0.16, yoyo:true, repeat:13, ease:"sine.inOut", stagger:0.05}}, {w('himmel', 3, 2) - 0.4});
"""
    return scene_html("himmel", "", body, js)


# ------------------------------------------------------------------ Supermarkt

def scene_essen():
    r = rng(5)
    cols = [C["coral"], C["teal"], C["gold"], C["blue"], C["green"], "#E6E9F0", "#B57BFF"]
    items = []
    for shelf_y in (760, 930, 1100):
        x = 110
        while x < 950:
            kind = r.choice(["box", "bottle", "can"])
            col = r.choice(cols)
            if kind == "box":
                wdt, h = r.randint(70, 100), r.randint(110, 140)
                svg = f'<rect x="0" y="{-h}" width="{wdt}" height="{h}" rx="8" fill="{col}"/><rect x="10" y="{-h + 20}" width="{wdt - 20}" height="22" rx="4" fill="#fff" opacity="0.6"/>'
            elif kind == "bottle":
                wdt, h = 46, r.randint(120, 145)
                svg = (f'<rect x="0" y="{-h + 40}" width="{wdt}" height="{h - 40}" rx="14" fill="{col}"/>'
                       f'<rect x="14" y="{-h + 8}" width="18" height="36" rx="5" fill="{col}"/><rect x="12" y="{-h}" width="22" height="12" rx="3" fill="#fff"/>')
            else:
                wdt, h = 58, 80
                svg = f'<rect x="0" y="{-h}" width="{wdt}" height="{h}" rx="10" fill="{col}"/><rect x="0" y="{-h + 28}" width="{wdt}" height="16" fill="#000" opacity="0.2"/>'
            if x + wdt > 970:
                break
            items.append(f'<g class="it" transform="translate({x},{shelf_y})"><g>{svg}</g></g>')
            x += wdt + r.randint(8, 18)
    r.shuffle(items)
    body = hud_card("ec", "Ware im Regal", "100", unit="%", color=C["gold"], bar=C["gold"], top=290) + f"""
    <svg id="es" viewBox="0 0 1080 1920" width="1080" height="1920" style="position:absolute;left:0;top:0">
      <rect x="80" y="560" width="920" height="600" rx="16" fill="#151E33" stroke="{C['line']}" stroke-width="6"/>
      {''.join(items)}
      <rect x="80" y="760" width="920" height="16" fill="#2E3A58"/>
      <rect x="80" y="930" width="920" height="16" fill="#2E3A58"/>
      <rect x="80" y="1100" width="920" height="16" fill="#2E3A58"/>
    </svg>
    <div id="es-stamp" style="position:absolute;left:0;right:0;top:760px;text-align:center">
      <span style="display:inline-block;font-weight:900;font-size:96px;color:{C['red']};border:10px solid {C['red']};border-radius:18px;
        padding:6px 30px;background:rgba(14,21,36,0.75)">AUSVERKAUFT</span></div>
    <div class="pill" id="es-pill" style="left:0;right:0;margin:0 auto;width:max-content;top:990px;background:{C['red']}">Keine Lieferung</div>
    """
    a, b = 0.15, w("essen", 1, 3)
    js = js_count("ec-num", 100, 0, a, b - a, ease="power1.in")
    js += f"""
    tl.fromTo(".it > g", {{y:0, opacity:1}}, {{y:-50, opacity:0, duration:0.15, ease:"power2.in", stagger:{(b - a - 0.15) / len(items):.4f}}}, {a});
    tl.fromTo("#ec-bar", {{scaleX:1}}, {{scaleX:0, duration:{b - a}, ease:"power1.in"}}, {a});
    tl.to("#ec-num", {{color:"{C['red']}", duration:0.1}}, {b});
    tl.fromTo("#es-stamp span", {{scale:2.2, rotation:-8, opacity:0}}, {{scale:1, rotation:-8, opacity:1, duration:0.22, ease:"expo.out"}}, {b});
    tl.fromTo("#es-pill", {{scale:1.4, opacity:0}}, {{scale:1, opacity:1, duration:0.25, ease:"expo.out"}}, {w("essen", 2, 1)});
"""
    return scene_html("essen", "", body, js)


# ------------------------------------------------------------------ Wasserhahn

def scene_wasser():
    body = hud_card("wa", "Wasserdruck", "3,0", unit="bar", color=C["blue"], bar=C["blue"], top=290) + f"""
    <svg viewBox="0 0 1080 1920" width="1080" height="1920" style="position:absolute;left:0;top:0">
      <defs><linearGradient id="chr" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#D5DCE8"/><stop offset="1" stop-color="#7F8BA3"/></linearGradient></defs>
      <g transform="translate(0,90)">
      <rect x="0" y="560" width="300" height="60" fill="url(#chr)"/>
      <rect x="290" y="530" width="120" height="120" rx="20" fill="url(#chr)"/>
      <rect x="320" y="490" width="60" height="44" rx="8" fill="#9AA6BF"/>
      <rect x="250" y="470" width="200" height="30" rx="15" fill="{C['blue']}"/>
      <path d="M 400 560 L 560 560 Q 600 560 600 600 L 600 660 L 540 660 L 540 620 L 400 620 Z" fill="url(#chr)"/>
      <rect id="wa-stream" x="552" y="660" width="36" height="290" rx="14" fill="#5BB4FF" opacity="0.9"/>
      <circle class="wa-drop" cx="570" cy="680" r="13" fill="#5BB4FF" opacity="0"/>
      <circle class="wa-drop" cx="570" cy="680" r="13" fill="#5BB4FF" opacity="0"/>
      </g>
      <path d="M 300 1030 L 840 1030 Q 830 1130 700 1130 L 440 1130 Q 310 1130 300 1030 Z" fill="#C9D2E3"/>
      <rect x="280" y="1010" width="580" height="28" rx="14" fill="#E3E8F1"/>
    </svg>
    """
    k = w("wasser", 2, 1)
    js = js_count("wa-num", 3.0, 0.0, 0.2, k + 0.2, decimals=1, ease="power2.in")
    js += f"""
    tl.fromTo("#wa-bar", {{scaleX:1}}, {{scaleX:0, duration:{k + 0.2}, ease:"power2.in"}}, 0.2);
    tl.fromTo("#wa-stream", {{scaleX:1}}, {{scaleX:0.25, duration:{k - 0.3}, ease:"power2.in", transformOrigin:"50% 0%"}}, 0.3);
    tl.to("#wa-stream", {{scaleY:0, duration:0.25, ease:"power2.in", transformOrigin:"50% 100%"}}, {k});
    tl.to("#wa-num", {{color:"{C['red']}", duration:0.1}}, {k + 0.4});
"""
    for i, t in enumerate((k + 0.45, k + 1.0)):
        js += f"""    tl.fromTo(".wa-drop:nth-of-type({i + 1})", {{opacity:1, y:0}}, {{y:260, duration:0.4, ease:"power2.in"}}, {t:.3f});
    tl.set(".wa-drop:nth-of-type({i + 1})", {{opacity:0}}, {t + 0.4:.3f});
"""
    return scene_html("wasser", "", body, js)


# ------------------------------------------------------------------ Handy (Urlaub + Notruf)

PHONE_CSS = f"""
.phone {{ position:absolute; left:290px; top:400px; width:500px; height:740px; background:#0A0F1C; border:12px solid #2A3652;
  border-radius:64px; overflow:hidden; }}
.phone .notch {{ position:absolute; left:170px; top:14px; width:136px; height:30px; border-radius:15px; background:#2A3652; }}
.phone .scr {{ position:absolute; inset:0; padding:70px 26px 26px; }}
.phone .clock {{ font-family:'JetBrains Mono',monospace; font-weight:700; font-size:30px; color:{C['mute']}; text-align:center; }}
.note {{ position:relative; margin-top:18px; background:#18223A; border:3px solid {C['line']}; border-radius:22px; padding:16px 20px; }}
.note .app {{ font-family:'JetBrains Mono',monospace; font-weight:700; font-size:28px; letter-spacing:0.08em; color:{C['mute']}; }}
.note .msg {{ font-weight:800; font-size:34px; margin-top:4px; }}
.note .tag {{ position:absolute; right:16px; top:14px; font-family:'JetBrains Mono',monospace; font-weight:700; font-size:28px;
  padding:2px 12px; border-radius:8px; color:#0A0F1C; background:{C['green']}; }}
"""


def scene_morgen():
    notes = [("wk", "WECKER", "Ausgeschaltet", "AUS", w("morgen", 0, 2)),
             ("mt", "KALENDER", "Meeting 09:00", "ABGESAGT", w("morgen", 2, 1)),
             ("st", "NAVI", "Arbeitsweg", "0 KM STAU", w("morgen", 3, 1))]
    nh = "".join(f'<div class="note" id="mg-{i}"><div class="app">{a}</div><div class="msg">{m}</div>'
                 f'<div class="tag">{t}</div></div>' for i, a, m, t, _ in notes)
    body = f"""
    <div class="phone" id="mg-ph"><div class="notch"></div><div class="scr">
      <div class="clock">07:30</div>{nh}
      <div class="note" id="mg-sun" style="border-color:{C['green']};text-align:center">
        <div class="msg" style="font-size:44px;color:{C['green']}">URLAUBS-MODUS</div></div>
    </div></div>"""
    js = [f'    tl.fromTo("#mg-ph", {{y:260, opacity:0}}, {{y:0, opacity:1, duration:0.6, ease:"expo.out"}}, 0);']
    for i, _, _, _, at in notes:
        js.append(f'    tl.fromTo("#mg-{i}", {{y:-40, opacity:0}}, {{y:0, opacity:1, duration:0.35, ease:"expo.out"}}, {at});')
        js.append(f'    tl.fromTo("#mg-{i} .tag", {{scale:1.6, opacity:0}}, {{scale:1, opacity:1, duration:0.2, ease:"back.out(2)"}}, {at + 0.25});')
    js.append(f'    tl.fromTo("#mg-sun", {{scale:0.8, opacity:0}}, {{scale:1, opacity:1, duration:0.3, ease:"back.out(2)"}}, {w("morgen", 1, 3)});')
    return scene_html("morgen", PHONE_CSS, body, "\n".join(js))


def scene_notruf():
    css = PHONE_CSS + f"""
.call {{ text-align:center; padding-top:40px; }}
.call .who {{ font-family:'JetBrains Mono',monospace; font-weight:700; font-size:32px; letter-spacing:0.14em; color:{C['red']}; }}
.call .num {{ font-weight:900; font-size:150px; line-height:1.1; }}
.call .st {{ position:relative; height:60px; font-family:'JetBrains Mono',monospace; font-weight:700; font-size:34px; color:{C['mute']}; }}
.call .st span {{ position:absolute; left:0; right:0; }}
.call .tm {{ font-family:'JetBrains Mono',monospace; font-weight:700; font-size:44px; margin-top:24px; font-variant-numeric:tabular-nums; }}
.hang {{ position:absolute; left:50%; bottom:60px; width:130px; height:130px; margin-left:-65px; border-radius:50%; background:{C['red']}; }}
.hang i {{ position:absolute; left:30px; top:52px; width:70px; height:26px; border-radius:13px; background:#fff; }}
.ring {{ position:absolute; left:540px; top:770px; width:10px; height:10px; border-radius:50%; border:6px solid {C['red']}; opacity:0; }}
"""
    rings = "".join(f'<div class="ring" id="nr-r{i}"></div>' for i in range(4))
    body = f"""{rings}
    <div class="phone" id="nr-ph"><div class="notch"></div><div class="scr call">
      <div class="who">Notruf</div><div class="num">112</div>
      <div class="st"><span id="nr-s0">Wählt …</span><span id="nr-s1" style="opacity:0">Klingelt …</span>
        <span id="nr-s2" style="opacity:0;color:{C['red']}">KEINE ANTWORT</span></div>
      <div class="tm"><span id="nr-tm">00:00</span></div>
      <div class="hang"><i></i></div>
    </div></div>"""
    k1, k2, n = w("notruf", 2, 1), w("notruf", 3, 1), w("notruf", 4, 0)
    end = E["notruf"] - S["notruf"]
    js = f"""
    tl.fromTo("#nr-ph", {{scale:0.85, opacity:0}}, {{scale:1, opacity:1, duration:0.5, ease:"expo.out"}}, 0);
    (function(){{ const o={{v:0}}; const el=document.getElementById("nr-tm");
      tl.fromTo(o,{{v:0}},{{v:{end - 1.2:.2f},duration:{end - 1.2:.2f},ease:"none",onUpdate:()=>{{const s=Math.floor(o.v*6); el.textContent="00:"+String(Math.min(s,59)).padStart(2,"0");}}}},1.2); }})();
    tl.set("#nr-s0", {{opacity:0}}, {k1 - 0.1});
    tl.set("#nr-s1", {{opacity:1}}, {k1 - 0.1});
    tl.set("#nr-s1", {{opacity:0}}, {n});
    tl.fromTo("#nr-s2", {{opacity:0, scale:1.4}}, {{opacity:1, scale:1, duration:0.25, ease:"expo.out"}}, {n});
    tl.to("#nr-tm", {{color:"{C['red']}", duration:0.1}}, {n});
"""
    for i, t in enumerate((k1, k1 + 0.35, k2, k2 + 0.35)):
        js += f'    tl.fromTo("#nr-r{i}", {{scale:1, opacity:0.9}}, {{scale:90, opacity:0, duration:0.9, ease:"power2.out"}}, {t:.3f});\n'
    return scene_html("notruf", css, body, js)


# ------------------------------------------------------------------ Internet + Akku

def scene_netz():
    css = f"""
#nz-wifi {{ position:absolute; left:290px; top:400px; }}
#nz-x {{ position:absolute; left:0; right:0; top:560px; text-align:center; }}
#nz-x span {{ display:inline-block; font-weight:900; font-size:64px; color:#fff; background:{C['red']}; padding:6px 28px; border-radius:16px; }}
#nz-bat {{ position:absolute; left:220px; top:760px; width:600px; height:260px; border:14px solid #E6E9F0; border-radius:40px; padding:16px; }}
#nz-bat:after {{ content:""; position:absolute; right:-44px; top:72px; width:30px; height:90px; border-radius:0 14px 14px 0; background:#E6E9F0; }}
#nz-fill {{ width:100%; height:100%; border-radius:22px; background:{C['green']}; transform-origin:left center; }}
#nz-pct {{ position:absolute; inset:0; display:flex; align-items:center; justify-content:center; font-weight:900; font-size:110px;
  color:#fff; -webkit-text-stroke:10px #0A0F1C; paint-order:stroke fill; font-variant-numeric:tabular-nums; }}
"""
    arcs = "".join(f'<path class="nz-a" d="M {250 - r} {300 - r * 0.15} Q 250 {300 - r * 1.25} {250 + r} {300 - r * 0.15}" />'
                   for r in (200, 140, 80))
    body = f"""
    <svg id="nz-wifi" viewBox="0 0 500 340" width="500" height="340">
      <g fill="none" stroke="{C['teal']}" stroke-width="30" stroke-linecap="round">{arcs}</g>
      <circle id="nz-dot" cx="250" cy="290" r="30" fill="{C['teal']}"/>
    </svg>
    <div id="nz-x"><span>KEIN NETZ</span></div>
    <div id="nz-bat"><div id="nz-fill"></div><div id="nz-pct"><span id="nz-num">100</span>%</div></div>"""
    i0, a, p = w("netz", 1, 2), w("netz", 2, 1), w("netz", 3, 0)
    js = f"""
    tl.fromTo("#nz-wifi", {{scale:0.8, opacity:0}}, {{scale:1, opacity:1, duration:0.5, ease:"expo.out"}}, 0);
    tl.fromTo("#nz-bat", {{y:80, opacity:0}}, {{y:0, opacity:1, duration:0.5, ease:"expo.out"}}, 0.15);
    tl.fromTo(".nz-a", {{opacity:1}}, {{opacity:0.12, duration:0.12, ease:"none", stagger:0.18}}, {i0 - 0.4});
    tl.to(["#nz-dot", ".nz-a"], {{fill:"{C['red']}", stroke:"{C['red']}", duration:0.1}}, {i0});
    tl.fromTo("#nz-x span", {{scale:1.6, opacity:0}}, {{scale:1, opacity:1, duration:0.25, ease:"expo.out"}}, {i0 + 0.05});
    tl.fromTo("#nz-fill", {{scaleX:1, backgroundColor:"{C['green']}"}}, {{scaleX:0.12, backgroundColor:"{C['red']}", duration:{p - 0.4:.2f},
      ease:"power2.inOut"}}, 0.4);
"""
    js += js_count("nz-num", 100, 12, 0.4, p - 0.4, ease="power2.inOut")
    js += f'    tl.fromTo("#nz-bat", {{borderColor:"#E6E9F0"}}, {{borderColor:"{C["red"]}", duration:0.1}}, {p});\n'
    return scene_html("netz", css, body, js)


# ------------------------------------------------------------------ Müll

def scene_muell():
    r = rng(21)
    bags = []
    rows = [(9, 1110), (7, 1040), (5, 970), (3, 900), (1, 840)]
    for n, y in rows:
        for i in range(n):
            x = 540 + (i - (n - 1) / 2) * 92 + r.randint(-12, 12)
            col = r.choice(["#2C3A2E", "#3A4436", "#262D3D", "#34405C"])
            rot = r.randint(-14, 14)
            bags.append(f'<g class="mu-bag" transform="translate({x:.0f},{y}) rotate({rot})"><g>'
                        f'<path d="M -50 0 Q -56 -70 -18 -82 L -8 -100 L 8 -100 L 18 -82 Q 56 -70 50 0 Z" fill="{col}"/>'
                        f'<path d="M -14 -100 L 0 -116 L 14 -100" stroke="{col}" stroke-width="8" fill="none"/></g></g>')
    flies = "".join(f'<circle class="mu-fly" cx="{r.randint(330, 750)}" cy="{r.randint(700, 860)}" r="6" fill="#0A0F1C"/>' for _ in range(9))
    stink = "".join(f'<path class="mu-st" d="M {x} 820 q 20 -30 0 -60 q -20 -30 0 -60 q 20 -30 0 -60" stroke="{C["green"]}" stroke-width="9" fill="none" stroke-linecap="round" opacity="0"/>'
                    for x in (430, 540, 650))
    body = hud_card("mc", "Tage ohne Müllabfuhr", "0", color=C["gold"], top=290) + f"""
    <svg data-layout-allow-overflow viewBox="0 0 1080 1920" width="1080" height="1920" style="position:absolute;left:0;top:0">
      <rect x="0" y="1100" width="1080" height="820" fill="#151C2C"/>
      <rect x="0" y="1100" width="1080" height="12" fill="#2A3652"/>
      <g transform="translate(110,1110)"><rect x="0" y="-240" width="150" height="240" rx="14" fill="{C['teal']}" opacity="0.8"/>
        <rect x="-10" y="-262" width="170" height="30" rx="10" fill="{C['teal']}"/></g>
      {''.join(bags)}
      {stink}
      <g id="mu-flies">{flies}</g>
    </svg>"""
    st = w("muell", 2, 2)
    js = js_count("mc-num", 0, 14, 0.2, 1.8, ease="power1.inOut")
    js += f"""
    tl.fromTo(".mu-bag > g", {{y:-700, opacity:1}}, {{y:0, opacity:1, duration:0.45, ease:"bounce.out", stagger:0.06}}, 0.1);
    tl.fromTo(".mu-st", {{opacity:0, y:20}}, {{opacity:0.9, y:-30, duration:0.6, ease:"power2.out", stagger:0.12}}, {st - 0.2});
    tl.fromTo(".mu-fly", {{opacity:0}}, {{opacity:1, duration:0.1, stagger:0.04}}, {st - 0.3});
    tl.fromTo(".mu-fly", {{x:0, y:0}}, {{x:40, y:-25, duration:0.18, yoyo:true, repeat:9, ease:"sine.inOut", stagger:0.03}}, {st - 0.3});
"""
    return scene_html("muell", "", body, js)


# ------------------------------------------------------------------ Geld

def scene_geld():
    body = hud_card("gc", "Wert deines Geldes", "100", unit="€", color=C["green"], top=290) + f"""
    <div id="gd-note" style="position:absolute;left:110px;top:580px;width:860px;height:430px;border-radius:26px;
      background:#6FAE73;border:8px solid #4E8C55;overflow:hidden">
      <div style="position:absolute;left:-60px;top:-60px;width:360px;height:360px;border-radius:50%;background:#83C287"></div>
      <div style="position:absolute;right:40px;top:30px;font-weight:900;font-size:150px;color:#E9F5E6">100</div>
      <div style="position:absolute;left:46px;bottom:30px;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:44px;letter-spacing:0.3em;color:#E9F5E6">EURO</div>
      <div style="position:absolute;left:330px;top:120px;width:200px;height:200px;border-radius:50%;border:10px solid #E9F5E6;opacity:0.5"></div>
      <div id="gd-grey" style="position:absolute;inset:0;background:#3B4254;opacity:0"></div>
    </div>
    <div id="gd-stamp" style="position:absolute;left:0;right:0;top:720px;text-align:center">
      <span style="display:inline-block;font-weight:900;font-size:110px;color:{C['red']};border:10px solid {C['red']};border-radius:18px;
        padding:6px 30px;background:rgba(14,21,36,0.8)">WERTLOS</span></div>"""
    n, k = w("geld", 1, 2), w("geld", 2, 5)
    js = js_count("gc-num", 100, 0, n - 0.3, 0.9, ease="power3.in")
    js += f"""
    tl.fromTo("#gd-note", {{y:120, rotation:4, opacity:0}}, {{y:0, rotation:-3, opacity:1, duration:0.6, ease:"expo.out"}}, 0);
    tl.to("#gc-num", {{color:"{C['red']}", duration:0.1}}, {n + 0.6});
    tl.fromTo("#gd-grey", {{opacity:0}}, {{opacity:0.7, duration:0.6, ease:"power2.inOut"}}, {n - 0.2});
    tl.to("#gd-note", {{scale:0.86, rotation:-9, duration:0.6, ease:"power2.inOut"}}, {n - 0.2});
    tl.fromTo("#gd-stamp span", {{scale:2.2, rotation:-8, opacity:0}}, {{scale:1, rotation:-8, opacity:1, duration:0.22, ease:"expo.out"}}, {k});
"""
    return scene_html("geld", "", body, js)


# ------------------------------------------------------------------ Wende: einer steht auf

def person(pid, x, col):
    """Strichfigur im Stil von Referenz A, Füße auf y=1110."""
    return (f'<div id="{pid}" style="position:absolute;left:{x - 40}px;top:770px;width:80px;height:340px;z-index:2">'
            f'<div class="pp" style="position:absolute;inset:0">'
            f'<div style="position:absolute;left:26px;top:230px;width:26px;height:110px;border-radius:13px;background:{col}"></div>'
            f'<div style="position:absolute;left:44px;top:230px;width:26px;height:110px;border-radius:13px;background:{col};opacity:0.75"></div>'
            f'<div style="position:absolute;left:14px;top:90px;width:64px;height:150px;border-radius:30px;background:{col}"></div>'
            f'<div style="position:absolute;left:6px;top:8px;width:80px;height:80px;border-radius:50%;background:#F4F1E6"></div>'
            f'</div></div>')


def scene_wende():
    blds, wins, nwin = skyline("wd")
    body = hud_card("dc", "Menschen bei der Arbeit", "0", color=C["green"], top=290) + f"""
    <div style="position:absolute;inset:0;background:linear-gradient(180deg,#0B1530 0%,#1A2550 60%,#3A3560 100%)"></div>
    <svg data-layout-allow-overflow viewBox="0 0 1080 1920" width="1080" height="1920" style="position:absolute;left:0;top:0">
      {blds}<g id="wd-wins">{wins}</g>
      <rect x="0" y="1110" width="1080" height="810" fill="#0B101D"/>
    </svg>
    {person("wd-p1", 400, C['teal'])}
    {person("wd-p2", 700, C['coral'])}"""
    e, g, nx = w("wende", 1, 0), w("wende", 3, 3), w("wende", 4, 2)
    end = E["wende"] - S["wende"]
    js = f"""
    tl.fromTo("#wd-p1 .pp", {{rotation:-90, opacity:0.6}}, {{rotation:0, opacity:1, duration:0.6, ease:"back.out(1.4)",
      transformOrigin:"50% 100%"}}, {e - 0.1});
    tl.fromTo("#wd-p1", {{x:0}}, {{x:160, duration:{g - e - 0.4:.2f}, ease:"power1.inOut"}}, {e + 0.6});
    tl.fromTo("#wd-p2 .pp", {{rotation:90, opacity:0}}, {{rotation:0, opacity:1, duration:0.6, ease:"back.out(1.4)",
      transformOrigin:"50% 100%"}}, {nx - 0.2});
    tl.fromTo(".wd-win", {{opacity:0}}, {{opacity:1, duration:0.05, stagger:{1.2 / nwin:.4f}, ease:"none"}}, {nx});
    tl.fromTo("#dc", {{borderColor:"{C['line']}"}}, {{borderColor:"{C['green']}", duration:0.15}}, {e + 0.3});
    (function(){{ const el=document.getElementById("dc-num"); const o={{t:0}};
      const f=(n)=>String(n).replace(/\\B(?=(\\d{{3}})+(?!\\d))/g,".");
      tl.fromTo(o,{{t:0}},{{t:{end:.3f},duration:{end:.3f},ease:"none",onUpdate:()=>{{
        const t=o.t; let n=0;
        if (t>={e + 0.3:.3f}) n=1;
        if (t>={nx:.3f}) n=2;
        if (t>={nx + 0.3:.3f}) {{ const p=Math.min(1,(t-{nx + 0.3:.3f})/{end - nx - 0.4:.3f}); n=Math.max(2,Math.round(48213*p*p*p)); }}
        el.textContent=f(n); }}}},0); }})();
"""
    return scene_html("wende", ".hudcard { z-index:3; }", body, js)


# ------------------------------------------------------------------ zusammensetzen

SCENES = [
    ("hook", scene_hook()), ("welt", scene_welt()), ("morgen", scene_morgen()), ("verkehr", scene_verkehr()),
    ("notruf", scene_notruf()), ("strom", scene_strom()), ("netz", scene_netz()), ("essen", scene_essen()),
    ("wasser", scene_wasser()), ("muell", scene_muell()), ("geld", scene_geld()), ("himmel", scene_himmel()),
    ("wende", scene_wende()), ("loop", scene_loop()),
]

SFX = [
    (wa("hook", 1, 1), "ping.mp3", 0.5),
    (S["welt"] - 0.15, "whoosh-short.mp3", 0.5),
    (wa("welt", 2, 2) + 0.2, "glitch-1.mp3", 0.25),
    (S["morgen"] - 0.15, "whoosh.mp3", 0.5),
    (wa("morgen", 0, 2) + 0.25, "pop.mp3", 0.4),
    (wa("morgen", 1, 3), "notification.mp3", 0.35),
    (wa("morgen", 2, 1) + 0.25, "pop.mp3", 0.4),
    (wa("morgen", 3, 1) + 0.25, "pop.mp3", 0.4),
    (S["verkehr"] - 0.15, "whoosh-short.mp3", 0.5),
    (wa("verkehr", 1, 1) + 0.1, "pop.mp3", 0.5),
    (wa("verkehr", 2, 1) + 0.1, "pop.mp3", 0.5),
    (wa("verkehr", 2, 1) + 0.35, "click-soft.mp3", 0.5),
    (wa("verkehr", 3, 1) + 0.1, "pop.mp3", 0.5),
    (S["notruf"] - 0.15, "whoosh.mp3", 0.5),
    (wa("notruf", 2, 1), "ping.mp3", 0.45),
    (wa("notruf", 3, 1), "ping.mp3", 0.45),
    (wa("notruf", 4, 0), "error.mp3", 0.45),
    (S["strom"] - 0.15, "whoosh-short.mp3", 0.5),
    (wa("strom", 1, 2) + 0.05, "impact-bass-1.mp3", 0.6),
    (S["netz"] - 0.15, "whoosh.mp3", 0.5),
    (wa("netz", 1, 2), "glitch-2.mp3", 0.25),
    (wa("netz", 3, 0), "click-soft.mp3", 0.5),
    (S["essen"] - 0.15, "whoosh-short.mp3", 0.5),
    (wa("essen", 1, 3), "impact-bass-2.mp3", 0.6),
    (wa("essen", 2, 1), "pop.mp3", 0.45),
    (S["wasser"] - 0.15, "whoosh.mp3", 0.5),
    (wa("wasser", 2, 1) + 0.85, "click-soft.mp3", 0.4),
    (S["muell"] - 0.15, "whoosh-short.mp3", 0.5),
    (S["muell"] + 0.3, "pop.mp3", 0.35),
    (S["muell"] + 0.9, "pop.mp3", 0.35),
    (S["geld"] - 0.15, "whoosh.mp3", 0.5),
    (wa("geld", 2, 5), "impact-bass-2.mp3", 0.55),
    (S["himmel"] - 0.2, "whoosh-cinematic.mp3", 0.35),
    (wa("himmel", 2, 3), "sparkle.mp3", 0.5),
    (S["wende"] - 0.15, "whoosh-short.mp3", 0.5),
    (wa("wende", 3, 3), "chime.mp3", 0.35),
    (S["loop"] - 0.15, "whoosh.mp3", 0.5),
    (wa("loop", 2, 1), "ping.mp3", 0.5),
]

CHECKLIST = [
    (wa("verkehr", 3, 1) + 0.3, "✕ VERKEHR", C["red"]),
    (wa("notruf", 4, 0) + 0.3, "✕ NOTRUF", C["red"]),
    (wa("strom", 1, 2) + 0.1, "✕ STROM", C["red"]),
    (wa("netz", 1, 2) + 0.3, "✕ INTERNET", C["red"]),
    (wa("essen", 1, 3) + 0.1, "✕ ESSEN", C["red"]),
    (wa("wasser", 2, 1) + 0.2, "✕ WASSER", C["red"]),
    (wa("geld", 1, 2) + 0.3, "✕ GELD", C["red"]),
    (wa("himmel", 2, 3) + 0.1, "✓ LUFT", C["green"]),
]

if __name__ == "__main__":
    write_project(HERE, "Was wäre, wenn niemand mehr arbeiten geht?",
                  [(sid, S[sid], E[sid], html) for sid, html in SCENES],
                  SFX, CHECKLIST, TOTAL, sfx_root=SFX_ROOT, check_end=S["wende"])
    print("ok:", ", ".join(f"{sid} {fmt(S[sid])}-{fmt(E[sid])}" for sid, _ in SCENES), "| total", TOTAL)
