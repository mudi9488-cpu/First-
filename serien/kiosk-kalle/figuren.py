"""Figuren der Serie „Kiosk-Kalle“ als Flat-SVG (wiederverwendbar in jeder Folge).

Jede Funktion liefert ein komplettes <svg>, Ursprung (0,0) = Mitte zwischen den Füßen.
Ausdrücke (Mund/Augen) liegen als Gruppen übereinander; sichtbar ist nur die gewählte.
Umschalten in der Timeline mit `face_js(prefix, mund, zeit)`.
"""

INK = "#1B1530"
SW = 7  # Konturstärke
SKIN = "#FFD6B0"
SKIN_SH = "#F2B890"

MUNDE = ["grin", "shock", "sad", "flat", "smirk", "open"]


def _o(extra=""):
    return f'stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round" stroke-linecap="round" {extra}'


def _mund(prefix, x, y, s, active):
    """Alle Mund-Varianten an Position x,y (Skalierung s)."""
    out = []
    for m in MUNDE:
        vis = "1" if m == active else "0"
        if m == "grin":
            d = (f'<path d="M {-46*s} 0 Q 0 {58*s} {46*s} 0 Z" fill="#7A2230" {_o()}/>'
                 f'<path d="M {-36*s} {4*s} L {36*s} {4*s} L {30*s} {16*s} L {-30*s} {16*s} Z" fill="#fff"/>')
        elif m == "shock":
            d = (f'<ellipse cx="0" cy="{12*s}" rx="{30*s}" ry="{38*s}" fill="#7A2230" {_o()}/>'
                 f'<ellipse cx="0" cy="{30*s}" rx="{16*s}" ry="{12*s}" fill="#FF7A8A"/>')
        elif m == "sad":
            d = f'<path d="M {-34*s} {18*s} Q 0 {-14*s} {34*s} {18*s}" fill="none" {_o()}/>'
        elif m == "flat":
            d = f'<path d="M {-26*s} {6*s} L {26*s} {6*s}" fill="none" {_o()}/>'
        elif m == "smirk":
            d = f'<path d="M {-30*s} {4*s} Q {6*s} {26*s} {36*s} {-8*s}" fill="none" {_o()}/>'
        else:  # open (sprechen/staunen)
            d = (f'<path d="M {-34*s} 0 Q 0 {46*s} {34*s} 0 Q 0 {12*s} {-34*s} 0 Z" fill="#7A2230" {_o()}/>')
        out.append(f'<g id="{prefix}-m-{m}" opacity="{vis}" transform="translate({x},{y})">{d}</g>')
    return "".join(out)


def face_js(prefix, mund, at):
    """GSAP-Zeilen: an Zeitpunkt `at` auf Mund `mund` umschalten."""
    return "".join(f'tl.set("#{prefix}-m-{m}",{{opacity:{1 if m == mund else 0}}},{at});' for m in MUNDE)


def eyes_js(prefix, mode, at):
    """Augen: normal | wide | closed."""
    return "".join(f'tl.set("#{prefix}-e-{m}",{{opacity:{1 if m == mode else 0}}},{at});'
                   for m in ("normal", "wide", "closed"))


def _augen(prefix, xs, y, rx, ry, pr, active="normal", look=(6, 4)):
    lx, ly = look
    out = []
    for mode in ("normal", "wide", "closed"):
        vis = "1" if mode == active else "0"
        parts = []
        for x in xs:
            if mode == "closed":
                parts.append(f'<path d="M {x-rx} {y} Q {x} {y+ry*0.7} {x+rx} {y}" fill="none" {_o()}/>')
            else:
                k = 1.25 if mode == "wide" else 1.0
                p = pr * (0.7 if mode == "wide" else 1.0)
                parts.append(f'<ellipse cx="{x}" cy="{y}" rx="{rx*k}" ry="{ry*k}" fill="#fff" {_o()}/>'
                             f'<circle cx="{x+lx}" cy="{y+ly}" r="{p}" fill="{INK}"/>'
                             f'<circle cx="{x+lx-p*0.35}" cy="{y+ly-p*0.4}" r="{p*0.32}" fill="#fff"/>')
        out.append(f'<g id="{prefix}-e-{mode}" opacity="{vis}">{"".join(parts)}</g>')
    return "".join(out)


