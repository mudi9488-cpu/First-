#!/usr/bin/env python3
"""Baut das Video „Du wachst auf – und bist nur noch 2 cm groß“ (POV, Regeln wie Referenz B).

1. Stimme: python3 ../../tools/align.py . assets/source/<aufnahme>.mp3   (oder tools/tts.py als Platzhalter)
2. python3 build.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "tools"))
from simkit import C, scene_html, hud_card, js_count, load_timings, write_project, rng, fmt  # noqa: E402

SFX_ROOT = "/root/.claude/plugins/cache/hyperframes/hyperframes/0.8.197/skills/media-use/audio/assets/sfx"

T = load_timings(HERE)
TOTAL = round(T["duration"] + 1.4, 2)
B = {b["id"]: b for b in T["beats"]}
ORDER = [b["id"] for b in T["beats"]]
S = {bid: (0.0 if i == 0 else B[bid]["start"]) for i, bid in enumerate(ORDER)}
E = {bid: (S[ORDER[i + 1]] if i + 1 < len(ORDER) else TOTAL) for i, bid in enumerate(ORDER)}


def w(bid, li, wi=0):
    """Startzeit eines Wortes relativ zum Szenenbeginn."""
    return round(B[bid]["lines"][li]["words"][wi]["start"] - S[bid], 3)


def wa(bid, li, wi=0):
    return round(B[bid]["lines"][li]["words"][wi]["start"], 3)


def dur(bid):
    return round(E[bid] - S[bid], 3)


# ------------------------------------------------------------------ Hauptfigur „DU“

SKIN, HAIR, HOODIE, HOODIE2, JEANS = "#F2C9A0", "#5B3A29", C["teal"], "#2FA79F", "#2B3A67"


def du(pid, x, feet, h=300, tag=True, arms="down", face="n"):
    """Cartoon-Figur (Stil Referenz B). x = Mitte, feet = y der Füße. Teile per Klasse schaltbar:
    .m-n/.m-s (Mund normal/erschrocken), .a-d/.a-u (Arme unten/oben)."""
    wdt = h * 0.5
    up = 1 if arms == "up" else 0
    sc = 1 if face == "s" else 0
    t = (f'<div class="du-tag" style="position:absolute;left:0;right:0;top:-58px;text-align:center"><span>DU</span></div>'
         if tag else "")
    return f"""<div id="{pid}" class="du" style="position:absolute;left:{x - wdt / 2:.0f}px;top:{feet - h:.0f}px;width:{wdt:.0f}px;height:{h}px">{t}
      <svg viewBox="0 0 200 400" width="{wdt:.0f}" height="{h}" style="overflow:visible">
        <g class="a-d" opacity="{1 - up}"><rect x="16" y="168" width="32" height="112" rx="16" fill="{HOODIE2}"/>
          <rect x="152" y="168" width="32" height="112" rx="16" fill="{HOODIE2}"/>
          <circle cx="32" cy="282" r="16" fill="{SKIN}"/><circle cx="168" cy="282" r="16" fill="{SKIN}"/></g>
        <g class="a-u" opacity="{up}"><rect x="16" y="60" width="32" height="120" rx="16" fill="{HOODIE2}"/>
          <rect x="152" y="60" width="32" height="120" rx="16" fill="{HOODIE2}"/>
          <circle cx="32" cy="58" r="16" fill="{SKIN}"/><circle cx="168" cy="58" r="16" fill="{SKIN}"/></g>
        <rect x="56" y="270" width="36" height="112" rx="10" fill="{JEANS}"/>
        <rect x="108" y="270" width="36" height="112" rx="10" fill="{JEANS}"/>
        <rect x="48" y="374" width="48" height="26" rx="10" fill="#F4F1E6"/>
        <rect x="104" y="374" width="48" height="26" rx="10" fill="#F4F1E6"/>
        <rect x="38" y="158" width="124" height="134" rx="42" fill="{HOODIE}"/>
        <circle cx="100" cy="94" r="70" fill="{SKIN}"/>
        <path d="M 28 98 Q 26 18 100 20 Q 174 18 172 98 Q 156 52 100 56 Q 46 52 28 98 Z" fill="{HAIR}"/>
        <circle cx="76" cy="100" r="8" fill="#1A1A1A"/><circle cx="124" cy="100" r="8" fill="#1A1A1A"/>
        <path class="m-n" opacity="{1 - sc}" d="M 84 130 Q 100 140 116 130" stroke="#1A1A1A" stroke-width="6" fill="none" stroke-linecap="round"/>
        <ellipse class="m-s" opacity="{sc}" cx="100" cy="134" rx="12" ry="15" fill="#1A1A1A"/>
      </svg></div>"""


DU_CSS = f"""
.du-tag span {{ display:inline-block; font-family:'JetBrains Mono',monospace; font-weight:700; font-size:28px; letter-spacing:0.14em;
  color:{C['gold']}; border:3px solid {C['gold']}; border-radius:10px; padding:2px 14px; background:rgba(14,21,36,0.85); }}
