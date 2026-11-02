#!/usr/bin/env python3
"""Builds "How a French drain keeps water away from your house" (English) – same structure as videos/07–09:
one growing world (drain trench next to the house, ground cut open), a chain of problem → fix (red problem words,
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
TITLE = "How a French drain keeps water away from your house"

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
    "dry_w": word("want", "dry"), "rains": word("flood", "rains"), "wall_w": word("flood", "wall"),
    "trench_w": word("trench", "trench"), "half": word("trench", "half"),
    "gravel_w": word("gravel", "gravel"), "perforated": word("gravel", "perforated"),
    "sits": word("flat", "sits"), "slope_w": word("flat", "slope"), "onecm": word("flat", "one"),
    "down": word("holes", "down"), "rises": word("holes", "rises"),
    "clogs": word("clog", "clogs"), "fabric": word("clog", "fabric"),
    "where": word("outlet", "where"), "neighbor": word("outlet", "neighbor"), "well": word("outlet", "dry"), "far": word("outlet", "far"),
    "congrats": word("end", "Congratulations"), "dry_end": word("end", "dry"),
})
# (Start, Kamera von, Kamera nach, Ziel, FOV); None = Kamerafahrt
SHOTS = [
    (K["want"], (4.6, 2.4, 7.4), (3.8, 2.0, 6.5), (0.4, 0.5, -1.2), 50),
    (K["flood"], (1.4, 1.0, 3.6), (1.1, 0.85, 3.1), (-0.7, -0.25, -0.4), 50),
    (K["trench"], (2.4, 1.3, 5.8), (2.1, 1.1, 5.2), (0.7, -0.2, -0.3), 50),
    (K["gravel"], (-0.1, 0.1, 2.5), (0.05, 0.05, 2.2), (0.0, -0.35, 0.0), 50),
    (K["flat"], (1.3, -0.05, 2.5), (1.1, -0.1, 2.2), (1.0, -0.42, 0.0), 50),
    (K["holes"], (0.55, -0.15, 2.1), (0.45, -0.2, 1.85), (0.3, -0.42, 0.0), 50),
    (K["clog"], (-0.4, 0.0, 2.0), (-0.25, -0.05, 1.7), (-0.25, -0.33, 0.0), 50),
    (K["outlet"], (4.6, 1.3, 6.6), (4.0, 1.0, 5.8), (2.6, -0.25, -0.6), 50),
    (K["end"], None, None, (1.0, 0.1, -0.8), 50),
]

# Schwebende 3D-Wörter: rot = Problem, gelb = Lösung
LABELS = [
    ("l-dry", "DRY YARD?", "g", 0.5, 0.6, -0.5, K["dry_w"], K["flood"]),
    ("l-pool", "WATER AT THE WALL!", "r", -0.9, 0.35, 0.0, K["wall_w"] - 0.4, K["trench"]),
    ("l-trench", "TRENCH", "y", 0.7, 0.15, 0.5, K["trench_w"], K["half"]),
    ("l-depth", "50 CM", "y", 2.0, -0.3, 0.5, K["half"], K["gravel"]),
    ("l-gravel", "WASHED GRAVEL", "y", 0.0, -0.15, 0.5, K["gravel_w"], K["perforated"]),
    ("l-pipe", "PERFORATED PIPE", "y", 0.4, -0.3, 0.5, K["perforated"], K["flat"]),
    ("l-sits", "WATER SITS!", "r", 1.0, -0.3, 0.5, K["sits"] - 0.3, K["slope_w"]),
    ("l-slope", "1 CM PER METER", "y", 1.0, -0.28, 0.5, K["slope_w"], K["holes"]),
    ("l-down", "HOLES DOWN", "y", 0.3, -0.33, 0.5, K["down"], K["clog"]),
    ("l-clog", "CLOGGED!", "r", -0.25, -0.2, 0.5, K["clogs"] - 0.3, K["fabric"]),
    ("l-fabric", "FILTER FABRIC", "y", -0.25, -0.2, 0.5, K["fabric"], K["outlet"]),
    ("l-neighbor", "NOT THE NEIGHBOR ✕", "r", 3.9, 0.7, 0.0, K["neighbor"] - 0.3, K["well"]),
    ("l-well", "DRY WELL", "y", 2.95, -0.45, 0.5, K["well"], K["end"]),
    ("l-congrats", "CONGRATULATIONS!", "y", 0.6, 1.8, -0.8, K["congrats"], TOTAL),
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

  // ---------- Garten mit Querschnitt (Schnittkante bei z = 0.5); Graben verläuft entlang der Schnittkante (x = TX0..TX1)
  const PX0 = -1.5, TX0 = -1.2, TX1 = 2.6, TB = -0.6;
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


  // ---------- Graben im Schnitt (Ebenen direkt vor der Schnittkante)
  const sec = (mat, z) => { const m = add(new THREE.Mesh(new THREE.PlaneGeometry(1, 1), mat), false, false); m.position.z = z; return m; };
  function rect(m, x0, x1, y0, y1) { const ok = x1 - x0 > 0.002 && y1 - y0 > 0.002; m.visible = ok;
    if (ok) { m.scale.set(x1 - x0, y1 - y0, 1); m.position.x = (x0 + x1) / 2; m.position.y = (y0 + y1) / 2; } }
  const holeSec = sec(new THREE.MeshStandardMaterial({ color: 0x1A110B, roughness: 1 }), 0.503);
  const gstoneT = stoneT.clone(); gstoneT.needsUpdate = true; gstoneT.repeat.set(12, 2.4);
  const gravSec = sec(std({ map: gstoneT }), 0.505);
  const mudOv = sec(new THREE.MeshBasicMaterial({ map: mudT, transparent: true, opacity: 0 }), 0.506);
  const fabM = new THREE.MeshBasicMaterial({ color: 0xF4F4F0 });
  const fabs = [0, 1, 2, 3].map(() => sec(fabM, 0.507));
  // Rohr (Längsschnitt): Streifen mit Löchern oben bzw. unten, neigbar
  const pipeT = (down) => tex(512, 32, down ? 52 : 51, (g, r, w, h) => { g.fillStyle = "#2E2E2E"; g.fillRect(0, 0, w, h);
    g.fillStyle = "#4A4A4A"; g.fillRect(0, 5, w, h - 10); g.fillStyle = "#0E0E0E";
    for (let x = 12; x < w; x += 26) { g.beginPath(); g.ellipse(x, down ? h - 7 : 7, 5, 3, 0, 0, 6.3); g.fill(); } }, [1, 1]);
  const pipeUp = pipeT(false), pipeDown = pipeT(true);
  const pipeM = new THREE.MeshStandardMaterial({ map: pipeUp, roughness: 0.6 });
  const pipe = add(new THREE.Mesh(new THREE.PlaneGeometry(1, 0.1), pipeM), false, false); pipe.position.z = 0.509;
  const pipeWater = add(new THREE.Mesh(new THREE.PlaneGeometry(1, 1), new THREE.MeshBasicMaterial({ color: 0x3E8EDB, transparent: true, opacity: 0.85 })), false, false); pipeWater.position.z = 0.510;
  // Kiesstreifen + Grabenöffnung von oben
  const topStrip = add(new THREE.Mesh(new THREE.PlaneGeometry(TX1 - TX0, 0.36), std({ map: gstoneT })), false, true);
  topStrip.rotation.x = -Math.PI / 2; topStrip.position.set((TX0 + TX1) / 2, 0.004, 0.32);
  const topHole = add(new THREE.Mesh(new THREE.PlaneGeometry(TX1 - TX0, 0.36), new THREE.MeshBasicMaterial({ color: 0x1A110B })), false, false);
  topHole.rotation.x = -Math.PI / 2; topHole.position.set((TX0 + TX1) / 2, 0.003, 0.32);
  const dirt = add(new THREE.Mesh(new THREE.ConeGeometry(0.6, 0.45, 20), std({ map: topT }))); dirt.position.set(0.6, 0, -0.6);
  // Sickergrube rechts (x 2.7..3.4)
  const wellHole = sec(new THREE.MeshStandardMaterial({ color: 0x1A110B, roughness: 1 }), 0.503);
  const wellGrav = sec(std({ map: gstoneT, color: 0xC8C8C8 }), 0.505);
  const wellPipe = add(new THREE.Mesh(new THREE.PlaneGeometry(1, 0.1), new THREE.MeshStandardMaterial({ map: pipeDown, roughness: 0.6 })), false, false); wellPipe.position.z = 0.509;
  // Zaun + Nachbarhaus rechts, Pfeil zum Nachbarn
  const fence = new THREE.Group(); fence.position.set(4.2, 0, 0); scene.add(fence);
  for (let i = 0; i < 18; i++) { const p = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.9, 0.03), std({ map: woodT })); p.position.set(0, 0.45, 0.45 - i * 0.22); p.castShadow = true; fence.add(p); }
  for (const y of [0.25, 0.7]) { const r = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.06, 4), std({ map: woodT })); r.position.set(-0.05, y, -1.5); fence.add(r); }
  const nArrow = new THREE.Group(); scene.add(nArrow);
  { const m = new THREE.MeshBasicMaterial({ color: 0xFF4D4D }); const sh = new THREE.Mesh(new THREE.BoxGeometry(1.2, 0.02, 0.07), m); nArrow.add(sh);
    const hd = new THREE.Mesh(new THREE.ConeGeometry(0.12, 0.26, 3), m); hd.rotation.z = -Math.PI / 2; hd.position.x = 0.72; nArrow.add(hd); }
  nArrow.position.set(3.2, 0.04, 0.2);
  // Pfütze an der Hauswand, Regen, Wassertropfen im Boden
  const puddle = add(new THREE.Mesh(new THREE.CircleGeometry(1, 32), new THREE.MeshStandardMaterial({ color: 0x4A8ED0, roughness: 0.05, transparent: true, opacity: 0.8 })), false, false);
  puddle.rotation.x = -Math.PI / 2; puddle.position.set(-0.9, 0.006, -0.2);
  const NR = 420, rainBase = [], rainPos = new Float32Array(NR * 6);
  for (let i = 0; i < NR; i++) rainBase.push([rr(-3, 5), rr(-4, 1.5), rr(0, 1), rr(0.9, 1.3)]);
  const rainGeo = new THREE.BufferGeometry(); rainGeo.setAttribute("position", new THREE.BufferAttribute(rainPos, 3));
  const rainL = new THREE.LineSegments(rainGeo, new THREE.LineBasicMaterial({ color: 0xBFD8F0, transparent: true, opacity: 0.6 })); rainL.frustumCulled = false; scene.add(rainL);
  const drops = [];
  for (let i = 0; i < 46; i++) { const d = add(new THREE.Mesh(new THREE.SphereGeometry(0.028, 10, 8), new THREE.MeshStandardMaterial({ color: 0x3E8EDB, roughness: 0.1 })), false, false);
    d.userData = { o: R(), x: rr(-1.4, 2.2), j: R() }; drops.push(d); }
  // Person (nur am Anfang)
  const person = new THREE.Group(); person.position.set(0.9, 0, -1.4); person.rotation.y = -0.6; scene.add(person);
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
    if (!s[1]) { const a = 0.45 - p * 0.5, r = 7.6; camera.position.set(Math.sin(a) * r + 1.0, 2.6 + p * 0.4, Math.cos(a) * r - 0.8); }
    else camera.position.set(s[1][0] + (s[2][0] - s[1][0]) * p, s[1][1] + (s[2][1] - s[1][1]) * p, s[1][2] + (s[2][2] - s[1][2]) * p);
    look.set(s[3][0], s[3][1], s[3][2]); camera.fov = s[4]; camera.updateProjectionMatrix(); camera.lookAt(look);
  }
  const E = (t, t0, d) => ease((t - t0) / (d || 0.6));

  function render(t) {
    shotAt(t);
    // Graben ausheben (von links nach rechts), Kies, Rohr, Gefälle
    const dk = E(t, K.trench_w - 0.2, 1.0);
    rect(holeSec, TX0, TX0 + (TX1 - TX0) * dk, TB, 0);
    topHole.visible = dk > 0.01; topHole.scale.x = Math.max(0.01, dk); topHole.position.x = TX0 + (TX1 - TX0) * dk / 2;
    dirt.visible = dk > 0.02 && t < K.end; dirt.scale.set(1, Math.max(0.01, dk), 1); dirt.position.y = 0.22 * dk;
    const gk = E(t, K.gravel_w - 0.2, 0.8);
    rect(gravSec, TX0, TX1, TB, TB + (-0.05 - TB) * gk); if (t < K.gravel_w - 0.2) gravSec.visible = false;
    topStrip.visible = gk > 0.98;
    const slK = E(t, K.slope_w, 1.0), ang = -0.025 * slK, len = TX1 - TX0 + (t >= K.well ? 0.45 * E(t, K.well, 0.6) : 0);
    const pk = E(t, K.perforated - 0.1, 0.6), pl = len * pk;
    pipe.visible = pk > 0.01; pipe.scale.x = Math.max(0.01, pl); pipe.rotation.z = ang;
    pipe.position.set(TX0 + Math.cos(ang) * pl / 2, -0.47 + Math.sin(ang) * pl / 2, 0.509);
    pipeM.map = t >= K.down - 0.1 ? pipeDown : pipeUp;
    // stehendes Wasser im flachen Rohr
    const sitK = E(t, K.sits - 0.4, 0.6) * (1 - E(t, K.slope_w + 0.3, 0.8));
    pipeWater.visible = sitK > 0.01; pipeWater.scale.set(TX1 - TX0 - 0.1, 0.06 * sitK, 1); pipeWater.position.set((TX0 + TX1) / 2, -0.5 + 0.03 * sitK, 0.510);
    // Verschlammen + Filtervlies
    const clogK = E(t, K.clogs - 0.4, 1.0) * (1 - E(t, K.fabric, 0.8));
    rect(mudOv, TX0, TX1, TB, -0.05); mudOv.material.opacity = 0.85 * clogK; mudOv.visible = clogK > 0.01;
    const fk = E(t, K.fabric, 0.7), fl = 0.012, fy1 = TB + (-0.02 - TB) * fk;
    rect(fabs[0], TX0 - fl, TX1 + fl, TB - fl, TB); rect(fabs[1], TX0 - fl, TX0, TB, fy1); rect(fabs[2], TX1, TX1 + fl, TB, fy1); rect(fabs[3], TX0 - fl, TX1 + fl, -0.03, -0.03 + fl);
    fabs.forEach((m, i) => { if (fk < 0.01 || (i === 3 && fk < 0.98)) m.visible = false; });
    // Sickergrube
    const wk = E(t, K.well, 0.8);
    rect(wellHole, 2.7, 3.45, -1.3 * wk, -0.05); rect(wellGrav, 2.72, 3.43, -1.28 * wk, -0.12 * wk); if (wk < 0.01) { wellHole.visible = wellGrav.visible = false; }
    wellPipe.visible = false;
    nArrow.visible = t >= K.neighbor - 0.3 && t < K.well; nArrow.scale.x = 1 + 0.08 * Math.sin(t * 8);
    // Regen, Pfütze
    const raining = (t >= K.flood - 0.2 && t < K.trench) || (t >= K.sits - 0.6 && t < K.holes) || (t >= K.rises - 0.6 && t < K.clog) || (t >= K.where - 0.3 && t < K.end);
    rainL.visible = raining;
    if (raining) { for (let i = 0; i < NR; i++) { const [x, z, o, sp] = rainBase[i], y = 5 - (((t) * 9 * sp + o * 6) % 6);
      rainPos.set([x, y, z, x - 0.03, y - 0.28, z], i * 6); } rainGeo.attributes.position.needsUpdate = true; }
    const puK = E(t, K.rains, 1.0) * (1 - E(t, K.trench_w, 1.0)); puddle.visible = puK > 0.01; puddle.scale.set(0.6 * puK + 0.01, 0.8 * puK + 0.01, 1);
    // Wasser im Boden: erst an die Wand; später in den Graben → stehen / fließen → Sickergrube
    const pipeY = (x) => -0.47 + Math.tan(ang) * (x - TX0);
    drops.forEach((d) => { const u = d.userData; d.visible = false;
      if (t >= K.rains && t < K.trench) { const ph = ((t - K.rains) * 0.5 + u.o) % 1; d.visible = true;
        d.position.set(-1.45 + (u.x + 1.4) * 0.12 * (1 - ph), -0.05 - ph * 1.1, 0.512); }
      else if (t >= K.sits - 0.6 && t < K.end) { const ph = ((t - K.sits) * 0.45 + u.o) % 1; d.visible = true;
        const flowing = t >= K.slope_w + 0.3, fromBelow = t >= K.rises - 0.2, gx = Math.min(TX1 - 0.1, Math.max(TX0 + 0.1, u.x));
        if (!flowing) { const k = Math.min(1, ph * 1.6); d.position.set(gx, -0.02 + (pipeY(gx) + 0.02) * k + (k >= 1 ? Math.sin(t * 6 + u.j * 9) * 0.006 : 0), 0.512); }
        else if (ph < 0.45) { const k = ph / 0.45;
          if (fromBelow) d.position.set(gx, k < 0.6 ? -0.05 - (k / 0.6) * 0.52 : -0.57 + ((k - 0.6) / 0.4) * (pipeY(gx) + 0.57), 0.512);
          else d.position.set(gx, -0.02 + (pipeY(gx) + 0.02) * k, 0.512); }
        else { const k = (ph - 0.45) / 0.55, x = gx + (TX1 + 0.4 - gx) * k;
          if (x < TX1 + 0.1 || t < K.well) d.position.set(Math.min(x, TX1), pipeY(Math.min(x, TX1)), 0.512);
          else d.position.set(3.05 + (u.j - 0.5) * 0.4, pipeY(TX1) - (x - TX1 - 0.1) * 3, 0.512);
          if (t < K.well && x > TX1 - 0.05) d.visible = false; } } });
    person.visible = t < K.flood; sunBall.visible = false;

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
for key, f, v in [("wall_w", "error.mp3", 0.35), ("sits", "error.mp3", 0.3), ("clogs", "error.mp3", 0.3), ("neighbor", "error.mp3", 0.3),
                  ("trench_w", "impact-bass-2.mp3", 0.3), ("gravel_w", "impact-bass-2.mp3", 0.3), ("perforated", "click.mp3", 0.4),
                  ("slope_w", "pop.mp3", 0.4), ("down", "click.mp3", 0.4), ("fabric", "pop.mp3", 0.4), ("well", "pop.mp3", 0.4),
                  ("dry_end", "sparkle.mp3", 0.4), ("congrats", "sparkle.mp3", 0.5)]:
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
