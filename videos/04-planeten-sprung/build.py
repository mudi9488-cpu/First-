#!/usr/bin/env python3
"""Baut „Was wäre, wenn du auf jedem Planeten einmal hochspringst?“ – Bahnen-Simulation wie Referenz A.

Physik: gleiche Absprunggeschwindigkeit v (= 50 cm auf der Erde). Höhe h = v²/2g, Flugzeit 2v/g.
1. Stimme: python3 ../../tools/align.py . assets/source/<aufnahme>.mp3   (Platzhalter: tools/tts.py)
2. python3 build.py
"""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "tools"))
from simkit import C, load_timings, fmt, audio_len, captions_html, rng  # noqa: E402

SFX_ROOT = Path("/root/.claude/plugins/cache/hyperframes/hyperframes/0.8.197/skills/media-use/audio/assets/sfx")
W, H = 1080, 1920

T = load_timings(HERE)
B = {b["id"]: b for b in T["beats"]}
VOICE_END = T["beats"][-1]["end"]
TOTAL = round(VOICE_END + 2.4, 2)


def wa(bid, li, wi=0):
    return round(B[bid]["lines"][li]["words"][wi]["start"], 3)


def lend(bid, li):
    return round(B[bid]["lines"][li]["end"], 3)


V = math.sqrt(2 * 9.81 * 0.5)
PHASE1 = [("ju", "Jupiter", 24.79, "#D9A066"), ("er", "Erde", 9.81, "#4F9BE8"), ("ma", "Mars", 3.71, "#C1502E"), ("mo", "Mond", 1.62, "#B8BCC6")]
PHASE2 = [("mo2", "Mond", 1.62, "#B8BCC6"), ("pl", "Pluto", 0.62, "#C9B7A0"), ("ce", "Ceres", 0.28, "#8A8F99"), ("be", "Bennu", 0.0, "#6E6A64")]

K = {
    "jump1": lend("setup", 3) - 0.1,
    # Zeitlupe: Sim-Zeit landet genau, wenn der Sprecher davon erzählt
    "a1": [[lend("setup", 3) - 0.1, 0], [wa("jupiter", 2, 2), 2 * V / 24.79], [wa("erde", 2, 3), 2 * V / 9.81],
           [lend("mars", 2) - 0.3, 2 * V / 3.71], [lend("mond", 2) - 0.2, 2 * V / 1.62]],
    "switch": B["hoeher"]["start"],
    "jump2": lend("hoeher", 0) + 0.15,
    "a2": [[lend("hoeher", 0) + 0.15, 0], [lend("pluto", 2) - 0.2, 2 * V / 0.62], [lend("ceres", 2) - 0.3, 2 * V / 0.28]],
    "focus": [[B["jupiter"]["start"], "ju"], [B["erde"]["start"], "er"], [B["mars"]["start"], "ma"], [B["mond"]["start"], "mo"],
              [B["hoeher"]["start"], ""], [B["pluto"]["start"], "pl"], [B["ceres"]["start"], "ce"], [B["bennu"]["start"], "be"],
              [B["frage"]["start"], ""]],
    "warum": B["warum"]["start"],
    "bennu_pill": wa("bennu", 2, 2),
    "end": B["frage"]["start"] - 0.1,
    "v": V,
}

GROUND = 1110
X0, LW = 110, 230
S1, S2 = 125.0, 30.0       # Pixel pro Meter in Phase 1 / 2