.pill {{ z-index:4; }}
.hudcard {{ z-index:4; }}
.rt {{ position:absolute; left:0; right:0; top:560px; text-align:center; z-index:5; }}
.rt div {{ display:inline-block; font-weight:900; font-size:150px; color:{C['gold']}; line-height:1; padding-bottom:16px;
  border-bottom:10px solid {C['gold']}; }}
"""


def rule_title(p, n):
    return f'<div class="rt" id="{p}-rt"><div>REGEL {n}</div></div>'


def rule_title_js(p, off):
    """Großer Kapitel-Titel (wie „REGEL 1“ in Referenz B): sofort da, verschwindet bei `off`."""
    return (f'    tl.fromTo("#{p}-rt div", {{scale:1.25, opacity:0}}, {{scale:1, opacity:1, duration:0.25, ease:"expo.out"}}, 0.02);\n'
            f'    tl.to("#{p}-rt div", {{opacity:0, y:-40, filter:"blur(8px)", duration:0.22, ease:"power2.in"}}, {off});\n')


def pill(pid, text, col, top, extra=""):
    return (f'<div class="pill" id="{pid}" style="left:0;right:0;margin:0 auto;width:max-content;top:{top}px;'
            f'background:{col};color:#0A0F1C;{extra}">{text}</div>')


def pop_js(sel, at, frm=1.5):
    return f'    tl.fromTo("{sel}", {{scale:{frm}, opacity:0}}, {{scale:1, opacity:1, duration:0.25, ease:"expo.out"}}, {at});\n'


FLOOR = f'<div style="position:absolute;left:0;right:0;top:1110px;bottom:0;background:#3A2B22"></div>' \
        f'<div style="position:absolute;left:0;right:0;top:1110px;height:10px;background:#5A4434"></div>'


# ------------------------------------------------------------------ 1 Hook: Bett-Landschaft

def scene_hook():
    body = f"""
    <div id="hk-world" style="position:absolute;inset:0">
      <svg viewBox="0 0 1080 1920" width="1080" height="1920" style="position:absolute;left:0;top:0">
        <path d="M -40 760 Q 200 640 420 720 Q 640 800 860 690 Q 1000 630 1120 700 L 1120 1920 L -40 1920 Z" fill="#5C4FA8"/>
        <path d="M -40 900 Q 260 800 520 880 Q 760 950 1120 860 L 1120 1920 L -40 1920 Z" fill="#6B5DC0"/>
        <path d="M 60 980 Q 300 930 540 990 M 600 1010 Q 820 960 1040 1000" stroke="#7D70D0" stroke-width="10" fill="none" stroke-linecap="round"/>
        <rect x="740" y="760" width="480" height="260" rx="110" fill="#E8E4F4"/>
        <path d="M 780 900 Q 930 870 1080 905" stroke="#CFC8E6" stroke-width="12" fill="none"/>
      </svg>
      {du("hk-du", 360, 960, h=230, tag=False, face="s")}
    </div>
    <div class="title" style="position:absolute;left:50px;right:50px;top:300px;text-align:center;z-index:5" id="hk-title">
      <div style="font-weight:900;font-size:58px;color:{C['mute']};line-height:1.05">DU WACHST AUF …</div>
      <div style="font-weight:900;font-size:96px;color:{C['gold']};line-height:1.0">UND BIST NUR</div>
      <div style="font-weight:900;font-size:120px;color:{C['red']};line-height:1.0">2 CM GROSS</div>
    </div>"""
    js = f"""
    tl.fromTo("#hk-world", {{scale:1.5, transformOrigin:"33% 50%"}}, {{scale:1, duration:{w('hook', 2, 1) + 0.3}, ease:"power2.inOut"}}, 0);
    tl.fromTo("#hk-du", {{y:0}}, {{y:-12, duration:0.18, yoyo:true, repeat:5, ease:"sine.inOut"}}, {w('hook', 0, 2)});
    tl.to("#hk-title", {{opacity:0, filter:"blur(8px)", duration:0.25, ease:"power2.in"}}, {dur('hook') - 0.3});
