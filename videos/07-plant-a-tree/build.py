#!/usr/bin/env python3
"""Builds "How to plant a tree so it actually survives" (English) – structure like the garden reference video:
one growing world, a chain of problem → fix (red problem words, yellow fixes), one word per caption, mid-screen.
No voice is mixed in: assets/timings.json comes from a timing guide (tools/tts.py, Piper en-us-ryan-medium)
until the creator's recording arrives, then tools/align.py.

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
    "tree_w": word("want", "tree"), "deep": word("dig", "deep"), "drop": word("dig", "drop"),
    "mistake": word("rot", "mistake"), "rot_w": word("rot", "rot"), "higher": word("flare", "higher"), "ground": word("flare", "ground"),
    "narrow_w": word("narrow", "narrow"), "circling": word("narrow", "circling"), "twice": word("wide", "twice"), "loosen": word("wide", "loosen"),
    "potting": word("pot", "potting"), "leave": word("pot", "leave"), "soil_w": word("native", "soil"),
    "wind_w": word("wind", "wind"), "leans": word("wind", "leans"), "stake_w": word("stake", "stake"), "one": word("stake", "one"),
    "dries": word("dry", "dries"), "deeply": word("water", "deeply"), "mulch": word("water", "mulch"), "trunk": word("volcano", "trunk"),
    "congrats": word("end", "Congratulations"), "outlive": word("end", "outlive"),
})
SHOTS = [
    (K["want"], (3.2, 2.1, 6.6), (2.7, 1.85, 5.9), (0, 0.6, 0), 48),
    (K["dig"], (0.3, 0.55, 4.3), (0, 0.45, 3.9), (0, -0.15, 0), 50),
    (K["rot"], (0, 0.25, 3.2), (0, 0.18, 2.9), (0, -0.3, 0), 50),
    (K["flare"], (0.25, 0.55, 3.9), (0, 0.5, 3.5), (0, -0.05, 0), 50),
    (K["narrow"], (0, 0.3, 3.4), (0, 0.25, 3.1), (0, -0.25, 0), 50),
    (K["wide"], (0.3, 0.5, 4.1), (0, 0.45, 3.7), (0, -0.2, 0), 50),
    (K["pot"], (0, 0.45, 3.7), (0, 0.4, 3.45), (0, -0.2, 0), 50),
    (K["native"], (0, 0.4, 3.45), (0.3, 0.6, 4.3), (0, -0.15, 0), 50),
    (K["wind"], (2.7, 1.8, 6.3), (2.4, 1.7, 5.8), (0, 0.85, 0), 48),
    (K["stake"], (1.9, 1.45, 4.7), (1.6, 1.35, 4.3), (0, 0.8, 0), 48),
    (K["dry"], (2.7, 1.9, 6.3), (2.4, 1.8, 5.8), (0, 0.75, 0), 48),
    (K["water"], (1.5, 2.3, 3.5), (1.25, 2.05, 3.05), (0, 0.15, 0), 48),
    (K["volcano"], (1.25, 2.05, 3.05), (1.0, 1.85, 2.75), (0, 0.15, 0), 48),
    (K["end"], None, None, (0, 1.1, -0.4), 50),
]

# Schwebende 3D-Wörter: rot = Problem, gelb = Lösung
LABELS = [
    ("l-tree", "TREE?", "g", 0.0, 2.6, 0.4, K["tree_w"], K["dig"]),
    ("l-deep", "DEEP HOLE", "y", 0.0, 0.25, 0.55, K["deep"], K["rot"]),
    ("l-mistake", "MISTAKE!", "r", 0.0, 0.3, 0.55, K["mistake"], K["rot_w"]),
    ("l-rot", "ROT!", "r", 0.35, -0.25, 0.55, K["rot_w"], K["flare"]),
    ("l-flare", "ROOT FLARE", "y", 0.45, 0.12, 0.55, K["ground"], K["narrow"]),
    ("l-circle", "CIRCLING ROOTS!", "r", 0.0, -0.75, 0.55, K["circling"], K["wide"]),
    ("l-wide", "2× WIDE", "y", 0.0, 0.2, 0.55, K["twice"], K["pot"]),
    ("l-pocket", "ROOTS STAY INSIDE!", "r", 0.0, -0.75, 0.55, K["leave"], K["native"]),
    ("l-native", "DUG-OUT SOIL", "y", 0.0, 0.2, 0.55, K["soil_w"], K["wind"]),
    ("l-wind", "WIND!", "r", -0.6, 2.3, 0.4, K["wind_w"], K["stake"]),
    ("l-stake", "STAKE · 1 YEAR", "y", 0.0, 2.45, 0.4, K["stake_w"], K["dry"]),
    ("l-dry", "DRY!", "r", 0.0, 2.45, 0.4, K["dries"], K["water"]),
    ("l-water", "WATER DEEPLY", "b", 0.0, 1.2, 0.4, K["deeply"], K["mulch"]),
    ("l-mulch", "MULCH RING", "y", 0.0, 0.5, 0.4, K["mulch"], K["volcano"]),
    ("l-volcano", "NOT THE TRUNK ✕", "r", 0.0, 0.75, 0.4, K["trunk"], K["end"]),
    ("l-congrats", "CONGRATULATIONS!", "y", 0.0, 3.5, 0.4, K["congrats"], TOTAL),
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

  const std = (o) => new THREE.MeshStandardMaterial(Object.assign({ roughness: 0.9, metalness: 0 }, o));
  const scene = new THREE.Scene();
  scene.background = skyT;
  scene.fog = new THREE.Fog(0xCFE2F3, 30, 90);
  const add = (m, cast = true, recv = true) => { m.castShadow = cast; m.receiveShadow = recv; scene.add(m); return m; };

  // ---------- Garten mit Querschnitt (Schnittkante bei z = 0.5)
  const groundTop = std({ map: grassT });
  const cutMat = std({ map: cutT });
  const gb = new THREE.BoxGeometry(60, 2.6, 40);
  const gMats = [groundTop, groundTop, groundTop, groundTop, cutMat, groundTop];
  cutT.repeat.set(12, 1);
  const ground = add(new THREE.Mesh(gb, gMats), false, true); ground.position.set(0, -1.3, 0.5 - 20);
  const floor = add(new THREE.Mesh(new THREE.BoxGeometry(60, 0.2, 30), std({ map: gravelT })), false, true); floor.position.set(0, -2.7, 15.5);
  // Wühlmausgang im Querschnitt
  const tunnel = add(new THREE.Mesh(new THREE.CircleGeometry(1, 24), std({ color: 0x24170F })), false, false);
  tunnel.scale.set(1.9, 0.13, 1); tunnel.position.set(-0.4, -0.38, 0.505);
  const vole = new THREE.Group(); scene.add(vole);
  { const body = new THREE.Mesh(new THREE.SphereGeometry(0.09, 16, 12), std({ color: 0x6E6458 })); body.scale.set(1.5, 0.8, 0.9); body.castShadow = true; vole.add(body);
    const head = new THREE.Mesh(new THREE.SphereGeometry(0.05, 12, 10), std({ color: 0x7A7064 })); head.position.set(0.14, 0.01, 0); vole.add(head);
    for (const s of [-1, 1]) { const ear = new THREE.Mesh(new THREE.SphereGeometry(0.018, 8, 6), std({ color: 0xC9A08A })); ear.position.set(0.12, 0.05, s * 0.03); vole.add(ear); }
    const eye = new THREE.Mesh(new THREE.SphereGeometry(0.009, 8, 6), std({ color: 0x050505 })); eye.position.set(0.18, 0.02, 0.03); vole.add(eye);
    const tail = new THREE.Mesh(new THREE.CylinderGeometry(0.006, 0.003, 0.12, 6), std({ color: 0xC9A08A })); tail.rotation.z = 1.3; tail.position.set(-0.17, -0.01, 0); vole.add(tail); }

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

  // ---------- Hochbeet (Innen: x ±0.96, z -0.46..0.5; Höhe 0.85; vordere Wand ist aufgeschnitten)
  const IN = { x0: -0.96, x1: 0.96, z0: -0.46, z1: 0.5 }, HB = 0.85;
  const wood = std({ map: woodT, roughness: 0.8 });
  const boards = [];
  for (let lvl = 0; lvl < 5; lvl++) {
    const y = 0.085 + lvl * 0.17;
    for (const [w, d, x, z] of [[2.08, 0.04, 0, -0.5], [0.04, 1.0, -1.0, 0.0], [0.04, 1.0, 1.0, 0.0]]) {
      const b = add(new THREE.Mesh(new THREE.BoxGeometry(w, 0.165, d), wood)); b.position.set(x, y, z); b.userData = { lvl, y }; boards.push(b); }
  }
  const footprint = add(new THREE.Mesh(new THREE.PlaneGeometry(2.08, 1.0), new THREE.MeshBasicMaterial({ color: 0xFFFFFF, transparent: true, opacity: 0.5 })), false, false);
  footprint.rotation.x = -Math.PI / 2; footprint.position.set(0, 0.012, 0);
  const arrow = new THREE.Group(); scene.add(arrow);
  { const m = new THREE.MeshBasicMaterial({ color: 0xFFD23F }); const sh = new THREE.Mesh(new THREE.BoxGeometry(3.6, 0.02, 0.08), m); arrow.add(sh);
    for (const s of [-1, 1]) { const hd = new THREE.Mesh(new THREE.ConeGeometry(0.16, 0.36, 3), m); hd.rotation.z = -s * Math.PI / 2; hd.position.x = s * 1.95; arrow.add(hd); } }
  arrow.position.set(0, 0.03, 0.75);
  // Füllschichten
  function layerBox(y0, y1, mat) { const g = new THREE.BoxGeometry(IN.x1 - IN.x0, 1, IN.z1 - IN.z0);
    const m = add(new THREE.Mesh(g, mat), false, true); m.position.set(0, (y0 + y1) / 2, (IN.z0 + IN.z1) / 2); m.userData = { y0, y1 }; return m; }
  const mats = { aeste: std({ map: barkT, color: 0x8A6A4A }), laub: std({ map: leafT }), komp: std({ map: compT }), erde: std({ map: soilT }) };
  const L = { aeste: [0, 0.30], laub: [0.30, 0.45], komp: [0.45, 0.65], erde: [0.65, 0.85] };
  const lay = { aeste: layerBox(0, 0.30, std({ map: twigT })), laub: layerBox(0.30, 0.45, mats.laub), komp: layerBox(0.45, 0.65, mats.komp), erde: layerBox(0.65, 0.85, mats.erde) };
  const allSoil = layerBox(0, 0.85, mats.erde);
  const extraKomp = layerBox(0.75, 0.85, mats.komp);
  // Äste als einzelne Stöcke
  const sticks = [];
  for (let i = 0; i < 70; i++) { const len = rr(0.35, 0.9);
    const s = add(new THREE.Mesh(new THREE.CylinderGeometry(rr(0.02, 0.045), rr(0.025, 0.05), len, 7), mats.aeste));
    s.userData = { x: rr(-0.9 + len / 2, 0.9 - len / 2), y: rr(0.04, 0.26), z: rr(-0.4, 0.42), rx: rr(-0.4, 0.4), rz: Math.PI / 2 + rr(-0.12, 0.12), ry: rr(-0.25, 0.25), d: i / 70 };
    sticks.push(s); }
  const leaves = [];
  for (let i = 0; i < 60; i++) { const l = add(new THREE.Mesh(new THREE.CircleGeometry(rr(0.04, 0.07), 7),
      std({ color: [0xC0732A, 0xA65A1F, 0xD9A13A, 0x8D6E2B, 0xB4472A][i % 5], side: THREE.DoubleSide })), true, false);
    l.userData = { x: rr(-0.85, 0.85), y: rr(0.38, 0.46), z: rr(-0.4, 0.46), r: rr(0, 6), d: i / 60 }; leaves.push(l); }
  const lumps = [];
  for (let i = 0; i < 40; i++) { const l = add(new THREE.Mesh(new THREE.IcosahedronGeometry(rr(0.03, 0.06), 0), std({ color: [0x3D2A1C, 0x55392A, 0x6B4A2C][i % 3], flatShading: true })));
    l.userData = { x: rr(-0.85, 0.85), y: rr(0.6, 0.66), z: rr(-0.4, 0.46), d: i / 40 }; lumps.push(l); }
  // Gitter, Folie, Wasser, Wärme
  const mesh = add(new THREE.Mesh(new THREE.PlaneGeometry(1.95, 0.98), new THREE.MeshStandardMaterial({ map: meshT, transparent: true, metalness: 0.6, roughness: 0.4, side: THREE.DoubleSide })), false, false);
  mesh.rotation.x = -Math.PI / 2; mesh.position.set(0, 0.01, 0.01);
  const foilMat = std({ color: 0x1C1C1C, roughness: 0.35 });
  const foils = [[1.92, 0.85, 0, -0.455, 0], [0.96, 0.85, -0.955, 0.02, Math.PI / 2], [0.96, 0.85, 0.955, 0.02, -Math.PI / 2]].map(([w, h, x, z, ry]) => {
    const f = add(new THREE.Mesh(new THREE.PlaneGeometry(w, h), foilMat), false, true); f.position.set(x, h / 2, z); f.rotation.y = ry; return f; });
  const badFoil = add(new THREE.Mesh(new THREE.PlaneGeometry(1.92, 0.96), std({ color: 0x8A1F1F, roughness: 0.3 })), false, true);
  badFoil.rotation.x = -Math.PI / 2; badFoil.position.set(0, 0.02, 0.02);
  const water = add(new THREE.Mesh(new THREE.BoxGeometry(1.92, 1, 0.96), new THREE.MeshStandardMaterial({ color: 0x3E8EDB, transparent: true, opacity: 0.75, roughness: 0.1 })), false, false);
  const drops = [];
  for (let i = 0; i < 24; i++) { const d = add(new THREE.Mesh(new THREE.SphereGeometry(0.022, 10, 8), new THREE.MeshStandardMaterial({ color: 0x5AA8F0, roughness: 0.1 })), false, false);
    d.userData = { x: rr(-0.85, 0.85), z: rr(0.3, 0.5), o: R() }; drops.push(d); }
  const heat = [];
  for (let i = 0; i < 14; i++) { const h = add(new THREE.Mesh(new THREE.TorusGeometry(rr(0.05, 0.09), 0.012, 6, 20), new THREE.MeshBasicMaterial({ color: 0xFF8A3D, transparent: true })), false, false);
    h.userData = { x: rr(-0.8, 0.8), z: rr(-0.3, 0.4), o: R() }; heat.push(h); }
  const glow = add(new THREE.Mesh(new THREE.BoxGeometry(1.9, 0.19, 0.95), new THREE.MeshBasicMaterial({ color: 0xFF7A2A, transparent: true, opacity: 0 })), false, false);
  glow.position.set(0, 0.55, 0.02);

  // Pflanzen
  function plant(kind, x, z) { const g = new THREE.Group(); g.position.set(x, 0.85, z); scene.add(g);
    const leafM = std({ color: kind === "kohl" ? 0x6F9C86 : 0x3F7A2E, flatShading: true });
    if (kind === "tomate") { const st = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 0.9, 6), std({ color: 0x9C7A4C })); st.position.y = 0.45; g.add(st);
      for (let i = 0; i < 7; i++) { const b = new THREE.Mesh(new THREE.IcosahedronGeometry(0.12, 0), leafM); b.position.set(rr(-0.1, 0.1), 0.15 + i * 0.1, rr(-0.1, 0.1)); b.castShadow = true; g.add(b); }
      for (let i = 0; i < 6; i++) { const f = new THREE.Mesh(new THREE.SphereGeometry(0.045, 12, 10), std({ color: 0xD2302A, roughness: 0.4 })); f.position.set(rr(-0.13, 0.13), rr(0.3, 0.8), rr(0.02, 0.15)); g.add(f); } }
    if (kind === "zucchini") { for (let i = 0; i < 6; i++) { const lf = new THREE.Mesh(new THREE.CircleGeometry(0.16, 8), std({ color: 0x3F7A2E, side: THREE.DoubleSide, flatShading: true }));
        lf.rotation.set(-1.1 + rr(-0.2, 0.2), i * 1.05, 0); lf.position.set(Math.cos(i * 1.05) * 0.12, 0.12 + rr(0, 0.08), Math.sin(i * 1.05) * 0.12); lf.castShadow = true; g.add(lf); }
      const z1 = new THREE.Mesh(new THREE.CapsuleGeometry(0.035, 0.18, 4, 8), std({ color: 0x2F5E23 })); z1.rotation.z = 1.4; z1.position.set(0.05, 0.05, 0.12); g.add(z1);
      const fl = new THREE.Mesh(new THREE.ConeGeometry(0.05, 0.08, 6), std({ color: 0xF2B51A })); fl.position.set(-0.05, 0.22, 0.05); g.add(fl); }
    if (kind === "kohl") { for (let i = 0; i < 9; i++) { const b = new THREE.Mesh(new THREE.SphereGeometry(rr(0.08, 0.12), 10, 8), leafM); b.position.set(rr(-0.08, 0.08), 0.1 + rr(0, 0.08), rr(-0.08, 0.08)); b.castShadow = true; g.add(b); } }
    return g; }
  const plants = [["tomate", -0.65, -0.15, "tomate"], ["tomate", -0.65, 0.2, "tomate"], ["zucchini", 0.0, 0.05, "zucchini"], ["kohl", 0.62, -0.15, "kohl"], ["kohl", 0.62, 0.22, "kohl"]]
    .map(([k, x, z, key]) => ({ g: plant(k, x, z), key }));

  // ---------- Baum-Szene: Pflanzloch und Wurzeln als Querschnitt direkt an der Schnittkante (z ≈ 0.5)
  const TZ = 0.42;
  const sec = (mat, z) => { const m = add(new THREE.Mesh(new THREE.PlaneGeometry(1, 1), mat), false, false); m.position.z = z; return m; };
  const subT = tex(256, 256, 31, (g, r, w, h) => { g.fillStyle = "#A8693A"; g.fillRect(0, 0, w, h);
    speck(g, r, w, h, 1400, ["#96592E", "#B9794A", "#8A4F25"], 1, 4); }, [2, 2]);
  const holeSec = sec(new THREE.MeshStandardMaterial({ color: 0x1A110B, roughness: 1 }), 0.503);
  const nativeBottom = sec(std({ map: subT }), 0.504);
  const potFill = sec(std({ map: soilT }), 0.505);
  const nativeFill = sec(std({ map: subT, color: 0xC8A080 }), 0.505);
  const trunkSec = sec(std({ map: barkT }), 0.507);
  const rotSec = sec(new THREE.MeshStandardMaterial({ color: 0x2C3A1E, roughness: 1, transparent: true, opacity: 0.85 }), 0.508);
  const ballSec = add(new THREE.Mesh(new THREE.CircleGeometry(1, 32), std({ color: 0x5A3A22 })), false, false); ballSec.position.z = 0.506;
  const ring = add(new THREE.Mesh(new THREE.TorusGeometry(0.17, 0.016, 8, 40), std({ color: 0xE0B080 })), false, false); ring.position.z = 0.509;
  const ring2 = add(new THREE.Mesh(new THREE.TorusGeometry(0.11, 0.014, 8, 40), std({ color: 0xE0B080 })), false, false); ring2.position.z = 0.509;
  const roots = [];
  for (let i = 0; i < 9; i++) { const a = -Math.PI * 0.08 - i * Math.PI * 0.105, L = rr(0.35, 0.6);
    const m = add(new THREE.Mesh(new THREE.BoxGeometry(1, 0.018, 0.01), std({ color: 0xE0B080 })), false, false);
    m.userData = { a, L }; m.position.z = 0.51; roots.push(m); }
  // Baum (Stamm hinter der Schnittkante)
  const ptree = new THREE.Group(); ptree.position.set(0, 0, TZ); scene.add(ptree);
  const crownM = std({ color: 0x4F8A35, flatShading: true });
  { const tr = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.075, 1.6, 10), std({ map: barkT })); tr.position.y = 0.8; tr.castShadow = true; ptree.add(tr);
    for (let i = 0; i < 7; i++) { const b = new THREE.Mesh(new THREE.IcosahedronGeometry(rr(0.28, 0.42), 1), crownM);
      b.position.set(rr(-0.35, 0.35), 1.75 + rr(-0.15, 0.35), rr(-0.3, 0.3)); b.castShadow = true; ptree.add(b); } }
  const stake = add(new THREE.Mesh(new THREE.BoxGeometry(0.05, 1.4, 0.05), std({ map: woodT }))); stake.position.set(0.32, 0.6, TZ);
  const tie = add(new THREE.Mesh(new THREE.BoxGeometry(0.3, 0.025, 0.025), std({ color: 0x3A6E2A }))); tie.position.set(0.16, 1.0, TZ);
  const mulchRing = add(new THREE.Mesh(new THREE.RingGeometry(0.16, 0.65, 40), std({ map: barkT, color: 0x9A6A44, side: THREE.DoubleSide })), false, true);
  mulchRing.rotation.x = -Math.PI / 2; mulchRing.position.set(0, 0.02, TZ);
  const volcano = add(new THREE.Mesh(new THREE.ConeGeometry(0.42, 0.42, 32, 1, true), std({ map: barkT, color: 0x9A6A44, side: THREE.DoubleSide })));
  volcano.position.set(0, 0.2, TZ);
  // Wind + Gießwasser
  const NW = 160, windBase = [], windPos = new Float32Array(NW * 6);
  for (let i = 0; i < NW; i++) windBase.push([rr(0, 8), rr(0.3, 3.2), rr(-2, 2.5), rr(0.4, 1.0), rr(0.8, 1.3)]);
  const windGeo = new THREE.BufferGeometry(); windGeo.setAttribute("position", new THREE.BufferAttribute(windPos, 3));
  const windL = new THREE.LineSegments(windGeo, new THREE.LineBasicMaterial({ color: 0xFFFFFF, transparent: true, opacity: 0.7 }));
  windL.frustumCulled = false; scene.add(windL);
  const wdrops = [];
  for (let i = 0; i < 40; i++) { const d = add(new THREE.Mesh(new THREE.SphereGeometry(0.02, 8, 6), new THREE.MeshStandardMaterial({ color: 0x5AA8F0, roughness: 0.1 })), false, false);
    d.userData = { x: rr(-0.5, 0.5), z: TZ + rr(-0.5, 0.4), o: R() }; wdrops.push(d); }
  const groundColor = groundTop.color.clone();

  // Person (nur am Anfang)
  const person = new THREE.Group(); person.position.set(1.2, 0, 0.9); person.rotation.y = -0.9; scene.add(person);
  { const skin = std({ color: 0xE3B48F }), shirt = std({ color: 0x3C7FA8 }), pants = std({ color: 0x2E3440 });
    for (const s of [-1, 1]) { const lg = new THREE.Mesh(new THREE.CapsuleGeometry(0.07, 0.75, 4, 8), pants); lg.position.set(s * 0.1, 0.45, 0); lg.castShadow = true; person.add(lg);
      const ar = new THREE.Mesh(new THREE.CapsuleGeometry(0.05, 0.55, 4, 8), shirt); ar.position.set(s * 0.27, 1.12, 0.02); ar.castShadow = true; person.add(ar); }
    const tor = new THREE.Mesh(new THREE.CapsuleGeometry(0.19, 0.42, 4, 10), shirt); tor.position.y = 1.15; tor.castShadow = true; person.add(tor);
    const hd = new THREE.Mesh(new THREE.SphereGeometry(0.12, 16, 12), skin); hd.position.y = 1.62; person.add(hd);
    const hair = new THREE.Mesh(new THREE.SphereGeometry(0.125, 16, 12, 0, 6.3, 0, 1.4), std({ color: 0x4A3324 })); hair.position.y = 1.64; person.add(hair); }

  // ---------- Beschriftungen (HTML, auf 3D-Punkte projiziert)
  const labelEls = LABELS.map((l) => document.getElementById(l[0]));
  const camera = new THREE.PerspectiveCamera(48, W / H, 0.05, 200);
  const look = new THREE.Vector3(), v3 = new THREE.Vector3();

  function shotAt(t) {
    let i = 0; for (let k = 0; k < SHOTS.length; k++) if (t >= SHOTS[k][0]) i = k;
    const s = SHOTS[i], end = i + 1 < SHOTS.length ? SHOTS[i + 1][0] : DUR, p = ease((t - s[0]) / (end - s[0]));
    if (!s[1]) { const a = 0.55 + p * 0.7, r = 5.6; camera.position.set(Math.sin(a) * r, 2.4 + p * 0.6, Math.cos(a) * r + 0.2); }
    else camera.position.set(s[1][0] + (s[2][0] - s[1][0]) * p, s[1][1] + (s[2][1] - s[1][1]) * p, s[1][2] + (s[2][2] - s[1][2]) * p);
    look.set(s[3][0], s[3][1], s[3][2]); camera.fov = s[4]; camera.updateProjectionMatrix(); camera.lookAt(look);
  }
  const fill = (t, t0, d) => ease((t - t0) / (d || 1.2));

  function rect(m, x0, x1, y0, y1) { const ok = x1 - x0 > 0.002 && y1 - y0 > 0.002; m.visible = ok;
    if (ok) { m.scale.set(x1 - x0, y1 - y0, 1); m.position.x = (x0 + x1) / 2; m.position.y = (y0 + y1) / 2; } }

  function render(t) {
    shotAt(t);
    // alles vom Hochbeet ausblenden
    for (const o of [footprint, arrow, sunBall, allSoil, mesh, badFoil, water, extraKomp, glow, vole, tunnel]) o.visible = false;
    for (const arr of [boards, foils, sticks, leaves, lumps, drops, heat]) for (const o of arr) o.visible = false;
    for (const k in lay) lay[k].visible = false; for (const p of plants) p.g.visible = false;

    // Pflanzloch: tief & schmal → Boden angehoben → doppelt so breit
    const dk = ease((t - K.deep) / 0.6);
    const hw = 0.35 + 0.45 * ease((t - K.twice) / 0.7);                  // halbe Lochbreite
    const lift = ease((t - K.higher) / 0.9);                               // Baum + Lochboden heben
    const depth = 0.95, baseY = -0.55 * (1 - lift), floor = -depth + 0.5 * lift;
    rect(holeSec, -hw * dk, hw * dk, -depth * dk, 0);
    rect(nativeBottom, -hw, hw, -depth, t >= K.higher ? floor : -depth);
    const potK = t >= K.potting && t < K.soil_w ? ease((t - K.potting) / 0.7) : 0;
    rect(potFill, -hw, hw, floor, floor + (0 - floor) * potK);
    const natK = t >= K.soil_w ? ease((t - K.soil_w) / 0.7) : 0;
    rect(nativeFill, -hw, hw, floor, floor + (0 - floor) * natK);
    if (natK > 0.99) { holeSec.visible = false; nativeBottom.visible = false; }
    // Baum fällt ins Loch, sitzt zu tief, wird angehoben
    const dropK = ease((t - K.drop) / 0.5);
    ptree.visible = t >= K.drop - 0.1;
    const y0 = t < K.dig ? 0 : baseY + (1 - dropK) * 1.4;
    const lean = ease((t - K.leans + 0.4) / 0.8) * 0.28 * (1 - ease((t - K.stake_w - 0.2) / 0.8));
    const grow = 1 + 0.9 * ease((t - K.outlive) / 1.5);
    ptree.position.y = t < K.dig ? 0 : y0; ptree.rotation.z = -lean; ptree.scale.setScalar(grow);
    // Stamm + Wurzelballen im Schnitt
    const showSec = t >= K.drop && t < K.wind;
    rect(trunkSec, -0.06, 0.06, Math.min(0, y0), 0); if (!showSec) trunkSec.visible = false;
    rect(rotSec, -0.065, 0.065, Math.max(y0, -0.3), -0.02); if (!(showSec && t >= K.rot_w && t < K.higher + 0.6)) rotSec.visible = false;
    ballSec.visible = showSec; ballSec.scale.set(0.24, 0.2, 1); ballSec.position.set(0, y0 - 0.12, 0.506);
    const circ = showSec && t >= K.narrow && t < K.loosen + 0.3;
    ring.visible = circ; ring2.visible = circ; ring.position.y = ring2.position.y = y0 - 0.12;
    ring.rotation.z = t * 2; ring2.rotation.z = -t * 2.6;
    ring.material.color.set(t >= K.circling ? 0xFF5A4A : 0xE0B080);
    // Wurzeln: kurz im Topfballen, nach dem Lockern länger, mit Aushub bis in den Boden
    let rk = 0; if (t >= K.loosen) rk = 0.35; if (natK > 0) rk = 0.35 + 0.65 * natK;
    roots.forEach((m) => { const { a, L } = m.userData, len = L * rk; m.visible = showSec && len > 0.02;
      m.scale.x = Math.max(0.001, len); const cx = Math.cos(a) * (0.12 + len / 2), cy = Math.sin(a) * (0.1 + len / 2);
      m.position.set(cx, y0 - 0.12 + cy, 0.51); m.rotation.z = a;
      m.material.color.set(t >= K.leave && t < K.soil_w ? 0xFF5A4A : 0xE0B080); });
    // Stützpfahl
    const sk = ease((t - K.stake_w) / 0.5); stake.visible = tie.visible = t >= K.stake_w && t < K.end; stake.position.y = 0.6 + (1 - sk) * 1.2;
    // Wind
    windL.visible = t >= K.wind && t < K.stake_w + 0.6;
    if (windL.visible) { for (let i = 0; i < NW; i++) { const [ox, y, z, len, sp] = windBase[i], x = -4 + ((ox + (t - K.wind) * 7 * sp) % 8);
      windPos.set([x, y, z, x + len, y, z], i * 6); } windGeo.attributes.position.needsUpdate = true; }
    // Trockenheit: Rasen gelb, Krone braun; Gießen + Mulch
    const dryK = t >= K.dries - 0.3 && t < K.end ? ease((t - K.dries + 0.3) / 0.8) * (1 - ease((t - K.deeply) / 1.5)) : 0;
    groundTop.color.copy(groundColor).lerp(new THREE.Color(0xD9C27A), dryK);
    crownM.color.set(0x4F8A35).lerp(new THREE.Color(0x9A8A3A), dryK);
    sun.color.set(0xFFF1D8).lerp(new THREE.Color(0xFFC98A), dryK);
    wdrops.forEach((d) => { const u = d.userData, ph = (t - K.deeply) / 0.9 + u.o;
      d.visible = t >= K.deeply && t < K.volcano; d.position.set(u.x, 1.4 - (ph % 1) * 1.4, u.z); });
    const mk = ease((t - K.mulch) / 0.5); mulchRing.visible = t >= K.mulch; mulchRing.scale.setScalar(Math.max(0.001, mk));
    const vk = t >= K.trunk - 0.2 && t < K.end ? ease((t - K.trunk + 0.2) / 0.4) : 0;
    volcano.visible = vk > 0.01; volcano.scale.set(1, Math.max(0.001, vk), 1); volcano.position.y = 0.21 * vk;
    person.visible = t < K.dig;

    renderer.render(scene, camera);

    LABELS.forEach((l, i) => { const el = labelEls[i]; v3.set(l[3], l[4], l[5]).project(camera);
      const on = t >= l[6] && t < l[7] && v3.z < 1;
      el.style.display = on ? "block" : "none";
      if (on) { el.style.left = clamp((v3.x + 1) / 2 * W, 330, W - 330) + "px"; el.style.top = clamp((1 - v3.y) / 2 * H, 200, H - 200) + "px"; } });
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
    .wd span {{ display:inline-block; font-family:'Inter',sans-serif; font-weight:900; font-size:104px; line-height:1;
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
for key, f, v in [("mistake", "error.mp3", 0.35), ("rot_w", "error.mp3", 0.3), ("circling", "glitch-1.mp3", 0.2), ("leave", "error.mp3", 0.3),
                  ("leans", "error.mp3", 0.3), ("dries", "error.mp3", 0.3), ("trunk", "error.mp3", 0.3),
                  ("drop", "impact-bass-2.mp3", 0.35), ("higher", "pop.mp3", 0.4), ("twice", "pop.mp3", 0.4), ("soil_w", "impact-bass-2.mp3", 0.3),
                  ("wind_w", "whoosh-cinematic.mp3", 0.3), ("stake_w", "click.mp3", 0.4), ("mulch", "pop.mp3", 0.4), ("outlive", "sparkle.mp3", 0.4),
                  ("congrats", "sparkle.mp3", 0.5)]:
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
    <title>How to plant a tree so it actually survives</title>
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