def _svg(prefix, vb, w, inner, cls="fig"):
    x, y, vw, vh = vb
    h = round(w * vh / vw)
    return (f'<svg id="{prefix}" class="{cls}" viewBox="{x} {y} {vw} {vh}" width="{w}" height="{h}" '
            f'style="overflow:visible">{inner}</svg>')


# ------------------------------------------------------------------ Kalle

def kalle(prefix="kalle", w=420, mund="grin", augen="normal", pose="down", item=None,
          hood="#3FA866", hood_sh="#2F8A52", hair="#E8622C", brows="#B5461C", cap=True, fleck=True, schuerze=False):
    """pose: down | up | hold (Arme nach vorn, optional item: 'controller' | 'phone' | 'coins').
    Farben/cap/fleck/schuerze machen aus dem Körper auch andere Figuren (z. B. Helfer Max)."""
    arms = {
        "down": (f'<path d="M -112 -250 Q -165 -190 -150 -120" fill="none" stroke="{INK}" stroke-width="54" stroke-linecap="round"/>'
                 f'<path d="M -112 -250 Q -165 -190 -150 -120" fill="none" stroke="{hood}" stroke-width="40" stroke-linecap="round"/>'
                 f'<circle cx="-150" cy="-112" r="24" fill="{SKIN}" {_o()}/>'
                 f'<path d="M 112 -250 Q 165 -190 150 -120" fill="none" stroke="{INK}" stroke-width="54" stroke-linecap="round"/>'
                 f'<path d="M 112 -250 Q 165 -190 150 -120" fill="none" stroke="{hood}" stroke-width="40" stroke-linecap="round"/>'
                 f'<circle cx="150" cy="-112" r="24" fill="{SKIN}" {_o()}/>'),
        "up": (f'<path d="M -110 -255 Q -190 -330 -170 -430" fill="none" stroke="{INK}" stroke-width="54" stroke-linecap="round"/>'
               f'<path d="M -110 -255 Q -190 -330 -170 -430" fill="none" stroke="{hood}" stroke-width="40" stroke-linecap="round"/>'
               f'<circle cx="-170" cy="-442" r="26" fill="{SKIN}" {_o()}/>'
               f'<path d="M 110 -255 Q 190 -330 170 -430" fill="none" stroke="{INK}" stroke-width="54" stroke-linecap="round"/>'
               f'<path d="M 110 -255 Q 190 -330 170 -430" fill="none" stroke="{hood}" stroke-width="40" stroke-linecap="round"/>'
               f'<circle cx="170" cy="-442" r="26" fill="{SKIN}" {_o()}/>'),
        "hold": (f'<path d="M -112 -250 Q -150 -170 -60 -170" fill="none" stroke="{INK}" stroke-width="54" stroke-linecap="round"/>'
                 f'<path d="M -112 -250 Q -150 -170 -60 -170" fill="none" stroke="{hood}" stroke-width="40" stroke-linecap="round"/>'
                 f'<path d="M 112 -250 Q 150 -170 60 -170" fill="none" stroke="{INK}" stroke-width="54" stroke-linecap="round"/>'
                 f'<path d="M 112 -250 Q 150 -170 60 -170" fill="none" stroke="{hood}" stroke-width="40" stroke-linecap="round"/>'),
    }[pose]
    held = ""
    if pose == "hold":
        if item == "controller":
            held = (f'<path d="M -80 -200 Q -95 -140 -60 -140 Q -40 -140 -30 -160 L 30 -160 Q 40 -140 60 -140 Q 95 -140 80 -200 Z" '
                    f'fill="#2B2B3A" {_o()}/><circle cx="-45" cy="-180" r="8" fill="#6CF"/><circle cx="48" cy="-182" r="7" fill="#F55"/>'
                    f'<circle cx="62" cy="-170" r="7" fill="#5D5"/>')
        elif item == "phone":
            held = (f'<rect x="-34" y="-250" width="68" height="110" rx="12" fill="#2B2B3A" {_o()}/>'
                    f'<rect x="-24" y="-238" width="48" height="84" rx="6" fill="#7FD3FF"/>')
        elif item == "coins":
            held = "".join(f'<ellipse cx="{x}" cy="{y}" rx="22" ry="9" fill="#F5C542" {_o("stroke-width=\'5\'")}/>'
                           for x, y in ((-30, -165), (-10, -175), (14, -168), (34, -178), (0, -186)))
        held += (f'<circle cx="-60" cy="-168" r="24" fill="{SKIN}" {_o()}/>'
                 f'<circle cx="60" cy="-168" r="24" fill="{SKIN}" {_o()}/>')
    inner = f"""
  <ellipse cx="0" cy="2" rx="125" ry="18" fill="rgba(0,0,0,0.18)"/>
  <rect x="-70" y="-120" width="56" height="112" rx="22" fill="#8C90A6" {_o()}/>
  <rect x="14" y="-120" width="56" height="112" rx="22" fill="#8C90A6" {_o()}/>
  <ellipse cx="-50" cy="-10" rx="46" ry="20" fill="#fff" {_o()}/>
  <ellipse cx="50" cy="-10" rx="46" ry="20" fill="#fff" {_o()}/>
  <path d="M -92 -12 L -8 -12" stroke="#E04848" stroke-width="6"/><path d="M 8 -12 L 92 -12" stroke="#E04848" stroke-width="6"/>
  <ellipse cx="0" cy="-200" rx="128" ry="118" fill="{hood}" {_o()}/>
  <path d="M -60 -180 Q 0 -160 60 -180 L 52 -120 Q 0 -108 -52 -120 Z" fill="{hood_sh}" {_o('stroke-width=\'5\'')}/>
  {'<path d="M 30 -236 q 18 -14 34 2 q 10 18 -6 30 q -20 12 -30 -6 q -8 -14 2 -26 Z" fill="#D8343A"/><circle cx="74" cy="-196" r="7" fill="#D8343A"/>' if fleck else ''}
  {f'<path d="M -78 -268 L 78 -268 L 92 -110 Q 0 -92 -92 -110 Z" fill="#E8413A" {_o()}/><text x="0" y="-180" text-anchor="middle" font-family="Inter" font-weight="900" font-size="34" fill="#fff">KIOSK</text>' if schuerze else ''}
  <path d="M -24 -305 L -18 -250 M 24 -305 L 18 -250" stroke="#EDEDED" stroke-width="7" stroke-linecap="round"/>
  {arms}{held}
  <ellipse cx="-138" cy="-410" rx="22" ry="30" fill="{SKIN}" {_o()}/>
  <ellipse cx="138" cy="-410" rx="22" ry="30" fill="{SKIN}" {_o()}/>
  <circle cx="0" cy="-405" r="138" fill="{SKIN}" {_o()}/>
  <path d="M -150 -470 q -10 -50 30 -70 q -10 -40 40 -50 q 10 -40 60 -30 q 30 -30 70 -5 q 40 -10 55 30 q 45 10 35 60 q 30 30 5 60
           q -40 -45 -100 -55 q -60 -10 -120 10 q -50 20 -75 50 Z" fill="{hair}" {_o()}/>
  {f'<path d="M -120 -500 Q 0 -620 120 -500 Q 0 -540 -120 -500 Z" fill="#2E3A8C" {_o()}/><path d="M 70 -560 Q 150 -575 180 -540 Q 140 -530 100 -535 Z" fill="#2E3A8C" {_o()}/>' if cap else ''}
  {_augen(prefix, (-52, 52), -410, 40, 46, 17, augen)}
  <path d="M -88 -470 Q -55 -488 -22 -472 M 22 -472 Q 55 -488 88 -470" fill="none" stroke="{brows}" stroke-width="10" stroke-linecap="round"/>
  <ellipse cx="0" cy="-365" rx="16" ry="12" fill="{SKIN_SH}"/>
  <ellipse cx="-88" cy="-352" rx="24" ry="14" fill="#FF8A8A" opacity="0.75"/>
  <ellipse cx="88" cy="-352" rx="24" ry="14" fill="#FF8A8A" opacity="0.75"/>
  <circle cx="-95" cy="-372" r="3.5" fill="#D9895A"/><circle cx="-80" cy="-378" r="3.5" fill="#D9895A"/>
  <circle cx="95" cy="-372" r="3.5" fill="#D9895A"/><circle cx="82" cy="-379" r="3.5" fill="#D9895A"/>
  {_mund(prefix, 0, -328, 1.0, mund)}
"""
    return _svg(prefix, (-200, -620, 400, 640), w, inner)