"""
    return scene_html("hook", DU_CSS + ".bg{background:#2A2350;}", body, js)


# ------------------------------------------------------------------ 2 Größe: Lineal, Gummibärchen, Bett-Hochhaus

def scene_groesse():
    ticks = "".join(f'<rect x="{0 if i % 5 else 0}" y="{i * 34}" width="{60 if i % 5 == 0 else 34}" height="5" fill="#3B2A10"/>'
                    for i in range(0, 21))
    nums = "".join(f'<text x="70" y="{i * 34 + 14}" font-family="JetBrains Mono" font-weight="700" font-size="30" fill="#3B2A10">{(20 - i) // 10}</text>'
                   for i in (0, 10))
    body = hud_card("gc", "Deine Größe", "180", unit="cm", color=C["gold"], top=290) + f"""
    {FLOOR}
    <div id="gr-a" style="position:absolute;inset:0">
      <svg id="gr-ruler" viewBox="0 0 140 720" width="140" height="720" style="position:absolute;left:140px;top:400px">
        <rect x="0" y="0" width="140" height="720" rx="10" fill="{C['gold']}"/><g transform="translate(0,20)">{ticks}{nums}</g>
      </svg>
      {du("gr-du", 420, 1110, h=340, tag=False)}
      <svg id="gr-bear" viewBox="0 0 240 340" width="240" height="340" style="position:absolute;left:640px;top:770px">
        <g fill="#FF4D5E" opacity="0.88">
          <circle cx="120" cy="80" r="70"/><circle cx="62" cy="26" r="28"/><circle cx="178" cy="26" r="28"/>
          <ellipse cx="120" cy="220" rx="96" ry="110"/><ellipse cx="36" cy="190" rx="34" ry="48"/><ellipse cx="204" cy="190" rx="34" ry="48"/>
          <ellipse cx="70" cy="318" rx="44" ry="30"/><ellipse cx="170" cy="318" rx="44" ry="30"/></g>
        <ellipse cx="88" cy="60" rx="18" ry="26" fill="#fff" opacity="0.35"/>
      </svg>
    </div>
    <div id="gr-b" style="position:absolute;inset:0;opacity:0">
      <svg viewBox="0 0 1080 1920" width="1080" height="1920" style="position:absolute;left:0;top:0">
        <rect x="300" y="-40" width="560" height="980" fill="#6B5DC0"/>
        <rect x="300" y="900" width="560" height="60" fill="#5C4FA8"/>
        <rect x="330" y="960" width="70" height="150" fill="#7A5638"/><rect x="760" y="960" width="70" height="150" fill="#7A5638"/>
        <g stroke="{C['gold']}" stroke-width="6"><line x1="230" y1="500" x2="230" y2="1100"/><line x1="200" y1="1100" x2="260" y2="1100"/>
          <path d="M 210 530 L 230 500 L 250 530" fill="none"/></g>
      </svg>
      {du("gr-du2", 560, 1110, h=70, tag=False)}
      {pill("gr-p", "FÜR DICH: 45 m · 15 STOCKWERKE", C['gold'], 560)}
    </div>"""
    a, b = w("groesse", 1, 0), w("groesse", 1, 2)
    bear, bed = w("groesse", 3, 1), w("groesse", 4, 0)
    js = js_count("gc-num", 180, 2, a, b - a + 0.3, ease="power3.in")
    js += f"""
    tl.fromTo("#gr-ruler", {{y:80, opacity:0}}, {{y:0, opacity:1, duration:0.5, ease:"expo.out"}}, 0.1);
    tl.fromTo("#gr-du", {{scale:1}}, {{scale:0.33, duration:{b - a + 0.3}, ease:"power3.in", transformOrigin:"50% 100%"}}, {a});
    tl.to("#gc-num", {{color:"{C['red']}", duration:0.1}}, {b + 0.3});
    tl.fromTo("#gr-bear", {{y:-500, opacity:0}}, {{y:0, opacity:1, duration:0.5, ease:"bounce.out"}}, {bear - 0.15});
    tl.to("#gr-a", {{opacity:0, duration:0.2}}, {bed - 0.1});
    tl.fromTo("#gr-b", {{opacity:0}}, {{opacity:1, duration:0.2}}, {bed - 0.1});
    tl.fromTo("#gr-b svg", {{y:200}}, {{y:0, duration:0.8, ease:"expo.out"}}, {bed - 0.1});