def lane_svg(prefix, lanes, scale):
    r = rng(3)
    out = []
    for i, (lid, name, g, col) in enumerate(lanes):
        x = X0 + i * LW
        cx = x + LW / 2
        h = (V * V / 2 / g) if g else None
        tf = (2 * V / g) if g else None
        gtxt = f"{g:.2f}".replace(".", ",") if g else "≈ 0"
        f = scale / 140
        peak_y = GROUND - h * scale if h else -100
        out.append(f"""
      <g id="{lid}-lane">
        <rect x="{x + 6}" y="350" width="{LW - 12}" height="{GROUND - 350}" rx="18" fill="#FFFFFF" opacity="0.03"/>
        <circle cx="{x + 42}" cy="402" r="26" fill="{col}"/>
        <text x="{x + 78}" y="397" font-family="Inter" font-weight="800" font-size="32" fill="#fff">{name}</text>
        <text x="{x + 78}" y="430" font-family="JetBrains Mono" font-weight="700" font-size="28" fill="{C['mute']}">g {gtxt}</text>
        <rect x="{x + 6}" y="{GROUND}" width="{LW - 12}" height="26" rx="6" fill="{col}"/>
        <line id="{lid}-peak" x1="{x + 14}" x2="{x + LW - 14}" y1="{peak_y:.1f}" y2="{peak_y:.1f}" stroke="{C['gold']}" stroke-width="4" stroke-dasharray="10 10" opacity="0"/>
        <g id="{lid}-fig" transform="translate({cx},{GROUND})"><g transform="scale({f:.4f})">
          <g class="armsdown"><rect x="-38" y="-200" width="14" height="92" rx="7" fill="{C['teal']}" opacity="0.8"/><rect x="24" y="-200" width="14" height="92" rx="7" fill="{C['teal']}" opacity="0.8"/></g>
          <g class="armsup" opacity="0"><rect x="-40" y="-292" width="14" height="96" rx="7" fill="{C['teal']}" opacity="0.8"/><rect x="26" y="-292" width="14" height="96" rx="7" fill="{C['teal']}" opacity="0.8"/></g>
          <rect x="-22" y="-205" width="44" height="112" rx="22" fill="{C['teal']}"/>
          <rect x="-20" y="-100" width="16" height="100" rx="8" fill="{C['teal']}"/><rect x="4" y="-100" width="16" height="100" rx="8" fill="#2FA79F"/>
          <circle cx="0" cy="-232" r="27" fill="#F4F1E6"/></g></g>
        <text id="{lid}-h" x="{cx}" y="{GROUND - 280 * f - 20:.0f}" text-anchor="middle" font-family="JetBrains Mono" font-weight="700" font-size="30" fill="#fff">0,00 m</text>
        <g id="{lid}-done" opacity="0">
          <rect x="{cx - 92}" y="{GROUND - 60}" width="184" height="44" rx="22" fill="{C['green']}"/>
          <text x="{cx}" y="{GROUND - 29}" text-anchor="middle" font-family="Inter" font-weight="900" font-size="28" fill="#0A0F1C">{(f"{tf:.2f}".replace('.', ',') + ' s') if tf else ''}</text></g>
      </g>""")
    return "".join(out)


def ruler(prefix, scale, step, maxm):
    out = [f'<g id="{prefix}-ruler"><line x1="96" x2="96" y1="{GROUND}" y2="{GROUND - maxm * scale}" stroke="{C["dim"]}" stroke-width="3"/>']
    m = 0.0
    while m <= maxm + 1e-6:
        y = GROUND - m * scale
        lab = (f"{m:.1f}".rstrip("0").rstrip(".") if step < 1 else f"{int(m)}").replace(".", ",")
        out.append(f'<line x1="84" x2="104" y1="{y:.1f}" y2="{y:.1f}" stroke="{C["dim"]}" stroke-width="3"/>'
                   f'<text x="78" y="{y + 10:.1f}" text-anchor="end" font-family="JetBrains Mono" font-weight="700" font-size="28" fill="{C["dim"]}">{lab}</text>')
        m += step
    out.append(f'<text x="30" y="{GROUND + 60}" font-family="JetBrains Mono" font-weight="700" font-size="28" fill="{C["dim"]}">m</text></g>')
    return "".join(out)


