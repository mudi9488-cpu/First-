#!/usr/bin/env python3
"""Kiosk-Kalle – Folge 3 (~89 s). Abstimmung Folge 2: A „Preise senken“ 12 % / B „Omas Kakao“ 88 % (34 Stimmen).

1. python3 ../../tools/align.py . assets/source/take1.mp3  (danach Zeilen mit falscher Silbenrate korrigiert, siehe Commit)
2. python3 build.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "serien" / "kiosk-kalle"))
from simkit import load_timings  # noqa: E402
import seriekit as sk  # noqa: E402
from seriekit import pop_in, pop_out, shake, hop, breathe, punch, walk_in, lautmalerei, show, hide, red_ring  # noqa: E402
import figuren as fg  # noqa: E402
import orte  # noqa: E402
from requisiten import (place, stempel, preis, kommentar, herz, traenen, schild, becher, topf, rauch,  # noqa: E402
                        rauchmelder, zettel, einkaufswagen)

T = load_timings(HERE)
TOTAL = round(T["duration"] + 1.6, 2)
B = {b["id"]: b for b in T["beats"]}

KASSE0, K_EINKAUF, K_VERKAUF = 137.40, 97.40, 189.40
STERNE0, STERNE1 = 1.8, 2.6


def L(bid, li):
    return B[bid]["lines"][li]["start"]


def E(bid, li):
    return B[bid]["lines"][li]["end"]


def cut(bid, li=0):
    return round(max(0.0, L(bid, li) - 0.08), 3)


SFX = []


def sfx(t, f, vol=0.6):
    SFX.append((round(t, 3), f, vol))


def layer(lid, inner, visible=True, z=1):
    return (f'<div id="{lid}" class="abs" style="left:0;top:0;width:1080px;height:1920px;z-index:{z};'
            f'opacity:{1 if visible else 0}">{inner}</div>')


def fremder(prefix, w=360, hood="#B05CF0", hair="#3A2A1E"):
    return fg.kalle(prefix, w=w, mund="grin", hood=hood, hood_sh=hood, hair=hair, brows="#3A2A1E", cap=False, fleck=False)


ICON_GELD = ('<svg width="120" height="120" viewBox="0 0 120 120"><path d="M 44 30 L 76 30 L 68 42 Q 100 58 100 84 Q 100 108 60 108 Q 20 108 20 84 '
             'Q 20 58 52 42 Z" fill="#FFC233" stroke="#1B1530" stroke-width="6" stroke-linejoin="round"/><text x="60" y="92" text-anchor="middle" '
             'font-family="Inter" font-weight="900" font-size="40" fill="#1B1530">€</text></svg>')
ICON_LUPE = ('<svg width="120" height="120" viewBox="0 0 120 120"><rect x="18" y="14" width="64" height="84" rx="6" fill="#fff" stroke="#1B1530" stroke-width="6"/>'
             '<path d="M 30 34 L 70 34 M 30 50 L 70 50 M 30 66 L 56 66" stroke="#9AA6B4" stroke-width="6"/>'
             '<circle cx="76" cy="74" r="22" fill="#BFF0FF" stroke="#1B1530" stroke-width="7"/><path d="M 92 90 L 110 108" stroke="#1B1530" '
             'stroke-width="10" stroke-linecap="round"/></svg>')


# ------------------------------------------------------------------ Szenen

def s_recap(s0, s1):
    r = lambda t: round(t - s0, 3)  # noqa: E731
    a = orte.kiosk_aussen("ka", shutter=0) + place(fg.kalle("k", w=420, mund="flat"), 330, 1660)
    a += place(fg.max_helfer("mx", w=380, mund="grin"), 760, 1680, z=3)
    a += lautmalerei("hook", "NOCH 28 TAGE", 70, 420, size=122, color=sk.YEL, rot=-4).replace("opacity:0", "opacity:1")
    b = orte.strasse_spaeti("st") + place(fg.dennis("d", w=220, mund="smirk"), 960, 1185, z=2)
    b += schild("sch", "ALLE GETRÄNKE", "50 CENT!", 110, 760).replace("opacity:0", "opacity:1")
    b += place(fg.kalle("k2", w=460, mund="sad"), 250, 1820, z=5)
    body = layer("la", a) + layer("lb", b, visible=False)
    js = breathe("#k", 0, s1 - s0) + f'tl.fromTo("#hook",{{scale:1.25}},{{scale:1,duration:0.35,ease:"back.out(2)"}},0);\n'
    js += pop_out("#hook", r(L("recap", 1)) + 0.5)
    t = r(L("recap", 3))
    js += fg.face_js("k", "sad", t) + fg.eyes_js("k", "wide", t) + fg.face_js("mx", "flat", t)
    t2 = r(L("recap", 4))
    js += hide("#la", t2) + show("#lb", t2) + hop("#d", t2 + 0.3, 30, n=2) + punch("#sch", r(L("recap", 6)), 1.08)
    sfx(0.0, "impact-bass-2.mp3", 0.5)
    sfx(L("recap", 3), "kling.wav", 0.4)
    sfx(L("recap", 4), "whoosh-short.mp3", 0.5)
    return sk.scene("recap", "", body, js)


def s_ergebnis(s0, s1):
    r = lambda t: round(t - s0, 3)  # noqa: E731
    body = sk.strahlen("rbg", "#12333A", "#1C4A52")
    body += place(fg.kalle_kopf("ek", w=860, mund="open"), 540, 1930).replace("z-index:2", "z-index:1")
    body += sk.result_cards("Preise senken", "Omas Kakao", 12, 88)
    body += kommentar("km", "„Hausgemacht – da kommen die Kunden von allein!“", 40, 1040, size=34)
    body += herz("h1", 900, 980) + herz("h2", 60, 960, 70)
    js = f'tl.fromTo("#rbg-r",{{rotation:0}},{{rotation:25,duration:{s1 - s0},ease:"none",svgOrigin:"540 1000"}},0);\n'
    js += sk.result_js(0.1, 12, 88)
    t = r(L("ergebnis", 3))
    js += fg.face_js("ek", "grin", t) + hop("#ek", t, 40, n=2)
    t2 = r(L("ergebnis", 4))
    js += pop_in("#km", t2) + pop_in("#h1", t2 + 0.3) + pop_in("#h2", t2 + 0.45)
    sfx(s0 + 0.1, "whoosh-short.mp3", 0.5)
    sfx(s0 + 0.6, "ratter.wav", 0.25)
    sfx(s0 + 1.8, "sparkle.mp3", 0.6)
    sfx(L("ergebnis", 4), "pop.mp3", 0.55)
    return sk.scene("ergebnis", sk.RESULT_CSS, body, js, bg="#12333A")


def s_suche(s0, s1):
    r = lambda t: round(t - s0, 3)  # noqa: E731
    body = orte.kiosk_innen("ki", uhr="9:00") + place(fg.kalle("k", w=420, mund="grin"), 540, 1760, z=3)
    body += lautmalerei("q", "WO IST ES?!", 160, 440, size=110, color=sk.RED, rot=-5)
    body += lautmalerei("da", "DA!", 640, 560, size=160, color=sk.GRN, rot=8)
    body += ('<svg id="zt" class="abs" style="left:520px;top:400px;opacity:0;z-index:5" width="120" height="140" viewBox="0 0 120 140">'
             '<g transform="rotate(-12 60 70)"><rect x="10" y="10" width="100" height="120" rx="6" fill="#FFF9E6" stroke="#1B1530" stroke-width="6"/>'
             '<path d="M 26 40 L 94 40 M 26 62 L 94 62 M 26 84 L 70 84" stroke="#2A3A8C" stroke-width="6"/></g></svg>')
    js = ""
    t = r(L("rezept", 1))
    js += fg.face_js("k", "shock", t) + fg.eyes_js("k", "wide", t) + shake("#k", t, n=4, amp=8)
    t2 = r(L("rezept", 3))
    js += pop_in("#q", t2, rot=-5)
    js += f'tl.to("#k",{{x:-200,duration:0.35,ease:"power2.inOut"}},{r(L("rezept", 6))});\n' + fg.face_js("k", "open", r(L("rezept", 6)))
    js += shake("#ki-counter", r(L("rezept", 6)) + 0.4, n=5, amp=6)
    js += pop_out("#q", r(L("rezept", 7)) - 0.1)
    js += f'tl.to("#k",{{x:300,duration:0.35,ease:"power2.inOut"}},{r(L("rezept", 7))});\n' + shake("#ki-fridge", r(L("rezept", 7)) + 0.4, n=5, amp=6)
    js += f'tl.to("#k",{{x:0,duration:0.35,ease:"power2.inOut"}},{r(L("rezept", 8))});\n'
    js += f'tl.to("#ki-oma",{{rotation:14,duration:0.25,ease:"back.out(3)",svgOrigin:"545 330"}},{r(L("rezept", 8)) + 0.5});\n'
    t3 = r(L("rezept", 9))
    js += pop_in("#da", t3, rot=8) + fg.face_js("k", "grin", t3) + fg.eyes_js("k", "wide", t3) + hop("#k", t3, 50)
    js += f'tl.fromTo("#zt",{{opacity:1,y:0,rotation:0}},{{opacity:1,y:520,rotation:200,duration:0.8,ease:"power1.in",immediateRender:false}},{t3 - 0.05});\n'
    sfx(s0, "whoosh-short.mp3", 0.5)
    sfx(L("rezept", 1), "error.mp3", 0.5)
    sfx(L("rezept", 3), "pop.mp3", 0.5)
    sfx(L("rezept", 6), "whoosh-short.mp3", 0.4)
    sfx(L("rezept", 6) + 0.4, "ratter.wav", 0.3)
    sfx(L("rezept", 7), "whoosh-short.mp3", 0.4)
    sfx(L("rezept", 8), "whoosh-short.mp3", 0.4)
    sfx(L("rezept", 9), "sparkle.mp3", 0.6)
    return sk.scene("suche", "", body, js)


def s_zettel(s0, s1):
    r = lambda t: round(t - s0, 3)  # noqa: E731
    body = sk.strahlen("zbg", "#3B2A1E", "#4A3626")
    body += zettel("rz", [("<b>Omas Geheimrezept</b>", "color:#C0202E;font-size:58px"), ("1 Liter Milch", ""), ("4 EL Kakao", ""),
                          ("1 Prise Zimt", ""), ("+ <span style='background:#7A6A50;color:#7A6A50;border-radius:8px'>██████</span> ???", "")])
    body += red_ring("rr", 470, 1015, 90)
    js = f'tl.fromTo("#zbg-r",{{rotation:0}},{{rotation:15,duration:{s1 - s0},ease:"none",svgOrigin:"540 1000"}},0);\n'
    js += f'tl.fromTo("#rz",{{y:700,rotation:-20,opacity:1}},{{y:0,rotation:-2,opacity:1,duration:0.45,ease:"back.out(1.6)"}},0.05);\n'
    js += pop_in("#rr", r(L("rezept", 11)) + 0.6)
    sfx(s0, "whoosh-short.mp3", 0.5)
    sfx(L("rezept", 11), "sparkle.mp3", 0.6)
    sfx(L("rezept", 11) + 0.6, "pop.mp3", 0.5)
    return sk.scene("zettel", "", body, js, bg="#3B2A1E")


def s_einkauf(s0, s1):
    r = lambda t: round(t - s0, 3)  # noqa: E731
    body = orte.grossmarkt("gm")
    body += einkaufswagen("w0", 330, 1330, voll=False) + einkaufswagen("w1", 330, 1330, voll=True).replace('z-index:3"', 'z-index:3;opacity:0"')
    body += place(fg.kalle("k", w=380, mund="grin"), 210, 1760, z=4) + place(fg.max_helfer("mx", w=380, mund="grin"), 860, 1760, z=4)
    body += preis("pr", "−40 €", 640, 470) + lautmalerei("kr", "KRACH!", 380, 700, size=150, color=sk.RED, rot=-8)
    body += lautmalerei("kl", "KLIMPER… KLIMPER…", 120, 1020, size=70, rot=-4)
    js = breathe("#k", 0, s1 - s0)
    t = r(L("einkauf", 1))
    js += hide("#w0", t) + show("#w1", t) + punch("#w1", t, 1.06)
    js += pop_in("#pr", r(L("einkauf", 3)), rot=-8) + fg.face_js("k", "flat", r(L("einkauf", 3)))
    t2 = r(L("einkauf", 4))
    js += pop_out("#pr", t2)
    js += f'tl.to(["#w1","#mx"],{{x:-520,duration:0.6,ease:"power2.in"}},{t2});\n'
    t3 = r(L("einkauf", 6))
    js += pop_in("#kr", t3, rot=-8) + shake("#gm", t3, n=6, amp=12) + fg.face_js("k", "shock", t3) + fg.eyes_js("k", "wide", t3)
    js += fg.face_js("mx", "shock", t3) + fg.eyes_js("mx", "wide", t3)
    t4 = r(L("einkauf", 7))
    js += pop_out("#kr", t4) + f'tl.to(["#w1","#mx"],{{x:0,duration:0.4,ease:"power2.out"}},{t4});\n'
    js += fg.face_js("k", "sad", t4) + fg.eyes_js("k", "normal", t4)
    js += pop_in("#kl", r(L("einkauf", 9)), rot=-4) + fg.face_js("mx", "grin", r(L("einkauf", 9))) + fg.eyes_js("mx", "normal", r(L("einkauf", 9)))
    sfx(s0, "whoosh-short.mp3", 0.5)
    sfx(L("einkauf", 1), "pop.mp3", 0.5)
    sfx(L("einkauf", 3), "click.mp3", 0.5)
    sfx(L("einkauf", 4), "ratter.wav", 0.35)
    sfx(L("einkauf", 6), "impact-bass-2.mp3", 0.75)
    sfx(L("einkauf", 9), "kling.wav", 0.6)
    return sk.scene("einkauf", "", body, js, bg="#DDE3EA")


def innen_basis(p, uhr="12:00", night=False, **kw):
    k = dict(w=420, mund="grin")
    k.update(kw)
    return (orte.kiosk_innen(p, night=night, uhr=uhr) + place(fg.kalle("k", **k), 300, 1390)
            + orte.theke_front(p + "f").replace('class="abs" style="', 'class="abs" style="z-index:3;'))


def s_kochen(s0, s1):
    r = lambda t: round(t - s0, 3)  # noqa: E731
    a = innen_basis("ki2", uhr="13:00", mund="grin") + topf("tp", 40, 930).replace("z-index:4", "z-index:4")
    a += rauchmelder("rm", 620, 330) + rauch("ra", 40, 560)
    a += lautmalerei("pl", "PLITSCH!", 560, 560, size=110, color="#7FD3FF", rot=8)
    a += lautmalerei("zi", "ZISCH!", 520, 700, size=120, color=sk.RED, rot=-6)
    a += lautmalerei("pi", "PIEP! PIEP! PIEP!", 160, 440, size=90, color=sk.RED, rot=-4)
    a += '<div id="alarm" class="abs" style="left:0;top:0;width:1080px;height:1920px;background:#FF2A2A;opacity:0;z-index:6"></div>'
    b = orte.nahaufnahme("na") + place(fg.kalle_kopf("kk", w=1000, mund="flat"), 540, 1201) + becher("bc", 640, 1020, s=260)
    b += lautmalerei("le", "LECKER!", 160, 380, size=170, color=sk.GRN, rot=-6).replace("left:", "z-index:7;left:")
    body = layer("la", a) + layer("lb", b, visible=False, z=2)
    js = ""
    t = r(L("kochen", 3))
    js += f'tl.set("#tp-inhalt",{{attr:{{fill:"#D9C2A8"}}}},0);\n' + pop_in("#pl", t, rot=8) + fg.face_js("k", "sad", t)
    t2 = r(L("kochen", 5))
    js += pop_out("#pl", t2 - 0.3) + f'tl.set("#tp-inhalt",{{attr:{{fill:"#1E1A18"}}}},{t2});\n'
    js += pop_in("#ra", t2) + pop_in("#zi", t2 + 0.05, rot=-6) + fg.face_js("k", "shock", t2) + fg.eyes_js("k", "wide", t2)
    t3 = r(L("kochen", 6))
    js += pop_out("#zi", t3)
    for k in range(8):
        js += f'tl.set("#alarm",{{opacity:{0.28 if k % 2 == 0 else 0}}},{t3 + 0.2 + k * 0.18});\n'
        js += f'tl.set("#rm-led",{{attr:{{fill:"{"#FF2A2A" if k % 2 == 0 else "#7E8492"}"}}}},{t3 + 0.2 + k * 0.18});\n'
    js += pop_in("#pi", t3 + 0.2, rot=-4) + shake("#k", t3 + 0.2, n=8, amp=10) + shake("#rm", t3 + 0.2, n=8, amp=6)
    t4 = r(L("kochen", 8))
    js += pop_out("#pi", t4) + pop_out("#ra", t4) + f'tl.set("#tp-inhalt",{{attr:{{fill:"#8B4A2B"}}}},{t4});\n'
    js += fg.face_js("k", "grin", t4) + fg.eyes_js("k", "normal", t4)
    t5 = r(L("kochen", 9))
    js += hide("#la", t5) + show("#lb", t5) + pop_in("#bc", t5 + 0.1)
    js += fg.eyes_js("kk", "closed", t5 + 0.3)
    t6 = r(L("kochen", 10))
    js += fg.eyes_js("kk", "wide", t6) + fg.face_js("kk", "grin", t6) + pop_in("#le", t6, rot=-6) + punch("#kk", t6, 1.08)
    sfx(s0, "whoosh-short.mp3", 0.5)
    sfx(L("kochen", 3), "pop.mp3", 0.5)
    sfx(L("kochen", 5), "brumm.wav", 0.4)
    sfx(L("kochen", 5) + 0.05, "error.mp3", 0.4)
    for k in range(4):
        sfx(L("kochen", 6) + 0.2 + k * 0.36, "tick.wav", 0.55)
    sfx(L("kochen", 9), "whoosh-short.mp3", 0.4)
    sfx(L("kochen", 10), "sparkle.mp3", 0.7)
    return sk.scene("kochen", "", body, js)


def s_horst(s0, s1):
    r = lambda t: round(t - s0, 3)  # noqa: E731
    body = innen_basis("ki3", uhr="15:00") + place(fg.horst("h", w=380, mund="open"), 800, 1740, z=4)
    body += becher("bc", 860, 1210, s=130, z=5) + traenen("t1", 763, 1290, 140).replace("z-index:4", "z-index:5")
    body += '<div id="hb" class="bubble" style="left:250px;top:800px;opacity:0;z-index:6;font-size:44px">SCHMECKT WIE BEI ERIKA!</div>'
    body += herz("h1", 600, 300, 80) + herz("h2", 380, 330, 60)
    js = walk_in("#h", 0, 500, 0.55) + breathe("#k", 0, s1 - s0)
    t = r(L("verkauf", 2))
    js += pop_in("#bc", t - 0.1) + f'tl.to("#bc",{{y:-60,duration:0.3,ease:"power2.out"}},{t + 0.2});\n'
    t2 = r(L("verkauf", 3))
    js += fg.face_js("h", "sad", t2) + f'tl.fromTo("#t1",{{opacity:0,scaleY:0.2}},{{opacity:1,scaleY:1,duration:0.6,ease:"power2.out",transformOrigin:"50% 0%"}},{t2});\n'
    js += fg.face_js("k", "open", t2)
    t3 = r(L("verkauf", 4))
    js += pop_in("#hb", t3) + pop_in("#h1", t3 + 0.3) + pop_in("#h2", t3 + 0.45) + fg.face_js("k", "grin", t3 + 0.5)
    sfx(s0, "whoosh-short.mp3", 0.5)
    sfx(L("verkauf", 2), "pop.mp3", 0.4)
    sfx(L("verkauf", 4), "sparkle.mp3", 0.6)
    return sk.scene("horst", "", body, js)


def s_schlange(s0, s1):
    r = lambda t: round(t - s0, 3)  # noqa: E731
    body = orte.kiosk_aussen("ka2", shutter=0)
    body += schild("ok", "OMAS KAKAO", "2 €", 220, 330, w=640, rot=3, farbe="#FFF4E0", z2col="#8B4A2B", z2size=120)
    q = [("kind", dict(prefix="c0", w=190, shirt="#FF7A3D", hair="#5A3A22", bag="#3B6FF0"), 1750),
         ("bau", dict(prefix="b0", w=290), 1770),
         ("fr", dict(prefix="f0", w=330, hood="#B05CF0", hair="#3A2A1E"), 1780),
         ("kind", dict(prefix="c1", w=190, shirt="#3DDC84", hair="#E8C04A", bag="#FF4F8B"), 1760),
         ("bau", dict(prefix="b1", w=290, haut="#C98A5E", bart=False), 1790),
         ("fr", dict(prefix="f1", w=330, hood="#E8413A", hair="#F2C14E"), 1770),
         ("fr", dict(prefix="f2", w=330, hood="#2EC4D6", hair="#1E1E2A"), 1785)]
    for i, (kind, kw, fy) in enumerate(q):
        svg = fg.kind(**kw) if kind == "kind" else fg.bauarbeiter(**kw) if kind == "bau" else fremder(**kw)
        body += place(svg, 160 + i * 140, fy, z=3 + (i % 2))
    body += ('<div id="rec" class="abs" style="left:880px;top:1150px;opacity:0;z-index:6;background:#2B2B3A;border:5px solid #1B1530;border-radius:16px;'
             'width:110px;height:170px"><div style="margin:14px auto 0;width:28px;height:28px;border-radius:50%;background:#FF2A2A"></div>'
             '<div style="color:#fff;font-weight:900;font-size:24px;text-align:center;margin-top:8px">REC</div></div>')
    body += lautmalerei("bc", "46 BECHER!", 150, 600, size=140, color=sk.GRN, rot=-5) + becher("bcu", 820, 520, s=180, z=6)
    js = ""
    t = r(L("verkauf", 7))
    ids = ["c0", "b0", "f0", "c1", "b1", "f1", "f2"]
    for i, pid in enumerate(ids[:4]):
        js += walk_in(f"#{pid}", 0.05 + i * 0.12, 700, 0.5)
    for i, pid in enumerate(ids[4:]):
        js += f'tl.set("#{pid}",{{x:900}},0);\n' + walk_in(f"#{pid}", r(L("verkauf", 11)) + i * 0.15, 900, 0.5)
    js += pop_in("#ok", t, rot=3)
    js += pop_in("#rec", r(L("verkauf", 9))) + f'tl.fromTo("#rec",{{rotation:-6}},{{rotation:6,duration:0.25,yoyo:true,repeat:5}},{r(L("verkauf", 9)) + 0.3});\n'
    t2 = r(L("verkauf", 13))
    js += pop_out("#ok", t2 - 0.1) + pop_in("#bc", t2, rot=-5) + pop_in("#bcu", t2 + 0.15)
    for i, pid in enumerate(ids):
        js += hop(f"#{pid}", t2 + 0.1 + i * 0.07, 35)
    sfx(s0, "whoosh-short.mp3", 0.5)
    sfx(L("verkauf", 7), "pop.mp3", 0.5)
    sfx(L("verkauf", 9), "click.mp3", 0.5)
    sfx(L("verkauf", 11), "whoosh-short.mp3", 0.4)
    sfx(L("verkauf", 13), "kling.wav", 0.7)
    sfx(L("verkauf", 13) + 0.2, "sparkle.mp3", 0.6)
    return sk.scene("schlange", "", body, js)


def s_dennis(s0, s1):
    r = lambda t: round(t - s0, 3)  # noqa: E731
    body = orte.strasse_spaeti("st2") + place(fg.dennis("d", w=260, mund="sad"), 860, 1200, z=2)
    body += schild("sch", "ALLE GETRÄNKE", "50 CENT!", 110, 760).replace("opacity:0", "opacity:1")
    body += lautmalerei("gr", "ZIRP… ZIRP…", 520, 1230, size=70, color="#fff", rot=5).replace("left:", "z-index:5;left:")
    js = ""
    js += f'tl.to("#sch",{{rotation:-14,y:60,duration:0.6,ease:"bounce.out"}},{r(L("verkauf", 15))});\n'
    js += pop_in("#gr", 0.4, rot=5)
    sfx(s0, "whoosh-short.mp3", 0.5)
    sfx(L("verkauf", 15), "error.mp3", 0.45)
    return sk.scene("dennis", ".st2-q { opacity:0; }", body, js)


def s_abend(s0, s1):
    r = lambda t: round(t - s0, 3)  # noqa: E731
    body = orte.kiosk_innen("ki4", night=True, uhr="21:00")
    body += place(fg.kalle("k", w=420, mund="grin", pose="up"), 360, 1760, z=3) + place(fg.max_helfer("mx", w=400, mund="grin", pose="up"), 760, 1760, z=3)
    disco = "".join(f'<div id="dl{i}" class="abs" style="left:{x}px;top:{y}px;width:220px;height:220px;border-radius:50%;background:{c};opacity:0;z-index:2"></div>'
                    for i, (x, y, c) in enumerate(((80, 700, "#FF4F8B"), (700, 560, "#3B6FF0"), (420, 900, "#FFC233"), (820, 1000, "#3DDC84"))))
    body += disco + lautmalerei("ye", "JAAA!", 360, 520, size=150, color=sk.YEL, rot=-6)
    js = ""
    t = r(L("abend", 2))
    js += pop_in("#ye", t, rot=-6)
    t2 = r(L("abend", 3))
    for i in range(4):
        js += f'tl.fromTo("#dl{i}",{{opacity:0}},{{opacity:0.45,duration:0.2,yoyo:true,repeat:5}},{t2 + i * 0.12});\n'
    js += (f'tl.fromTo("#k",{{rotation:-8}},{{rotation:8,duration:0.25,yoyo:true,repeat:7,ease:"sine.inOut",transformOrigin:"50% 100%"}},{t2});\n'
           f'tl.fromTo("#mx",{{rotation:8}},{{rotation:-8,duration:0.25,yoyo:true,repeat:7,ease:"sine.inOut",transformOrigin:"50% 100%"}},{t2});\n')
    js += hop("#k", t2, 40, n=3, dur=0.2) + hop("#mx", t2 + 0.1, 40, n=3, dur=0.2)
    sfx(s0, "whoosh-short.mp3", 0.5)
    sfx(L("abend", 0) + 0.3, "kling.wav", 0.5)
    sfx(L("abend", 2), "sparkle.mp3", 0.6)
    return sk.scene("abend", "", body, js)


def s_wendung(s0, s1):
    r = lambda t: round(t - s0, 3)  # noqa: E731
    a = innen_basis("ki5", uhr="21:30", night=True, mund="grin") + place(fg.geier("g", w=380, mund="smirk"), 800, 1760, z=4)
    a += '<div id="gb1" class="bubble" style="left:320px;top:680px;opacity:0;z-index:6;font-size:40px">STEHT NICHT IM MIETVERTRAG!</div>'
    a += '<div id="gb2" class="bubble" style="left:330px;top:680px;opacity:0;z-index:6;font-size:40px">10 % VON JEDEM BECHER!</div>'
    a += stempel("st", "10 %", 140, 400, 160)
    b = orte.nahaufnahme("na2", farbe="#DDE6EE") + place(fg.kalle_kopf("kp", w=1000, mund="shock", augen="wide"), 540, 1201)
    b += lautmalerei("kb", "KREIDEBLEICH!", 90, 380, size=110, color="#fff", rot=-5).replace("left:", "z-index:7;left:")
    body = layer("la", a) + layer("lb", b, visible=False, z=2)
    js = walk_in("#g", 0.1, 520, 0.55)
    js += pop_in("#gb1", r(L("wendung", 3)))
    t = r(L("wendung", 5))
    js += pop_out("#gb1", t - 0.1) + pop_in("#gb2", t) + fg.face_js("k", "shock", t) + fg.eyes_js("k", "wide", t)
    t2 = r(L("wendung", 6))
    js += f'tl.fromTo("#st",{{scale:2.6,opacity:0}},{{scale:1,opacity:1,duration:0.2,ease:"power3.in"}},{t2});\n' + shake("#st", t2 + 0.2, n=3, amp=10)
    t3 = r(L("wendung", 8))
    js += hide("#la", t3) + show("#lb", t3)
    js += f'tl.fromTo("#kp",{{filter:"saturate(1) brightness(1)"}},{{filter:"saturate(0) brightness(1.35)",duration:0.6,ease:"power2.in"}},{t3 + 0.2});\n'
    js += pop_in("#kb", t3 + 0.3, rot=-5) + shake("#kp", t3 + 0.3, n=6, amp=6)
    sfx(s0, "whoosh-short.mp3", 0.5)
    sfx(L("wendung", 3), "pop.mp3", 0.5)
    sfx(L("wendung", 6), "impact-bass-2.mp3", 0.75)
    sfx(L("wendung", 8), "whoosh-short.mp3", 0.5)
    sfx(L("wendung", 8) + 0.3, "error.mp3", 0.5)
    return sk.scene("wendung", "", body, js)


def s_vote(s0, s1):
    r = lambda t: round(t - s0, 3)  # noqa: E731
    body = sk.strahlen("vbg")
    body += place(fg.kalle_kopf("kv", w=900, mund="open"), 540, 1900).replace("z-index:2", "z-index:1;opacity:0.4")
    body += sk.vote_cards(["WAS SOLL", "KALLE TUN?"], {"titel": "Zahlen", "unter": "10 % an Geier – kein Ärger"},
                          {"titel": "Wehren", "unter": "Mietvertrag lesen – Risiko!"}, (ICON_GELD, ICON_LUPE))
    js = f'tl.fromTo("#vbg-r",{{rotation:0}},{{rotation:40,duration:{s1 - s0},ease:"none",svgOrigin:"540 1000"}},0);\n'
    js += pop_in("#vt", 0.1) + pop_in("#va", r(L("abstimmung", 0))) + pop_in("#vb", r(L("abstimmung", 2)))
    t = r(L("abstimmung", 5))
    js += pop_in("#vpill", t) + punch("#va", t, 1.06) + punch("#vb", t + 0.4, 1.06) + punch("#vpill", r(L("abstimmung", 6)), 1.1)
    sfx(s0, "whoosh-short.mp3", 0.5)
    sfx(s0 + 0.1, "pop.mp3", 0.5)
    sfx(L("abstimmung", 0), "pop.mp3", 0.55)
    sfx(L("abstimmung", 2), "pop.mp3", 0.55)
    sfx(L("abstimmung", 5), "sparkle.mp3", 0.5)
    return sk.scene("abstimmung", sk.VOTE_CSS, body, js, bg="#12333A")


CUTS = [
    ("recap", 0.0, s_recap),
    ("ergebnis", cut("ergebnis"), s_ergebnis),
    ("suche", cut("rezept"), s_suche),
    ("zettel", cut("rezept", 10), s_zettel),
    ("einkauf", cut("einkauf"), s_einkauf),
    ("kochen", cut("kochen"), s_kochen),
    ("horst", cut("verkauf"), s_horst),
    ("schlange", cut("verkauf", 6), s_schlange),
    ("dennis", cut("verkauf", 14), s_dennis),
    ("abend", cut("abend"), s_abend),
    ("wendung", cut("wendung"), s_wendung),
    ("abstimmung", cut("abstimmung"), s_vote),
]


def main():
    scenes = []
    for i, (sid, s0, fn) in enumerate(CUTS):
        s1 = CUTS[i + 1][1] if i + 1 < len(CUTS) else TOTAL
        scenes.append((sid, s0, s1, fn(s0, s1)))
    hud = sk.hud_serie(TOTAL, folge=3, tage=28, kasse0=KASSE0,
                       kasse_events=[(L("einkauf", 3), K_EINKAUF), (L("verkauf", 13), K_VERKAUF)],
                       sterne=(0.2, STERNE0, [(L("abend", 2) + 0.4, STERNE1)]),
                       tage_flip=(L("abend", 0) + 0.3, 27))
    caps = sk.captions_html(T, TOTAL)
    music = ("music.mp3", 0.16) if (HERE / "assets" / "music.mp3").exists() else None
    sk.write_project(HERE, "Kiosk-Kalle – Folge 3", scenes, sorted(SFX), hud, caps, TOTAL, music=music)
    print(f"{len(scenes)} Szenen, {len(SFX)} SFX, {TOTAL}s")


if __name__ == "__main__":
    main()