"""
    js += pop_js("#gr-p", bed + 0.5)
    return scene_html("groesse", DU_CSS, body, js)


# ------------------------------------------------------------------ 3 Regel 1: Fallen

def scene_fallen():
    body = rule_title("fa", 1) + f"""
    {FLOOR}
    <div id="fa-world" style="position:absolute;inset:0">
      <svg viewBox="0 0 1080 1920" width="1080" height="1920" style="position:absolute;left:0;top:0">
        <rect x="-20" y="560" width="560" height="120" rx="20" fill="#6B5DC0"/>
        <rect x="-20" y="680" width="560" height="40" fill="#5C4FA8"/>
        <rect x="420" y="720" width="70" height="390" fill="#7A5638"/>
        <path id="fa-trail" d="M 470 560 C 560 700 600 900 640 1100" stroke="#fff" stroke-width="6" stroke-dasharray="4 22"
          stroke-linecap="round" fill="none" opacity="0"/>
      </svg>
      {du("fa-du", 440, 560, h=150)}
    </div>
    {hud_card("fc", "Fallhöhe für dich", "45", unit="m", color=C["red"], top=290)}
    {pill("fa-p", "AUFPRALL: HARMLOS", C['green'], 520)}"""
    off, jump, land = w("fallen", 1, 0) - 0.1, w("fallen", 3, 1), w("fallen", 4, 2)
    js = rule_title_js("fa", off)
    js += f"""
    tl.fromTo("#fa-world", {{opacity:0}}, {{opacity:1, duration:0.3}}, {off});
    tl.fromTo("#fc", {{y:-30, opacity:0}}, {{y:0, opacity:1, duration:0.4, ease:"expo.out"}}, {off + 0.1});
    tl.set("#fa-du .m-n", {{opacity:0}}, {w('fallen', 2, 2)});
    tl.set("#fa-du .m-s", {{opacity:1}}, {w('fallen', 2, 2)});
    tl.fromTo("#fa-du", {{x:0, y:0, rotation:0}}, {{x:200, y:550, rotation:14, duration:{land - jump + 0.2:.2f}, ease:"power1.in"}}, {jump});
    tl.set("#fa-du .a-d", {{opacity:0}}, {jump});
    tl.set("#fa-du .a-u", {{opacity:1}}, {jump});
    tl.fromTo("#fa-trail", {{opacity:0}}, {{opacity:0.6, duration:0.3}}, {jump + 0.2});
    tl.to("#fa-du", {{rotation:0, duration:0.25, ease:"back.out(2)"}}, {land + 0.22});
    tl.set("#fa-du .a-u", {{opacity:0}}, {land + 0.2});
    tl.set("#fa-du .a-d", {{opacity:1}}, {land + 0.2});
    tl.set("#fa-du .m-s", {{opacity:0}}, {land + 0.2});
    tl.set("#fa-du .m-n", {{opacity:1}}, {land + 0.2});
"""
    js += pop_js("#fa-p", land + 0.2)
    return scene_html("fallen", DU_CSS, body, js)


# ------------------------------------------------------------------ 4 Regel 2: Wasser

def scene_wasser():
    body = rule_title("wa", 2) + f"""
    {FLOOR}
    <div id="wa-world" style="position:absolute;inset:0">
      <svg viewBox="0 0 1080 1920" width="1080" height="1920" style="position:absolute;left:0;top:0">
        <g id="wa-drop"><path d="M 560 1110 Q 520 620 760 600 Q 1000 620 960 1110 Z" fill="#4FA8FF" opacity="0.82"/>
          <ellipse cx="690" cy="760" rx="44" ry="90" fill="#fff" opacity="0.4" transform="rotate(20 690 760)"/></g>
      </svg>
      {du("wa-du", 300, 1110, h=280)}
    </div>
    {hud_card("wc", "Ein Tropfen für dich", "36", unit="Liter", color=C["blue"], top=290)}
    {pill("wa-p", "OBERFLÄCHENSPANNUNG", C['red'], 520)}"""
    off, touch, stuck = w("wasser", 1, 0) - 0.1, w("wasser", 3, 0), w("wasser", 4, 2)
    js = rule_title_js("wa", off)
    js += f"""
    tl.fromTo("#wa-world", {{opacity:0}}, {{opacity:1, duration:0.3}}, {off});
    tl.fromTo("#wc", {{y:-30, opacity:0}}, {{y:0, opacity:1, duration:0.4, ease:"expo.out"}}, {off + 0.1});
    tl.fromTo("#wa-drop", {{scaleY:0.9}}, {{scaleY:1.04, duration:0.6, yoyo:true, repeat:9, ease:"sine.inOut", transformOrigin:"50% 100%"}}, 0);
    tl.fromTo("#wa-du", {{x:0}}, {{x:250, duration:{touch - off - 0.3:.2f}, ease:"power1.inOut"}}, {off + 0.3});
    tl.to("#wa-du", {{x:300, duration:0.25, ease:"power3.in"}}, {touch});
    tl.set("#wa-du .m-n", {{opacity:0}}, {touch + 0.25});
    tl.set("#wa-du .m-s", {{opacity:1}}, {touch + 0.25});
    tl.fromTo("#wa-du svg", {{x:0}}, {{x:-14, duration:0.08, yoyo:true, repeat:17, ease:"sine.inOut"}}, {stuck - 0.6});