SIM_JS = r"""
    const K = __K__, V = K.v;
    const L1 = __L1__, L2 = __L2__;
    const GROUND = __GROUND__, S1 = __S1__, S2 = __S2__;
    const interp = (a, t, extend) => {
      if (t <= a[0][0]) return 0;
      for (let i = 1; i < a.length; i++) if (t <= a[i][0]) {
        const [t0, v0] = a[i - 1], [t1, v1] = a[i]; return v0 + (v1 - v0) * (t - t0) / (t1 - t0); }
      const [t0, v0] = a[a.length - 2], [t1, v1] = a[a.length - 1];
      return extend ? v1 + (v1 - v0) / (t1 - t0) * (t - t1) : v1;
    };
    const height = (tau, g) => g ? Math.max(0, V * tau - g * tau * tau / 2) : V * tau;
    const num = (x, d) => x.toFixed(d).replace(".", ",");
    const $ = (id) => document.getElementById(id);
    function lane(l, tau, scale, cx) {
      const h = height(tau, l[2]), tf = l[2] ? 2 * V / l[2] : Infinity, landed = tau >= tf, air = tau > 0 && !landed;
      const fig = $(l[0] + "-fig");
      let yy = GROUND - h * scale;
      fig.setAttribute("transform", `translate(${cx},${yy})`);
      fig.querySelector(".armsup").setAttribute("opacity", air ? 1 : 0);
      fig.querySelector(".armsdown").setAttribute("opacity", air ? 0 : 1);
      const ht = $(l[0] + "-h"), f = scale / 140;
      let ty = yy - 280 * f - 20;
      let label = num(h, h < 10 ? 2 : 1) + " m";
      if (ty < 480) { ty = 480; label = "↑ " + label; }
      ht.setAttribute("y", ty); ht.textContent = label;
      const peakPassed = l[2] && tau >= V / l[2];
      $(l[0] + "-peak").setAttribute("opacity", peakPassed ? 0.9 : 0);
      $(l[0] + "-done").setAttribute("opacity", landed ? 1 : 0);
    }
    function render(t) {
      const p2 = t >= K.switch;
      const tau1 = interp(K.a1, t, false), tau2 = interp(K.a2, t, true);
      L1.forEach((l, i) => lane(l, tau1, S1, __X0__ + i * __LW__ + __LW__ / 2));
      L2.forEach((l, i) => lane(l, tau2, S2, __X0__ + i * __LW__ + __LW__ / 2));
      // Fokus: aktive Bahn hell, andere gedimmt
      let focus = "";
      for (const [ft, id] of K.focus) if (t >= ft) focus = id;
      for (const l of L1.concat(L2)) $(l[0] + "-lane").setAttribute("opacity", !focus || focus === l[0] ? 1 : 0.32);
      const tau = p2 ? tau2 : tau1;
      $("tm").textContent = "0:" + (tau < 10 ? "0" : "") + num(tau, 2).replace(",", ".");
      $("tm-mode").textContent = !p2 ? (t < K.jump1 ? "BEREIT" : (tau1 >= K.a1[K.a1.length - 1][1] ? "ALLE GELANDET" : "ZEITLUPE"))
                                     : (t < K.jump2 ? "BEREIT" : "ZEITRAFFER");
    }
    const st = { t: 0 };
    tl.to(st, { t: __DUR__, duration: __DUR__, ease: "none", onUpdate: () => render(st.t) }, 0);
    render(0);
"""


