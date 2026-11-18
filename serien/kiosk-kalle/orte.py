"""Hintergründe der Serie „Kiosk-Kalle“ (Flat-SVG, 1080x1920). Wiederverwendbar in jeder Folge.

Animierbare Teile haben IDs mit dem übergebenen Präfix (z. B. f"{p}-shutter").
"""
INK = "#1B1530"
W, H = 1080, 1920


def _o(sw=7):
    return f'stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"'


def _svg(p, inner):
    return (f'<svg id="{p}" class="abs" style="left:0;top:0" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{inner}</svg>')


def _wolke(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})" fill="#fff" opacity="0.95">'
            f'<ellipse cx="0" cy="0" rx="90" ry="44"/><ellipse cx="-70" cy="14" rx="60" ry="34"/>'
            f'<ellipse cx="74" cy="12" rx="66" ry="36"/><ellipse cx="10" cy="-30" rx="58" ry="40"/></g>')


def _regal_ware(x0, x1, y, seed):
    cols = ["#FF5A5F", "#FFC233", "#3B6FF0", "#3DDC84", "#FF7A2F", "#B05CF0", "#FF4F8B", "#2EC4D6"]
    out, x, i = [], x0 + 10, seed
    while x < x1 - 40:
        c = cols[(i * 5 + seed) % len(cols)]
        w = 34 + (i * 7 + seed) % 22
        h = 60 + (i * 13 + seed) % 50
        if i % 3 == 0:  # Glas
            out.append(f'<rect x="{x}" y="{y - h}" width="{w}" height="{h}" rx="10" fill="#DFF3FF" {_o(4)}/>'
                       f'<rect x="{x + 5}" y="{y - h * 0.6}" width="{w - 10}" height="{h * 0.6 - 5}" rx="6" fill="{c}"/>'
                       f'<rect x="{x - 2}" y="{y - h - 10}" width="{w + 4}" height="14" rx="4" fill="{c}" {_o(4)}/>')
        else:
            out.append(f'<rect x="{x}" y="{y - h}" width="{w}" height="{h}" rx="5" fill="{c}" {_o(4)}/>'
                       f'<rect x="{x + 6}" y="{y - h + 12}" width="{w - 12}" height="10" rx="3" fill="#fff" opacity="0.7"/>')
        x += w + 8
        i += 1
    return "".join(out)


# ------------------------------------------------------------------ Kiosk von außen

