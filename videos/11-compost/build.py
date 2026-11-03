#!/usr/bin/env python3
"""Builds "How to start a compost pile that doesn't stink" (English) – same structure as videos/07–10:
one growing world (compost bin cut open at the front, ground cut open below), a chain of problem → fix (red problem words,
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
TITLE = "How to start a compost pile that doesn't stink"

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
    "fert": word("want", "fertilizer"), "scraps": word("pile", "scraps"), "two_weeks": word("pile", "Two"), "stinks": word("pile", "stinks"),
    "greens": word("browns", "greens"), "browns_w": word("browns", "browns"), "leaves": word("browns", "leaves"), "ratio": word("browns", "two"),
    "green_end": word("browns", "green", 2),
    "rats_w": word("rats", "rats"), "meat": word("rats", "meat"),
    "soggy": word("turn", "soggy"), "turn_w": word("turn", "turn"),
    "dries": word("dry", "dries"), "stops": word("dry", "stops"), "damp": word("dry", "damp"), "sponge": word("dry", "sponge"),
    "soil_w": word("soil", "soil"), "worms": word("soil", "worms"),
    "dark": word("done", "dark"), "crumbly": word("done", "crumbly"),
    "congrats": word("end", "Congratulations"), "free_end": word("end", "free"),
})
# (Start, Kamera von, Kamera nach, Ziel, FOV); None = Kamerafahrt
SHOTS = [
    (K["want"], (3.8, 2.0, 5.6), (3.2, 1.7, 4.9), (0.8, 0.6, -0.6), 50),
    (K["pile"], (1.6, 0.95, 3.0), (1.3, 0.85, 2.6), (0.6, 0.4, 0.0), 50),
    (K["browns"], (0.6, 0.65, 2.7), (0.6, 0.55, 2.35), (0.6, 0.38, 0.0), 50),
    (K["rats"], (2.7, 0.75, 2.9), (2.35, 0.65, 2.55), (1.2, 0.3, -0.2), 50),
    (K["turn"], (0.25, 0.75, 2.5), (0.45, 0.62, 2.15), (0.6, 0.38, 0.0), 50),
    (K["dry"], (1.25, 0.95, 2.7), (1.0, 0.82, 2.35), (0.6, 0.4, 0.0), 50),
    (K["soil"], (1.1, 0.35, 3.4), (0.9, 0.25, 3.0), (0.6, 0.05, 0.0), 50),
    (K["done"], (0.6, 0.55, 2.3), (0.6, 0.48, 1.95), (0.6, 0.3, 0.0), 50),
    (K["end"], None, None, (1.3, 0.4, -0.4), 50),
]

# Schwebende 3D-Wörter: rot = Problem, gelb = Lösung
LABELS = [
    ("l-fert", "FREE FERTILIZER?", "g", 0.6, 1.4, 0.0, K["fert"], K["pile"]),
    ("l-scraps", "KITCHEN SCRAPS", "y", 0.6, 0.55, 0.5, K["scraps"], K["stinks"]),
    ("l-stink", "STINKS!", "r", 0.6, 0.95, 0.0, K["stinks"] - 0.2, K["browns"]),
    ("l-greens", "TOO MUCH GREEN!", "r", 0.6, 0.6, 0.5, K["greens"] - 0.2, K["browns_w"]),
    ("l-browns", "LEAVES · CARDBOARD · STRAW", "y", 0.6, 0.98, 0.3, K["browns_w"], K["ratio"]),
    ("l-ratio", "2 BROWN : 1 GREEN", "y", 0.6, 0.98, 0.3, K["ratio"], K["rats"]),
    ("l-rats", "RATS!", "r", 1.7, 0.35, 0.0, K["rats_w"] - 0.2, K["meat"]),
    ("l-meat", "NO MEAT · DAIRY · OIL", "y", 1.2, 0.75, 0.0, K["meat"], K["turn"]),
    ("l-soggy", "NO AIR!", "r", 0.6, 0.62, 0.5, K["soggy"] - 0.2, K["turn_w"]),
    ("l-turn", "TURN WEEKLY", "y", 0.6, 1.05, 0.3, K["turn_w"], K["dry"]),
    ("l-dry", "TOO DRY!", "r", 0.6, 1.0, 0.3, K["dries"], K["sponge"]),
    ("l-sponge", "DAMP LIKE A SPONGE", "b", 0.6, 1.0, 0.3, K["sponge"] - 0.3, K["soil"]),
    ("l-soil", "BARE SOIL", "y", 0.6, -0.08, 0.5, K["soil_w"], K["worms"]),
    ("l-worms", "WORMS MOVE IN", "g", 0.6, -0.35, 0.5, K["worms"], K["done"]),
    ("l-done", "DARK & CRUMBLY", "g", 0.6, 0.85, 0.3, K["crumbly"] - 0.3, K["end"]),
    ("l-congrats", "CONGRATULATIONS!", "y", 1.3, 1.9, -0.4, K["congrats"], TOTAL),
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

  // ---------- Garten mit Querschnitt (Schnittkante bei z = 0.5)
  const PX0 = -1.5;
  const groundTop = std({ map: grassT });
  const groundBlock = (x0, x1, y0, y1, z0, z1, frontMap) => { const m = [groundTop, groundTop, groundTop, groundTop, std({ map: frontMap }), groundTop];
    const b = add(new THREE.Mesh(new THREE.BoxGeometry(x1 - x0, y1 - y0, z1 - z0), m), false, true); b.position.set((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2); return b; };
  const cutRep = (w) => { const t = cutT.clone(); t.needsUpdate = true; t.repeat.set(w / 4, 1); return t; };
  groundBlock(-30, 30, -3.4, 0, -19.5, 0.5, cutRep(60));
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

  // ---------- Haus links (Wand bei x = -1.5), Terrassentür
  const wallM = std({ color: 0xF2EFEA }), winM = std({ color: 0x2C3440, roughness: 0.3 });
  boxAt(-7.5, PX0, 0, 3.2, -7, 0.5, wallM);
  boxAt(-7.5, PX0, -1.0, 0, -7, 0.503, [std({ map: concT }), std({ map: concT }), std({ map: concT }), std({ map: concT }), std({ map: secT }), std({ map: concT })]);
  { const d = add(new THREE.Mesh(new THREE.BoxGeometry(0.06, 2.1, 1.4), winM), false, false); d.position.set(PX0 + 0.02, 1.08, -1.4);
    const w2 = add(new THREE.Mesh(new THREE.BoxGeometry(0.06, 1.0, 0.9), winM), false, false); w2.position.set(PX0 + 0.02, 1.7, -4.2);
    const s = new THREE.Shape(); s.moveTo(-4.4, 0); s.lineTo(4.4, 0); s.lineTo(0, 2.4); s.lineTo(-4.4, 0);
    const rg = new THREE.ExtrudeGeometry(s, { depth: 8.0, bevelEnabled: false }); rg.translate(0, 0, -7.25);
    const roof = add(new THREE.Mesh(rg, std({ map: roofT }))); roof.position.set(-4.5, 3.2, 0); }



  // ---------- Komposter (innen x 0.1..1.1, z -0.5..0.5; Front = Schnittkante)
  const scrapT = tex(256, 128, 61, (g, r, w, h) => { g.fillStyle = "#3E4A22"; g.fillRect(0, 0, w, h);
    speck(g, r, w, h, 700, ["#6FA444", "#9BC75A", "#4E7F2E", "#E2B23A", "#D9772E", "#B9452E", "#C9C08A", "#7A9A3A"], 3, 8); }, [2, 1]);
  const brownT = tex(256, 128, 62, (g, r, w, h) => { g.fillStyle = "#8A5A2A"; g.fillRect(0, 0, w, h);
    speck(g, r, w, h, 700, ["#C0732A", "#A65A1F", "#D9A13A", "#8D6E2B", "#B4472A", "#E3C27A"], 3, 9);
    for (let i = 0; i < 40; i++) { g.fillStyle = "#B99569"; g.fillRect(r() * w, r() * h, 10 + r() * 16, 3); } }, [2, 1]);
  const mixT = tex(256, 128, 63, (g, r, w, h) => { g.fillStyle = "#5A4128"; g.fillRect(0, 0, w, h);
    speck(g, r, w, h, 900, ["#7A5A32", "#4A3322", "#8D6E2B", "#6B4C33", "#9C7A3C", "#55602C"], 2, 6); }, [2, 1]);
  const BX0 = 0.1, BX1 = 1.1, BZ0 = -0.5, BZ1 = 0.5;
  const bin = new THREE.Group(); scene.add(bin);
  const wood2 = std({ map: woodT, roughness: 0.8 });
  for (let i = 0; i < 6; i++) { const y = 0.08 + i * 0.165;
    for (const [w, d, x, z] of [[1.08, 0.03, 0.6, BZ0 - 0.02], [0.03, 1.02, BX0 - 0.02, 0.0], [0.03, 1.02, BX1 + 0.02, 0.0]]) {
      const b = new THREE.Mesh(new THREE.BoxGeometry(w, 0.13, d), wood2); b.position.set(x, y, z); b.castShadow = b.receiveShadow = true; bin.add(b); } }
  for (const [x, z] of [[BX0 - 0.03, BZ0 - 0.03], [BX1 + 0.03, BZ0 - 0.03], [BX0 - 0.03, BZ1 - 0.02], [BX1 + 0.03, BZ1 - 0.02]]) {
    const p = new THREE.Mesh(new THREE.BoxGeometry(0.05, 1.05, 0.05), wood2); p.position.set(x, 0.52, z); p.castShadow = true; bin.add(p); }
  const slab = boxAt(-0.05, 1.25, -0.06, 0.0, -0.65, 0.5, std({ color: 0x9A9894, roughness: 0.8 }));
  const layerBox = (mat) => { const m = new THREE.Mesh(new THREE.BoxGeometry(BX1 - BX0, 1, BZ1 + 0.004 - BZ0), mat); m.castShadow = false; m.receiveShadow = true; bin.add(m); return m; };
  const setL = (m, y0, y1) => { const ok = y1 - y0 > 0.003; m.visible = ok; if (ok) { m.scale.y = y1 - y0; m.position.set((BX0 + BX1) / 2, (y0 + y1) / 2, (BZ0 + BZ1 + 0.004) / 2); } };
  const gM = std({ map: scrapT, roughness: 0.6 }), bM = std({ map: brownT });
  const stackA = [0, 1, 2].map(() => layerBox(gM));
  const B_LAY = [["b", 0, 0.14], ["g", 0.14, 0.21], ["b", 0.21, 0.35], ["g", 0.35, 0.42], ["b", 0.42, 0.56], ["g", 0.56, 0.63], ["b", 0.63, 0.77]];
  const stackB = B_LAY.map(([k]) => layerBox(k === "g" ? gM : bM));
  const mixM = new THREE.MeshStandardMaterial({ map: mixT, roughness: 0.95, transparent: true, opacity: 0 });
  const mixBox = layerBox(mixM);
  const compM = new THREE.MeshStandardMaterial({ map: compT, roughness: 1, transparent: true, opacity: 0 });
  const compBox = layerBox(compM);
  const soggy = add(new THREE.Mesh(new THREE.CircleGeometry(1, 32), new THREE.MeshBasicMaterial({ color: 0x1A1A12, transparent: true, opacity: 0 })), false, false);
  soggy.scale.set(0.3, 0.16, 1); soggy.position.set(0.6, 0.36, 0.508);
  // Gestank (grüne Wellenlinien), Luft, Mistgabel
  const stinks = [];
  for (let i = 0; i < 6; i++) { const pts = []; for (let k = 0; k < 12; k++) pts.push(new THREE.Vector3(0, k * 0.05, 0));
    const g = new THREE.BufferGeometry().setFromPoints(pts); const l = new THREE.Line(g, new THREE.LineBasicMaterial({ color: 0x8BC34A, transparent: true, opacity: 0.9 }));
    l.userData = { x: 0.25 + i * 0.14, o: R() }; l.frustumCulled = false; scene.add(l); stinks.push(l); }
  const fork = new THREE.Group(); scene.add(fork);
  { const h = new THREE.Mesh(new THREE.CylinderGeometry(0.016, 0.016, 1.2, 8), std({ map: woodT })); h.position.y = 0.75; fork.add(h);
    for (let i = -1.5; i <= 1.5; i++) { const t = new THREE.Mesh(new THREE.CylinderGeometry(0.006, 0.004, 0.3, 6), std({ color: 0x9AA0A6, metalness: 0.7, roughness: 0.3 })); t.position.set(i * 0.04, 0.0, 0); fork.add(t); }
    const bar = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.02, 0.02), std({ color: 0x9AA0A6, metalness: 0.7 })); bar.position.y = 0.15; fork.add(bar); }
  const puffs = [];
  for (let i = 0; i < 16; i++) { const p = add(new THREE.Mesh(new THREE.SphereGeometry(rr(0.025, 0.045), 10, 8), new THREE.MeshBasicMaterial({ color: 0xFFFFFF, transparent: true, opacity: 0.6, depthWrite: false })), false, false);
    p.userData = { o: R(), x: rr(0.2, 1.0) }; puffs.push(p); }
  // Gießwasser, Risse, Wassertropfen im nassen Kern
  const drops = [];
  for (let i = 0; i < 30; i++) { const d = add(new THREE.Mesh(new THREE.SphereGeometry(0.016, 8, 6), new THREE.MeshStandardMaterial({ color: 0x5AA8F0, roughness: 0.1 })), false, false);
    d.userData = { o: R(), x: rr(0.2, 1.0), z: rr(-0.4, 0.45) }; drops.push(d); }
  const crackT = (() => { const c = document.createElement("canvas"); c.width = 256; c.height = 128; const g = c.getContext("2d"); const r = mulberry(64);
    g.strokeStyle = "rgba(40,25,10,0.9)"; g.lineWidth = 2; for (let i = 0; i < 14; i++) { let x = r() * 256, y = r() * 128; g.beginPath(); g.moveTo(x, y);
      for (let k = 0; k < 6; k++) { x += (r() - 0.5) * 40; y += (r() - 0.5) * 30; g.lineTo(x, y); } g.stroke(); }
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; })();
  const cracks = add(new THREE.Mesh(new THREE.PlaneGeometry(BX1 - BX0, 0.7), new THREE.MeshBasicMaterial({ map: crackT, transparent: true, opacity: 0, depthWrite: false })), false, false);
  cracks.position.set(0.6, 0.38, 0.509);
  // Würmer im Boden-Schnitt
  const worms = [];
  for (let i = 0; i < 7; i++) { const w = add(new THREE.Mesh(new THREE.CapsuleGeometry(0.012, 0.09, 4, 8), std({ color: 0xD98C8C, roughness: 0.5 })), false, false);
    w.userData = { o: R(), x: rr(0.2, 1.0) }; worms.push(w); }
  // Ratte
  const rat = new THREE.Group(); scene.add(rat);
  { const c = 0x6E6862; const body = new THREE.Mesh(new THREE.SphereGeometry(0.07, 16, 12), std({ color: c })); body.scale.set(1.7, 0.85, 0.9); body.position.y = 0.06; body.castShadow = true; rat.add(body);
    const head = new THREE.Mesh(new THREE.ConeGeometry(0.04, 0.1, 12), std({ color: c })); head.rotation.z = -Math.PI / 2; head.position.set(0.15, 0.07, 0); rat.add(head);
    for (const s of [-1, 1]) { const ear = new THREE.Mesh(new THREE.SphereGeometry(0.018, 8, 6), std({ color: 0xD9A09A })); ear.position.set(0.11, 0.11, s * 0.03); rat.add(ear); }
    const tail = new THREE.Mesh(new THREE.CylinderGeometry(0.006, 0.003, 0.22, 6), std({ color: 0xD9A09A })); tail.rotation.z = 1.35; tail.position.set(-0.2, 0.04, 0); rat.add(tail); }
  // Beet daneben, Pflanzen wachsen am Ende
  const bed = boxAt(2.0, 3.1, 0.0, 0.18, -1.0, 0.2, [std({ map: woodT }), std({ map: woodT }), std({ map: soilT }), std({ map: woodT }), std({ map: woodT }), std({ map: woodT })]);
  const plants = [];
  for (let i = 0; i < 6; i++) { const g = new THREE.Group(); g.position.set(2.2 + (i % 3) * 0.35, 0.18, -0.65 + Math.floor(i / 3) * 0.55); scene.add(g);
    for (let k = 0; k < 5; k++) { const b = new THREE.Mesh(new THREE.IcosahedronGeometry(rr(0.07, 0.11), 0), std({ color: [0x4F8A35, 0x5C9A3A][k % 2], flatShading: true })); b.position.set(rr(-0.06, 0.06), 0.06 + k * 0.05, rr(-0.06, 0.06)); b.castShadow = true; g.add(b); }
    if (i % 2 === 0) { const f = new THREE.Mesh(new THREE.SphereGeometry(0.04, 12, 10), std({ color: 0xD2302A, roughness: 0.4 })); f.position.set(0.07, 0.15, 0.04); g.add(f); }
    plants.push(g); }
  // Person mit Eimer (nur am Anfang)
  const person = new THREE.Group(); person.position.set(1.55, 0, -0.2); person.rotation.y = -1.2; scene.add(person);
  { const skin = std({ color: 0xE3B48F }), shirt = std({ color: 0x3C7FA8 }), pants = std({ color: 0x2E3440 });
    for (const s of [-1, 1]) { const lg = new THREE.Mesh(new THREE.CapsuleGeometry(0.07, 0.75, 4, 8), pants); lg.position.set(s * 0.1, 0.45, 0); lg.castShadow = true; person.add(lg);
      const ar = new THREE.Mesh(new THREE.CapsuleGeometry(0.05, 0.55, 4, 8), shirt); ar.position.set(s * 0.27, 1.12, 0.02); ar.castShadow = true; person.add(ar); }
    const tor = new THREE.Mesh(new THREE.CapsuleGeometry(0.19, 0.42, 4, 10), shirt); tor.position.y = 1.15; tor.castShadow = true; person.add(tor);
    const hd = new THREE.Mesh(new THREE.SphereGeometry(0.12, 16, 12), skin); hd.position.y = 1.62; person.add(hd);
    const hair = new THREE.Mesh(new THREE.SphereGeometry(0.125, 16, 12, 0, 6.3, 0, 1.4), std({ color: 0x4A3324 })); hair.position.y = 1.64; person.add(hair);
    const bucket = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.08, 0.2, 14), std({ color: 0x3E8E4A, roughness: 0.5 })); bucket.position.set(0.3, 0.72, 0.05); bucket.castShadow = true; person.add(bucket); }

  // ---------- Beschriftungen (HTML, auf 3D-Punkte projiziert)
  const labelEls = LABELS.map((l) => document.getElementById(l[0]));
  const camera = new THREE.PerspectiveCamera(50, W / H, 0.05, 200);
  const look = new THREE.Vector3(), v3 = new THREE.Vector3();

  function shotAt(t) {
    let i = 0; for (let k = 0; k < SHOTS.length; k++) if (t >= SHOTS[k][0]) i = k;
    const s = SHOTS[i], end = i + 1 < SHOTS.length ? SHOTS[i + 1][0] : DUR, p = ease((t - s[0]) / (end - s[0]));
    if (!s[1]) { const a = 0.45 - p * 0.55, r = 5.0; camera.position.set(Math.sin(a) * r + 1.3, 1.9 + p * 0.3, Math.cos(a) * r - 0.4); }
    else camera.position.set(s[1][0] + (s[2][0] - s[1][0]) * p, s[1][1] + (s[2][1] - s[1][1]) * p, s[1][2] + (s[2][2] - s[1][2]) * p);
    look.set(s[3][0], s[3][1], s[3][2]); camera.fov = s[4]; camera.updateProjectionMatrix(); camera.lookAt(look);
  }
  const E = (t, t0, d) => ease((t - t0) / (d || 0.6));

  function render(t) {
    shotAt(t);
    // Kompost steht erst auf einer Platte, ab "soil" auf nacktem Boden
    const soilK = E(t, K.soil_w - 0.1, 0.6); slab.visible = soilK < 0.99; slab.position.y = -0.03 - soilK * 0.4; bin.position.y = 0.0;
    // Stapel A: nur Küchenabfälle (3 Lagen) bis "browns"
    const ta = [K.scraps - 0.1, K.scraps + 0.45, K.two_weeks - 0.1], goneA = E(t, K.browns_w - 0.1, 0.35);
    stackA.forEach((m, i) => { const k = E(t, ta[i], 0.35); setL(m, i * 0.12 * (1 - goneA), (i * 0.12 + 0.12 * k) * (1 - goneA)); if (t < ta[i] || goneA > 0.99) m.visible = false; });
    // Stapel B: Braun/Grün im Verhältnis 2:1
    const span = K.green_end + 0.3 - K.browns_w;
    stackB.forEach((m, i) => { const [k0, y0, y1] = B_LAY[i], tt = K.browns_w + span * i / B_LAY.length, k = E(t, tt, 0.3);
      setL(m, y0, y0 + (y1 - y0) * k); if (t < tt) m.visible = false; });
    // Umsetzen → gemischt; trocken → hell + Risse; feucht → wieder dunkel; fertig → Kompost (sackt zusammen)
    const mixK = E(t, K.turn_w, 1.0), dryK = E(t, K.dries - 0.2, 0.8) * (1 - E(t, K.sponge - 0.3, 1.0)), doneK = E(t, K.dark - 0.3, 1.4);
    const topY = 0.77 - 0.22 * doneK;
    mixM.opacity = mixK; setL(mixBox, 0, topY); mixBox.visible = mixK > 0.01; mixM.color.set(0xFFFFFF).lerp(new THREE.Color(0xF0D8A8), dryK * 0.8);
    compM.opacity = doneK; setL(compBox, 0, topY + 0.002); compBox.visible = doneK > 0.01;
    stackB.forEach((m) => { if (mixK > 0.99) m.visible = false; });
    cracks.material.opacity = dryK; cracks.visible = dryK > 0.01;
    const sogK = E(t, K.soggy - 0.3, 0.6) * (1 - E(t, K.turn_w + 0.3, 0.8));
    soggy.material.opacity = 0.75 * sogK; soggy.visible = sogK > 0.01;
    // Gestank
    const stK = E(t, K.stinks - 0.3, 0.5) * (1 - E(t, K.browns_w + 0.6, 0.8)), sogStink = sogK * 0.7, sv = Math.max(stK, sogStink);
    const pileTop = t < K.browns_w ? 0.36 : 0.77;
    stinks.forEach((l) => { l.visible = sv > 0.02; if (!l.visible) return; const u = l.userData, pos = l.geometry.attributes.position, ph = ((t * 0.5 + u.o) % 1);
      for (let k = 0; k < 12; k++) pos.setXYZ(k, u.x + Math.sin(k * 0.9 + t * 4 + u.o * 6) * 0.03, pileTop + 0.05 + ph * 0.25 + k * 0.035, 0.1);
      pos.needsUpdate = true; l.material.opacity = sv * Math.sin(Math.PI * ph); });
    // Mistgabel + Luft beim Umsetzen
    const fOn = t >= K.turn_w - 0.2 && t < K.dry; fork.visible = fOn;
    if (fOn) { const ph = (t - K.turn_w) * 1.3; fork.position.set(0.35 + (Math.floor(ph) % 3) * 0.25, 0.55 - Math.abs(Math.sin(ph * Math.PI)) * 0.3, 0.15); fork.rotation.z = 0.3 + Math.sin(ph * Math.PI) * 0.4; }
    puffs.forEach((p) => { const u = p.userData, ph = ((t - K.turn_w) * 0.6 + u.o) % 1; p.visible = t >= K.turn_w && t < K.dry;
      p.position.set(u.x, 0.95 - ph * 0.6, 0.45); p.material.opacity = 0.6 * Math.sin(Math.PI * ph); });
    // Wasser: nasser Kern (Tropfen) bzw. Gießen bei "sponge"
    drops.forEach((d) => { const u = d.userData; d.visible = false;
      if (t >= K.soggy - 0.3 && t < K.turn_w + 0.5) { const ph = ((t - K.soggy) * 0.8 + u.o) % 1; d.visible = true; d.position.set(0.45 + u.x * 0.3, 0.42 - ph * 0.15, 0.51); }
      else if (t >= K.sponge - 0.3 && t < K.soil) { const ph = ((t - K.sponge) * 1.4 + u.o) % 1; d.visible = true; d.position.set(u.x, 1.3 - ph * (1.3 - topY), u.z); } });
    // Würmer kommen von unten herein
    worms.forEach((w) => { const u = w.userData, ph = ((t - K.worms) * 0.35 + u.o) % 1; w.visible = t >= K.worms - 0.2 && t < K.end;
      w.position.set(u.x + Math.sin(t * 3 + u.o * 9) * 0.02, -0.6 + ph * 0.85, 0.512); w.rotation.z = Math.sin(t * 4 + u.o * 7) * 0.5; });
    // Ratte rennt zum Kompost und wieder weg
    const rIn = E(t, K.rats_w - 0.3, 0.7), rOut = E(t, K.meat + 0.2, 0.7);
    rat.visible = t >= K.rats_w - 0.3 && t < K.turn; rat.position.set(2.6 - 1.2 * rIn + 2.0 * rOut, 0, 0.1); rat.rotation.y = rOut > 0.01 ? 0 : Math.PI;
    // Beet wächst am Ende
    const gk = E(t, K.free_end - 0.8, 1.4); plants.forEach((g) => g.scale.setScalar(0.6 + 0.7 * gk));
    person.visible = t < K.pile; sunBall.visible = false;

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
for key, f, v in [("stinks", "error.mp3", 0.35), ("greens", "error.mp3", 0.3), ("rats_w", "error.mp3", 0.3), ("soggy", "error.mp3", 0.3),
                  ("stops", "error.mp3", 0.3), ("scraps", "impact-bass-2.mp3", 0.3), ("browns_w", "pop.mp3", 0.4), ("ratio", "pop.mp3", 0.35),
                  ("meat", "click.mp3", 0.4), ("turn_w", "whoosh.mp3", 0.3), ("sponge", "pop.mp3", 0.4), ("soil_w", "click.mp3", 0.4),
                  ("crumbly", "pop.mp3", 0.4), ("free_end", "sparkle.mp3", 0.4), ("congrats", "sparkle.mp3", 0.5)]:
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
