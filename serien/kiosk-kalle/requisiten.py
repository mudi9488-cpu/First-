"""Requisiten (HTML/SVG-Schnipsel) der Serie „Kiosk-Kalle“ – wiederverwendbar in jeder Folge."""
import re

INK = "#1B1530"


def place(svg, cx, fy, z=2):
    """SVG-Figur so setzen, dass ihr Ursprung (zwischen den Füßen) bei (cx, fy) liegt."""
    vb = [float(x) for x in re.search(r'viewBox="([^"]+)"', svg).group(1).split()]
    w = float(re.search(r'width="([\d.]+)"', svg).group(1))
    s = w / vb[2]
    return svg.replace('style="overflow:visible"',
                       f'style="overflow:visible;left:{cx + vb[0] * s:.0f}px;top:{fy + vb[1] * s:.0f}px;z-index:{z}"', 1)


def stempel(pid, text, x, y, size=120, col="#E0202E", rot=-12):
    return (f'<div id="{pid}" class="abs" style="left:{x}px;top:{y}px;opacity:0;transform:rotate({rot}deg);border:14px solid {col};z-index:6;'
            f'border-radius:24px;padding:4px 30px;color:{col};font-weight:900;font-size:{size}px;background:rgba(255,255,255,0.85)">{text}</div>')


def preis(pid, text, x, y, col="#E8413A", rot=-8, size=70):
    return (f'<div id="{pid}" class="abs" style="left:{x}px;top:{y}px;opacity:0;transform:rotate({rot}deg);background:{col};color:#fff;z-index:6;'
            f'font-weight:900;font-size:{size}px;padding:10px 30px;border-radius:18px;border:6px solid {INK}">{text}</div>')


def kommentar(pid, text, x, y, size=36):
    return (f'<div id="{pid}" class="abs" style="left:{x}px;top:{y}px;opacity:0;z-index:6;background:#fff;color:{INK};font-weight:800;font-size:{size}px;'
            f'padding:16px 26px;border-radius:26px;border:5px solid {INK};display:flex;gap:14px;align-items:center;white-space:nowrap">'
            f'<span style="width:44px;height:44px;border-radius:50%;background:#B05CF0;display:inline-block;flex:none"></span>{text}</div>')


def herz(pid, x, y, s=90):
    return (f'<svg id="{pid}" class="abs" style="left:{x}px;top:{y}px;opacity:0;z-index:6" width="{s}" height="{s}" viewBox="0 0 24 24">'
            '<path d="M12 21s-7.5-4.6-10-9.3C.4 8.4 2.3 4 6.3 4c2.3 0 3.9 1.4 5.7 3.4C13.8 5.4 15.4 4 17.7 4c4 0 5.9 4.4 4.3 7.7C19.5 16.4 12 21 12 21z" '
            f'fill="#FF4F6B" stroke="{INK}" stroke-width="1.6"/></svg>')


def traenen(pid, x, y, h=260):
    return (f'<svg id="{pid}" class="abs" style="left:{x}px;top:{y}px;opacity:0;z-index:4" width="70" height="{h}" viewBox="0 0 70 260" preserveAspectRatio="none">'
            f'<path d="M 35 0 Q 60 120 50 200 Q 35 250 20 200 Q 10 120 35 0 Z" fill="#7FD3FF" stroke="{INK}" stroke-width="5" opacity="0.95"/></svg>')


def schild(pid, zeile1, zeile2, x, y, w=860, rot=-3, farbe="#FFE14A", z2col="#E0202E", z2size=150):
    return (f'<div id="{pid}" class="abs" style="left:{x}px;top:{y}px;width:{w}px;opacity:0;z-index:4;background:{farbe};border:10px solid {INK};'
            f'border-radius:26px;text-align:center;padding:16px 0;transform:rotate({rot}deg)">'
            f'<div style="font-weight:900;font-size:58px;color:{INK}">{zeile1}</div>'
            f'<div style="font-weight:900;font-size:{z2size}px;color:{z2col};line-height:1;-webkit-text-stroke:6px {INK};paint-order:stroke fill">{zeile2}</div></div>')


def becher(pid, x, y, s=120, z=5):
    return (f'<svg id="{pid}" class="abs" style="left:{x}px;top:{y}px;opacity:0;z-index:{z}" width="{s}" height="{s}" viewBox="0 0 120 120">'
            '<path d="M 46 28 Q 36 18 46 8 M 66 28 Q 56 18 66 8" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" opacity="0.9"/>'
            f'<path d="M 22 36 L 90 36 L 82 108 Q 56 116 30 108 Z" fill="#fff" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
            '<path d="M 26 48 L 86 48" stroke="#8B4A2B" stroke-width="10"/>'
            f'<rect x="34" y="64" width="44" height="22" rx="5" fill="#E8413A"/><text x="56" y="81" text-anchor="middle" font-family="Inter" '
            'font-weight="900" font-size="14" fill="#fff">OMA</text></svg>')