def kiosk_aussen(p="ka", shutter=1.0):
    """shutter: 1 = Rollladen ganz unten, 0 = offen (Startzustand)."""
    off = -(1 - shutter) * 370
    stripes = "".join(f'<path d="M 160 {1085 + k * 27} L 920 {1085 + k * 27}" stroke="#868C99" stroke-width="5"/>' for k in range(1, 14))
    awn = "".join(f'<path d="M {120 + k * 84} 1010 L {204 + k * 84} 1010 L {204 + k * 84} 1070 Q {162 + k * 84} 1100 {120 + k * 84} 1070 Z" '
                  f'fill="{"#E8413A" if k % 2 == 0 else "#fff"}" {_o(5)}/>' for k in range(10))
    tiles = "".join(f'<path d="M 0 {1500 + k * 90} L 1080 {1500 + k * 90}" stroke="#C6C0B6" stroke-width="4"/>' for k in range(5))
    tiles += "".join(f'<path d="M {k * 135} 1460 L {k * 135 - 60} 1920" stroke="#C6C0B6" stroke-width="4"/>' for k in range(10))
    inner = f"""
  <rect width="{W}" height="{H}" fill="#9ED8F5"/>
  {_wolke(200, 420)}{_wolke(860, 360, 0.8)}
  <rect x="-20" y="620" width="120" height="880" fill="#B9C3D6" {_o()}/>
  <rect x="980" y="560" width="140" height="940" fill="#C9B7D9" {_o()}/>
  <rect x="90" y="560" width="900" height="940" fill="#F4E3B5" {_o()}/>
  <path d="M 70 560 L 1010 560 L 990 520 L 90 520 Z" fill="#C98A4B" {_o()}/>
  <rect x="190" y="620" width="200" height="200" rx="10" fill="#7FC6EA" {_o()}/>
  <path d="M 290 620 L 290 820 M 190 720 L 390 720" stroke="{INK}" stroke-width="6"/>
  <rect x="690" y="620" width="200" height="200" rx="10" fill="#7FC6EA" {_o()}/>
  <path d="M 790 620 L 790 820 M 690 720 L 890 720" stroke="{INK}" stroke-width="6"/>
  <rect x="150" y="860" width="780" height="150" rx="16" fill="#2E5E4E" {_o()}/>
  <text x="510" y="968" text-anchor="middle" font-family="Inter" font-weight="900" font-size="96" fill="#FFD23F"
    stroke="{INK}" stroke-width="6" paint-order="stroke">KIOSK ERIK</text>
  <text id="{p}-a" x="842" y="985" text-anchor="middle" font-family="Inter" font-weight="900" font-size="96" fill="#FFD23F"
    stroke="{INK}" stroke-width="6" paint-order="stroke" transform="rotate(24 842 950)">A</text>
  {awn}
  <rect x="170" y="1090" width="390" height="360" fill="#5A8DB5" {_o()}/>
  <path d="M 170 1200 L 560 1200 M 170 1320 L 560 1320" stroke="{INK}" stroke-width="6"/>
  {_regal_ware(170, 560, 1196, 1)}{_regal_ware(170, 560, 1316, 4)}{_regal_ware(170, 560, 1446, 7)}
  <rect x="610" y="1090" width="300" height="360" fill="#6B4A2E" {_o()}/>
  <rect x="640" y="1120" width="240" height="200" fill="#9DD3F0" {_o(5)}/>
  <text x="760" y="1240" text-anchor="middle" font-family="Inter" font-weight="900" font-size="44" fill="#E8413A">OFFEN</text>
  <circle cx="870" cy="1300" r="12" fill="#FFD23F" {_o(4)}/>
  <clipPath id="{p}-clip"><rect x="155" y="1080" width="770" height="380"/></clipPath>
  <g clip-path="url(#{p}-clip)"><g id="{p}-shutter" transform="translate(0,{off})">
    <rect x="155" y="1075" width="770" height="380" fill="#A9AEB8" {_o()}/>{stripes}
    <rect x="155" y="1440" width="770" height="20" rx="6" fill="#7E8492" {_o(5)}/>
    <rect x="510" y="1442" width="60" height="16" rx="6" fill="{INK}"/>
  </g></g>
  <rect x="0" y="1460" width="{W}" height="460" fill="#D9D4CC"/>
  {tiles}
  <rect x="0" y="1450" width="{W}" height="22" fill="#B8B1A6" {_o(5)}/>
  <g transform="translate(930,1300)"><rect x="0" y="0" width="110" height="200" fill="#3B6FF0" {_o(5)}/>
    <rect x="10" y="20" width="90" height="70" fill="#fff" {_o(4)}/><text x="55" y="66" text-anchor="middle" font-family="Inter"
    font-weight="900" font-size="26" fill="#E8413A">BLITZ</text></g>
"""
    return _svg(p, inner)


# ------------------------------------------------------------------ Kiosk innen