def sim_html():
    r = rng(9)
    stars = "".join(f'<circle cx="{r.randint(0, 1080)}" cy="{r.randint(0, 1100)}" r="{r.choice([1.5, 2, 2.5])}" fill="#fff" opacity="{r.choice([0.25, 0.4, 0.6])}"/>'
                    for _ in range(140))
    p1 = lane_svg("p1", PHASE1, S1)
    p2 = lane_svg("p2", PHASE2, S2)
    js = (SIM_JS.replace("__K__", json.dumps(K)).replace("__L1__", json.dumps([list(x) for x in PHASE1]))
          .replace("__L2__", json.dumps([list(x) for x in PHASE2])).replace("__GROUND__", str(GROUND))
          .replace("__S1__", str(S1)).replace("__S2__", str(S2)).replace("__X0__", str(X0)).replace("__LW__", str(LW))
          .replace("__DUR__", str(TOTAL)))
    sw, j2, wy, en = K["switch"], K["jump2"], K["warum"], K["end"]
    js += f"""
    tl.fromTo("#p1", {{opacity:1}}, {{opacity:0, duration:0.4, ease:"power2.in"}}, {sw});
    tl.fromTo("#p2", {{opacity:0}}, {{opacity:1, duration:0.5, ease:"power2.out"}}, {sw + 0.35});
    tl.fromTo("#cmp", {{opacity:0, scale:1.3}}, {{opacity:1, scale:1, duration:0.3, ease:"expo.out", svgOrigin:"540 640"}}, {wy});
    tl.to("#cmp", {{opacity:0, duration:0.2}}, {en});
    tl.fromTo("#bennu-pill", {{opacity:0, scale:1.5}}, {{opacity:1, scale:1, duration:0.25, ease:"expo.out", svgOrigin:"{X0 + 3 * LW + LW / 2} 520"}}, {K['bennu_pill']});
    tl.to("#bennu-pill", {{opacity:0, duration:0.2}}, {wy});
    tl.fromTo("#lanes", {{opacity:1}}, {{opacity:0.15, duration:0.4}}, {en});
    tl.fromTo("#endcard", {{opacity:0, y:40}}, {{opacity:1, y:0, duration:0.5, ease:"expo.out"}}, {en + 0.1});
    tl.fromTo(".erow", {{opacity:0, x:-30}}, {{opacity:1, x:0, duration:0.3, stagger:0.12, ease:"expo.out"}}, {en + 0.35});
"""
    rows = [("Jupiter", 0.20, "#D9A066"), ("Erde", 0.50, "#4F9BE8"), ("Mars", 1.32, "#C1502E"), ("Mond", 3.03, "#B8BCC6"),
            ("Pluto", 7.91, "#C9B7A0"), ("Ceres", 17.5, "#8A8F99"), ("Bennu", None, "#FF4D5E")]
    erows = []
    for i, (n, h, col) in enumerate(rows):
        y = 590 + i * 70
        wbar = 24 + (h / 17.5) * 250 if h else 274
        val = (f"{h:.2f}".replace(".", ",") + " m") if h else "∞"
        erows.append(f'<g class="erow"><circle cx="210" cy="{y - 10}" r="16" fill="{col}"/>'
                     f'<text x="240" y="{y}" font-family="Inter" font-weight="800" font-size="34" fill="#fff">{n}</text>'
                     f'<rect x="420" y="{y - 26}" width="{wbar:.0f}" height="30" rx="8" fill="{col}" opacity="{0.9 if h else 0.35}"/>'
                     f'<text x="880" y="{y}" text-anchor="end" font-family="JetBrains Mono" font-weight="700" font-size="34" fill="{C["red"] if not h else "#fff"}">{val}</text></g>')
    bx = X0 + 3 * LW + LW / 2
    return f"""<template>
  <style>
    #root {{ position:absolute; inset:0; background:radial-gradient(ellipse 90% 60% at 50% 40%, #18223A 0%, #0B1120 75%); }}
    #tmbox {{ position:absolute; left:0; right:0; top:176px; text-align:center; }}
    #tm {{ display:inline-block; font-family:'JetBrains Mono',monospace; font-weight:700; font-size:64px; color:#fff; background:#121A2B;
      border:3px solid {C['line']}; border-radius:18px; padding:4px 26px; font-variant-numeric:tabular-nums; }}
    #tm-mode {{ display:block; width:max-content; margin:10px auto 0; font-family:'Inter',sans-serif; font-weight:900; font-size:28px;
      letter-spacing:0.1em; color:#0A0F1C; background:#E6E9F0; border-radius:999px; padding:4px 18px; }}
  </style>
  <div id="root" data-composition-id="sim" data-width="{W}" data-height="{H}" data-layout-allow-overlap>
    <svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" style="position:absolute;left:0;top:0" data-layout-allow-overflow>
      <g>{stars}</g>
      <rect x="0" y="{GROUND + 26}" width="{W}" height="{H - GROUND}" fill="#0A0E18"/>
      <g id="lanes" data-layout-ignore>
        <g id="p1">{ruler("p1", S1, 0.5, 4.5)}{p1}</g>
        <g id="p2" opacity="0"><g id="p2-zoom">{ruler("p2", S2, 5, 20)}</g>{p2}</g>
      </g>
      <g id="bennu-pill" opacity="0"><rect x="{bx - 112}" y="490" width="224" height="88" rx="22" fill="{C['red']}"/>
        <text x="{bx}" y="527" text-anchor="middle" font-family="Inter" font-weight="900" font-size="28" fill="#fff">KOMMT NIE</text>
        <text x="{bx}" y="562" text-anchor="middle" font-family="Inter" font-weight="900" font-size="28" fill="#fff">ZURÜCK</text></g>
      <g id="cmp" opacity="0">
        <rect x="110" y="520" width="860" height="250" rx="26" fill="#121A2B" stroke="{C['red']}" stroke-width="4"/>
        <text x="540" y="578" text-anchor="middle" font-family="JetBrains Mono" font-weight="700" font-size="28" fill="{C['mute']}">DEIN SPRUNG   vs   BENNU-FLUCHT</text>
        <text x="540" y="672" text-anchor="middle" font-family="Inter" font-weight="900" font-size="80" fill="#fff">3,1 <tspan fill="{C['red']}">&gt;</tspan> 0,2</text>
        <text x="540" y="730" text-anchor="middle" font-family="JetBrains Mono" font-weight="700" font-size="28" fill="{C['mute']}">METER PRO SEKUNDE</text>
      </g>
      <g id="endcard" opacity="0">
        <rect x="150" y="440" width="780" height="640" rx="26" fill="#121A2B" stroke="{C['line']}" stroke-width="4"/>
        <text x="540" y="505" text-anchor="middle" font-family="JetBrains Mono" font-weight="700" font-size="30" fill="{C['mute']}" letter-spacing="6">ENDSTAND · SPRUNGHÖHE</text>
        {''.join(erows)}
      </g>
    </svg>
    <div id="tmbox"><span id="tm">0:00.00</span><span id="tm-mode">BEREIT</span></div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{js}
    window.__timelines["sim"] = tl;
  </script>
</template>
"""