"""
    js += pop_js("#wa-p", touch + 0.3)
    return scene_html("wasser", DU_CSS, body, js)


# ------------------------------------------------------------------ 5 Regel 3: Kälte

def scene_kaelte():
    r = rng(4)
    frost = "".join(f'<circle class="kf" cx="{r.randint(30, 1050)}" cy="{r.randint(450, 1100)}" r="{r.choice([4, 6, 8])}" fill="#CFE6FF" opacity="0"/>'
                    for _ in range(40))
    body = rule_title("ka", 3) + f"""
    {FLOOR}
    <div id="ka-world" style="position:absolute;inset:0">
      <div id="ka-cold" style="position:absolute;inset:0;background:#4FA8FF;opacity:0"></div>
      <svg viewBox="0 0 1080 1920" width="1080" height="1920" style="position:absolute;left:0;top:0">{frost}
        <g id="ka-crumb"><path d="M 600 1110 L 590 900 L 660 820 L 780 800 L 900 860 L 960 980 L 940 1110 Z" fill="#C98A4B"/>
          <circle cx="700" cy="900" r="18" fill="#7A4A22"/><circle cx="840" cy="960" r="14" fill="#7A4A22"/><circle cx="760" cy="1040" r="16" fill="#7A4A22"/></g>
      </svg>
      {du("ka-du", 340, 1110, h=280)}
    </div>
    {hud_card("kc", "Körpertemperatur", "37,0", unit="°C", color=C["green"], top=290)}
    {pill("ka-p", "1 KRÜMEL = 1 MAHLZEIT", C['gold'], 520)}"""
    off, fast, crumb = w("kaelte", 1, 0) - 0.1, w("kaelte", 4, 0), w("kaelte", 5, 1)
    js = rule_title_js("ka", off)
    js += f"""
    tl.fromTo("#ka-world", {{opacity:0}}, {{opacity:1, duration:0.3}}, {off});
    tl.fromTo("#kc", {{y:-30, opacity:0}}, {{y:0, opacity:1, duration:0.4, ease:"expo.out"}}, {off + 0.1});
    tl.fromTo("#ka-cold", {{opacity:0}}, {{opacity:0.22, duration:{fast - off:.2f}, ease:"power1.in"}}, {off});
    tl.fromTo(".kf", {{opacity:0}}, {{opacity:0.8, duration:0.2, stagger:0.04}}, {fast - 1.0});
    tl.fromTo("#ka-du svg", {{x:0}}, {{x:-8, duration:0.06, yoyo:true, repeat:25, ease:"sine.inOut"}}, {fast - 0.6});
    tl.to("#kc-num", {{color:"{C['blue']}", duration:0.3}}, {fast});
    tl.fromTo("#ka-crumb", {{y:-700, opacity:1}}, {{y:0, opacity:1, duration:0.55, ease:"bounce.out"}}, {crumb - 0.35});
    tl.to("#ka-du", {{x:200, duration:0.6, ease:"power2.inOut"}}, {crumb + 0.3});
    tl.to("#ka-cold", {{opacity:0.08, duration:0.6}}, {crumb + 0.5});
"""
    js += js_count("kc-num", 37.0, 35.4, off + 0.2, fast - off + 0.3, decimals=1, ease="power1.in")
    js += pop_js("#ka-p", crumb + 0.1)
    return scene_html("kaelte", DU_CSS, body, js)


# ------------------------------------------------------------------ 6 Regel 4: Spinne

def scene_spinne():
    legs = []
    for side in (-1, 1):
        for k, (dx, dy, kx, ky) in enumerate(((260, -220, 140, -260), (330, -60, 200, -160), (330, 120, 220, -20), (260, 300, 170, 140))):
            legs.append(f'<path class="sp-leg" d="M 0 0 Q {side * kx} {ky} {side * dx} {dy}" stroke="#0B0F18" stroke-width="26" fill="none" stroke-linecap="round"/>')
    body = rule_title("sp", 4) + f"""
    {FLOOR}
    <div id="sp-world" style="position:absolute;inset:0">
      <div style="position:absolute;inset:0;background:radial-gradient(ellipse 70% 50% at 70% 40%,#1E2238 0%,#0A0D16 80%)"></div>
      <div id="sp-spider" style="position:absolute;left:400px;top:420px;width:600px;height:600px">
        <svg viewBox="-350 -350 700 700" width="600" height="600" style="overflow:visible">
          <g>{''.join(legs)}</g>
          <ellipse cx="0" cy="110" rx="150" ry="180" fill="#151A26"/><circle cx="0" cy="-90" r="110" fill="#1B2130"/>
          <g fill="{C['red']}"><circle cx="-40" cy="-110" r="18"/><circle cx="40" cy="-110" r="18"/><circle cx="-80" cy="-80" r="10"/><circle cx="80" cy="-80" r="10"/></g>
        </svg></div>
      {du("sp-du", 220, 1110, h=240, face="s")}
    </div>
    {hud_card("sc", "Spinne für dich", "6", unit="Meter", color=C["red"], top=290)}
    {pill("sp-p", "SO GROSS WIE EIN AUTO", C['red'], 520, "color:#fff")}"""
    off, auto = w("spinne", 1, 0) - 0.1, w("spinne", 3, 4)
    js = rule_title_js("sp", off)
    js += f"""
    tl.fromTo("#sp-world", {{opacity:0}}, {{opacity:1, duration:0.3}}, {off});
    tl.fromTo("#sc", {{y:-30, opacity:0}}, {{y:0, opacity:1, duration:0.4, ease:"expo.out"}}, {off + 0.1});
    tl.fromTo("#sp-spider", {{y:-500}}, {{y:0, duration:1.2, ease:"power2.out"}}, {off + 0.2});
    tl.fromTo(".sp-leg", {{rotation:0}}, {{rotation:4, duration:0.3, yoyo:true, repeat:9, ease:"sine.inOut", stagger:0.05,
      transformOrigin:"0px 0px"}}, {off + 0.4});
    tl.to("#sp-spider", {{scale:1.12, x:-60, duration:0.25, ease:"power3.out"}}, {auto});
    tl.fromTo("#sp-du", {{x:0}}, {{x:-90, duration:0.25, ease:"power3.out"}}, {auto});
