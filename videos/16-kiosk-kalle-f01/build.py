#!/usr/bin/env python3
"""Kiosk-Kalle – Folge 1 (Pilot). Format: Community-Serie (Skill tiktok-community-serie).

1. python3 ../../tools/align.py . assets/source/take1.mp3   (ElevenLabs „Timon“ → voice.wav + timings.json)
2. python3 build.py                                          (index.html + compositions/)
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "serien" / "kiosk-kalle"))
from simkit import fmt, load_timings  # noqa: E402
import seriekit as sk  # noqa: E402
from seriekit import pop_in, pop_out, shake, hop, breathe, punch, walk_in, lautmalerei, red_ring, hide, show  # noqa: E402
import figuren as fg  # noqa: E402
import orte  # noqa: E402

T = load_timings(HERE)
TOTAL = round(T["duration"] + 1.6, 2)
B = {b["id"]: b for b in T["beats"]}


def L(bid, li):
    return B[bid]["lines"][li]["start"]


def Wd(bid, li, wi):
    return B[bid]["lines"][li]["words"][wi]["start"]


def cut(bid, li):
    return round(max(0.0, L(bid, li) - 0.08), 3)


def place(svg, cx, fy, z=2):
    """SVG-Figur so positionieren, dass (0,0) der Figur bei (cx, fy) liegt."""
    vb = [float(x) for x in re.search(r'viewBox="([^"]+)"', svg).group(1).split()]
    w = float(re.search(r'width="([\d.]+)"', svg).group(1))
    s = w / vb[2]
    left = cx + vb[0] * s
    top = fy + vb[1] * s
    return svg.replace('style="overflow:visible"', f'style="overflow:visible;left:{left:.0f}px;top:{top:.0f}px;z-index:{z}"', 1)


SFX = []


def sfx(t, f, vol=0.6):
    SFX.append((round(t, 3), f, vol))


# ------------------------------------------------------------------ kleine Requisiten

def oma_polaroid(pid):
    return f"""<div id="{pid}" class="card" style="left:640px;top:380px;width:330px;height:390px;padding:22px;opacity:0;transform:rotate(6deg)">
  <svg width="270" height="270" viewBox="0 0 150 150"><rect width="150" height="150" fill="#FCE9D2"/>
  <circle cx="75" cy="72" r="36" fill="#FFD6B0" stroke="#1B1530" stroke-width="4"/><circle cx="75" cy="32" r="22" fill="#C9C9D4" stroke="#1B1530" stroke-width="4"/>
  <circle cx="61" cy="70" r="10" fill="none" stroke="#1B1530" stroke-width="3"/><circle cx="89" cy="70" r="10" fill="none" stroke="#1B1530" stroke-width="3"/>
  <path d="M 62 92 Q 75 101 88 92" fill="none" stroke="#1B1530" stroke-width="3"/><path d="M 25 150 Q 75 100 125 150 Z" fill="#B05CF0" stroke="#1B1530" stroke-width="4"/>
  <path d="M 112 0 L 150 0 L 150 38 Z" fill="#1B1530"/></svg>
  <div style="text-align:center;font-weight:900;font-size:36px;margin-top:10px">Oma Erika</div></div>"""


def key_svg(pid, x, y):
    return (f'<svg id="{pid}" class="abs" style="left:{x}px;top:{y}px;opacity:0" width="190" height="110" viewBox="0 0 190 110">'
            '<circle cx="50" cy="55" r="36" fill="#FFC233" stroke="#1B1530" stroke-width="7"/><circle cx="50" cy="55" r="13" fill="#9ED8F5" stroke="#1B1530" stroke-width="6"/>'
            '<path d="M 84 48 L 180 48 L 180 64 L 160 64 L 160 84 L 140 84 L 140 64 L 84 64 Z" fill="#FFC233" stroke="#1B1530" stroke-width="7" stroke-linejoin="round"/></svg>')


def schuld_karte(pid):
    return (f'<div id="{pid}" class="card" style="left:190px;top:390px;width:700px;height:300px;opacity:0;text-align:center;'
            f'border-color:#1B1530;background:#FFF4F4">'
            '<div style="background:#E8413A;color:#fff;font-weight:900;font-size:44px;padding:14px 0;border-radius:22px 22px 0 0;letter-spacing:0.06em">MIETSCHULDEN</div>'
            '<div style="font-weight:900;font-size:150px;color:#E8413A;line-height:1.25">3.000 €</div></div>')


def stempel(pid, text, x, y, size=120):
    return (f'<div id="{pid}" class="abs" style="left:{x}px;top:{y}px;opacity:0;transform:rotate(-12deg);border:14px solid #E0202E;'
            f'border-radius:24px;padding:4px 30px;color:#E0202E;font-weight:900;font-size:{size}px;background:rgba(255,255,255,0.75)">{text}</div>')


def konto_karte(pid):
    return (f'<div id="{pid}" class="card" style="z-index:5;left:120px;top:1020px;width:840px;height:250px;opacity:0;display:flex;align-items:center;gap:30px;padding:0 40px">'
            '<svg width="150" height="110" viewBox="0 0 150 110"><rect x="4" y="4" width="142" height="102" rx="14" fill="#3B6FF0" stroke="#1B1530" stroke-width="7"/>'
            '<rect x="4" y="28" width="142" height="20" fill="#1B1530"/><rect x="20" y="66" width="34" height="24" rx="5" fill="#FFC233"/></svg>'
            '<div><div style="font-weight:900;font-size:40px;color:#7A7490">KONTOSTAND</div>'
            '<div style="font-weight:900;font-size:110px;color:#E8413A;line-height:1">0,00 €</div></div></div>')


def uhr_karte(pid, text):
    return (f'<div id="{pid}" class="card" style="left:330px;top:400px;width:420px;height:180px;opacity:0;background:#22303F;'
            f'display:flex;align-items:center;justify-content:center;font-weight:900;font-size:120px;color:#4BE08A;font-variant-numeric:tabular-nums">{text}</div>')


def blatt(pid, x, y, rot):
    return (f'<svg id="{pid}" class="abs" style="left:{x}px;top:{y}px;opacity:0;z-index:4" width="90" height="110" viewBox="0 0 90 110">'
            f'<g transform="rotate({rot} 45 55)"><rect x="8" y="8" width="74" height="94" rx="6" fill="#fff" stroke="#1B1530" stroke-width="5"/>'
            '<path d="M 20 30 L 70 30 M 20 48 L 70 48 M 20 66 L 54 66" stroke="#E8413A" stroke-width="5"/></g></svg>')


def muenzen(pid, x, y):
    coins = "".join(f'<ellipse cx="{cx}" cy="{cy}" rx="26" ry="11" fill="#F5C542" stroke="#1B1530" stroke-width="5"/>'
                    for cx, cy in ((40, 60), (80, 64), (60, 50), (110, 58), (90, 44)))
    return f'<svg id="{pid}" class="abs" style="left:{x}px;top:{y}px;opacity:0;z-index:4" width="150" height="90" viewBox="0 0 150 90">{coins}</svg>'


def tropfen(pid, x, y):
    return (f'<svg id="{pid}" class="abs" style="left:{x}px;top:{y}px;opacity:0;z-index:3" width="40" height="56" viewBox="0 0 40 56">'
            '<path d="M 20 4 Q 36 30 32 40 Q 26 54 14 50 Q 2 44 8 30 Z" fill="#7FD3FF" stroke="#1B1530" stroke-width="4"/></svg>')


def thermo_karte(pid):
    return (f'<div id="{pid}" class="card" style="left:90px;top:400px;width:360px;height:170px;opacity:0;display:flex;align-items:center;'
            'justify-content:center;gap:18px;font-weight:900;font-size:90px;color:#E8413A">'
            '<svg width="50" height="120" viewBox="0 0 50 120"><rect x="15" y="6" width="20" height="86" rx="10" fill="#fff" stroke="#1B1530" stroke-width="5"/>'
            '<rect x="20" y="30" width="10" height="66" fill="#E8413A"/><circle cx="25" cy="98" r="18" fill="#E8413A" stroke="#1B1530" stroke-width="5"/></svg>28°</div>')


def gluehbirne(pid, x, y):
    return (f'<svg id="{pid}" class="abs" style="left:{x}px;top:{y}px;opacity:0;z-index:4" width="200" height="240" viewBox="0 0 200 240">'
            '<g stroke="#FFC233" stroke-width="10" stroke-linecap="round"><path d="M 100 10 L 100 30"/><path d="M 30 40 L 45 55"/>'
            '<path d="M 170 40 L 155 55"/><path d="M 10 110 L 30 110"/><path d="M 190 110 L 170 110"/></g>'
            '<circle cx="100" cy="110" r="60" fill="#FFE14A" stroke="#1B1530" stroke-width="8"/>'
            '<rect x="72" y="166" width="56" height="44" rx="8" fill="#9AA0AE" stroke="#1B1530" stroke-width="7"/></svg>')


def geier_avatar():
    svg = fg.geier("gav", w=84)
    return re.sub(r'viewBox="[^"]+"', 'viewBox="-110 -770 220 230"', svg).replace('height="', 'data-h="', 1).replace(
        'style="overflow:visible"', 'style="width:84px;height:84px"', 1)


ICON_KONSOLE = ('<svg width="120" height="120" viewBox="0 0 120 120"><path d="M 14 50 Q 10 92 32 92 Q 46 92 52 78 L 68 78 Q 74 92 88 92 Q 110 92 106 50 '
                'Q 102 32 84 32 L 36 32 Q 18 32 14 50 Z" fill="#fff" stroke="#1B1530" stroke-width="6"/><path d="M 32 52 L 32 68 M 24 60 L 40 60" stroke="#1B1530" '
                'stroke-width="6" stroke-linecap="round"/><circle cx="84" cy="54" r="6" fill="#E8413A"/><circle cx="94" cy="66" r="6" fill="#3DDC84"/></svg>')
ICON_GELD = ('<svg width="120" height="120" viewBox="0 0 120 120"><path d="M 44 30 L 76 30 L 68 42 Q 100 58 100 84 Q 100 108 60 108 Q 20 108 20 84 '
             'Q 20 58 52 42 Z" fill="#FFC233" stroke="#1B1530" stroke-width="6" stroke-linejoin="round"/><text x="60" y="92" text-anchor="middle" '
             'font-family="Inter" font-weight="900" font-size="40" fill="#1B1530">€</text></svg>')


# ------------------------------------------------------------------ Szenen

def s_intro(s0, s1):
    r = lambda t: round(t - s0, 3)  # noqa: E731
    body = orte.kiosk_aussen("ka", shutter=1) + place(fg.kalle("k", w=440, mund="grin"), 540, 1640)
    body += lautmalerei("hook", "30 TAGE", 150, 400, size=190, color=sk.YEL, rot=-4).replace("opacity:0", "opacity:1")
    body += ('<div id="tag" class="bubble" style="left:110px;top:760px;opacity:0;font-size:46px">KALLE, 24</div>'
             + oma_polaroid("oma") + key_svg("key", 90, 1150) + lautmalerei("geerbt", "GEERBT!", 80, 520, size=110, rot=-8)
             + schuld_karte("schuld"))
    js = breathe("#k", 0, s1 - s0)
    js += f'tl.fromTo("#hook",{{scale:1.25}},{{scale:1,duration:0.35,ease:"back.out(2)"}},0);\n'
    js += pop_out("#hook", r(L("praemisse", 1)) + 0.9)
    js += pop_in("#tag", r(Wd("praemisse", 1, 3))) + hop("#k", r(Wd("praemisse", 1, 3)), 50)
    js += pop_in("#oma", r(Wd("praemisse", 3, 1)), rot=6)
    js += pop_in("#key", r(Wd("praemisse", 4, 3)), rot=-10) + pop_in("#geerbt", r(Wd("praemisse", 4, 3)) + 0.1, rot=-8)
    js += fg.face_js("k", "open", r(Wd("praemisse", 4, 3)))
    t = r(L("praemisse", 5))
    js += pop_out("#tag", t - 0.2) + pop_out("#oma", t - 0.2) + pop_out("#geerbt", t - 0.2) + pop_out("#key", t - 0.2)
    js += f'tl.fromTo("#schuld",{{scale:2.4,opacity:0,rotation:-8}},{{scale:1,opacity:1,rotation:-3,duration:0.22,ease:"power3.in"}},{t});\n'
    js += shake("#schuld", t + 0.22, n=3, amp=12) + fg.face_js("k", "shock", t + 0.2) + fg.eyes_js("k", "wide", t + 0.2)
    js += shake("#k", t + 0.25, n=4, amp=8)
    sfx(s0 + 0.0, "impact-bass-2.mp3", 0.55)
    sfx(Wd("praemisse", 1, 3), "pop.mp3", 0.5)
    sfx(Wd("praemisse", 3, 1), "pop.mp3", 0.5)
    sfx(Wd("praemisse", 4, 3), "sparkle.mp3", 0.5)
    sfx(L("praemisse", 5), "impact-bass-2.mp3", 0.7)
    return sk.scene("intro", "", body, js)


def s_geier(s0, s1):
    r = lambda t: round(t - s0, 3)  # noqa: E731
    body = orte.kiosk_aussen("ka2", shutter=1) + place(fg.kalle("k", w=400, mund="sad"), 300, 1660)
    body += place(fg.geier("g", w=380, mund="smirk"), 780, 1680, z=3)
    body += '<div id="gb" class="bubble" style="left:330px;top:640px;opacity:0;font-size:42px;z-index:5">30 TAGE, HERR KALLE.</div>'
    body += stempel("st", "RÄUMUNG!", 170, 440, 130) + lautmalerei("tt", "TICK, TACK.", 560, 1190, size=70, color="#fff", rot=6)
    js = walk_in("#g", 0, 600, 0.55) + breathe("#k", 0.3, s1 - s0) + breathe("#g", 0.8, s1 - s0, amp=0.015)
    js += pop_in("#gb", r(L("praemisse", 8)))
    t = r(L("praemisse", 9))
    js += pop_out("#gb", t - 0.1)
    js += show("#g-stamp", t + 0.25)
    js += f'tl.fromTo("#st",{{scale:2.6,opacity:0}},{{scale:1,opacity:1,duration:0.2,ease:"power3.in"}},{t + 0.25});\n'
    js += shake("#st", t + 0.45, n=3, amp=10) + fg.face_js("k", "shock", t + 0.3) + fg.eyes_js("k", "wide", t + 0.3)
    js += pop_in("#tt", t + 0.7, rot=6)
    sfx(s0, "whoosh-short.mp3", 0.5)
    sfx(L("praemisse", 8), "pop.mp3", 0.5)
    sfx(L("praemisse", 9) + 0.25, "impact-bass-2.mp3", 0.75)
    return sk.scene("geier", "", body, js)


def s_kopf(s0, s1):
    r = lambda t: round(t - s0, 3)  # noqa: E731
    body = orte.nahaufnahme("na") + place(fg.kalle_kopf("kk", w=1000, mund="grin"), 540, 1201)
    body += red_ring("ring1", 677, 1232, 90) + red_ring("ring2", 540, 640, 170)
    body += lautmalerei("q", "???", 760, 380, size=150, color=sk.YEL, rot=10) + konto_karte("konto")
    js = breathe("#kk", 0, s1 - s0, amp=0.012)
    js += pop_in("#ring1", 0.25) + pop_in("#ring2", 0.55)
    js += pop_in("#q", r(Wd("szene1", 1, 0)), rot=10) + fg.face_js("kk", "flat", r(Wd("szene1", 1, 0)))
    t = r(L("szene1", 2))
    js += pop_out("#ring1", t - 0.15) + pop_out("#ring2", t - 0.15)
    js += f'tl.fromTo("#konto",{{y:300,opacity:0}},{{y:0,opacity:1,duration:0.3,ease:"back.out(1.8)"}},{t});\n'
    js += fg.face_js("kk", "sad", t + 0.3) + fg.eyes_js("kk", "wide", t + 0.3) + shake("#konto", t + 0.9, n=3, amp=10)
    sfx(s0, "whoosh-short.mp3", 0.5)
    sfx(s0 + 0.25, "pop.mp3", 0.45)
    sfx(Wd("szene1", 1, 0), "pop.mp3", 0.5)
    sfx(L("szene1", 2) + 0.9, "error.mp3", 0.6)
    return sk.scene("kopf", "", body, js)


def s_rollladen(s0, s1):
    r = lambda t: round(t - s0, 3)  # noqa: E731
    body = orte.kiosk_aussen("ka3", shutter=1) + place(fg.kalle("k", w=400, mund="flat", pose="up"), 540, 1700)
    body += lautmalerei("rat", "RATTER…", 90, 560, size=110, rot=-8) + lautmalerei("klonk", "KLONK!", 560, 700, size=120, color=sk.RED, rot=8)
    body += uhr_karte("uhr", "11:00") + lautmalerei("offen", "OFFEN!", 300, 600, size=150, color=sk.GRN, rot=-6)
    js = ""
    t1 = r(L("szene1", 4))
    js += pop_in("#rat", t1, rot=-8) + shake("#ka3-shutter", t1, n=7, amp=8, dur=0.045) + fg.face_js("k", "open", t1)
    js += shake("#k", t1, n=6, amp=6, dur=0.05)
    t2 = r(Wd("szene1", 4, 2))
    js += pop_out("#rat", t2 - 0.05) + pop_in("#klonk", t2, rot=8) + fg.face_js("k", "shock", t2) + fg.eyes_js("k", "wide", t2)
    t3 = r(L("szene1", 5))
    js += pop_out("#klonk", t3 - 0.1) + pop_in("#uhr", t3) + fg.face_js("k", "flat", t3) + fg.eyes_js("k", "normal", t3)
    t4 = r(L("szene1", 6))
    js += pop_out("#uhr", t4 + 0.1)
    js += f'tl.to("#ka3-shutter",{{y:-370,duration:0.55,ease:"power2.in"}},{t4});\n'
    js += pop_in("#offen", t4 + 0.55, rot=-6) + fg.face_js("k", "grin", t4 + 0.5) + hop("#k", t4 + 0.55, 60, n=2)
    sfx(s0, "whoosh-short.mp3", 0.5)
    sfx(L("szene1", 4), "ratter.wav", 0.6)
    sfx(Wd("szene1", 4, 2), "impact-bass-2.mp3", 0.6)
    sfx(L("szene1", 5), "pop.mp3", 0.5)
    sfx(L("szene1", 6), "ratter.wav", 0.45)
    sfx(L("szene1", 6) + 0.55, "sparkle.mp3", 0.55)
    return sk.scene("rollladen", "", body, js)


def innen_basis(p, uhr="11:00", night=False, kalle_kw=None):
    kw = dict(w=420, mund="grin")
    kw.update(kalle_kw or {})
    return (orte.kiosk_innen(p, night=night, uhr=uhr) + place(fg.kalle("k", **kw), 300, 1390)
            + orte.theke_front(p + "f").replace('class="abs" style="', 'class="abs" style="z-index:3;'))


def s_horst(s0, s1):
    r = lambda t: round(t - s0, 3)  # noqa: E731
    body = innen_basis("ki1") + place(fg.horst("h", w=360, mund="open"), 820, 1720, z=4)
    body += '<div id="hb" class="bubble" style="left:470px;top:700px;opacity:0;font-size:44px;z-index:6">EINMAL LOTTO, JUNGE!</div>'
    body += lautmalerei("wo", "WO SIND DIE DINGER?!", 60, 450, size=72, rot=-4)
    sheets = [(180, 980, -20), (300, 930, 15), (120, 1060, 30), (420, 990, -35), (250, 1020, 5)]
    body += "".join(blatt(f"bl{i}", x, y, rr) for i, (x, y, rr) in enumerate(sheets))
    js = walk_in("#h", 0, 500, 0.6) + breathe("#k", 0, s1 - s0) + pop_in("#hb", 0.5)
    t = r(L("szene2", 2))
    js += pop_out("#hb", t - 0.1) + fg.face_js("k", "shock", t) + fg.eyes_js("k", "wide", t) + shake("#k", t, n=6, amp=8)
    js += pop_in("#wo", t + 0.15, rot=-4) + fg.face_js("h", "flat", t)
    for i, (x, y, rr) in enumerate(sheets):
        dx = (i - 2) * 120
        js += (f'tl.set("#bl{i}",{{opacity:1}},{t + 0.1 + i * 0.12});\n'
               f'tl.to("#bl{i}",{{x:{dx},y:-420 - {i * 40},rotation:{rr * 6},duration:0.55,'
               f'ease:"power2.out"}},{t + 0.1 + i * 0.12});\n'
               f'tl.to("#bl{i}",{{y:{180 - i * 40},opacity:0,duration:0.8,ease:"power1.in"}},{t + 0.65 + i * 0.12});\n')
    sfx(s0, "whoosh-short.mp3", 0.5)
    sfx(s0 + 0.5, "pop.mp3", 0.5)
    sfx(L("szene2", 2), "click.mp3", 0.6)
    sfx(L("szene2", 2) + 0.15, "pop.mp3", 0.5)
    return sk.scene("horst", "", body, js)


def s_kinder(s0, s1):
    r = lambda t: round(t - s0, 3)  # noqa: E731
    body = innen_basis("ki2", kalle_kw=dict(mund="flat"))
    for i, (cx, col, hair, bag) in enumerate(((690, "#FF7A3D", "#5A3A22", "#3B6FF0"), (840, "#3DDC84", "#E8C04A", "#FF4F8B"),
                                              (985, "#B05CF0", "#1E1E2A", "#FFC233"))):
        body += place(fg.kind(f"c{i}", w=200, shirt=col, hair=hair, bag=bag), cx, 1730, z=4)
    body += muenzen("mz", 120, 1090) + '<div id="cent" class="bubble" style="left:110px;top:960px;opacity:0;z-index:6;background:#FFE14A">30 CENT</div>'
    body += '<div id="kb" class="bubble" style="left:600px;top:1180px;opacity:0;z-index:6">1… 2… 3…</div>'
    body += lautmalerei("min", "+10 MIN", 230, 470, size=90, rot=-6) + lautmalerei("gaehn", "GÄHN…", 40, 760, size=80, color="#fff", rot=-10)
    js = breathe("#k", 0, s1 - s0)
    for i in range(3):
        js += walk_in(f"#c{i}", i * 0.12, 420, 0.5)
    t = r(L("szene2", 5))
    js += pop_in("#mz", t) + pop_in("#cent", t + 0.1)
    t2 = r(L("szene2", 6))
    js += pop_out("#cent", t2) + pop_in("#kb", t2)
    for i in range(3):
        js += hop(f"#c{i}", t2 + 0.1 + i * 0.2, 25, n=2, dur=0.13)
    t3 = r(L("szene2", 7))
    js += pop_in("#min", t3, rot=-6)
    js += f'tl.to("#ki2-mh",{{rotation:"+=720",duration:1.4,ease:"power1.inOut",svgOrigin:"0 0"}},{t3});\n'
    js += f'tl.to("#ki2-hh",{{rotation:"+=60",duration:1.4,ease:"power1.inOut",svgOrigin:"0 0"}},{t3});\n'
    js += fg.eyes_js("k", "closed", t3 + 0.4) + pop_in("#gaehn", t3 + 0.5, rot=-10)
    sfx(s0, "whoosh-short.mp3", 0.5)
    sfx(L("szene2", 5), "kling.wav", 0.6)
    sfx(L("szene2", 7), "tick.wav", 0.6)
    return sk.scene("kinder", "", body, js)


def s_kuehl(s0, s1):
    r = lambda t: round(t - s0, 3)  # noqa: E731
    body = '<div id="zoom" class="abs" style="left:0;top:0;width:1080px;height:1920px;transform-origin:905px 880px">'
    body += orte.kiosk_innen("ki3", uhr="13:00")
    body += "".join(tropfen(f"tr{i}", 800 + (i % 4) * 52, 600 + (i // 4) * 170) for i in range(12)) + '</div>'
    body += place(fg.kalle("k", w=440, mund="grin"), 330, 1780, z=3)
    body += lautmalerei("brz", "BRZZZT…", 560, 420, size=100, rot=8) + lautmalerei("pff", "PFFF.", 600, 560, size=110, color="#fff", rot=-6)
    body += thermo_karte("th")
    js = f'tl.fromTo("#zoom",{{scale:1}},{{scale:1.22,duration:0.5,ease:"power2.out"}},0);\n'
    t = r(L("szene3", 0)) + 0.15
    js += pop_in("#brz", t, rot=8) + shake("#ki3-fridge", t, n=8, amp=6, dur=0.04)
    for k in range(4):
        js += f'tl.set("#ki3-glow",{{opacity:{0.2 if k % 2 == 0 else 1}}},{t + 0.12 * k});\n'
    t2 = r(Wd("szene3", 1, 2))
    js += f'tl.set("#ki3-glow",{{opacity:0}},{t2});\n' + pop_out("#brz", t2) + pop_in("#pff", t2 + 0.05, rot=-6)
    js += fg.face_js("k", "shock", t2) + fg.eyes_js("k", "wide", t2)
    t3 = r(L("szene3", 2))
    for i in range(12):
        js += pop_in(f"#tr{i}", t3 + 0.04 * i)
        js += f'tl.to("#tr{i}",{{y:40,duration:0.8,ease:"power1.in"}},{t3 + 0.3 + 0.04 * i});\n'
    js += pop_out("#pff", t3) + pop_in("#th", t3 + 0.1) + fg.face_js("k", "sad", t3 + 0.4)
    sfx(s0, "whoosh-short.mp3", 0.5)
    sfx(L("szene3", 0) + 0.15, "brumm.wav", 0.6)
    sfx(Wd("szene3", 1, 2), "error.mp3", 0.5)
    sfx(L("szene3", 2) + 0.1, "pop.mp3", 0.45)
    return sk.scene("kuehlschrank", "", body, js)


def s_spaeti(s0, s1):
    r = lambda t: round(t - s0, 3)  # noqa: E731
    body = orte.strasse_spaeti("st") + place(fg.dennis("d", w=200, mund="smirk"), 980, 1175, z=2)
    body += place(fg.kalle("k", w=460, mund="flat"), 260, 1820, z=3)
    body += lautmalerei("neu", "NEU ERÖFFNET!", 420, 1500, size=78, color="#FF4F8B", rot=-6)
    js = f'tl.set("#st-neon",{{opacity:0.15}},0);\n'
    t = r(Wd("szene3", 5, 0))
    for k in range(5):
        js += f'tl.set("#st-neon",{{opacity:{1 if k % 2 == 0 else 0.3}}},{t + 0.08 * k});\n'
    js += hop(".st-q", t + 0.4, 30, n=2, dur=0.14) + hop("#d", t + 0.3, 30, n=1)
    t2 = r(L("szene3", 6))
    js += fg.face_js("k", "shock", t2) + fg.eyes_js("k", "wide", t2) + shake("#k", t2, n=5, amp=8) + pop_in("#neu", t2 + 0.2, rot=-6)
    sfx(s0, "whoosh-short.mp3", 0.5)
    sfx(Wd("szene3", 5, 0), "sparkle.mp3", 0.5)
    sfx(L("szene3", 6) + 0.2, "pop.mp3", 0.5)
    return sk.scene("spaeti", "", body, js)


def s_kasse(s0, s1):
    r = lambda t: round(t - s0, 3)  # noqa: E731
    body = innen_basis("ki4", uhr="21:00", night=True, kalle_kw=dict(mund="sad", pose="hold", item="coins"))
    body += lautmalerei("kl", "KLIMPER…", 520, 520, size=90, rot=6)
    js = breathe("#k", 0, s1 - s0) + pop_in("#kl", 0.35, rot=6)
    t = r(L("wendung", 2))
    js += f'tl.set("#ki4f-disp",{{innerHTML:"3,40"}},{t});\n' + punch("#k", t, 1.04) + fg.eyes_js("k", "wide", t)
    sfx(s0, "whoosh-short.mp3", 0.5)
    sfx(s0 + 0.35, "kling.wav", 0.6)
    sfx(L("wendung", 2), "click.mp3", 0.6)
    return sk.scene("kasse", "", body, js)


def s_handy(s0, s1):
    r = lambda t: round(t - s0, 3)  # noqa: E731
    css, phone = sk.chat_phone("Herr Geier", geier_avatar(),
                               [("m1", "in", "Noch 29 Tage."), ("m2", "in", "Tick, tack. Herr Kalle.")], top=330)
    body = sk.strahlen("bg", "#12333A", "#163E46") + phone
    body += lautmalerei("bz", "BZZZ!", 640, 300, size=100, rot=10).replace("left:", "z-index:6;left:")
    js = (f'tl.fromTo("#phone",{{y:900,rotation:8}},{{y:0,rotation:0,duration:0.4,ease:"back.out(1.4)"}},0);\n'
          + pop_in("#bz", 0.25, rot=10) + shake("#phone", 0.3, n=6, amp=9, dur=0.04) + pop_out("#bz", 1.0))
    t = r(L("wendung", 4))
    js += pop_in("#typ", t)
    t2 = r(L("wendung", 5))
    js += hide("#typ", t2) + pop_in("#m1", t2) + pop_in("#m2", r(L("wendung", 6)))
    sfx(s0 + 0.25, "bzz.wav", 0.7)
    sfx(L("wendung", 5), "pop.mp3", 0.55)
    sfx(L("wendung", 6), "tick.wav", 0.6)
    return sk.scene("handy", css, body, js, bg="#12333A")


def s_plan(s0, s1):
    r = lambda t: round(t - s0, 3)  # noqa: E731
    body = orte.nahaufnahme("na2") + place(fg.kalle_kopf("kp", w=1000, mund="shock", augen="wide"), 540, 1201)
    body += lautmalerei("ex", "!!", 820, 420, size=160, color=sk.RED, rot=10) + gluehbirne("bulb", 760, 330)
    body += lautmalerei("du", "DU ENTSCHEIDEST!", 70, 1010, size=92, rot=-5).replace("left:", "z-index:6;left:")
    js = pop_in("#ex", 0.05, rot=10) + shake("#kp", 0.05, n=4, amp=8)
    t = r(L("wendung", 8))
    js += pop_out("#ex", t - 0.1) + pop_in("#bulb", t) + fg.face_js("kp", "grin", t) + fg.eyes_js("kp", "normal", t)
    t2 = r(L("wendung", 9))
    js += pop_in("#du", t2, rot=-5) + punch("#kp", t2, 1.05)
    sfx(s0, "whoosh-short.mp3", 0.5)
    sfx(s0 + 0.05, "impact-bass-2.mp3", 0.45)
    sfx(L("wendung", 8), "sparkle.mp3", 0.6)
    sfx(L("wendung", 9), "pop.mp3", 0.55)
    return sk.scene("plan", "", body, js)


def s_vote(s0, s1):
    r = lambda t: round(t - s0, 3)  # noqa: E731
    body = sk.strahlen("vbg")
    body += place(fg.kalle_kopf("kv", w=900, mund="open"), 540, 1900).replace("z-index:2", "z-index:1;opacity:0.4")
    body += sk.vote_cards(["WAS SOLL", "KALLE TUN?"], {"titel": "Konsole verkaufen", "unter": "neuer Kühlschrank"},
                          {"titel": "Kredit bei Dennis", "unter": "500 € – mit Zinsen"}, (ICON_KONSOLE, ICON_GELD))
    js = f'tl.fromTo("#vbg-r",{{rotation:0}},{{rotation:40,duration:{s1 - s0},ease:"none",svgOrigin:"540 1000"}},0);\n'
    js += pop_in("#vt", 0.1)
    js += pop_in("#va", r(Wd("abstimmung", 1, 0))) + pop_in("#vb", r(L("abstimmung", 3)))
    t = r(L("abstimmung", 5))
    js += pop_in("#vpill", t) + punch("#va", t, 1.06) + punch("#vb", r(Wd("abstimmung", 5, 2)), 1.06)
    t2 = r(L("abstimmung", 6))
    js += punch("#vpill", t2, 1.1)
    sfx(s0, "whoosh-short.mp3", 0.5)
    sfx(s0 + 0.1, "pop.mp3", 0.5)
    sfx(Wd("abstimmung", 1, 0), "pop.mp3", 0.55)
    sfx(L("abstimmung", 3), "pop.mp3", 0.55)
    sfx(L("abstimmung", 5), "sparkle.mp3", 0.5)
    return sk.scene("abstimmung", sk.VOTE_CSS, body, js, bg="#12333A")


# ------------------------------------------------------------------ Zusammenbau

CUTS = [
    ("intro", 0.0, s_intro),
    ("geier", cut("praemisse", 7), s_geier),
    ("kopf", cut("szene1", 0), s_kopf),
    ("rollladen", cut("szene1", 3), s_rollladen),
    ("horst", cut("szene2", 0), s_horst),
    ("kinder", cut("szene2", 4), s_kinder),
    ("kuehlschrank", cut("szene3", 0), s_kuehl),
    ("spaeti", cut("szene3", 4), s_spaeti),
    ("kasse", cut("wendung", 0), s_kasse),
    ("handy", cut("wendung", 3), s_handy),
    ("plan", cut("wendung", 7), s_plan),
    ("abstimmung", cut("abstimmung", 0), s_vote),
]


def main():
    scenes = []
    for i, (sid, s0, fn) in enumerate(CUTS):
        s1 = CUTS[i + 1][1] if i + 1 < len(CUTS) else TOTAL
        scenes.append((sid, s0, s1, fn(s0, s1)))
    hud = sk.hud_html(TOTAL, folge=1, tage=30, tage_flip=(L("wendung", 5) + 0.3, 29),
                      kasse=(L("wendung", 2), "3,40 €", 3.4 / 3000))
    caps = sk.captions_html(T, TOTAL)
    music = ("music.mp3", 0.16) if (HERE / "assets" / "music.mp3").exists() else None
    sk.write_project(HERE, "Kiosk-Kalle – Folge 1", scenes, sorted(SFX), hud, caps, TOTAL, music=music)
    print(f"{len(scenes)} Szenen, {len(SFX)} SFX, {TOTAL}s")


if __name__ == "__main__":
    main()