def topf(pid, x, y, inhalt="#8B4A2B", s=320):
    return (f'<svg id="{pid}" class="abs" style="left:{x}px;top:{y}px;z-index:4" width="{s}" height="{s * 0.75:.0f}" viewBox="0 0 320 240">'
            f'<rect x="20" y="190" width="280" height="40" rx="10" fill="#2B2B3A" stroke="{INK}" stroke-width="6"/>'
            f'<ellipse id="{pid}-platte" cx="160" cy="190" rx="100" ry="10" fill="#E8413A" opacity="0.6"/>'
            f'<path d="M 50 70 L 270 70 L 256 186 L 64 186 Z" fill="#9AA6B4" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
            f'<ellipse cx="160" cy="70" rx="110" ry="22" fill="#7E8492" stroke="{INK}" stroke-width="7"/>'
            f'<ellipse id="{pid}-inhalt" cx="160" cy="74" rx="96" ry="16" fill="{inhalt}"/>'
            f'<path d="M 50 92 L 14 86 M 270 92 L 306 86" stroke="{INK}" stroke-width="12" stroke-linecap="round"/></svg>')


def rauch(pid, x, y, s=360):
    return (f'<svg id="{pid}" class="abs" style="left:{x}px;top:{y}px;opacity:0;z-index:5" width="{s}" height="{s}" viewBox="0 0 200 200">'
            '<g fill="#5B5F6B" opacity="0.85"><circle cx="70" cy="140" r="40"/><circle cx="120" cy="120" r="48"/><circle cx="90" cy="80" r="44"/>'
            '<circle cx="140" cy="60" r="36"/><circle cx="60" cy="40" r="28"/></g></svg>')


def rauchmelder(pid, x, y):
    return (f'<svg id="{pid}" class="abs" style="left:{x}px;top:{y}px;z-index:5" width="160" height="80" viewBox="0 0 160 80">'
            f'<ellipse cx="80" cy="24" rx="70" ry="22" fill="#F4F4F4" stroke="{INK}" stroke-width="6"/>'
            f'<circle id="{pid}-led" cx="80" cy="28" r="10" fill="#7E8492"/></svg>')


def zettel(pid, zeilen, x=150, y=420, w=780):
    rows = "".join(f'<div style="border-bottom:3px solid #C9D8F0;padding:10px 0;{st}">{t}</div>' for t, st in zeilen)
    return (f'<div id="{pid}" class="abs" style="left:{x}px;top:{y}px;width:{w}px;opacity:0;z-index:5;background:#FFF9E6;border:7px solid {INK};'
            f'border-radius:12px;padding:30px 40px;font-family:\'Segoe Print\',\'Comic Sans MS\',cursive;font-size:50px;color:#2A3A8C;'
            f'transform:rotate(-2deg);box-shadow:0 14px 0 rgba(0,0,0,0.2)">{rows}</div>')


def einkaufswagen(pid, x, y, w=420, voll=True):
    ware = ""
    if voll:
        ware = "".join(f'<rect x="{90 + k * 60}" y="{40 - (k % 2) * 20}" width="52" height="{70 + (k % 2) * 20}" rx="6" '
                       f'fill="{["#8B4A2B", "#F4F4F4", "#FFC233", "#E8413A", "#3B6FF0"][k]}" stroke="{INK}" stroke-width="5"/>' for k in range(5))
    return (f'<svg id="{pid}" class="abs" style="left:{x}px;top:{y}px;z-index:3" width="{w}" height="{w * 0.62:.0f}" viewBox="0 0 420 260">'
            f'{ware}<path d="M 10 30 L 60 30 L 90 170 L 380 170 L 400 70 L 70 70" fill="none" stroke="#7E8492" stroke-width="12" '
            'stroke-linejoin="round" stroke-linecap="round"/>'
            '<path d="M 80 110 L 390 110 M 140 70 L 150 170 M 220 70 L 225 170 M 300 70 L 300 170" stroke="#7E8492" stroke-width="7"/>'
            f'<circle cx="120" cy="215" r="24" fill="#2B2B3A" stroke="{INK}" stroke-width="6"/><circle cx="350" cy="215" r="24" fill="#2B2B3A" '
            f'stroke="{INK}" stroke-width="6"/><path d="M 100 170 L 120 200 M 360 170 L 350 200" stroke="#7E8492" stroke-width="10"/></svg>')