"""
    js += pop_js("#sp-p", w("spinne", 3, 1))
    return scene_html("spinne", DU_CSS, body, js)


# ------------------------------------------------------------------ 7 Regel 5: Stimme

def wave(freq, amp):
    import math
    pts = " ".join(f"{x},{40 + amp * math.sin(x / 480 * 6.283 * freq):.1f}" for x in range(0, 481, 4))
    return pts


def scene_stimme():
    body = rule_title("st", 5) + f"""
    {FLOOR}
    <div id="st-world" style="position:absolute;inset:0">
      <div id="st-shoe" style="position:absolute;left:420px;top:-480px;width:760px;height:420px">
        <svg viewBox="0 0 760 420" width="760" height="420"><path d="M 40 300 Q 20 120 200 100 L 560 60 Q 740 60 740 260 L 740 340 L 40 340 Z" fill="#E6E9F0"/>
          <rect x="30" y="330" width="720" height="70" rx="30" fill="#2A2F3A"/><path d="M 200 140 L 420 120" stroke="#B8C0D0" stroke-width="16"/></svg></div>
      {du("st-du", 330, 1110, h=280)}
      <svg id="st-rings" viewBox="0 0 400 400" width="400" height="400" style="position:absolute;left:330px;top:720px" fill="none" stroke="{C['gold']}" stroke-width="8" stroke-linecap="round">
        <path class="st-r" d="M 60 120 Q 110 200 60 280"/><path class="st-r" d="M 120 80 Q 190 200 120 320"/><path class="st-r" d="M 180 40 Q 270 200 180 360"/>
      </svg>
    </div>
    <div class="hudcard" id="vc" style="top:290px;width:560px;margin-left:-280px">
      <div class="lab">Deine Stimme</div>
      <svg viewBox="0 0 480 80" width="480" height="80" style="display:block;margin-top:10px">
        <polyline id="vc-lo" points="{wave(3, 30)}" fill="none" stroke="{C['gold']}" stroke-width="5"/>
        <polyline id="vc-hi" points="{wave(22, 30)}" fill="none" stroke="{C['red']}" stroke-width="4" opacity="0"/>
      </svg>
    </div>
    {pill("st-p", "NIEMAND HÖRT DICH", C['red'], 520, "color:#fff")}"""
    off, hoch, leise, niemand = w("stimme", 1, 0) - 0.1, w("stimme", 3, 1), w("stimme", 3, 3), w("stimme", 4, 2)
    js = rule_title_js("st", off)
    js += f"""
    tl.fromTo("#st-world", {{opacity:0}}, {{opacity:1, duration:0.3}}, {off});
    tl.fromTo("#vc", {{y:-30, opacity:0}}, {{y:0, opacity:1, duration:0.4, ease:"expo.out"}}, {off + 0.1});
    tl.set("#st-du .m-n", {{opacity:0}}, {off + 0.3});
    tl.set("#st-du .m-s", {{opacity:1}}, {off + 0.3});
    tl.set("#st-du .a-d", {{opacity:0}}, {off + 0.3});
    tl.set("#st-du .a-u", {{opacity:1}}, {off + 0.3});
    tl.fromTo(".st-r", {{opacity:0}}, {{opacity:1, duration:0.15, stagger:0.12, yoyo:true, repeat:5}}, {off + 0.3});
    tl.set("#vc-lo", {{opacity:0}}, {hoch});
    tl.set("#vc-hi", {{opacity:1}}, {hoch});
    tl.to("#vc-hi", {{scaleY:0.15, duration:0.4, ease:"power2.in", transformOrigin:"50% 50%"}}, {leise});
    tl.to("#st-rings", {{scale:0.4, opacity:0.3, duration:0.4, transformOrigin:"0% 50%"}}, {leise});
    tl.fromTo("#st-shoe", {{y:0, x:0}}, {{y:1130, x:-120, duration:0.6, ease:"power3.in"}}, {niemand - 0.3});
    tl.to("#st-shoe", {{y:-300, x:-700, duration:0.9, ease:"power2.inOut"}}, {niemand + 0.6});