def kiosk_innen(p="ki", night=False, uhr="7:00"):
    hh, mm = [int(x) for x in uhr.split(":")]
    ha, ma = (hh % 12) * 30 + mm * 0.5, mm * 6
    floor = "".join(f'<rect x="{(k % 8) * 135}" y="{1250 + (k // 8) * 135}" width="135" height="135" '
                    f'fill="{"#E8E1D4" if (k + k // 8) % 2 else "#D3CAB8"}"/>' for k in range(8 * 6))
    bottles = "".join(f'<rect x="{800 + (k % 4) * 52}" y="{640 + (k // 4) * 170}" width="34" height="110" rx="12" '
                      f'fill="{["#FF5A5F", "#3DDC84", "#FFC233", "#2EC4D6"][k % 4]}" {_o(4)}/>'
                      f'<rect x="{808 + (k % 4) * 52}" y="{620 + (k // 4) * 170}" width="18" height="26" rx="4" fill="#ddd" {_o(3)}/>'
                      for k in range(12))
    nightov = (f'<rect id="{p}-night" width="{W}" height="{H}" fill="#0B1A40" opacity="0.55"/>'
               f'<circle cx="300" cy="700" r="420" fill="#FFD27A" opacity="0.18"/>') if night else ""
    inner = f"""
  <rect width="{W}" height="1260" fill="#F7E7C6"/>
  <rect y="1240" width="{W}" height="20" fill="#C9A878"/>
  {floor}
  <rect x="40" y="520" width="680" height="22" fill="#B5651D" {_o(5)}/>
  <rect x="40" y="760" width="680" height="22" fill="#B5651D" {_o(5)}/>
  <rect x="40" y="1000" width="680" height="22" fill="#B5651D" {_o(5)}/>
  {_regal_ware(40, 720, 520, 2)}{_regal_ware(40, 720, 760, 5)}{_regal_ware(40, 720, 1000, 8)}
  <g id="{p}-clock" transform="translate(150,410)">
    <circle r="70" fill="#fff" {_o()}/>
    <path id="{p}-hh" d="M 0 0 L 0 -38" stroke="{INK}" stroke-width="9" stroke-linecap="round" transform="rotate({ha})"/>
    <path id="{p}-mh" d="M 0 0 L 0 -56" stroke="#E8413A" stroke-width="6" stroke-linecap="round" transform="rotate({ma})"/>
    <circle r="8" fill="{INK}"/></g>
  <g id="{p}-oma" transform="translate(470,330)">
    <rect x="0" y="0" width="150" height="170" rx="8" fill="#C98A4B" {_o()}/>
    <rect x="16" y="16" width="118" height="138" fill="#FCE9D2"/>
    <circle cx="75" cy="72" r="34" fill="#FFD6B0" {_o(4)}/>
    <circle cx="75" cy="34" r="20" fill="#C9C9D4" {_o(4)}/>
    <circle cx="62" cy="70" r="9" fill="none" stroke="{INK}" stroke-width="3"/><circle cx="88" cy="70" r="9" fill="none" stroke="{INK}" stroke-width="3"/>
    <path d="M 64 90 Q 75 98 86 90" fill="none" stroke="{INK}" stroke-width="3"/>
    <path d="M 30 154 Q 75 110 120 154 Z" fill="#B05CF0" {_o(4)}/></g>
  <g id="{p}-fridge">
    <rect x="770" y="520" width="270" height="740" rx="18" fill="#EAF2F8" {_o()}/>
    <rect x="770" y="520" width="270" height="70" rx="18" fill="#E8413A" {_o()}/>
    <text x="905" y="570" text-anchor="middle" font-family="Inter" font-weight="900" font-size="36" fill="#fff">KALT</text>
    <rect id="{p}-glow" x="790" y="610" width="230" height="620" rx="8" fill="#BFF0FF"/>
    {bottles}
    <rect x="790" y="610" width="230" height="620" rx="8" fill="none" {_o(5)}/>
  </g>
  <g id="{p}-counter">
    <rect x="20" y="1180" width="600" height="420" rx="10" fill="#D98C4A" {_o()}/>
    <rect x="0" y="1160" width="640" height="40" rx="10" fill="#8E4F22" {_o()}/>
    <rect x="60" y="1240" width="240" height="300" rx="10" fill="#C77A3A" {_o(5)}/>
    <rect x="340" y="1240" width="240" height="300" rx="10" fill="#C77A3A" {_o(5)}/>
    <g transform="translate(380,1020)">
      <rect x="0" y="40" width="200" height="100" rx="12" fill="#5E6275" {_o()}/>
      <rect x="20" y="0" width="160" height="60" rx="8" fill="#22303F" {_o()}/>
      <text id="{p}-disp" x="100" y="44" text-anchor="middle" font-family="Inter" font-weight="900" font-size="38" fill="#4BE08A">0,00</text>
    </g>
  </g>
  {nightov}
"""
    return _svg(p, inner)


def theke_front(p="kf"):
    """Theke als eigene Ebene vor Kalle (damit er dahinter steht)."""
    inner = f"""
    <rect x="20" y="1180" width="600" height="420" rx="10" fill="#D98C4A" {_o()}/>
    <rect x="0" y="1160" width="640" height="40" rx="10" fill="#8E4F22" {_o()}/>
    <rect x="60" y="1240" width="240" height="300" rx="10" fill="#C77A3A" {_o(5)}/>
    <rect x="340" y="1240" width="240" height="300" rx="10" fill="#C77A3A" {_o(5)}/>
    <g transform="translate(380,1020)">
      <rect x="0" y="40" width="200" height="100" rx="12" fill="#5E6275" {_o()}/>
      <rect x="20" y="0" width="160" height="60" rx="8" fill="#22303F" {_o()}/>
      <text id="{p}-disp" x="100" y="44" text-anchor="middle" font-family="Inter" font-weight="900" font-size="38" fill="#4BE08A">0,00</text>
    </g>"""
    return _svg(p, inner)


# ------------------------------------------------------------------ Straße mit Dennis' Mega-Späti

