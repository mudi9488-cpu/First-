#!/usr/bin/env python3
"""Kiosk-Kalle – Folge 2. Abstimmung Folge 1: A „Konsole verkaufen“ 90 % / B „Kredit bei Dennis“ 10 % (41 Stimmen).

1. python3 ../../tools/align.py . assets/source/take1.mp3
2. python3 build.py
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "serien" / "kiosk-kalle"))
from simkit import load_timings  # noqa: E402
import seriekit as sk  # noqa: E402
from seriekit import pop_in, pop_out, shake, hop, breathe, punch, walk_in, lautmalerei, show, hide  # noqa: E402
import figuren as fg  # noqa: E402
import orte  # noqa: E402

T = load_timings(HERE)
TOTAL = round(T["duration"] + 1.6, 2)
B = {b["id"]: b for b in T["beats"]}

KASSE0 = 3.40
K_VERKAUF, K_KUEHL, K_BAU = 253.40, 73.40, 137.40
STERNE0, STERNE1 = 1.2, 1.8


def L(bid, li):
    return B[bid]["lines"][li]["start"]


def Wd(bid, li, wi):
    return B[bid]["lines"][li]["words"][wi]["start"]


def cut(bid, li=0):
    return round(max(0.0, L(bid, li) - 0.08), 3)


def place(svg, cx, fy, z=2):
    vb = [float(x) for x in re.search(r'viewBox="([^"]+)"', svg).group(1).split()]
    w = float(re.search(r'width="([\d.]+)"', svg).group(1))
    s = w / vb[2]
    return svg.replace('style="overflow:visible"',
                       f'style="overflow:visible;left:{cx + vb[0] * s:.0f}px;top:{fy + vb[1] * s:.0f}px;z-index:{z}"', 1)


SFX = []


def sfx(t, f, vol=0.6):
    SFX.append((round(t, 3), f, vol))


# ------------------------------------------------------------------ Requisiten

def stempel(pid, text, x, y, size=120, col="#E0202E", rot=-12):
    return (f'<div id="{pid}" class="abs" style="left:{x}px;top:{y}px;opacity:0;transform:rotate({rot}deg);border:14px solid {col};z-index:6;'
            f'border-radius:24px;padding:4px 30px;color:{col};font-weight:900;font-size:{size}px;background:rgba(255,255,255,0.85)">{text}</div>')


def preis(pid, text, x, y, col="#E8413A", rot=-8, size=70):
    return (f'<div id="{pid}" class="abs" style="left:{x}px;top:{y}px;opacity:0;transform:rotate({rot}deg);background:{col};color:#fff;z-index:6;'
            f'font-weight:900;font-size:{size}px;padding:10px 30px;border-radius:18px;border:6px solid #1B1530">{text}</div>')


KONSOLE_SVG = ('<svg width="420" height="300" viewBox="0 0 140 100"><rect x="10" y="10" width="120" height="44" rx="10" fill="#2B2B3A" stroke="#1B1530" stroke-width="4"/>'
               '<rect x="20" y="24" width="50" height="6" rx="3" fill="#4F7CFF"/><circle cx="110" cy="32" r="6" fill="#3DDC84"/>'
               '<path d="M 16 70 Q 12 96 30 96 Q 40 96 44 86 L 56 86 Q 60 96 70 96 Q 88 96 84 70 Q 80 58 68 58 L 32 58 Q 20 58 16 70 Z" fill="#fff" stroke="#1B1530" stroke-width="4"/>'
               '<path d="M 70 70 Q 66 96 84 96 Q 94 96 98 86 L 110 86 Q 114 96 124 96 Q 142 96 138 70 Q 134 58 122 58 L 86 58 Q 74 58 70 70 Z" fill="#fff" stroke="#1B1530" stroke-width="4"/></svg>')


def kleinanzeige(pid):
    return f"""<div id="{pid}" class="abs" style="left:150px;top:330px;width:780px;height:1020px;background:#15122A;border-radius:80px;border:10px solid #2C2747;overflow:hidden;z-index:3">
  <div style="position:absolute;inset:18px;border-radius:62px;background:#F6F4FB;overflow:hidden">
    <div style="height:150px;background:#3DA35D;display:flex;align-items:flex-end;padding:0 40px 26px;color:#fff;font-weight:900;font-size:46px">Kleinanzeigen</div>
    <div style="margin:36px 36px 0;background:#fff;border-radius:30px;border:4px solid #DDD8EA;padding:30px;text-align:center">
      <div style="background:#E8F1F8;border-radius:22px;padding:20px 0">{KONSOLE_SVG}</div>
      <div style="font-weight:900;font-size:44px;color:#1B1530;margin-top:24px;text-align:left">Spielkonsole + 2 Controller</div>
      <div style="font-weight:900;font-size:76px;color:#3DA35D;text-align:left">250 €</div>
      <div style="font-weight:700;font-size:30px;color:#8A84A8;text-align:left">Abholung heute · Kiosk Erika</div>
    </div>
    <div id="{pid}-msg" style="position:absolute;left:36px;right:36px;bottom:40px;background:#7B5CF5;color:#fff;font-weight:800;font-size:40px;
      padding:24px 30px;border-radius:30px;opacity:0">Käufer: „Nehme sie! Bin in 5 Min da.“</div>
  </div></div>"""


def kuehlschrank_svg(pid, x, y, w=260, glow=False):
    g = "#BFF0FF" if glow else "#C9D3DC"
    bottles = "".join(f'<rect x="{30 + (k % 3) * 60}" y="{90 + (k // 3) * 150}" width="36" height="100" rx="12" fill="{["#FF5A5F", "#3DDC84", "#FFC233"][k % 3]}" '
                      f'stroke="#1B1530" stroke-width="4"/>' for k in range(9))
    return (f'<svg id="{pid}" class="abs" style="left:{x}px;top:{y}px;z-index:3" width="{w}" height="{w * 560 / 240:.0f}" viewBox="0 0 240 560">'
            f'<rect x="4" y="4" width="232" height="552" rx="18" fill="#EAF2F8" stroke="#1B1530" stroke-width="7"/>'
            f'<rect x="4" y="4" width="232" height="60" rx="18" fill="#3B6FF0" stroke="#1B1530" stroke-width="7"/>'
            f'<text x="120" y="48" text-anchor="middle" font-family="Inter" font-weight="900" font-size="32" fill="#fff">KALT</text>'
            f'<rect id="{pid}-glow" x="20" y="78" width="200" height="460" rx="8" fill="{g}"/>{bottles}'
            f'<rect x="20" y="78" width="200" height="460" rx="8" fill="none" stroke="#1B1530" stroke-width="5"/></svg>')


def sackkarre(pid, x, y):
    return (f'<svg id="{pid}" class="abs" style="left:{x}px;top:{y}px;z-index:2" width="300" height="200" viewBox="0 0 300 200">'
            '<path d="M 40 20 L 60 170 L 260 170" fill="none" stroke="#5E6275" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>'
            '<circle cx="70" cy="172" r="26" fill="#2B2B3A" stroke="#1B1530" stroke-width="6"/></svg>')


def thermo_karte(pid, text="30°"):
    return (f'<div id="{pid}" class="card" style="left:90px;top:420px;width:360px;height:170px;opacity:0;display:flex;align-items:center;z-index:6;'
            'justify-content:center;gap:18px;font-weight:900;font-size:90px;color:#E8413A">'
            '<svg width="50" height="120" viewBox="0 0 50 120"><rect x="15" y="6" width="20" height="86" rx="10" fill="#fff" stroke="#1B1530" stroke-width="5"/>'
            f'<rect x="20" y="20" width="10" height="76" fill="#E8413A"/><circle cx="25" cy="98" r="18" fill="#E8413A" stroke="#1B1530" stroke-width="5"/></svg>{text}</div>')


def sonne(pid, x, y):
    rays = "".join(f'<path d="M 100 100 L 100 8" stroke="#FFC233" stroke-width="14" stroke-linecap="round" transform="rotate({k * 45} 100 100)"/>' for k in range(8))
    return (f'<svg id="{pid}" class="abs" style="left:{x}px;top:{y}px;opacity:0;z-index:5" width="200" height="200" viewBox="0 0 200 200">'
            f'{rays}<circle cx="100" cy="100" r="54" fill="#FFE14A" stroke="#1B1530" stroke-width="7"/></svg>')


def flasche(pid, x, y, col):
    return (f'<svg id="{pid}" class="abs" style="left:{x}px;top:{y}px;opacity:0;z-index:5" width="60" height="140" viewBox="0 0 60 140">'
            f'<rect x="16" y="4" width="28" height="30" rx="6" fill="#ddd" stroke="#1B1530" stroke-width="5"/>'
            f'<rect x="6" y="30" width="48" height="104" rx="16" fill="{col}" stroke="#1B1530" stroke-width="6"/>'
            '<path d="M 18 60 L 18 100" stroke="#fff" stroke-width="6" stroke-linecap="round" opacity="0.6"/></svg>')


def herz(pid, x, y, s=90):
    return (f'<svg id="{pid}" class="abs" style="left:{x}px;top:{y}px;opacity:0;z-index:6" width="{s}" height="{s}" viewBox="0 0 24 24">'
            '<path d="M12 21s-7.5-4.6-10-9.3C.4 8.4 2.3 4 6.3 4c2.3 0 3.9 1.4 5.7 3.4C13.8 5.4 15.4 4 17.7 4c4 0 5.9 4.4 4.3 7.7C19.5 16.4 12 21 12 21z" '
            'fill="#FF4F6B" stroke="#1B1530" stroke-width="1.6"/></svg>')


def kommentar(pid, text, x, y):
    return (f'<div id="{pid}" class="abs" style="left:{x}px;top:{y}px;opacity:0;z-index:6;background:#fff;color:#1B1530;font-weight:800;font-size:36px;'
            f'padding:16px 26px;border-radius:26px;border:5px solid #1B1530;display:flex;gap:14px;align-items:center;white-space:nowrap">'
            f'<span style="width:44px;height:44px;border-radius:50%;background:#B05CF0;display:inline-block;flex:none"></span>{text}</div>')


def traenen(pid, x, y):
    return (f'<svg id="{pid}" class="abs" style="left:{x}px;top:{y}px;opacity:0;z-index:4" width="70" height="260" viewBox="0 0 70 260">'
            '<path d="M 35 0 Q 60 120 50 200 Q 35 250 20 200 Q 10 120 35 0 Z" fill="#7FD3FF" stroke="#1B1530" stroke-width="5" opacity="0.95"/></svg>')


def spaeti_schild(pid):
    return (f'<div id="{pid}" class="abs" style="left:110px;top:760px;width:860px;opacity:0;z-index:4;background:#FFE14A;border:10px solid #1B1530;'
            'border-radius:26px;text-align:center;padding:16px 0;transform:rotate(-3deg)">'
            '<div style="font-weight:900;font-size:58px;color:#1B1530">ALLE GETRÄNKE</div>'
            '<div style="font-weight:900;font-size:150px;color:#E0202E;line-height:1;-webkit-text-stroke:6px #1B1530;paint-order:stroke fill">50 CENT!</div></div>')


ICON_PREIS = ('<svg width="120" height="120" viewBox="0 0 120 120"><path d="M 14 60 L 54 18 L 104 18 L 104 68 L 62 108 Z" fill="#fff" stroke="#1B1530" '
              'stroke-width="6" stroke-linejoin="round"/><circle cx="84" cy="38" r="9" fill="#1B1530"/><text x="58" y="78" text-anchor="middle" '
              'font-family="Inter" font-weight="900" font-size="30" fill="#E8413A" transform="rotate(-45 58 70)">−50%</text></svg>')
ICON_KAKAO = ('<svg width="120" height="120" viewBox="0 0 120 120"><path d="M 46 30 Q 36 20 46 10 M 66 30 Q 56 20 66 10" fill="none" stroke="#fff" stroke-width="6" '
              'stroke-linecap="round"/><path d="M 20 40 L 92 40 L 86 104 Q 56 112 26 104 Z" fill="#fff" stroke="#1B1530" stroke-width="6" stroke-linejoin="round"/>'
              '<path d="M 26 52 L 86 52" stroke="#8B4A2B" stroke-width="10"/><path d="M 92 54 Q 112 58 106 76 Q 100 90 88 86" fill="none" stroke="#1B1530" '
              'stroke-width="6"/></svg>')
ICON_KONSOLE = ('<svg width="90" height="90" viewBox="0 0 120 120"><path d="M 14 50 Q 10 92 32 92 Q 46 92 52 78 L 68 78 Q 74 92 88 92 Q 110 92 106 50 '
                'Q 102 32 84 32 L 36 32 Q 18 32 14 50 Z" fill="#fff" stroke="#1B1530" stroke-width="6"/></svg>')


# ------------------------------------------------------------------ Szenen

def s_recap(s0, s1):
    r = lambda t: round(t - s0, 3)  # noqa: E731
    body = orte.kiosk_aussen("ka", shutter=0) + place(fg.kalle("k", w=430, mund="flat"), 360, 1660)
    body += place(fg.geier("g", w=360, mund="smirk"), 820, 1680, z=3)
    body += lautmalerei("hook", "NOCH 29 TAGE", 70, 420, size=122, color=sk.YEL, rot=-4).replace("opacity:0", "opacity:1")
    body += '<div id="gb" class="bubble" style="left:420px;top:700px;opacity:0;font-size:44px;z-index:5">TICK, TACK.</div>'
    js = breathe("#k", 0, s1 - s0)
    js += f'tl.fromTo("#hook",{{scale:1.25}},{{scale:1,duration:0.35,ease:"back.out(2)"}},0);\n'
    js += pop_out("#hook", r(L("recap", 1)) + 0.4)
    js += walk_in("#g", r(L("recap", 1)), 500, 0.5) + pop_in("#gb", r(L("recap", 2)))
    t = r(L("recap", 4))
    js += fg.face_js("k", "sad", t) + fg.eyes_js("k", "wide", t) + shake("#k", t, n=3, amp=6)
    sfx(0.0, "impact-bass-2.mp3", 0.5)
    sfx(L("recap", 1), "whoosh-short.mp3", 0.45)
    sfx(L("recap", 2), "tick.wav", 0.6)
    return sk.scene("recap", "", body, js)


def s_ergebnis(s0, s1):
    r = lambda t: round(t - s0, 3)  # noqa: E731
    body = sk.strahlen("rbg", "#12333A", "#1C4A52")
    body += place(fg.kalle_kopf("ek", w=860, mund="open"), 540, 1930).replace("z-index:2", "z-index:1")
    body += sk.result_cards("Konsole verkaufen", "Kredit bei Dennis", 90, 10)
    body += traenen("t1", 400, 1500) + traenen("t2", 610, 1500)
    body += lautmalerei("nein", "NEEEIN!", 600, 1040, size=110, color=sk.RED, rot=8)
    js = f'tl.fromTo("#rbg-r",{{rotation:0}},{{rotation:20,duration:{s1 - s0},ease:"none",svgOrigin:"540 1000"}},0);\n'
    js += sk.result_js(0.1, 90, 10)
    t = r(L("ergebnis", 3))
    js += fg.face_js("ek", "shock", t) + fg.eyes_js("ek", "wide", t)
    t2 = r(L("ergebnis", 4))
    js += fg.face_js("ek", "sad", t2) + fg.eyes_js("ek", "closed", t2) + pop_in("#nein", t2, rot=8)
    for i, tid in enumerate(("#t1", "#t2")):
        js += f'tl.fromTo("{tid}",{{opacity:0,scaleY:0.2}},{{opacity:1,scaleY:1,duration:0.5,ease:"power2.out",transformOrigin:"50% 0%"}},{t2 + 0.1 + i * 0.05});\n'
    js += shake("#ek", t2 + 0.2, n=5, amp=5)
    sfx(s0 + 0.1, "whoosh-short.mp3", 0.5)
    sfx(s0 + 0.6, "ratter.wav", 0.25)
    sfx(s0 + 1.8, "sparkle.mp3", 0.6)
    sfx(L("ergebnis", 4), "error.mp3", 0.55)
    return sk.scene("ergebnis", sk.RESULT_CSS, body, js, bg="#12333A")


def s_verkauf(s0, s1):
    r = lambda t: round(t - s0, 3)  # noqa: E731
    body = sk.strahlen("vbg", "#12333A", "#163E46") + kleinanzeige("ka")
    body += lautmalerei("min", "+10 MIN", 640, 300, size=90, rot=8).replace("left:", "z-index:6;left:")
    body += stempel("vk", "VERKAUFT!", 200, 660, 120)
    js = f'tl.fromTo("#ka",{{y:900,rotation:6}},{{y:0,rotation:0,duration:0.4,ease:"back.out(1.4)"}},0);\n'
    t = r(L("verkauf", 2))
    js += pop_in("#min", t, rot=8) + pop_in("#ka-msg", r(L("verkauf", 3)))
    t2 = r(L("verkauf", 4))
    js += f'tl.fromTo("#vk",{{scale:2.6,opacity:0}},{{scale:1,opacity:1,duration:0.2,ease:"power3.in"}},{t2});\n' + shake("#vk", t2 + 0.2, n=3, amp=10)
    sfx(s0, "whoosh-short.mp3", 0.5)
    sfx(L("verkauf", 2), "tick.wav", 0.5)
    sfx(L("verkauf", 3), "pop.mp3", 0.55)
    sfx(L("verkauf", 4), "impact-bass-2.mp3", 0.6)
    sfx(L("verkauf", 4) + 0.3, "kling.wav", 0.6)
    return sk.scene("verkauf", "", body, js, bg="#12333A")


def s_kuehl(s0, s1):
    r = lambda t: round(t - s0, 3)  # noqa: E731
    a = '<div id="la" class="abs" style="left:0;top:0;width:1080px;height:1920px">'
    a += orte.kiosk_aussen("ka2", shutter=0)
    a += '<div id="trupp" class="abs" style="left:0;top:0;width:1080px;height:1920px;z-index:3">'
    a += kuehlschrank_svg("ks", 120, 1050, w=250) + sackkarre("sk", 80, 1470)
    a += place(fg.kalle("k", w=380, mund="grin", pose="up"), 470, 1680)
    a += '</div>' + preis("pr", "180 €", 600, 900) + lautmalerei("ae", "ÄCHZ!", 560, 560, size=110, rot=8) + '</div>'
    b = '<div id="lb" class="abs" style="left:0;top:0;width:1080px;height:1920px;opacity:0">'
    b += orte.kiosk_innen("ki", uhr="10:00") + place(fg.kalle("k2", w=420, mund="grin", pose="up"), 360, 1760, z=3)
    b += lautmalerei("br", "BRUMM… KALT!", 300, 440, size=96, color="#7FD3FF", rot=-5) + '</div>'
    js = f'tl.set("#trupp",{{x:-380}},0);\n'
    js += f'tl.to("#trupp",{{x:-120,duration:0.8,ease:"power2.out"}},0);\n'
    js += pop_in("#pr", r(L("kuehlschrank", 2)), rot=-8)
    t = r(L("kuehlschrank", 3))
    js += pop_out("#pr", t) + f'tl.to("#trupp",{{x:260,duration:{r(L("kuehlschrank", 5)) - t - 0.1:.2f},ease:"power1.inOut"}},{t});\n'
    js += pop_in("#ae", t + 0.2, rot=8) + fg.face_js("k", "open", t) + fg.eyes_js("k", "closed", t)
    js += f'tl.fromTo("#trupp",{{rotation:-1}},{{rotation:1,duration:0.15,yoyo:true,repeat:7,ease:"sine.inOut"}},{t});\n'
    t2 = r(L("kuehlschrank", 5))
    js += hide("#la", t2) + show("#lb", t2) + pop_in("#br", t2 + 0.1, rot=-5) + hop("#k2", t2 + 0.2, 60, n=2)
    for k in range(3):
        js += f'tl.set("#ki-glow",{{opacity:{0.2 if k % 2 == 0 else 1}}},{t2 + 0.1 * k});\n'
    sfx(s0, "whoosh-short.mp3", 0.5)
    sfx(L("kuehlschrank", 2), "pop.mp3", 0.55)
    sfx(L("kuehlschrank", 3), "ratter.wav", 0.35)
    sfx(L("kuehlschrank", 3) + 0.2, "pop.mp3", 0.45)
    sfx(L("kuehlschrank", 5), "brumm.wav", 0.5)
    sfx(L("kuehlschrank", 5) + 0.3, "sparkle.mp3", 0.55)
    return sk.scene("kuehlschrank", "", a + b, js)


def innen_basis(p, uhr="12:00", night=False, **kw):
    k = dict(w=420, mund="grin")
    k.update(kw)
    return (orte.kiosk_innen(p, night=night, uhr=uhr) + place(fg.kalle("k", **k), 300, 1390)
            + orte.theke_front(p + "f").replace('class="abs" style="', 'class="abs" style="z-index:3;'))


def s_bau(s0, s1):
    r = lambda t: round(t - s0, 3)  # noqa: E731
    body = innen_basis("ki2")
    for i, (cx, haut, bart) in enumerate(((700, "#FFD6B0", True), (860, "#C98A5E", False), (1010, "#F1C7A0", True))):
        body += place(fg.bauarbeiter(f"b{i}", w=300, haut=haut, bart=bart), cx, 1800 + (i % 2) * 30, z=4)
    body += sonne("so", 830, 330) + thermo_karte("th")
    body += '<div id="bb" class="bubble" style="left:470px;top:880px;opacity:0;z-index:6">ENDLICH WAS KALTES!</div>'
    body += "".join(flasche(f"fl{i}", 620 + i * 130, 1000, c) for i, c in enumerate(("#FF5A5F", "#3DDC84", "#FFC233")))
    js = breathe("#k", 0, s1 - s0)
    t = r(L("bauarbeiter", 1))
    for i in range(3):
        js += walk_in(f"#b{i}", t + i * 0.15, 500, 0.55)
    t2 = r(L("bauarbeiter", 3))
    js += pop_in("#so", t2) + pop_in("#th", r(L("bauarbeiter", 4)))
    for i in range(3):
        js += pop_in(f"#fl{i}", t2 + 0.2 + i * 0.12) + hop(f"#b{i}", t2 + 0.3 + i * 0.12, 30)
    js += pop_in("#bb", t2 + 0.5)
    t3 = r(L("bauarbeiter", 5))
    js += pop_out("#bb", t3) + pop_out("#th", t3) + pop_out("#so", t3)
    js += f'tl.set("#ki2f-disp",{{innerHTML:"64,00"}},{r(L("bauarbeiter", 6))});\n' + hop("#k", r(L("bauarbeiter", 6)), 40, n=2)
    sfx(s0, "whoosh-short.mp3", 0.5)
    sfx(L("bauarbeiter", 1), "pop.mp3", 0.45)
    sfx(L("bauarbeiter", 3) + 0.2, "pop.mp3", 0.5)
    sfx(L("bauarbeiter", 3) + 0.5, "click.mp3", 0.5)
    sfx(L("bauarbeiter", 6), "kling.wav", 0.7)
    sfx(L("bauarbeiter", 6) + 1.2, "sparkle.mp3", 0.5)
    return sk.scene("bauarbeiter", "", body, js)


def s_max(s0, s1):
    r = lambda t: round(t - s0, 3)  # noqa: E731
    body = innen_basis("ki3", uhr="15:00", mund="open") + place(fg.max_helfer("mx", w=420, mund="grin"), 800, 1760, z=4)
    body += '<div id="mb" class="bubble" style="left:430px;top:780px;opacity:0;z-index:6">ICH HELF DIR – UMSONST!</div>'
    body += lautmalerei("eh", "EHRENAMTLICH!", 120, 470, size=110, color=sk.GRN, rot=-5)
    body += (kommentar("c1", "Darf ich mitarbeiten?", 60, 420) + kommentar("c2", "Ich würd umsonst helfen!", 330, 545)
             + kommentar("c3", "A – langfristig denken!", 120, 670))
    body += "".join(herz(f"h{i}", x, y) for i, (x, y) in enumerate(((880, 560), (140, 900), (900, 1000), (620, 480))))
    t = r(L("max", 1))
    js = walk_in("#mx", t, 520, 0.6) + fg.face_js("k", "shock", t + 0.3) + fg.eyes_js("k", "wide", t + 0.3)
    js += pop_in("#mb", r(L("max", 4))) + fg.face_js("k", "grin", r(L("max", 4))) + fg.eyes_js("k", "normal", r(L("max", 4)))
    t2 = r(L("max", 5))
    js += pop_in("#eh", t2, rot=-5) + hop("#k", t2, 50, n=2) + hop("#mx", t2 + 0.1, 50, n=2)
    t3 = r(L("max", 6))
    js += pop_out("#mb", t3 - 0.1) + pop_out("#eh", t3 - 0.1)
    for i in range(3):
        js += pop_in(f"#c{i + 1}", t3 + i * 0.25)
    for i in range(4):
        js += pop_in(f"#h{i}", t3 + 0.2 + i * 0.15) + f'tl.to("#h{i}",{{y:-120,opacity:0,duration:1.0,ease:"power1.in"}},{t3 + 0.6 + i * 0.15});\n'
    sfx(s0, "whoosh-short.mp3", 0.5)
    sfx(L("max", 1), "pop.mp3", 0.5)
    sfx(L("max", 4), "pop.mp3", 0.5)
    sfx(L("max", 5), "sparkle.mp3", 0.6)
    sfx(L("max", 6), "pop.mp3", 0.45)
    sfx(L("max", 6) + 0.25, "pop.mp3", 0.45)
    sfx(L("max", 6) + 0.5, "pop.mp3", 0.45)
    return sk.scene("max", "", body, js)


def s_wendung(s0, s1):
    r = lambda t: round(t - s0, 3)  # noqa: E731
    body = orte.strasse_spaeti("st") + place(fg.dennis("d", w=220, mund="smirk"), 960, 1185, z=2)
    body += place(fg.kalle("k", w=460, mund="grin"), 250, 1820, z=3)
    body += f'<div id="nacht" class="abs" style="left:0;top:0;width:1080px;height:1920px;background:#0B1A40;opacity:0;z-index:3"></div>'
    body += spaeti_schild("schild") + lautmalerei("hm", "HEHEHE…", 640, 1060, size=70, color="#FF4F8B", rot=6).replace("left:", "z-index:5;left:")
    js = pop_in("#hm", r(L("wendung", 1)), rot=6) + hop("#d", r(L("wendung", 1)), 20)
    t = r(L("wendung", 2))
    js += pop_out("#hm", t) + f'tl.to("#nacht",{{opacity:0.45,duration:0.5}},{t});\n'
    t2 = r(L("wendung", 5))
    js += f'tl.fromTo("#schild",{{scale:2.4,opacity:0}},{{scale:1,opacity:1,duration:0.22,ease:"power3.in"}},{t2});\n' + shake("#schild", t2 + 0.22, n=3, amp=10)
    js += fg.face_js("k", "shock", t2 + 0.2) + fg.eyes_js("k", "wide", t2 + 0.2) + shake("#k", t2 + 0.25, n=5, amp=8)
    sfx(s0, "whoosh-short.mp3", 0.5)
    sfx(L("wendung", 1), "pop.mp3", 0.45)
    sfx(L("wendung", 5), "impact-bass-2.mp3", 0.75)
    return sk.scene("wendung", "", body, js)


def s_vote(s0, s1):
    r = lambda t: round(t - s0, 3)  # noqa: E731
    body = sk.strahlen("vbg")
    body += place(fg.kalle_kopf("kv", w=900, mund="open"), 540, 1900).replace("z-index:2", "z-index:1;opacity:0.4")
    body += sk.vote_cards(["WAS SOLL", "KALLE TUN?"], {"titel": "Preise senken", "unter": "Preiskampf mit Dennis"},
                          {"titel": "Omas Kakao", "unter": "Geheimrezept – 40 € Zutaten"}, (ICON_PREIS, ICON_KAKAO))
    js = f'tl.fromTo("#vbg-r",{{rotation:0}},{{rotation:40,duration:{s1 - s0},ease:"none",svgOrigin:"540 1000"}},0);\n'
    js += pop_in("#vt", 0.1) + pop_in("#va", r(L("abstimmung", 1))) + pop_in("#vb", r(L("abstimmung", 2)))
    t = r(L("abstimmung", 4))
    js += pop_in("#vpill", t) + punch("#va", t, 1.06) + punch("#vb", r(Wd("abstimmung", 4, 2)), 1.06)
    js += punch("#vpill", r(L("abstimmung", 5)), 1.1)
    sfx(s0, "whoosh-short.mp3", 0.5)
    sfx(s0 + 0.1, "pop.mp3", 0.5)
    sfx(L("abstimmung", 1), "pop.mp3", 0.55)
    sfx(L("abstimmung", 2), "pop.mp3", 0.55)
    sfx(L("abstimmung", 4), "sparkle.mp3", 0.5)
    return sk.scene("abstimmung", sk.VOTE_CSS, body, js, bg="#12333A")


CUTS = [
    ("recap", 0.0, s_recap),
    ("ergebnis", cut("ergebnis"), s_ergebnis),
    ("verkauf", cut("verkauf"), s_verkauf),
    ("kuehlschrank", cut("kuehlschrank"), s_kuehl),
    ("bauarbeiter", cut("bauarbeiter"), s_bau),
    ("max", cut("max"), s_max),
    ("wendung", cut("wendung"), s_wendung),
    ("abstimmung", cut("abstimmung"), s_vote),
]


def main():
    scenes = []
    for i, (sid, s0, fn) in enumerate(CUTS):
        s1 = CUTS[i + 1][1] if i + 1 < len(CUTS) else TOTAL
        scenes.append((sid, s0, s1, fn(s0, s1)))
    tb = L("bauarbeiter", 6)
    hud = sk.hud_serie(TOTAL, folge=2, tage=29, kasse0=KASSE0,
                       kasse_events=[(L("verkauf", 4), K_VERKAUF), (L("kuehlschrank", 2) + 0.2, K_KUEHL), (tb, K_BAU)],
                       sterne=(tb + 0.9, STERNE0, [(tb + 1.5, STERNE1)]),
                       tage_flip=(L("wendung", 2) + 0.3, 28))
    caps = sk.captions_html(T, TOTAL)
    music = ("music.mp3", 0.16) if (HERE / "assets" / "music.mp3").exists() else None
    sk.write_project(HERE, "Kiosk-Kalle – Folge 2", scenes, sorted(SFX), hud, caps, TOTAL, music=music)
    print(f"{len(scenes)} Szenen, {len(SFX)} SFX, {TOTAL}s")


if __name__ == "__main__":
    main()