"""
    js += pop_js("#st-p", niemand)
    return scene_html("stimme", DU_CSS, body, js)


# ------------------------------------------------------------------ 8 Twist: superstark

def scene_stark():
    body = f"""
    {FLOOR}
    <div id="sk-world" style="position:absolute;inset:0">
      <div id="sk-cube" style="position:absolute;left:340px;top:730px;width:400px;height:380px">
        <svg viewBox="0 0 400 380" width="400" height="380">
          <path d="M 200 20 L 380 100 L 200 180 L 20 100 Z" fill="#FFFFFF"/>
          <path d="M 20 100 L 200 180 L 200 370 L 20 290 Z" fill="#DDE3EE"/>
          <path d="M 380 100 L 200 180 L 200 370 L 380 290 Z" fill="#C3CBDA"/>
          <g fill="#AEB8CC" opacity="0.6"><circle cx="90" cy="200" r="6"/><circle cx="140" cy="260" r="5"/><circle cx="290" cy="220" r="6"/><circle cx="320" cy="280" r="5"/></g>
        </svg></div>
      {du("sk-du", 540, 1110, h=240)}
    </div>
    {hud_card("kc2", "Du hebst", "1", unit="× dein Gewicht", color=C["green"], top=290)}
    <div class="pill" id="sk-p" style="left:618px;top:960px;background:{C['green']};color:#0A0F1C;font-size:48px">SUPERSTARK</div>"""
    lift, x25, sup = w("stark", 3, 1), w("stark", 4, 1), w("stark", 6, 2)
    js = f"""
    tl.fromTo("#kc2", {{y:-30, opacity:0}}, {{y:0, opacity:1, duration:0.4, ease:"expo.out"}}, 0.2);
    tl.fromTo("#sk-du", {{x:-300}}, {{x:0, duration:{lift - 0.4:.2f}, ease:"power1.inOut"}}, 0.2);
    tl.set("#sk-du .a-d", {{opacity:0}}, {lift});
    tl.set("#sk-du .a-u", {{opacity:1}}, {lift});
    tl.fromTo("#sk-cube", {{y:0}}, {{y:-250, duration:0.7, ease:"power2.out"}}, {lift});
    tl.fromTo("#sk-du svg", {{scaleY:1}}, {{scaleY:0.92, duration:0.12, yoyo:true, repeat:1, transformOrigin:"50% 100%"}}, {lift});
    tl.to("#kc2-num", {{color:"{C['green']}", duration:0.1}}, {x25});
    tl.to("#sk-cube", {{y:-270, duration:0.4, yoyo:true, repeat:7, ease:"sine.inOut"}}, {lift + 0.7});
"""
    js += js_count("kc2-num", 1, 25, x25 - 0.5, 1.0, ease="power2.out")
    js += pop_js("#sk-p", sup, 2.0)
    return scene_html("stark", DU_CSS, body, js)


# ------------------------------------------------------------------ 9 Ende: Saugroboter (Cliffhanger)

def scene_ende():
    body = f"""
    {FLOOR}
    <div id="en-world" style="position:absolute;inset:0">
      <svg viewBox="0 0 1080 1920" width="1080" height="1920" style="position:absolute;left:0;top:0">
        <rect x="760" y="-40" width="420" height="1150" fill="#6E4B32"/>
        <rect x="760" y="1096" width="420" height="14" fill="#F5C451" opacity="0.8"/>
        <circle cx="800" cy="560" r="20" fill="{C['gold']}"/>
      </svg>
      {du("en-du", 300, 1110, h=260)}
      <div id="en-robot" data-layout-ignore style="position:absolute;left:-1000px;top:900px;width:1000px;height:300px">
        <svg viewBox="0 0 1000 300" width="1000" height="300">
          <ellipse cx="500" cy="210" rx="500" ry="90" fill="#0B0F18"/>
          <rect x="0" y="40" width="1000" height="170" rx="85" fill="#2A2F3A"/>
          <ellipse cx="500" cy="40" rx="500" ry="70" fill="#3A404D"/>
          <circle id="en-led" cx="760" cy="40" r="22" fill="{C['red']}"/>
        </svg></div>
      <div id="en-dark" style="position:absolute;inset:0;background:#000;opacity:0"></div>
    </div>
    {pill("en-p", "REINIGUNG GESTARTET · 08:00", C['red'], 520, "color:#fff")}"""
    summen, robo = w("ende", 2, 3), w("ende", 3, 1)
    end = dur("ende")
    js = f"""
    tl.fromTo("#en-du", {{x:0}}, {{x:220, duration:{summen - 0.3:.2f}, ease:"power1.inOut"}}, 0.1);
    tl.set("#en-du .m-n", {{opacity:0}}, {summen});
    tl.set("#en-du .m-s", {{opacity:1}}, {summen});
    tl.fromTo("#en-world", {{x:0}}, {{x:6, duration:0.05, yoyo:true, repeat:{int((end - summen) / 0.1)}, ease:"none"}}, {summen});
    tl.fromTo("#en-robot", {{x:0}}, {{x:700, duration:{end - robo:.2f}, ease:"power1.in"}}, {robo - 0.3});
    tl.fromTo("#en-led", {{opacity:1}}, {{opacity:0.2, duration:0.25, yoyo:true, repeat:{int((end - robo) / 0.25)}}}, {robo});
    tl.fromTo("#en-dark", {{opacity:0}}, {{opacity:0.55, duration:{end - robo:.2f}, ease:"power2.in"}}, {robo});