def strasse_spaeti(p="st"):
    people = []
    cols = ["#FF7A2F", "#3B6FF0", "#3DDC84", "#FF4F8B", "#FFC233", "#B05CF0", "#2EC4D6"]
    for k in range(7):
        x = 600 - k * 80
        c = cols[k]
        people.append(f'<g class="{p}-q" transform="translate({x},1150)"><rect x="-26" y="-120" width="52" height="100" rx="24" fill="{c}" {_o(5)}/>'
                      f'<circle cx="0" cy="-150" r="32" fill="#FFD6B0" {_o(5)}/>'
                      f'<rect x="-22" y="-26" width="18" height="30" fill="#3B4A7A" {_o(4)}/><rect x="4" y="-26" width="18" height="30" fill="#3B4A7A" {_o(4)}/></g>')
    inner = f"""
  <rect width="{W}" height="{H}" fill="#9ED8F5"/>
  {_wolke(820, 420, 0.9)}
  <rect x="40" y="520" width="1000" height="640" fill="#3B2A6B" {_o()}/>
  <rect x="40" y="480" width="1000" height="50" fill="#2A1E50" {_o()}/>
  <g id="{p}-neon">
    <rect x="160" y="560" width="760" height="150" rx="24" fill="#1A1033" {_o()}/>
    <text x="540" y="672" text-anchor="middle" font-family="Inter" font-weight="900" font-size="104" fill="none"
      stroke="#FF4F8B" stroke-width="16" opacity="0.35">MEGA-SPÄTI</text>
    <text x="540" y="672" text-anchor="middle" font-family="Inter" font-weight="900" font-size="104" fill="#FFE3F0"
      stroke="#FF4F8B" stroke-width="5" paint-order="stroke">MEGA-SPÄTI</text>
  </g>
  <rect x="120" y="760" width="840" height="300" rx="10" fill="#FFE27A" {_o()}/>
  {_regal_ware(120, 960, 900, 3)}{_regal_ware(120, 960, 1050, 6)}
  <circle id="{p}-ring" cx="880" cy="980" r="70" fill="none" stroke="#fff" stroke-width="18"/>
  <path d="M 880 1050 L 880 1160" stroke="{INK}" stroke-width="8"/>
  <rect x="0" y="1150" width="{W}" height="30" fill="#B8B1A6" {_o(5)}/>
  {''.join(people)}
  <rect x="0" y="1180" width="{W}" height="300" fill="#5A5F6B"/>
  {''.join(f'<rect x="{k * 220 + 20}" y="1318" width="130" height="18" rx="6" fill="#fff"/>' for k in range(5))}
  <rect x="0" y="1480" width="{W}" height="440" fill="#D9D4CC"/>
  <rect x="0" y="1470" width="{W}" height="22" fill="#B8B1A6" {_o(5)}/>
"""
    return _svg(p, inner)


# ------------------------------------------------------------------ Spiegel-/Nahaufnahme-Hintergrund

def nahaufnahme(p="na", farbe="#E8F1F8"):
    tiles = "".join(f'<path d="M 0 {k * 120} L {W} {k * 120}" stroke="#D2E0EC" stroke-width="4"/>' for k in range(17))
    tiles += "".join(f'<path d="M {k * 120} 0 L {k * 120} {H}" stroke="#D2E0EC" stroke-width="4"/>' for k in range(10))
    inner = f"""
  <rect width="{W}" height="{H}" fill="{farbe}"/>{tiles}
  <ellipse cx="540" cy="900" rx="430" ry="560" fill="#FFF8EA" stroke="#E0A93A" stroke-width="34"/>
  <ellipse cx="540" cy="900" rx="430" ry="560" fill="none" stroke="{INK}" stroke-width="7"/>
  <ellipse cx="540" cy="900" rx="396" ry="526" fill="none" stroke="{INK}" stroke-width="5"/>
"""
    return _svg(p, inner)


# ------------------------------------------------------------------ Großmarkt (ab Folge 3)

def grossmarkt(p="gm"):
    regale = []
    for col, x in enumerate((40, 400, 760)):
        regale.append(f'<rect x="{x}" y="380" width="300" height="980" fill="#5E6B7A" {_o()}/>')
        for k, y in enumerate((560, 800, 1040, 1280)):
            regale.append(f'<rect x="{x}" y="{y}" width="300" height="20" fill="#F2A33A" {_o(5)}/>')
            regale.append(_regal_ware(x, x + 300, y, col * 4 + k))
    floor = "".join(f'<path d="M {k * 180} 1360 L {k * 180 - 120} 1920" stroke="#B9BFC8" stroke-width="5"/>' for k in range(8))
    inner = f"""
  <rect width="{W}" height="{H}" fill="#DDE3EA"/>
  <rect x="0" y="300" width="{W}" height="40" fill="#9AA6B4"/>
  <rect x="0" y="330" width="{W}" height="1040" fill="#C9D1DB"/>
  {''.join(regale)}
  <rect x="300" y="300" width="480" height="70" rx="12" fill="#E8413A" {_o(5)}/>
  <text x="540" y="350" text-anchor="middle" font-family="Inter" font-weight="900" font-size="40" fill="#fff">GROSSMARKT</text>
  <rect x="0" y="1360" width="{W}" height="560" fill="#E9ECEF"/>{floor}
"""
    return _svg(p, inner)