def kalle_kopf(prefix="kk", w=760, mund="grin", augen="normal"):
    """Nahaufnahme (Kopf + Schultern), für Reaktionen."""
    inner = f"""
  <ellipse cx="0" cy="40" rx="300" ry="170" fill="#3FA866" {_o()}/>
  <path d="M 60 0 q 30 -20 56 4 q 14 28 -10 46 q -30 18 -46 -10 q -12 -22 0 -40 Z" fill="#D8343A"/>
  <ellipse cx="-138" cy="-210" rx="24" ry="32" fill="{SKIN}" {_o()}/>
  <ellipse cx="138" cy="-210" rx="24" ry="32" fill="{SKIN}" {_o()}/>
  <circle cx="0" cy="-205" r="140" fill="{SKIN}" {_o()}/>
  <path d="M -150 -270 q -10 -50 30 -70 q -10 -40 40 -50 q 10 -40 60 -30 q 30 -30 70 -5 q 40 -10 55 30 q 45 10 35 60 q 30 30 5 60
           q -40 -45 -100 -55 q -60 -10 -120 10 q -50 20 -75 50 Z" fill="#E8622C" {_o()}/>
  <path d="M -120 -300 Q 0 -420 120 -300 Q 0 -340 -120 -300 Z" fill="#2E3A8C" {_o()}/>
  {_augen(prefix, (-52, 52), -210, 40, 46, 17, augen)}
  <path d="M -88 -270 Q -55 -288 -22 -272 M 22 -272 Q 55 -288 88 -270" fill="none" stroke="#B5461C" stroke-width="10" stroke-linecap="round"/>
  <ellipse cx="0" cy="-165" rx="16" ry="12" fill="{SKIN_SH}"/>
  <ellipse cx="-88" cy="-152" rx="24" ry="14" fill="#FF8A8A" opacity="0.75"/>
  <ellipse cx="88" cy="-152" rx="24" ry="14" fill="#FF8A8A" opacity="0.75"/>
  {_mund(prefix, 0, -128, 1.0, mund)}
"""
    return _svg(prefix, (-320, -380, 640, 600), w, inner)