"""
    js += pop_js("#en-p", robo)
    return scene_html("ende", DU_CSS, body, js)


# ------------------------------------------------------------------ zusammensetzen

SCENES = [("hook", scene_hook()), ("groesse", scene_groesse()), ("fallen", scene_fallen()), ("wasser", scene_wasser()),
          ("kaelte", scene_kaelte()), ("spinne", scene_spinne()), ("stimme", scene_stimme()), ("stark", scene_stark()),
          ("ende", scene_ende())]

SFX = [
    (wa("hook", 2, 1), "impact-bass-1.mp3", 0.45),
    (S["groesse"] - 0.15, "whoosh-short.mp3", 0.5),
    (wa("groesse", 1, 2), "glitch-1.mp3", 0.25),
    (wa("groesse", 3, 1), "pop.mp3", 0.5),
    (wa("groesse", 4, 0) - 0.1, "whoosh.mp3", 0.45),
    (S["fallen"] - 0.1, "impact-bass-2.mp3", 0.35),
    (wa("fallen", 3, 1), "whoosh-cinematic.mp3", 0.3),
    (wa("fallen", 4, 2) + 0.2, "pop.mp3", 0.5),
    (S["wasser"] - 0.1, "impact-bass-2.mp3", 0.35),
    (wa("wasser", 3, 0) + 0.25, "click-soft.mp3", 0.5),
    (wa("wasser", 3, 0) + 0.3, "error.mp3", 0.35),
    (S["kaelte"] - 0.1, "impact-bass-2.mp3", 0.35),
    (wa("kaelte", 5, 1) - 0.1, "pop.mp3", 0.5),
    (S["spinne"] - 0.1, "impact-bass-2.mp3", 0.35),
    (wa("spinne", 3, 4), "impact-bass-1.mp3", 0.55),
    (S["stimme"] - 0.1, "impact-bass-2.mp3", 0.35),
    (wa("stimme", 3, 1), "glitch-3.mp3", 0.2),
    (wa("stimme", 4, 2) + 0.25, "impact-bass-1.mp3", 0.5),
    (S["stark"] - 0.15, "whoosh.mp3", 0.5),
    (wa("stark", 3, 1), "whoosh-short.mp3", 0.4),
    (wa("stark", 6, 2), "sparkle.mp3", 0.5),
    (S["ende"] - 0.15, "whoosh-short.mp3", 0.5),
    (wa("ende", 2, 3) - 0.3, "riser.mp3", 0.25),
    (wa("ende", 3, 1), "error.mp3", 0.4),
]

CHECKLIST = [
    (wa("fallen", 4, 2) + 0.4, "1 · FALLEN", C["gold"]),
    (wa("wasser", 4, 2) + 0.3, "2 · WASSER", C["gold"]),
    (wa("kaelte", 6, 3), "3 · KÄLTE", C["gold"]),
    (wa("spinne", 3, 4) + 0.4, "4 · SPINNE", C["gold"]),
    (wa("stimme", 4, 2) + 0.5, "5 · STIMME", C["gold"]),
]

if __name__ == "__main__":
    write_project(HERE, "Du wachst auf – und bist nur noch 2 cm groß",
                  [(sid, S[sid], E[sid], html) for sid, html in SCENES],
                  SFX, CHECKLIST, TOTAL, sfx_root=SFX_ROOT, check_end=S["ende"])
    print("ok:", ", ".join(f"{sid} {fmt(S[sid])}-{fmt(E[sid])}" for sid, _ in SCENES), "| total", TOTAL)