def title_html():
    off = B["setup"]["start"] - 0.1
    return f"""<template>
  <style>#root {{ position:absolute; inset:0; }}
    #tt {{ position:absolute; left:40px; right:40px; top:330px; font-family:'Inter',sans-serif; text-align:center; background:rgba(11,17,32,0.92); border-radius:28px; padding:34px 20px; }}
    #tt .a {{ font-weight:900; font-size:86px; line-height:1.0; }}
    #tt .b {{ font-weight:900; font-size:52px; color:{C['mute']}; margin-top:18px; }}</style>
  <div id="root" data-composition-id="title" data-width="{W}" data-height="{H}">
    <div id="tt"><div class="a"><span style="color:#D9A066">JUPITER</span> <span style="color:{C['mute']};font-size:52px">vs</span> <span style="color:#4F9BE8">ERDE</span><br>
      <span style="color:#C1502E">MARS</span> <span style="color:{C['mute']};font-size:52px">vs</span> <span style="color:#B8BCC6">MOND</span></div>
      <div class="b">WIE HOCH SPRINGST DU?</div></div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    tl.fromTo("#tt", {{opacity:1}}, {{opacity:0, scale:0.96, duration:0.3, ease:"power2.in"}}, {off});
    window.__timelines["title"] = tl;
  </script>
</template>
"""


SFX = [
    (wa("setup", 3, 0), "click-soft.mp3", 0.5), (wa("setup", 3, 1), "click-soft.mp3", 0.5),
    (K["jump1"] - 0.05, "whoosh-short.mp3", 0.5),
    (K["a1"][1][0], "pop.mp3", 0.45), (K["a1"][2][0], "pop.mp3", 0.45), (K["a1"][3][0], "pop.mp3", 0.45), (K["a1"][4][0], "pop.mp3", 0.45),
    (K["switch"] - 0.1, "whoosh-cinematic.mp3", 0.35),
    (K["jump2"] - 0.05, "whoosh-short.mp3", 0.5),
    (K["a2"][1][0], "pop.mp3", 0.45), (K["a2"][2][0], "pop.mp3", 0.45),
    (K["bennu_pill"], "glitch-1.mp3", 0.25),
    (K["warum"], "impact-bass-1.mp3", 0.5),
    (K["end"] + 0.1, "whoosh.mp3", 0.4),
]


def write():
    comp = HERE / "compositions"
    comp.mkdir(exist_ok=True)
    (comp / "sim.html").write_text(sim_html())
    (comp / "title.html").write_text(title_html())
    (comp / "captions.html").write_text(captions_html(T, TOTAL, top=1170, upper=False, size=78))
    (HERE / "assets" / "sfx").mkdir(parents=True, exist_ok=True)
    audio = ['      <audio id="voice" class="clip" src="assets/voice.wav" data-start="0" data-track-index="10" data-volume="1"></audio>']
    for j, (t, f, vol) in enumerate(SFX):
        (HERE / "assets" / "sfx" / f).write_bytes((SFX_ROOT / f).read_bytes())
        d = min(audio_len(SFX_ROOT / f), TOTAL - t)
        audio.append(f'      <audio id="sfx{j}" class="clip" src="assets/sfx/{f}" data-start="{fmt(t)}" data-duration="{fmt(d)}" '
                     f'data-track-index="{11 + j}" data-volume="{vol}"></audio>')
    hosts = ""
    for z, (cid, kind, start, dur) in enumerate((("sim", "graphics", 0, TOTAL), ("title", "graphics", 0, B["setup"]["start"] + 0.3),
                                                 ("captions", "captions", 0, TOTAL))):
        hosts += (f'      <div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" data-start="{fmt(start)}" '
                  f'data-duration="{fmt(dur)}" data-track-index="{z + 1}" data-track-kind="{kind}" data-width="{W}" data-height="{H}" '
                  f'style="z-index:{z + 1}"></div>\n')
    (HERE / "index.html").write_text(f"""<!doctype html>
<html lang="de" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <title>Was wäre, wenn du auf jedem Planeten einmal hochspringst?</title>
    <script src="assets/gsap.min.js"></script>
    <style>
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:#0B1120; }}
      #root {{ position:relative; width:100%; height:100%; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{fmt(TOTAL)}" data-width="{W}" data-height="{H}">
{hosts}{chr(10).join(audio)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
""")
    print("K", {k: v for k, v in K.items() if k in ("jump1", "switch", "jump2", "warum", "end")}, "| total", TOTAL)


if __name__ == "__main__":
    write()