# ------------------------------------------------------------------ Herr Geier (Vermieter)

def geier(prefix="geier", w=360, mund="smirk"):
    suit = "#5E6275"
    inner = f"""
  <ellipse cx="0" cy="2" rx="95" ry="14" fill="rgba(0,0,0,0.18)"/>
  <rect x="-48" y="-260" width="38" height="252" rx="14" fill="#2C2F3D" {_o()}/>
  <rect x="10" y="-260" width="38" height="252" rx="14" fill="#2C2F3D" {_o()}/>
  <ellipse cx="-34" cy="-8" rx="40" ry="14" fill="#111" {_o()}/>
  <ellipse cx="34" cy="-8" rx="40" ry="14" fill="#111" {_o()}/>
  <path d="M -85 -520 Q -95 -380 -70 -240 L 70 -240 Q 95 -380 85 -520 Q 0 -545 -85 -520 Z" fill="{suit}" {_o()}/>
  <path d="M -60 -500 L -60 -250 M -30 -510 L -30 -245 M 30 -510 L 30 -245 M 60 -500 L 60 -250" stroke="#7B8095" stroke-width="3"/>
  <path d="M -26 -525 L 0 -470 L 26 -525 Z" fill="#fff" {_o('stroke-width=\'4\'')}/>
  <path d="M 0 -505 L -12 -470 L 0 -380 L 12 -470 Z" fill="#C0202E" {_o('stroke-width=\'4\'')}/>
  <path d="M 80 -500 Q 140 -420 110 -330" fill="none" stroke="{INK}" stroke-width="44" stroke-linecap="round"/>
  <path d="M 80 -500 Q 140 -420 110 -330" fill="none" stroke="{suit}" stroke-width="30" stroke-linecap="round"/>
  <g id="{prefix}-clip">
    <rect x="60" y="-420" width="120" height="160" rx="10" fill="#A8743A" {_o()}/>
    <rect x="75" y="-400" width="90" height="125" fill="#fff"/>
    <rect x="98" y="-432" width="44" height="22" rx="5" fill="#9AA0AE" {_o('stroke-width=\'4\'')}/>
    <path d="M 85 -380 L 150 -380 M 85 -360 L 150 -360 M 85 -340 L 130 -340" stroke="#9AA0AE" stroke-width="5"/>
    <g id="{prefix}-stamp" opacity="0"><rect x="70" y="-330" width="104" height="40" rx="6" fill="none" stroke="#E0202E" stroke-width="6" transform="rotate(-12 122 -310)"/>
      <text x="122" y="-300" text-anchor="middle" font-family="Inter" font-weight="900" font-size="22" fill="#E0202E" transform="rotate(-12 122 -310)">RÄUMUNG</text></g>
  </g>
  <circle cx="110" cy="-330" r="20" fill="#F4DCC4" {_o()}/>
  <path d="M -80 -500 Q -120 -420 -95 -320" fill="none" stroke="{INK}" stroke-width="44" stroke-linecap="round"/>
  <path d="M -80 -500 Q -120 -420 -95 -320" fill="none" stroke="{suit}" stroke-width="30" stroke-linecap="round"/>
  <circle cx="-95" cy="-315" r="20" fill="#F4DCC4" {_o()}/>
  <ellipse cx="0" cy="-640" rx="88" ry="110" fill="#F4DCC4" {_o()}/>
  <path d="M -40 -720 Q -10 -738 20 -728" fill="none" stroke="#fff" stroke-width="10" stroke-linecap="round" opacity="0.7"/>
  <path d="M -88 -640 q -14 -30 4 -50 M 88 -640 q 14 -30 -4 -50" fill="none" stroke="#9AA0AE" stroke-width="12" stroke-linecap="round"/>
  <path d="M -58 -680 L -14 -664 M 58 -680 L 14 -664" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>
  <ellipse cx="-34" cy="-648" rx="14" ry="10" fill="#fff" {_o('stroke-width=\'4\'')}/><circle cx="-32" cy="-647" r="6" fill="{INK}"/>
  <ellipse cx="34" cy="-648" rx="14" ry="10" fill="#fff" {_o('stroke-width=\'4\'')}/><circle cx="32" cy="-647" r="6" fill="{INK}"/>
  <path d="M 0 -640 Q 34 -600 30 -580 Q 14 -566 -4 -584" fill="#EBC3A4" {_o()}/>
  {_mund(prefix, 0, -560, 0.75, mund)}
"""
    return _svg(prefix, (-160, -770, 360, 790), w, inner)


