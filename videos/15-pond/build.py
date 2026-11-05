#!/usr/bin/env python3
"""Builds "How to build a pond that stays clear" (English) – same structure as videos/07–14:
one growing world (garden pond cut open at the front: liner, layers, deep zone), a chain of problem → fix (red problem words,
yellow fixes), one word per caption, mid-screen. No voice is mixed in: assets/timings.json comes from a timing guide
(tools/tts.py, Piper en-us-ryan-medium) until the creator's recording arrives, then tools/align.py.

1. Stimme: python3 ../../tools/align.py . assets/source/<aufnahme>.mp3   (Platzhalter: tools/tts.py)
2. python3 build.py
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "tools"))
from simkit import load_timings, fmt, audio_len  # noqa: E402

SFX_ROOT = Path("/root/.claude/plugins/cache/hyperframes/hyperframes/0.8.197/skills/media-use/audio/assets/sfx")
W, H = 1080, 1920
TITLE = "How to build a pond that stays clear"

T = load_timings(HERE)
B = {b["id"]: b for b in T["beats"]}
VOICE_END = T["beats"][-1]["end"]
TOTAL = round(VOICE_END + 1.6, 2)


def word(bid, prefix, n=1):
    """Startzeit des n-ten Wortes im Beat, das mit `prefix` beginnt."""
    k = 0
    for l in B[bid]["lines"]:
        for w in l["words"]:
            if re.sub(r"[^\wäöüÄÖÜß'-]", "", w["text"]).lower().startswith(prefix.lower()):
                k += 1
                if k == n:
                    return round(w["start"], 3)
    raise KeyError((bid, prefix))


K = {b["id"]: round(b["start"], 3) for b in T["beats"]}
K["want"] = 0.0
K.update({
    "clear_w": word("want", "clear"), "dig_w": word("dig", "dig"), "liner": word("dig", "liner"),
    "stone_w": word("stone", "stone"), "hole": word("stone", "hole"), "sand": word("stone", "sand"), "fleece": word("stone", "fleece"),
    "green_w": word("green", "green"), "warm": word("green", "warm"),
    "deep_w": word("deep", "deep"), "eighty": word("deep", "80"),
    "soil_w": word("soil", "soil"), "algae": word("soil", "algae"), "gravel": word("soil", "gravel"),
    "plants_w": word("plants", "plants"), "third": word("plants", "third"),
    "fert": word("rain", "fertilizer"), "edge": word("rain", "edge"),
    "leaves_w": word("leaves", "leaves"), "net": word("leaves", "net"),
    "congrats": word("end", "Congratulations"), "crystal": word("end", "crystal"),
})
# (Start, Kamera von, Kamera nach, Ziel, FOV); None = Kamerafahrt
SHOTS = [
    (K["want"], (3.4, 2.2, 5.2), (2.9, 1.9, 4.6), (0, 0.0, -0.6), 50),
    (K["dig"], (1.2, 0.45, 3.0), (1.0, 0.35, 2.6), (0, -0.3, 0.0), 50),
    (K["stone"], (0.65, -0.05, 2.1), (0.55, -0.1, 1.8), (0.25, -0.35, 0.0), 50),
    (K["green"], (1.7, 1.35, 3.1), (1.4, 1.15, 2.7), (0, -0.1, -0.5), 50),
    (K["deep"], (0.9, 0.15, 3.1), (0.75, 0.08, 2.7), (0, -0.45, 0.0), 50),
    (K["soil"], (1.45, 0.25, 2.4), (1.3, 0.18, 2.1), (0.85, -0.25, 0.0), 50),
    (K["plants"], (2.1, 1.5, 3.3), (1.8, 1.3, 2.9), (0, -0.1, -0.6), 50),
    (K["rain"], (3.1, 0.85, 3.0), (2.7, 0.72, 2.6), (1.3, 0.0, -0.3), 50),
    (K["leaves"], (1.6, 1.6, 3.0), (1.35, 1.4, 2.6), (0, -0.05, -0.6), 50),
    (K["end"], None, None, (0, 0.0, -0.6), 50),
]

# Schwebende 3D-Wörter: rot = Problem, gelb = Lösung
LABELS = [
    ("l-clear", "CLEAR POND?", "g", 0.0, 0.7, -0.6, K["clear_w"], K["dig"]),
    ("l-liner", "LINER", "y", 0.0, -0.15, 0.5, K["liner"], K["stone"]),
    ("l-hole", "STONE · LEAK!", "r", 0.3, -0.5, 0.5, K["hole"] - 0.4, K["sand"]),
    ("l-sand", "SAND + FLEECE", "y", 0.0, -0.5, 0.5, K["sand"], K["green"]),
    ("l-green", "ALGAE!", "r", 0.0, 0.45, -0.5, K["green_w"] - 0.3, K["warm"] - 0.4),
    ("l-warm", "TOO SHALLOW · TOO WARM", "r", 0.0, 0.45, -0.5, K["warm"] - 0.4, K["deep"]),
    ("l-80", "80 CM DEEP ZONE", "y", 0.0, -0.6, 0.5, K["eighty"] - 0.3, K["soil"]),
    ("l-soil", "GARDEN SOIL = ALGAE FOOD", "r", 0.9, -0.12, 0.5, K["soil_w"] - 0.3, K["gravel"]),
    ("l-gravel", "PLAIN GRAVEL", "y", 0.9, -0.12, 0.5, K["gravel"], K["plants"]),
    ("l-plants", "PLANTS · 1/3 COVER", "y", 0.0, 0.55, -0.6, K["plants_w"], K["rain"]),
    ("l-runoff", "FERTILIZER RUNOFF!", "r", 1.9, 0.4, -0.3, K["fert"] - 0.3, K["edge"]),
    ("l-edge", "RAISED EDGE", "y", 1.3, 0.3, 0.3, K["edge"], K["leaves"]),
    ("l-leaves", "ROTTING LEAVES!", "r", 0.0, 0.5, -0.6, K["leaves_w"] - 0.3, K["net"]),
    ("l-net", "POND NET", "y", 0.0, 0.5, -0.6, K["net"], K["end"]),
    ("l-congrats", "CONGRATULATIONS!", "y", 0.0, 1.5, -0.6, K["congrats"], TOTAL),
]

WORLD_JS = r"""
const K = __K__, SHOTS = __SHOTS__, LABELS = __LABELS__, DUR = __DUR__;
window.__hf = window.__hf || {}; window.__hf.buildReady = window.__hf.buildReady || {};
window.__hf.buildReady.world = import("./assets/three.module.min.js").then((THREE) => {
  const W = 1080, H = 1920;
  const canvas = document.getElementById("w-canvas");
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1); renderer.setSize(W, H, false);
  renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.05;

  function mulberry(a) { return function () { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
  const R = mulberry(11);
  const rr = (a, b) => a + (b - a) * R();
  const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
  const ease = (x) => { x = clamp(x, 0, 1); return x * x * (3 - 2 * x); };
  const outBack = (x) => { x = clamp(x, 0, 1); const c = 1.7; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };

  // ---------- prozedurale Texturen
  function tex(w, h, seed, draw, rep) {
    const c = document.createElement("canvas"); c.width = w; c.height = h;
    const g = c.getContext("2d"); const r = mulberry(seed); draw(g, r, w, h);
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace;
    t.wrapS = t.wrapT = THREE.RepeatWrapping; if (rep) t.repeat.set(rep[0], rep[1]); t.anisotropy = 4; return t;
  }
  const speck = (g, r, w, h, n, cols, s0, s1) => { for (let i = 0; i < n; i++) { g.fillStyle = cols[Math.floor(r() * cols.length)];
    const s = s0 + r() * (s1 - s0); g.beginPath(); g.ellipse(r() * w, r() * h, s, s * (0.5 + r() * 0.6), r() * 3, 0, 6.3); g.fill(); } };
  const grassT = tex(512, 512, 1, (g, r, w, h) => { g.fillStyle = "#4E7F2E"; g.fillRect(0, 0, w, h);
    for (let i = 0; i < 9000; i++) { const x = r() * w, y = r() * h, l = 6 + r() * 12;
      g.strokeStyle = ["#3F6E25", "#5E9238", "#6FA444", "#4A7A2B", "#7DB04E"][Math.floor(r() * 5)]; g.lineWidth = 1.4;
      g.beginPath(); g.moveTo(x, y); g.lineTo(x + (r() - 0.5) * 4, y - l); g.stroke(); } }, [24, 24]);
  const cutT = tex(1024, 256, 2, (g, r, w, h) => {
    g.fillStyle = "#9A5A2C"; g.fillRect(0, 0, w, h);
    speck(g, r, w, h, 2600, ["#8A4F25", "#A8663A", "#7E4620", "#B3713F"], 1, 4);
    g.fillStyle = "#4A3020"; g.fillRect(0, 0, w, h * 0.12);
    speck(g, r, w, h * 0.12, 900, ["#3A2618", "#5A3B28", "#2E1F14"], 1, 3);
    g.fillStyle = "#5C7F33"; g.fillRect(0, 0, w, h * 0.018);
    for (let i = 0; i < 26; i++) { const x = r() * w, y = h * (0.22 + r() * 0.72), s = 6 + r() * 16;
      g.fillStyle = ["#8C8279", "#9E958C", "#7A716A"][Math.floor(r() * 3)]; g.beginPath(); g.ellipse(x, y, s * 1.3, s, r() * 3, 0, 6.3); g.fill();
      g.fillStyle = "rgba(255,255,255,0.18)"; g.beginPath(); g.ellipse(x - s * 0.3, y - s * 0.3, s * 0.5, s * 0.3, 0, 0, 6.3); g.fill(); } });
  const woodT = tex(256, 64, 3, (g, r, w, h) => { g.fillStyle = "#9C6A3C"; g.fillRect(0, 0, w, h);
    for (let i = 0; i < 40; i++) { g.strokeStyle = ["#86592F", "#B07C49", "#7A4F28"][Math.floor(r() * 3)]; g.lineWidth = 1 + r() * 2;
      const y = r() * h; g.beginPath(); g.moveTo(0, y); g.bezierCurveTo(w * 0.3, y + (r() - 0.5) * 8, w * 0.7, y + (r() - 0.5) * 8, w, y); g.stroke(); }
    g.fillStyle = "rgba(60,35,15,0.5)"; g.fillRect(0, h - 3, w, 3); }, [1, 1]);
  const barkT = tex(128, 128, 4, (g, r, w, h) => { g.fillStyle = "#6B4A2F"; g.fillRect(0, 0, w, h);
    for (let i = 0; i < 200; i++) { g.fillStyle = ["#5A3D25", "#7B5838", "#4C331F"][Math.floor(r() * 3)]; g.fillRect(r() * w, r() * h, 2 + r() * 3, 8 + r() * 20); } }, [1, 1]);
  const twigT = tex(512, 256, 12, (g, r, w, h) => { g.fillStyle = "#3A2A1C"; g.fillRect(0, 0, w, h);
    for (let i = 0; i < 260; i++) { const x = r() * w, y = r() * h, s = 3 + r() * 9;
      g.fillStyle = ["#6B4A2F", "#7B5838", "#5A3D25"][Math.floor(r() * 3)]; g.beginPath(); g.ellipse(x, y, s, s * 0.8, 0, 0, 6.3); g.fill();
      g.fillStyle = "#C9A06A"; g.beginPath(); g.ellipse(x, y, s * 0.6, s * 0.45, 0, 0, 6.3); g.fill(); }
    for (let i = 0; i < 90; i++) { g.strokeStyle = "#6B4A2F"; g.lineWidth = 4; const x = r() * w, y = r() * h;
      g.beginPath(); g.moveTo(x, y); g.lineTo(x + 30 + r() * 40, y + (r() - 0.5) * 14); g.stroke(); } }, [2, 1]);
  const leafT = tex(512, 256, 5, (g, r, w, h) => { g.fillStyle = "#7A5A2A"; g.fillRect(0, 0, w, h);
    speck(g, r, w, h, 1400, ["#C0732A", "#A65A1F", "#D9A13A", "#8D6E2B", "#6E7A2C", "#B4472A"], 4, 11); }, [2, 1]);
  const compT = tex(512, 256, 6, (g, r, w, h) => { g.fillStyle = "#3D2A1C"; g.fillRect(0, 0, w, h);
    speck(g, r, w, h, 1800, ["#2C1E14", "#55392A", "#4A3322", "#6B4A2C"], 2, 7);
    for (let i = 0; i < 160; i++) { g.strokeStyle = ["#A27A3C", "#7E6233"][Math.floor(r() * 2)]; g.lineWidth = 1.5;
      const x = r() * w, y = r() * h; g.beginPath(); g.moveTo(x, y); g.lineTo(x + (r() - 0.5) * 20, y + (r() - 0.5) * 8); g.stroke(); } }, [2, 1]);
  const soilT = tex(512, 256, 7, (g, r, w, h) => { g.fillStyle = "#2F2219"; g.fillRect(0, 0, w, h);
    speck(g, r, w, h, 3000, ["#251A12", "#3B2B1F", "#463324", "#1E150F"], 1, 3); }, [2, 1]);
  const gravelT = tex(512, 512, 8, (g, r, w, h) => { g.fillStyle = "#B8A58A"; g.fillRect(0, 0, w, h);
    speck(g, r, w, h, 5000, ["#A8957A", "#C8B79C", "#9C8A70", "#D4C6AE"], 1, 4); }, [10, 10]);
  const roofT = tex(256, 256, 9, (g, r, w, h) => { g.fillStyle = "#A8432F"; g.fillRect(0, 0, w, h);
    for (let y = 0; y < h; y += 16) { g.fillStyle = "rgba(0,0,0,0.18)"; g.fillRect(0, y, w, 3);
      for (let x = (y / 16) % 2 * 12; x < w; x += 24) { g.fillStyle = "rgba(0,0,0,0.1)"; g.fillRect(x, y, 2, 16); } } }, [4, 4]);
  const meshT = tex(256, 256, 10, (g, r, w, h) => { g.clearRect(0, 0, w, h); g.strokeStyle = "#C9CED6"; g.lineWidth = 3;
    for (let i = 0; i <= w; i += 16) { g.beginPath(); g.moveTo(i, 0); g.lineTo(i, h); g.stroke(); g.beginPath(); g.moveTo(0, i); g.lineTo(w, i); g.stroke(); } }, [6, 3]);
  const skyT = tex(16, 512, 11, (g, r, w, h) => { const gr = g.createLinearGradient(0, 0, 0, h);
    gr.addColorStop(0, "#3F7FD1"); gr.addColorStop(0.55, "#8DB9EA"); gr.addColorStop(1, "#DCEBF7"); g.fillStyle = gr; g.fillRect(0, 0, w, h); });
  const subT = tex(256, 256, 31, (g, r, w, h) => { g.fillStyle = "#A8693A"; g.fillRect(0, 0, w, h);
    speck(g, r, w, h, 1400, ["#96592E", "#B9794A", "#8A4F25"], 1, 4); }, [2, 2]);
  const concT = tex(256, 256, 21, (g, r, w, h) => { g.fillStyle = "#B9B6B0"; g.fillRect(0, 0, w, h);
    speck(g, r, w, h, 1600, ["#A9A6A0", "#C6C3BD", "#9E9B95", "#D0CDC8"], 1, 3);
    g.strokeStyle = "rgba(0,0,0,0.08)"; g.lineWidth = 2; for (let y = 0; y < h; y += 64) { g.beginPath(); g.moveTo(0, y); g.lineTo(w, y); g.stroke(); } }, [3, 3]);
  const secT = tex(256, 256, 22, (g, r, w, h) => { g.fillStyle = "#8E8B86"; g.fillRect(0, 0, w, h);
    speck(g, r, w, h, 900, ["#7C7974", "#A19E99", "#6E6B66"], 1, 3); }, [1, 1]);
  const cardT = tex(128, 128, 23, (g, r, w, h) => { g.fillStyle = "#C49A6C"; g.fillRect(0, 0, w, h);
    for (let i = 0; i < 30; i++) { g.fillStyle = "rgba(120,80,40,0.12)"; g.fillRect(0, r() * h, w, 1); }
    g.fillStyle = "#D9BC8C"; g.fillRect(w * 0.44, 0, w * 0.12, h); g.strokeStyle = "#8A6440"; g.lineWidth = 3; g.strokeRect(1, 1, w - 2, h - 2); }, [1, 1]);
  const moldT = (() => { const c = document.createElement("canvas"); c.width = c.height = 256; const g = c.getContext("2d"); const r = mulberry(24);
    for (let k = 0; k < 9; k++) { const cx = 40 + r() * 176, cy = 40 + r() * 176, rad = 18 + r() * 40;
      for (let i = 0; i < 90; i++) { const a = r() * 6.3, d = Math.pow(r(), 0.7) * rad;
        g.fillStyle = ["rgba(28,40,22,0.85)", "rgba(15,20,12,0.9)", "rgba(60,72,40,0.7)", "rgba(40,45,30,0.8)"][Math.floor(r() * 4)];
        g.beginPath(); g.arc(cx + Math.cos(a) * d, cy + Math.sin(a) * d, 2 + r() * 6, 0, 6.3); g.fill(); } }
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; })();

  const topT = tex(256, 256, 41, (g, r, w, h) => { g.fillStyle = "#3A2A1E"; g.fillRect(0, 0, w, h);
    speck(g, r, w, h, 2200, ["#2C1F15", "#4A3526", "#56402C", "#22180F"], 1, 3);
    for (let i = 0; i < 70; i++) { g.strokeStyle = "#C9B48A"; g.lineWidth = 1; const x = r() * w, y = r() * h; g.beginPath(); g.moveTo(x, y); g.lineTo(x + (r() - 0.5) * 10, y + 6 + r() * 10); g.stroke(); } }, [3, 1]);
  const stoneT = tex(256, 128, 42, (g, r, w, h) => { g.fillStyle = "#6E6C68"; g.fillRect(0, 0, w, h);
    for (let i = 0; i < 520; i++) { const x = r() * w, y = r() * h, s = 3 + r() * 6; g.fillStyle = ["#8D8B86", "#A3A19B", "#5E5C58", "#7B7974", "#B4B1AA"][Math.floor(r() * 5)];
      g.beginPath(); g.moveTo(x - s, y); g.lineTo(x - s * 0.2, y - s * 0.8); g.lineTo(x + s, y - s * 0.2); g.lineTo(x + s * 0.4, y + s * 0.8); g.closePath(); g.fill(); } }, [4, 1]);
  const sandT = tex(256, 64, 43, (g, r, w, h) => { g.fillStyle = "#D8C08E"; g.fillRect(0, 0, w, h); speck(g, r, w, h, 1500, ["#C9AE78", "#E4CFA2", "#BFA36C"], 0.6, 1.6); }, [6, 1]);
  const mudT = tex(256, 128, 44, (g, r, w, h) => { g.fillStyle = "#5A3F2A"; g.fillRect(0, 0, w, h); speck(g, r, w, h, 900, ["#4A3322", "#6B4C33", "#3E2A1B"], 2, 6); }, [3, 1]);

  const std = (o) => new THREE.MeshStandardMaterial(Object.assign({ roughness: 0.9, metalness: 0 }, o));
  const scene = new THREE.Scene();
  scene.background = skyT;
  scene.fog = new THREE.Fog(0xCFE2F3, 30, 90);
  const add = (m, cast = true, recv = true) => { m.castShadow = cast; m.receiveShadow = recv; scene.add(m); return m; };
  const boxAt = (x0, x1, y0, y1, z0, z1, mat, cast = true) => { const m = add(new THREE.Mesh(new THREE.BoxGeometry(x1 - x0, y1 - y0, z1 - z0), mat), cast, true);
    m.position.set((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2); return m; };

  // ---------- Garten mit Querschnitt (Schnittkante bei z = 0.5); Teich-Aussparung (halbe Ellipse) in der oberen Bodenplatte
  const RX = 1.25, RZ = 1.4, SLAB = 1.5;
  const groundTop = std({ map: grassT });
  const deepT = tex(256, 256, 91, (g, r, w, h) => { g.fillStyle = "#9A5A2C"; g.fillRect(0, 0, w, h); speck(g, r, w, h, 1600, ["#8A4F25", "#A8663A", "#7E4620", "#B3713F"], 1, 4); }, [15, 1]);
  { const b = add(new THREE.Mesh(new THREE.BoxGeometry(60, 3.4 - SLAB, 20), [groundTop, groundTop, groundTop, groundTop, std({ map: deepT }), groundTop]), false, true); b.position.set(0, -SLAB - (3.4 - SLAB) / 2, -9.5); }
  const slabShape = new THREE.Shape(); slabShape.moveTo(-30, -0.5); slabShape.lineTo(-RX, -0.5);
  for (let i = 0; i <= 40; i++) { const a = Math.PI - (i / 40) * Math.PI; slabShape.lineTo(Math.cos(a) * RX, -0.5 + Math.sin(a) * RZ); }
  slabShape.lineTo(30, -0.5); slabShape.lineTo(30, 19.5); slabShape.lineTo(-30, 19.5); slabShape.lineTo(-30, -0.5);
  const slabG = new THREE.ExtrudeGeometry(slabShape, { depth: SLAB, bevelEnabled: false, curveSegments: 40 }); slabG.rotateX(-Math.PI / 2); slabG.translate(0, -SLAB, 0);
  const sideT = cutT.clone(); sideT.needsUpdate = true; sideT.repeat.set(0.25, -1 / SLAB); sideT.offset.set(0, 1 / SLAB);
  const slab = add(new THREE.Mesh(slabG, [groundTop, std({ map: sideT })]), false, true);
  const floorG = add(new THREE.Mesh(new THREE.BoxGeometry(60, 0.2, 30), std({ map: gravelT })), false, true); floorG.position.set(0, -3.5, 15.5);
  // Haus, Baum, Hecke, Wolken
  const house = new THREE.Group(); house.position.set(-5.5, 0, -14); house.rotation.y = 0.25; scene.add(house);
  { const wall = std({ color: 0xF2EFEA }), win = std({ color: 0x2C3440, roughness: 0.3 });
    const body = new THREE.Mesh(new THREE.BoxGeometry(9, 5.6, 7), wall); body.position.y = 2.8; body.castShadow = body.receiveShadow = true; house.add(body);
    const s = new THREE.Shape(); s.moveTo(-3.9, 0); s.lineTo(3.9, 0); s.lineTo(0, 3.2); s.lineTo(-3.9, 0);
    const rg = new THREE.ExtrudeGeometry(s, { depth: 9.6, bevelEnabled: false }); rg.translate(0, 0, -4.8); rg.rotateY(Math.PI / 2);
    const roof = new THREE.Mesh(rg, std({ map: roofT })); roof.position.y = 5.6; roof.castShadow = true; house.add(roof);
    for (const [x, y] of [[-3, 1.3], [0, 1.3], [3, 1.3], [-3, 4], [0, 4], [3, 4]]) {
      const w = new THREE.Mesh(new THREE.BoxGeometry(x === 0 && y < 2 ? 1.6 : 1.3, x === 0 && y < 2 ? 2.2 : 1.4, 0.1), win); w.position.set(x, y, 3.51); house.add(w); }
    const ch = new THREE.Mesh(new THREE.BoxGeometry(0.7, 2, 0.7), std({ color: 0x5A4A42 })); ch.position.set(2.2, 7.3, -1); house.add(ch); }
  const house2 = house.clone(); house2.position.set(7, 0, -18); house2.rotation.y = -0.2; scene.add(house2);
  function tree(x, z, s) { const g = new THREE.Group(); g.position.set(x, 0, z); g.scale.setScalar(s); scene.add(g);
    const tr = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.28, 3, 8), std({ map: barkT })); tr.position.y = 1.5; tr.castShadow = true; g.add(tr);
    for (let i = 0; i < 6; i++) { const b = new THREE.Mesh(new THREE.IcosahedronGeometry(rr(0.9, 1.4), 1), std({ color: [0x4F7A33, 0x5C8A3A, 0x46702F][i % 3], flatShading: true }));
      b.position.set(rr(-0.9, 0.9), 3.4 + rr(-0.3, 0.9), rr(-0.9, 0.9)); b.castShadow = true; g.add(b); } return g; }
  tree(-3.2, -5.5, 1.1); tree(4.2, -7.5, 1.3); tree(-9, -10, 1.4);
  for (let i = 0; i < 18; i++) { const hd = new THREE.Mesh(new THREE.IcosahedronGeometry(0.7, 1), std({ color: 0x3E6A2B, flatShading: true }));
    hd.position.set(-12 + i * 1.4, 0.5, -9); hd.scale.set(1.2, 0.9, 0.8); hd.castShadow = true; scene.add(hd); }
  for (const [x, y, z, s] of [[-14, 16, -40, 3], [6, 19, -45, 4], [18, 15, -38, 2.6], [-2, 22, -50, 3.5]]) {
    const cl = new THREE.Group(); cl.position.set(x, y, z); scene.add(cl);
    for (let i = 0; i < 7; i++) { const p = new THREE.Mesh(new THREE.SphereGeometry(s * rr(0.5, 0.9), 16, 12), new THREE.MeshBasicMaterial({ color: 0xFFFFFF, fog: false }));
      p.position.set(rr(-1.6, 1.6) * s, rr(-0.2, 0.5) * s, rr(-0.5, 0.5) * s); cl.add(p); } }

  // Licht
  scene.add(new THREE.HemisphereLight(0xD8E8FF, 0x6B5A40, 0.75));
  const sun = new THREE.DirectionalLight(0xFFF1D8, 2.6); sun.position.set(-6, 10, 7); sun.castShadow = true;
  sun.shadow.mapSize.set(2048, 2048); Object.assign(sun.shadow.camera, { left: -8, right: 8, top: 8, bottom: -8, near: 1, far: 40 });
  sun.shadow.bias = -0.0004; scene.add(sun); scene.add(sun.target);
  const sunBall = new THREE.Mesh(new THREE.SphereGeometry(1.4, 24, 16), new THREE.MeshBasicMaterial({ color: 0xFFF3B0, fog: false })); scene.add(sunBall);



  // ---------- Teich im Schnitt: Boden hinter dem Profil, Grube, Sand/Vlies, Folie, Wasser, Substrat
  const backT = cutT.clone(); backT.needsUpdate = true; backT.repeat.set(2 * RX * 0.25, 1); backT.offset.set(-RX * 0.25, 0);
  const soilBack = add(new THREE.Mesh(new THREE.PlaneGeometry(2 * RX, SLAB), std({ map: backT })), false, false); soilBack.position.set(0, -SLAB / 2, 0.501);
  const XE = 1.2;
  const shallowD = (x) => Math.abs(x) >= XE ? 0 : 0.35 * (1 - (x / XE) ** 2);
  const deepD = (x) => { const a = Math.abs(x); if (a >= XE) return 0; if (a > 1.05) return 0.32 * (XE - a) / 0.15; if (a > 0.72) return 0.32;
    if (a > 0.55) return 0.32 + (0.82 - 0.32) * (0.72 - a) / 0.17; return 0.82; };
  let deepK = 0, edgeK = 0;
  const D = (x) => shallowD(x) * (1 - deepK) + deepD(x) * deepK;
  const N = 96, xs = []; for (let i = 0; i <= N; i++) xs.push(-XE + 2 * XE * i / N);
  const edgeY = (x) => (Math.abs(x) > XE - 0.12 ? edgeK * 0.07 * (Math.abs(x) - (XE - 0.12)) / 0.12 : 0);
  function band(fTop, fBot) { const s = new THREE.Shape(); s.moveTo(xs[0], fTop(xs[0])); xs.forEach((x) => s.lineTo(x, fTop(x))); for (let i = xs.length - 1; i >= 0; i--) s.lineTo(xs[i], fBot(xs[i])); return new THREE.ShapeGeometry(s); }
  const mk = (mat, z) => { const m = add(new THREE.Mesh(new THREE.BufferGeometry(), mat), false, false); m.position.z = z; return m; };
  const holeMat = new THREE.MeshStandardMaterial({ color: 0x1A110B, roughness: 1 }); const holeM = mk(holeMat, 0.503);
  const sandM = mk(std({ color: 0xE3CFA0 }), 0.504);
  const fleeceM = mk(std({ color: 0xF4F4F0 }), 0.5045);
  const linerM = mk(std({ color: 0x1C1C1C, roughness: 0.4 }), 0.505);
  const gravelSubMat = std({ map: gravelT, color: 0xBFB7A8 }); const subM = mk(gravelSubMat, 0.506);
  const soilSubMat = std({ map: soilT });
  const waterMat = new THREE.MeshStandardMaterial({ color: 0x3E8EDB, transparent: true, opacity: 0.6, roughness: 0.1 });
  const waterM = mk(waterMat, 0.507);
  const setG = (m, g) => { m.geometry.dispose(); m.geometry = g; };
  const stone = add(new THREE.Mesh(new THREE.IcosahedronGeometry(0.06, 0), std({ color: 0x8C8279, flatShading: true })), false, false);
  // Wasseroberfläche (halbe Ellipse) + Algen, Seerosen, Uferpflanzen, Laub, Netz
  const surfShape = new THREE.Shape(); surfShape.moveTo(-RX + 0.03, 0);
  for (let i = 0; i <= 40; i++) { const a = Math.PI - (i / 40) * Math.PI; surfShape.lineTo(Math.cos(a) * (RX - 0.03), Math.sin(a) * (RZ - 0.03)); }
  surfShape.lineTo(-RX + 0.03, 0);
  const surfG = new THREE.ShapeGeometry(surfShape, 40); surfG.rotateX(-Math.PI / 2); surfG.translate(0, 0, 0.5);
  const surfMat = new THREE.MeshStandardMaterial({ color: 0x3E8EDB, transparent: true, opacity: 0.8, roughness: 0.05, metalness: 0.1 });
  const surf = add(new THREE.Mesh(surfG, surfMat), false, true);
  const pondBot = add(new THREE.Mesh(surfG.clone(), std({ color: 0x1C1C1C })), false, true);
  const blobs = [];
  for (let i = 0; i < 26; i++) { const a = R() * Math.PI, r = Math.sqrt(R()) * 0.9; const b = add(new THREE.Mesh(new THREE.CircleGeometry(rr(0.04, 0.11), 10), new THREE.MeshBasicMaterial({ color: 0x4F7A1E, transparent: true, opacity: 0.85 })), false, false);
    b.rotation.x = -Math.PI / 2; b.position.set(Math.cos(a) * r * RX, 0, 0.5 - Math.sin(a) * r * RZ); b.userData.o = R(); blobs.push(b); }
  const pads = [];
  for (let i = 0; i < 9; i++) { const a = 0.3 + R() * 2.5, r = rr(0.45, 0.85); const g = new THREE.Group(); g.position.set(Math.cos(a) * r * RX, 0, 0.5 - Math.sin(a) * r * RZ); scene.add(g);
    const pad = new THREE.Mesh(new THREE.CircleGeometry(rr(0.09, 0.14), 16, 0.3, Math.PI * 1.85), std({ color: 0x3F7A2E, side: THREE.DoubleSide })); pad.rotation.x = -Math.PI / 2; g.add(pad);
    if (i % 3 === 0) { const fl = new THREE.Mesh(new THREE.ConeGeometry(0.04, 0.05, 8), std({ color: 0xF2B8C8 })); fl.position.y = 0.025; g.add(fl); } g.userData.o = R(); pads.push(g); }
  const reeds = [];
  for (let i = 0; i < 8; i++) { const a = [0.15, 0.4, 0.7, 2.45, 2.75, 3.0, 1.4, 1.75][i]; const g = new THREE.Group(); g.position.set(Math.cos(a) * 0.86 * RX, 0, 0.5 - Math.sin(a) * 0.86 * RZ); scene.add(g);
    for (let k = 0; k < 7; k++) { const b = new THREE.Mesh(new THREE.ConeGeometry(0.012, rr(0.35, 0.6), 4), std({ color: [0x4F8A35, 0x6AA23A][k % 2], flatShading: true })); b.position.set(rr(-0.05, 0.05), 0.2, rr(-0.05, 0.05)); b.rotation.set(rr(-0.2, 0.2), 0, rr(-0.2, 0.2)); b.castShadow = true; g.add(b); }
    g.userData.o = R(); reeds.push(g); }
  const leaves = [];
  for (let i = 0; i < 24; i++) { const l = add(new THREE.Mesh(new THREE.CircleGeometry(rr(0.04, 0.06), 6), std({ color: [0xC0732A, 0xA65A1F, 0xD9A13A][i % 3], side: THREE.DoubleSide })), false, false);
    const a = R() * Math.PI, r = Math.sqrt(R()) * 0.85; l.userData = { x: Math.cos(a) * r * RX, z: 0.5 - Math.sin(a) * r * RZ, o: R() }; leaves.push(l); }
  const net = add(new THREE.Mesh(new THREE.PlaneGeometry(2.8, 1.7), new THREE.MeshBasicMaterial({ map: (() => { const t = tex(128, 128, 92, (g, r, w, h) => { g.clearRect(0, 0, w, h); g.strokeStyle = "rgba(30,30,30,0.9)"; g.lineWidth = 2;
      for (let i = 0; i <= w; i += 10) { g.beginPath(); g.moveTo(i, 0); g.lineTo(i, h); g.stroke(); g.beginPath(); g.moveTo(0, i); g.lineTo(w, i); g.stroke(); } }, [6, 4]); return t; })(), transparent: true, side: THREE.DoubleSide })), false, false);
  net.rotation.x = -Math.PI / 2; net.position.set(0, 0.12, -0.35);
  // Randsteine, Regen, Abfluss vom Rasen (Pfeile + Dünger)
  const rim = [];
  for (let i = 0; i <= 18; i++) { const a = Math.PI - (i / 18) * Math.PI; const s = add(new THREE.Mesh(new THREE.DodecahedronGeometry(rr(0.07, 0.1), 0), std({ color: [0x9A948C, 0xB0AAA2, 0x857F78][i % 3], flatShading: true })));
    s.position.set(Math.cos(a) * (RX + 0.06), 0.03, 0.5 - Math.sin(a) * (RZ + 0.06)); s.scale.y = 0.6; rim.push(s); }
  const NR = 380, rainBase = [], rainPos = new Float32Array(NR * 6);
  for (let i = 0; i < NR; i++) rainBase.push([rr(-3, 4), rr(-3, 0.5), rr(0, 1), rr(0.9, 1.3)]);
  const rainGeo = new THREE.BufferGeometry(); rainGeo.setAttribute("position", new THREE.BufferAttribute(rainPos, 3));
  const rainL = new THREE.LineSegments(rainGeo, new THREE.LineBasicMaterial({ color: 0xBFD8F0, transparent: true, opacity: 0.6 })); rainL.frustumCulled = false; scene.add(rainL);
  const runArrows = [];
  for (let i = 0; i < 3; i++) { const a = new THREE.Group(); const m = new THREE.MeshBasicMaterial({ color: 0x8A5A2A });
    const sh = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.015, 0.05), m); a.add(sh); const hd = new THREE.Mesh(new THREE.ConeGeometry(0.08, 0.18, 3), m); hd.rotation.z = Math.PI / 2; hd.position.x = -0.32; a.add(hd);
    a.position.set(2.0, 0.03, -0.1 - i * 0.45); scene.add(a); runArrows.push(a); }
  const pellets = [];
  for (let i = 0; i < 30; i++) { const p = add(new THREE.Mesh(new THREE.SphereGeometry(0.018, 6, 5), std({ color: 0x7FB6D9 })), false, false); p.userData = { o: R(), z: rr(-1.0, 0.2) }; pellets.push(p); }
  // Person (nur am Anfang)
  const person = new THREE.Group(); person.position.set(1.7, 0, -1.2); person.rotation.y = -0.9; scene.add(person);
  { const skin = std({ color: 0xE3B48F }), shirt = std({ color: 0x3C7FA8 }), pants = std({ color: 0x2E3440 });
    for (const s of [-1, 1]) { const lg = new THREE.Mesh(new THREE.CapsuleGeometry(0.07, 0.75, 4, 8), pants); lg.position.set(s * 0.1, 0.45, 0); lg.castShadow = true; person.add(lg);
      const ar = new THREE.Mesh(new THREE.CapsuleGeometry(0.05, 0.55, 4, 8), shirt); ar.position.set(s * 0.27, 1.12, 0.02); ar.castShadow = true; person.add(ar); }
    const tor = new THREE.Mesh(new THREE.CapsuleGeometry(0.19, 0.42, 4, 10), shirt); tor.position.y = 1.15; tor.castShadow = true; person.add(tor);
    const hd = new THREE.Mesh(new THREE.SphereGeometry(0.12, 16, 12), skin); hd.position.y = 1.62; person.add(hd);
    const hair = new THREE.Mesh(new THREE.SphereGeometry(0.125, 16, 12, 0, 6.3, 0, 1.4), std({ color: 0x4A3324 })); hair.position.y = 1.64; person.add(hair); }

  // ---------- Beschriftungen (HTML, auf 3D-Punkte projiziert)
  const labelEls = LABELS.map((l) => document.getElementById(l[0]));
  const camera = new THREE.PerspectiveCamera(50, W / H, 0.05, 200);
  const look = new THREE.Vector3(), v3 = new THREE.Vector3();

  function shotAt(t) {
    let i = 0; for (let k = 0; k < SHOTS.length; k++) if (t >= SHOTS[k][0]) i = k;
    const s = SHOTS[i], end = i + 1 < SHOTS.length ? SHOTS[i + 1][0] : DUR, p = ease((t - s[0]) / (end - s[0]));
    if (!s[1]) { const a = 0.5 - p * 0.6, r = 5.0; camera.position.set(Math.sin(a) * r, 2.0 + p * 0.3, Math.cos(a) * r - 0.6); }
    else camera.position.set(s[1][0] + (s[2][0] - s[1][0]) * p, s[1][1] + (s[2][1] - s[1][1]) * p, s[1][2] + (s[2][2] - s[1][2]) * p);
    look.set(s[3][0], s[3][1], s[3][2]); camera.fov = s[4]; camera.updateProjectionMatrix(); camera.lookAt(look);
  }
  const E = (t, t0, d) => ease((t - t0) / (d || 0.6));
  const greenC = new THREE.Color(0x4E8A2E), clearC = new THREE.Color(0x3E8EDB), brownC = new THREE.Color(0x6A5A3A);

  function render(t) {
    shotAt(t);
    deepK = E(t, K.deep_w - 0.2, 1.0); edgeK = E(t, K.edge - 0.1, 0.6);
    const digK = E(t, K.dig_w - 0.1, 0.8);
    const lin = E(t, K.liner - 0.1, 0.5), sandK = E(t, K.sand - 0.2, 0.5), fl = E(t, K.fleece, 0.4);
    const fillK = E(t, K.liner + 0.5, 1.0), leak = E(t, K.hole - 0.5, 0.5) * (1 - E(t, K.sand, 0.5));
    const pondOn = t >= K.dig - 0.2;
    // Profilgeometrien neu aufbauen
    const top = (x) => edgeY(x);
    const holeOn = pondOn && digK > 0.01;
    holeM.visible = holeOn; if (holeOn) setG(holeM, band((x) => 0.0, (x) => -D(x) * digK - 0.0001 - (sandK > 0 ? 0.07 * sandK : 0)));
    sandM.visible = sandK > 0.01; if (sandM.visible) setG(sandM, band((x) => -D(x) - 0.03, (x) => -D(x) - 0.03 - 0.045 * sandK));
    fleeceM.visible = fl > 0.01; if (fleeceM.visible) setG(fleeceM, band((x) => -D(x) - 0.02, (x) => -D(x) - 0.03));
    linerM.visible = lin > 0.01; if (linerM.visible) setG(linerM, band((x) => Math.max(-D(x), top(x) - 0.0001) * 1 + 0.0, (x) => -D(x) - 0.02 * lin + (Math.abs(x) > XE - 0.005 ? 0 : 0)));
    const subOn = t >= K.soil - 0.3 || (t >= K.deep_w + 0.6);
    const isGravel = t >= K.gravel - 0.1, subK = E(t, K.deep_w + 0.6, 0.6);
    subM.visible = subOn && subK > 0.01 && deepK > 0.9; subM.material = isGravel ? gravelSubMat : soilSubMat;
    if (subM.visible) setG(subM, band((x) => (Math.abs(x) > 0.74 && Math.abs(x) < 1.03 ? -D(x) + 0.08 * subK : -D(x)), (x) => -D(x)));
    holeMat.color.set(0x1A110B).lerp(new THREE.Color(0x2A6FAF), fillK);
    const wl = -0.05 + 0.0;
    waterM.visible = fillK > 0.01; if (waterM.visible) setG(waterM, band((x) => Math.max(wl - (1 - fillK) * 0.6, -D(x)), (x) => -D(x) + 0.0001));
    // Wasserfarbe: klar → grün → klar
    const greenK = Math.max(E(t, K.green_w - 0.8, 1.2) * (1 - E(t, K.eighty, 1.5)) , E(t, K.soil_w - 0.2, 0.8) * (1 - E(t, K.gravel + 0.3, 1.5)) * 0.8, E(t, K.leaves_w - 0.2, 0.8) * (1 - E(t, K.net + 0.3, 1.2)) * 0.5);
    const runK = E(t, K.fert - 0.2, 0.8) * (1 - E(t, K.edge + 0.3, 1.2));
    const col = clearC.clone().lerp(greenC, Math.max(greenK, runK * 0.7));
    waterMat.color.copy(col); waterMat.opacity = 0.55 + 0.35 * Math.max(greenK, runK * 0.7);
    surfMat.color.copy(col); surfMat.opacity = 0.75 + 0.2 * greenK;
    surf.visible = fillK > 0.6 && pondOn; surf.position.y = -0.05; pondBot.visible = pondOn && digK > 0.5; pondBot.position.y = -0.3 - 0.4 * deepK;
    blobs.forEach((b) => { const v = Math.max(greenK, runK * 0.7) > b.userData.o * 0.8 + 0.1; b.visible = surf.visible && v; b.position.y = -0.045; });
    // Leck: Stein unter der Folie, Wasser tropft raus
    const stoneOn = t >= K.stone - 0.2 && t < K.green; stone.visible = stoneOn; stone.position.set(0.3, -D(0.3) - 0.03 - 0.045 * sandK + 0.03 * (1 - sandK), 0.51);
    if (leak > 0.01) { waterMat.opacity *= 1; }
    // Pflanzen: Seerosen & Ufer ab "plants"
    const pk = E(t, K.plants_w - 0.2, 1.0);
    pads.forEach((g) => { const v = clamp(pk * 1.4 - g.userData.o * 0.4, 0, 1); g.visible = v > 0.02 && surf.visible; g.scale.setScalar(Math.max(0.01, v)); g.position.y = -0.04; });
    reeds.forEach((g) => { const v = clamp(pk * 1.4 - g.userData.o * 0.4, 0, 1); g.visible = v > 0.02; g.scale.setScalar(Math.max(0.01, v)); g.position.y = -0.05; });
    // Randsteine (erhöhter Rand)
    rim.forEach((s, i) => { s.visible = edgeK > 0.01; s.position.y = 0.03 + (1 - edgeK) * 0.5 + (i % 2) * 0.005; });
    // Regen + Abfluss
    const raining = t >= K.rain - 0.2 && t < K.leaves; rainL.visible = raining;
    if (raining) { for (let i = 0; i < NR; i++) { const [x, z, o, sp] = rainBase[i], y = 4 - (((t) * 9 * sp + o * 5) % 5);
      rainPos.set([x, y, z, x - 0.03, y - 0.28, z], i * 6); } rainGeo.attributes.position.needsUpdate = true; }
    runArrows.forEach((a, i) => { a.visible = t >= K.fert - 0.3 && t < K.leaves; const blocked = t >= K.edge + 0.2;
      const ph = ((t - K.fert) * 0.7 + i * 0.33) % 1; a.position.x = blocked ? 1.7 + Math.sin(ph * Math.PI) * 0.05 : 2.4 - ph * 1.0; a.children.forEach((c) => c.material.color.set(blocked ? 0xFFD23F : 0x8A5A2A)); a.rotation.y = blocked ? Math.PI : 0; });
    pellets.forEach((p) => { const u = p.userData, ph = ((t - K.fert) * 0.6 + u.o) % 1; p.visible = t >= K.fert - 0.2 && t < K.edge + 0.3;
      p.position.set(2.4 - ph * 1.6, ph < 0.62 ? 0.02 : -0.04 - (ph - 0.62) * 0.4, u.z); });
    // Laub + Netz
    const lk = E(t, K.leaves_w - 0.6, 1.0), nk = E(t, K.net - 0.1, 0.6);
    leaves.forEach((l) => { const u = l.userData, fall = E(t, K.leaves_w - 0.6 + u.o * 0.8, 0.8); l.visible = t >= K.leaves - 0.2 && t < K.end + 0.5;
      const onNet = nk > 0.5 && u.o > 0.25; l.rotation.set(-Math.PI / 2 + Math.sin(u.o * 9) * 0.3, 0, u.o * 6);
      l.position.set(u.x, onNet ? 0.125 : (1.2 - 1.24 * fall) + (fall >= 1 && !onNet ? -Math.min(0.5, (t - K.leaves_w) * 0.15) : 0), u.z); });
    net.visible = nk > 0.01; net.position.y = 0.12 + (1 - nk) * 0.8;
    person.visible = t < K.dig; sunBall.visible = false;
    sun.color.set(0xFFF1D8).lerp(new THREE.Color(0xFFC98A), E(t, K.green - 0.2, 0.6) * (1 - E(t, K.deep, 0.8)));

    renderer.render(scene, camera);

    LABELS.forEach((l, i) => { const el = labelEls[i]; v3.set(l[3], l[4], l[5]).project(camera);
      const on = t >= l[6] && t < l[7] && v3.z < 1;
      el.style.display = on ? "block" : "none";
      if (on) { el.style.left = clamp((v3.x + 1) / 2 * W, 330, W - 330) + "px"; let ty = clamp((1 - v3.y) / 2 * H, 200, H - 200); if (Math.abs(ty - 940) < 130) ty = ty < 940 ? 790 : 1090; el.style.top = ty + "px"; } });
  }

  const st = { t: 0 };
  const tl = gsap.timeline({ paused: true });
  tl.to(st, { t: DUR, duration: DUR, ease: "none", onUpdate: () => render(st.t) }, 0);
  LABELS.forEach((l) => tl.fromTo("#" + l[0] + " span", { scale: 1.6, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.25, ease: "back.out(2)" }, l[6]));
  window.__timelines["world"] = tl;
  render(0);
}).catch((e) => { console.error("world build failed", e); throw e; });
"""

LABEL_STYLE = {
    "w": "color:#FFFFFF", "o": "color:#FF9F43", "r": "color:#FF4D4D", "y": "color:#FFD23F",
    "g": "color:#7CE07C", "b": "color:#6FC3FF",
}


def world_html():
    k = dict(K)
    js = (WORLD_JS.replace("__K__", json.dumps(k)).replace("__SHOTS__", json.dumps(SHOTS))
          .replace("__LABELS__", json.dumps([list(l) for l in LABELS])).replace("__DUR__", str(TOTAL)))
    labels = "".join(f'<div id="{l[0]}" class="lab"><span style="{LABEL_STYLE[l[2]]}">{l[1]}</span></div>' for l in LABELS)
    return f"""<template>
  <style>
    #root {{ position:absolute; inset:0; background:#8DB9EA; }}
    #w-canvas {{ position:absolute; left:0; top:0; width:{W}px; height:{H}px; }}
    .lab {{ position:absolute; display:none; transform:translate(-50%,-50%); white-space:nowrap; }}
    .lab span {{ display:inline-block; font-family:'Inter',sans-serif; font-weight:900; font-size:52px; letter-spacing:0.01em;
      -webkit-text-stroke:10px #1A1208; paint-order:stroke fill; text-shadow:0 4px 10px rgba(0,0,0,0.35); }}
  </style>
  <div id="root" data-composition-id="world" data-width="{W}" data-height="{H}" data-duration="{fmt(TOTAL)}" data-layout-allow-overlap>
    <canvas id="w-canvas" width="{W}" height="{H}"></canvas>
    {labels}
  </div>
  <script>
{js}
  </script>
</template>
"""


HL = {"y": "#FFD23F", "r": "#FF4D4D", "g": "#7CE07C"}


def captions_html():
    """Ein Wort pro Untertitel, mittig – wie im Referenzvideo. Markierte Wörter farbig."""
    items = []
    for b in T["beats"]:
        for l in b["lines"]:
            cols = []
            for m in re.finditer(r"\{(\w):([^}]*)\}|([^{}\s]+)", l["show"]):
                cols += [None] * len(m.group(3).split()) if m.group(3) else [HL[m.group(1)]] * len(m.group(2).split())
            for w, c in zip(l["words"], cols):
                items.append((w["text"], w["start"], w["end"], c))
    groups, js = [], []
    for i, (txt, s, e, c) in enumerate(items):
        nxt = items[i + 1][1] if i + 1 < len(items) else TOTAL
        end = min(nxt - 0.04, e + 0.5)
        st = max(0.05, s - 0.02)
        gid = f"wd{i}"
        groups.append(f'<div id="{gid}" class="clip wd" data-start="{fmt(st)}" data-duration="{fmt(max(0.08, end - st))}" data-track-index="1">'
                      f'<span style="color:{c or "#FFFFFF"}">{txt}</span></div>')
        js.append(f'    tl.fromTo("#{gid} span", {{scale:1.18}}, {{scale:1, duration:0.09, ease:"power2.out"}}, {fmt(st)});')
    return f"""<template>
  <style>
    #root {{ position:absolute; inset:0; }}
    .wd {{ position:absolute; left:40px; right:40px; top:880px; text-align:center; overflow:visible; }}
    .wd span {{ display:inline-block; font-family:'Inter',sans-serif; font-weight:900; font-size:92px; line-height:1;
      -webkit-text-stroke:16px #000; paint-order:stroke fill; text-shadow:0 6px 0 #000; }}
  </style>
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


SFX = []
for s in SHOTS[1:]:
    SFX.append((s[0] - 0.12, "whoosh-short.mp3", 0.35))
for key, f, v in [("hole", "error.mp3", 0.35), ("green_w", "error.mp3", 0.3), ("soil_w", "error.mp3", 0.3), ("fert", "error.mp3", 0.3),
                  ("leaves_w", "error.mp3", 0.3), ("dig_w", "impact-bass-2.mp3", 0.3), ("liner", "pop.mp3", 0.35), ("sand", "pop.mp3", 0.4),
                  ("deep_w", "impact-bass-2.mp3", 0.3), ("gravel", "pop.mp3", 0.4), ("plants_w", "pop.mp3", 0.4), ("edge", "click.mp3", 0.4),
                  ("net", "pop.mp3", 0.4), ("crystal", "sparkle.mp3", 0.4), ("congrats", "sparkle.mp3", 0.5)]:
    SFX.append((K[key], f, v))


def write():
    comp = HERE / "compositions"
    comp.mkdir(exist_ok=True)
    (comp / "world.html").write_text(world_html())
    (comp / "captions.html").write_text(captions_html())
    (HERE / "assets" / "sfx").mkdir(parents=True, exist_ok=True)
    # Keine Stimme: der Creator schickt seine Aufnahme; dann tools/align.py und hier die voice.wav-Zeile wieder einsetzen
    audio = []
    if (HERE / "assets" / "voice.wav").exists():
        audio.append('      <audio id="voice" class="clip" src="assets/voice.wav" data-start="0" data-track-index="10" data-volume="1"></audio>')
    for j, (t, f, vol) in enumerate(SFX):
        (HERE / "assets" / "sfx" / f).write_bytes((SFX_ROOT / f).read_bytes())
        d = min(audio_len(SFX_ROOT / f), TOTAL - t)
        audio.append(f'      <audio id="sfx{j}" class="clip" src="assets/sfx/{f}" data-start="{fmt(t)}" data-duration="{fmt(d)}" '
                     f'data-track-index="{11 + j}" data-volume="{vol}"></audio>')
    hosts = ""
    for z, (cid, kind) in enumerate((("world", "graphics"), ("captions", "captions"))):
        hosts += (f'      <div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" data-start="0" '
                  f'data-duration="{fmt(TOTAL)}" data-track-index="{z + 1}" data-track-kind="{kind}" data-width="{W}" data-height="{H}" '
                  f'style="z-index:{z + 1}"></div>\n')
    (HERE / "index.html").write_text(f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <title>{TITLE}</title>
    <script src="assets/gsap.min.js"></script>
    <style>
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:#8DB9EA; }}
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
    print("total", TOTAL)


if __name__ == "__main__":
    write()