# ------------------------------------------------------------------ Horst (Stammkunde)

def horst(prefix="horst", w=330, mund="open"):
    inner = f"""
  <ellipse cx="0" cy="2" rx="140" ry="16" fill="rgba(0,0,0,0.18)"/>
  <rect x="-50" y="-110" width="40" height="104" rx="14" fill="#5B4A3A" {_o()}/>
  <rect x="10" y="-110" width="40" height="104" rx="14" fill="#5B4A3A" {_o()}/>
  <ellipse cx="-34" cy="-8" rx="36" ry="14" fill="#3A2C22" {_o()}/>
  <ellipse cx="34" cy="-8" rx="36" ry="14" fill="#3A2C22" {_o()}/>
  <path d="M -95 -330 Q -110 -180 -80 -100 L 80 -100 Q 110 -180 95 -330 Q 0 -360 -95 -330 Z" fill="#C9B48A" {_o()}/>
  <path d="M 0 -340 L 0 -110" stroke="#A8936A" stroke-width="5"/>
  <circle cx="0" cy="-420" r="90" fill="#FFD6B0" {_o()}/>
  <path d="M -95 -440 Q -90 -530 0 -530 Q 90 -530 95 -440 Z" fill="#6B4F3A" {_o()}/>
  <path d="M -95 -440 Q -20 -420 130 -440 Q 120 -455 90 -455" fill="#5A4130" {_o()}/>
  <ellipse cx="-32" cy="-415" rx="10" ry="12" fill="{INK}"/><ellipse cx="32" cy="-415" rx="10" ry="12" fill="{INK}"/>
  <ellipse cx="0" cy="-390" rx="18" ry="14" fill="#F2A88A"/>
  <path d="M -60 -370 Q -30 -390 0 -372 Q 30 -390 60 -370 Q 40 -350 0 -358 Q -40 -350 -60 -370 Z" fill="#F4F4F4" {_o('stroke-width=\'5\'')}/>
  {_mund(prefix, 0, -340, 0.6, mund)}
  <path d="M 90 -260 L 170 -250 L 190 -10 M 170 -250 L 120 -10 M 110 -120 L 185 -120" fill="none" stroke="#7A7F8C" stroke-width="12" stroke-linecap="round"/>
  <circle cx="190" cy="-6" r="14" fill="#333" {_o('stroke-width=\'4\'')}/><circle cx="120" cy="-6" r="14" fill="#333" {_o('stroke-width=\'4\'')}/>
  <path d="M 175 -250 L 180 -330 L 230 -310 L 178 -295" fill="#F0C430" {_o('stroke-width=\'4\'')}/>
  <circle cx="95" cy="-255" r="20" fill="#FFD6B0" {_o()}/>
"""
    return _svg(prefix, (-160, -560, 420, 580), w, inner)


# ------------------------------------------------------------------ Dennis (Rivale)

def dennis(prefix="dennis", w=330, mund="smirk"):
    inner = f"""
  <ellipse cx="0" cy="2" rx="100" ry="14" fill="rgba(0,0,0,0.18)"/>
  <rect x="-52" y="-130" width="44" height="124" rx="16" fill="#1E1E2A" {_o()}/>
  <rect x="8" y="-130" width="44" height="124" rx="16" fill="#1E1E2A" {_o()}/>
  <ellipse cx="-34" cy="-8" rx="40" ry="16" fill="#fff" {_o()}/><ellipse cx="34" cy="-8" rx="40" ry="16" fill="#fff" {_o()}/>
  <path d="M -100 -360 Q -110 -200 -80 -120 L 80 -120 Q 110 -200 100 -360 Q 0 -390 -100 -360 Z" fill="#8A3FF0" {_o()}/>
  <path d="M -40 -370 Q 0 -300 40 -370" fill="none" stroke="#F5C542" stroke-width="10"/>
  <circle cx="0" cy="-322" r="14" fill="#F5C542" {_o('stroke-width=\'4\'')}/>
  <path d="M 95 -340 Q 150 -300 120 -250" fill="none" stroke="{INK}" stroke-width="44" stroke-linecap="round"/>
  <path d="M 95 -340 Q 150 -300 120 -250" fill="none" stroke="#8A3FF0" stroke-width="30" stroke-linecap="round"/>
  <rect x="96" y="-330" width="44" height="76" rx="9" fill="#2B2B3A" {_o()}/>
  <circle cx="118" cy="-246" r="20" fill="#E8B892" {_o()}/>
  <circle cx="0" cy="-455" r="100" fill="#E8B892" {_o()}/>
  <path d="M -100 -470 Q -110 -580 10 -575 Q 110 -575 102 -480 Q 60 -530 -100 -470 Z" fill="#1E1E2A" {_o()}/>
  <rect x="-80" y="-475" width="70" height="40" rx="14" fill="#111" {_o('stroke-width=\'5\'')}/>
  <rect x="10" y="-475" width="70" height="40" rx="14" fill="#111" {_o('stroke-width=\'5\'')}/>
  <path d="M -10 -460 L 10 -460" stroke="#111" stroke-width="8"/>
  <path d="M -60 -468 L -40 -452" stroke="#fff" stroke-width="5" opacity="0.6"/>
  {_mund(prefix, 0, -395, 0.8, mund)}
"""
    return _svg(prefix, (-150, -600, 320, 620), w, inner)


# ------------------------------------------------------------------ Schulkinder

def kind(prefix, w=180, shirt="#FF7A3D", hair="#5A3A22", bag="#3B6FF0"):
    inner = f"""
  <ellipse cx="0" cy="2" rx="60" ry="10" fill="rgba(0,0,0,0.18)"/>
  <rect x="-30" y="-70" width="24" height="64" rx="10" fill="#3B4A7A" {_o('stroke-width=\'5\'')}/>
  <rect x="6" y="-70" width="24" height="64" rx="10" fill="#3B4A7A" {_o('stroke-width=\'5\'')}/>
  <rect x="-62" y="-170" width="44" height="80" rx="12" fill="{bag}" {_o('stroke-width=\'5\'')}/>
  <ellipse cx="0" cy="-120" rx="52" ry="58" fill="{shirt}" {_o('stroke-width=\'5\'')}/>
  <circle cx="0" cy="-215" r="58" fill="#FFD6B0" {_o('stroke-width=\'5\'')}/>
  <path d="M -60 -225 Q -58 -285 0 -285 Q 58 -285 60 -225 Q 30 -255 -60 -225 Z" fill="{hair}" {_o('stroke-width=\'5\'')}/>
  <circle cx="-20" cy="-212" r="8" fill="{INK}"/><circle cx="20" cy="-212" r="8" fill="{INK}"/>
  <path d="M -14 -186 Q 0 -174 14 -186" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>
  <circle cx="58" cy="-110" r="14" fill="#FFD6B0" {_o('stroke-width=\'5\'')}/>
"""
    return _svg(prefix, (-80, -300, 160, 310), w, inner)


def max_helfer(prefix="max", w=400, mund="grin", augen="normal", pose="down", item=None):
    """Maxim – ehrenamtlicher Helfer aus den Kommentaren (ab Folge 2): blonde Haare, blauer Pulli, rote Kiosk-Schürze."""
    return kalle(prefix, w=w, mund=mund, augen=augen, pose=pose, item=item, hood="#3B6FF0", hood_sh="#2D56C2",
                 hair="#F2C14E", brows="#B58A1C", cap=False, fleck=False, schuerze=True)


def bauarbeiter(prefix, w=300, haut="#FFD6B0", bart=True, mund="grin"):
    """Bauarbeiter (Stammkunden ab Folge 2): gelber Helm, orange Warnweste, Jeans."""
    inner = f"""
  <ellipse cx="0" cy="2" rx="100" ry="14" fill="rgba(0,0,0,0.18)"/>
  <rect x="-56" y="-150" width="48" height="144" rx="16" fill="#3B5C9A" {_o()}/>
  <rect x="8" y="-150" width="48" height="144" rx="16" fill="#3B5C9A" {_o()}/>
  <ellipse cx="-36" cy="-8" rx="42" ry="16" fill="#5A4130" {_o()}/><ellipse cx="36" cy="-8" rx="42" ry="16" fill="#5A4130" {_o()}/>
  <path d="M -105 -400 Q -115 -230 -85 -140 L 85 -140 Q 115 -230 105 -400 Q 0 -430 -105 -400 Z" fill="#8C90A6" {_o()}/>
  <path d="M -100 -398 Q -108 -240 -82 -142 L -30 -142 L -30 -410 Z M 100 -398 Q 108 -240 82 -142 L 30 -142 L 30 -410 Z" fill="#FF7A2F" {_o()}/>
  <path d="M -96 -300 L -30 -300 M 30 -300 L 96 -300 M -92 -240 L -30 -240 M 30 -240 L 92 -240" stroke="#F4F4F4" stroke-width="12"/>
  <path d="M -100 -380 Q -150 -300 -125 -210" fill="none" stroke="{INK}" stroke-width="48" stroke-linecap="round"/>
  <path d="M -100 -380 Q -150 -300 -125 -210" fill="none" stroke="#8C90A6" stroke-width="34" stroke-linecap="round"/>
  <circle cx="-125" cy="-200" r="22" fill="{haut}" {_o()}/>
  <path d="M 100 -380 Q 150 -300 125 -210" fill="none" stroke="{INK}" stroke-width="48" stroke-linecap="round"/>
  <path d="M 100 -380 Q 150 -300 125 -210" fill="none" stroke="#8C90A6" stroke-width="34" stroke-linecap="round"/>
  <circle cx="125" cy="-200" r="22" fill="{haut}" {_o()}/>
  <circle cx="0" cy="-500" r="100" fill="{haut}" {_o()}/>
  <path d="M -112 -520 Q -110 -630 0 -632 Q 110 -630 112 -520 Z" fill="#FFC233" {_o()}/>
  <rect x="-130" y="-534" width="260" height="26" rx="12" fill="#FFC233" {_o()}/>
  <ellipse cx="-34" cy="-482" rx="10" ry="12" fill="{INK}"/><ellipse cx="34" cy="-482" rx="10" ry="12" fill="{INK}"/>
  <ellipse cx="0" cy="-455" rx="16" ry="12" fill="#F2A88A"/>
  {f'<path d="M -70 -440 Q -40 -400 0 -405 Q 40 -400 70 -440 Q 70 -380 0 -385 Q -70 -380 -70 -440 Z" fill="#6B4F3A" {_o(chr(115)+"troke-width=" + chr(39) + "5" + chr(39))}/>' if bart else ''}
  {_mund(prefix, 0, -425, 0.6, mund)}
"""
    return _svg(prefix, (-160, -650, 320, 670), w, inner)
