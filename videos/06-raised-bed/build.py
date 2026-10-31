#!/usr/bin/env python3
"""Builds "How to build a raised bed the right way" (English) – structure like the garden reference video:
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
    "veg": word("want", "vegetables"), "dig_w": word("dig", "dig"), "soil1": word("dig", "soil"),
    "rain_w": word("rain", "rains"), "mud": word("rain", "Mud"), "frame_w": word("frame", "frame"),
    "bend_w": word("bend", "bend"), "back": word("bend", "back"), "tall90": word("tall", "90"),
    "voles_w": word("voles", "voles"), "carrots": word("voles", "carrots"), "mesh_w": word("mesh", "wire"),
    "rot_w": word("rot", "rot"), "foil_w": word("rot", "foil"), "bottom_w": word("bottom", "bottom"), "drain": word("bottom", "drain"),
    "layers_w": word("layers", "layers"), "branches": word("layers", "Branches"), "runs": word("layers", "runs"),
    "leaves_w": word("layers", "leaves"), "compost_w": word("layers", "compost"), "heats": word("layers", "heats"),
    "soil_w": word("layers", "soil"), "earlier": word("grow", "earlier"), "crazy": word("grow", "crazy"),
    "sinks": word("sink", "sinks"), "topup": word("sink", "compost"), "congrats": word("end", "Congratulations"),
})
BASE = ((2.6, 1.95, 5.8), (2.3, 1.85, 5.4), (0, 0.35, 0), 48)   # Grundansicht wie im Referenzvideo (Haus dahinter)
SHOTS = [
    (K["want"], (3.0, 2.2, 6.6), (2.6, 1.95, 5.9), (0, 0.3, 0), 48),
    (K["dig"], (1.9, 1.7, 4.6), (1.6, 1.5, 4.1), (0, 0.0, 0), 48),
    (K["rain"], *BASE),
    (K["frame"], (1.6, 1.3, 4.4), (1.3, 1.2, 4.0), (0, 0.2, 0), 48),
    (K["bend"], (3.6, 1.8, 5.6), (3.3, 1.7, 5.2), (0.7, 0.65, 0), 48),
    (K["tall"], (3.3, 1.7, 5.2), (3.1, 1.65, 4.9), (0.6, 0.6, 0), 48),
    (K["voles"], (0.3, 0.5, 4.3), (0, 0.38, 3.8), (0, -0.15, 0), 50),
    (K["mesh"], (0, 0.42, 3.9), (0.2, 0.5, 4.2), (0, -0.05, 0), 50),
    (K["rot"], (0, 3.0, 3.5), (0, 2.7, 3.1), (0, 0.15, -0.1), 48),
    (K["bottom"], (0.2, 2.6, 3.2), (0, 2.4, 2.9), (0, 0.1, 0), 48),
    (K["layers"], (0.4, 1.25, 4.9), (0, 1.1, 4.3), (0, 0.42, 0), 48),
    (K["compost_w"] - 0.15, (-0.3, 1.2, 4.4), (0, 1.15, 4.1), (0, 0.5, 0), 48),
    (K["grow"], (2.9, 2.4, 4.8), (2.4, 2.0, 4.0), (0, 0.8, 0), 48),
    (K["sink"], (0.3, 1.25, 4.7), (0, 1.12, 4.2), (0, 0.55, 0), 48),
    (K["end"], None, None, (0, 0.6, -0.4), 50),
]

# Schwebende 3D-Wörter: rot = Problem, gelb = Lösung
LABELS = [
    ("l-veg", "VEGETABLES?", "g", 0.0, 1.5, 0.0, K["veg"], K["dig"]),
    ("l-soil", "SOIL", "y", 0.0, 0.6, 0.0, K["soil1"], K["rain"]),
    ("l-mud", "MUD!", "r", 0.0, 0.8, 0.0, K["mud"], K["frame"]),
    ("l-frame", "FRAME", "y", 0.0, 0.9, 0.0, K["frame_w"], K["bend"]),
    ("l-back", "BACK PAIN!", "r", 1.25, 2.05, 0.15, K["back"], K["tall"]),
    ("l-90", "90 CM", "y", 0.0, 1.3, 0.0, K["tall90"], K["voles"]),
    ("l-voles", "VOLES!", "r", 0.55, -0.12, 0.55, K["voles_w"], K["mesh"]),
    ("l-mesh", "WIRE MESH", "y", 0.0, 0.32, 0.5, K["mesh_w"], K["rot"]),
    ("l-rot", "ROT!", "r", 0.0, 1.05, -0.45, K["rot_w"], K["foil_w"]),
    ("l-foil", "FOIL", "y", 0.0, 1.05, -0.45, K["foil_w"], K["bottom"]),
    ("l-never", "NOT THE BOTTOM ✕", "r", 0.0, 0.5, 0.0, K["bottom_w"], K["layers"]),
    ("l-wet", "WATERLOGGED!", "b", 0.0, 0.25, 0.3, K["drain"], K["layers"]),
    ("l-layers", "4 LAYERS", "y", 0.0, 1.4, 0.0, K["layers_w"], K["branches"]),
    ("l-br", "BRANCHES · 30 CM", "o", 0.0, 1.4, 0.0, K["branches"], K["leaves_w"]),
    ("l-drain", "DRAINS", "b", 0.0, -0.3, 0.55, K["runs"], K["leaves_w"]),
    ("l-lv", "LEAVES · 15 CM", "o", 0.0, 1.4, 0.0, K["leaves_w"], K["compost_w"]),
    ("l-cp", "COMPOST · 20 CM", "o", 0.0, 1.4, 0.0, K["compost_w"], K["soil_w"]),
    ("l-warm", "WARM!", "r", 0.0, 1.7, 0.3, K["heats"], K["soil_w"]),
    ("l-so", "SOIL · 20 CM", "o", 0.0, 1.4, 0.0, K["soil_w"], K["grow"]),
    ("l-early", "EARLIER START", "g", 0.0, 2.2, 0.0, K["earlier"], K["sink"]),
    ("l-sinks", "SINKS!", "r", 0.0, 1.4, 0.3, K["sinks"], K["topup"]),
    ("l-top", "+ COMPOST", "y", 0.0, 1.4, 0.3, K["topup"], K["end"]),
    ("l-congrats", "CONGRATULATIONS!", "y", 0.0, 2.3, 0.0, K["congrats"], TOTAL),
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

  // Gegrabenes Beet im Rasen (vor dem Rahmen) – sichtbar im Querschnitt
  const patchMat = std({ map: soilT });
  const patch = add(new THREE.Mesh(new THREE.BoxGeometry(2.0, 0.32, 1.0), patchMat), false, true); patch.position.set(0, -0.155, 0.005);
  const puddles = [[-0.5, 0.1, 0.22], [0.35, -0.2, 0.18], [0.6, 0.25, 0.12]].map(([x, z, r]) => {
    const p = add(new THREE.Mesh(new THREE.CircleGeometry(r, 20), new THREE.MeshStandardMaterial({ color: 0x5C7A90, roughness: 0.05, metalness: 0.2 })), false, false);
    p.rotation.x = -Math.PI / 2; p.position.set(x, 0.012, z); return p; });
  // Regen
  const NR = 700, rainBase = [], rainPos = new Float32Array(NR * 6);
  for (let i = 0; i < NR; i++) rainBase.push([rr(-5, 5), rr(0, 7), rr(-3, 4), rr(0.8, 1.2)]);
  const rainGeo = new THREE.BufferGeometry(); rainGeo.setAttribute("position", new THREE.BufferAttribute(rainPos, 3));
  const rain = new THREE.LineSegments(rainGeo, new THREE.LineBasicMaterial({ color: 0xBFD4E8, transparent: true, opacity: 0.7 }));
  rain.frustumCulled = false; scene.add(rain);
  const greySky = tex(16, 512, 21, (g, r, w, h) => { const gr = g.createLinearGradient(0, 0, 0, h);
    gr.addColorStop(0, "#59626E"); gr.addColorStop(1, "#A9B2BC"); g.fillStyle = gr; g.fillRect(0, 0, w, h); });
  // Karotten im Boden (im Querschnitt sichtbar)
  const carrots = [-0.7, -0.35, 0.0, 0.35, 0.7].map((x, i) => { const g = new THREE.Group(); g.position.set(x, 0, 0.51); scene.add(g);
    const root = new THREE.Mesh(new THREE.ConeGeometry(0.045, 0.24, 10), std({ color: 0xE8792A })); root.rotation.x = Math.PI; root.position.y = -0.12; g.add(root);
    for (let k = 0; k < 3; k++) { const lf = new THREE.Mesh(new THREE.ConeGeometry(0.02, 0.18, 5), std({ color: 0x4E9A3A })); lf.position.set((k - 1) * 0.025, 0.09, 0); lf.rotation.z = (k - 1) * 0.35; g.add(lf); }
    return { g, i }; });
  // faulendes Holz
  const woodRotT = tex(256, 64, 22, (g, r, w, h) => { g.drawImage(woodT.image, 0, 0);
    g.fillStyle = "rgba(40,30,20,0.35)"; g.fillRect(0, 0, w, h);
    for (let i = 0; i < 22; i++) { g.fillStyle = ["rgba(35,45,25,0.55)", "rgba(25,22,18,0.6)", "rgba(80,100,50,0.45)"][Math.floor(r() * 3)];
      g.beginPath(); g.ellipse(r() * w, r() * h, 3 + r() * 8, 2 + r() * 5, r() * 3, 0, 6.3); g.fill(); } }, [1, 1]);
  const woodRot = std({ map: woodRotT, roughness: 0.95 });

  // Person neben dem Beet – Oberkörper mit Hüftgelenk, um sich zu bücken
  const person = new THREE.Group(); person.position.set(1.45, 0, 0.1); person.rotation.y = -Math.PI / 2; scene.add(person);
  const upper = new THREE.Group(); upper.position.y = 0.88; person.add(upper);
  { const skin = std({ color: 0xE3B48F }), shirt = std({ color: 0x3C7FA8 }), pants = std({ color: 0x2E3440 });
    for (const s of [-1, 1]) { const lg = new THREE.Mesh(new THREE.CapsuleGeometry(0.07, 0.75, 4, 8), pants); lg.position.set(s * 0.1, 0.45, 0); lg.castShadow = true; person.add(lg);
      const ar = new THREE.Mesh(new THREE.CapsuleGeometry(0.05, 0.55, 4, 8), shirt); ar.position.set(s * 0.27, 0.24, 0.02); ar.rotation.z = s * 0.08; ar.castShadow = true; upper.add(ar); }
    const tor = new THREE.Mesh(new THREE.CapsuleGeometry(0.19, 0.42, 4, 10), shirt); tor.position.y = 0.27; tor.castShadow = true; upper.add(tor);
    const hd = new THREE.Mesh(new THREE.SphereGeometry(0.12, 16, 12), skin); hd.position.y = 0.74; hd.castShadow = true; upper.add(hd);
    const hair = new THREE.Mesh(new THREE.SphereGeometry(0.125, 16, 12, 0, 6.3, 0, 1.4), std({ color: 0x4A3324 })); hair.position.y = 0.76; upper.add(hair); }

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

  function render(t) {
    shotAt(t);
    const after = (x) => t >= x;
    // Himmel/Licht: Regen-Kapitel ist grau
    const rainy = t >= K.rain_w - 0.2 && t < K.frame;
    scene.background = rainy ? greySky : skyT; sun.intensity = rainy ? 0.6 : 2.6;
    scene.fog.color.set(rainy ? 0x9AA3AD : 0xCFE2F3); sunBall.visible = false; footprint.visible = false; arrow.visible = false;
    rain.visible = rainy;
    if (rainy) { for (let i = 0; i < NR; i++) { const [x, y0, z, sp] = rainBase[i], y = 7 - ((7 - y0) + (t - K.rain_w) * 9 * sp) % 7;
      rainPos.set([x, y, z, x - 0.02, y + 0.35, z], i * 6); } rainGeo.attributes.position.needsUpdate = true; }
    // gegrabenes Beet
    const dk = ease((t - K.dig_w) / Math.max(0.3, K.soil1 - K.dig_w + 0.4));
    patch.visible = dk > 0.001; patch.scale.x = Math.max(0.001, dk);
    const muddy = t >= K.mud - 0.3;
    patchMat.color.set(muddy && t < K.tall ? 0xB09A8A : 0xFFFFFF); patchMat.roughness = muddy && t < K.frame ? 0.25 : 0.9;
    puddles.forEach((p, i) => { const k = ease((t - K.mud + 0.3 - i * 0.15) / 0.5); p.visible = t < K.frame && k > 0.01; p.scale.setScalar(Math.max(0.01, k)); });
    // Rahmen: erst niedrig (2 Bretter), dann auf 90 cm (5 Bretter)
    for (const b of boards) {
      const lvl = b.userData.lvl, st = lvl < 2 ? K.frame_w + 0.1 + lvl * 0.35 : K.tall90 - 0.2 + (lvl - 2) * 0.35;
      const k = clamp((t - st) / 0.3, 0, 1);
      b.visible = k > 0; b.position.y = b.userData.y + (1 - outBack(k)) * 0.5;
      b.material = t >= K.rot_w - 0.1 && t < K.foil_w ? woodRot : wood;
    }
    // Person: bückt sich zum niedrigen Beet, richtet sich auf beim hohen
    person.visible = t < K.voles;
    const bendK = ease((t - K.bend_w) / 0.8) * (1 - ease((t - K.tall90 - 0.3) / 0.8));
    upper.rotation.x = bendK * 1.05; person.position.x = 1.45 - 0.12 * bendK;
    // Karotten + Wühlmaus + Gitter
    carrots.forEach((c) => { const eaten = K.carrots + 0.3 + c.i * 0.35; c.g.visible = t >= K.tall && t < K.layers && !(t >= eaten && t < K.mesh_w);
      if (t >= K.mesh_w) c.g.visible = t < K.rot; });
    vole.visible = t >= K.voles && t < K.rot; tunnel.visible = vole.visible;
    { const p = clamp((t - K.voles) / Math.max(0.5, K.mesh_w - K.voles), 0, 1); let x = -1.4 + p * 2.4, y = -0.38;
      if (t >= K.mesh_w + 0.4) { const b = (t - K.mesh_w - 0.4) % 1.0; x = 0.2; y = -0.38 + Math.sin(clamp(b / 0.5, 0, 1) * 3.14) * 0.3; }
      vole.position.set(x, y, 0.56); vole.rotation.z = t >= K.mesh_w + 0.4 ? Math.sin(t * 9) * 0.25 : 0; }
    mesh.visible = t >= K.mesh_w - 0.2; mesh.position.y = 0.01 + (1 - ease((t - K.mesh_w + 0.2) / 0.5)) * 0.8;
    // Folie (Seiten) + falsche Folie unten mit Staunässe
    const fk = ease((t - K.foil_w) / 0.6);
    for (const f of foils) { f.visible = t >= K.foil_w; f.scale.y = Math.max(0.001, fk); f.position.y = 0.425 * fk + (1 - fk) * 0.85; }
    badFoil.visible = t >= K.bottom_w && t < K.layers;
    const wl = t >= K.drain - 0.4 && t < K.layers ? ease((t - K.drain + 0.4) / 1.2) * 0.22 : 0;
    water.visible = wl > 0.001; water.scale.y = Math.max(0.001, wl); water.position.set(0, 0.02 + wl / 2, 0.02);
    allSoil.visible = false;
    // Schichten
    const sink = t >= K.sinks ? ease((t - K.sinks) / 1.4) * 0.1 : 0, sk = (HB - sink) / HB;
    function showLayer(key, t0) { const m = lay[key], [y0, y1] = L[key], k = t >= t0 ? fill(t, t0, 1.0) : 0;
      m.visible = k > 0.001; const a = y0 * sk, b = (y0 + (y1 - y0) * k) * sk; m.scale.y = Math.max(0.001, b - a); m.position.y = (a + b) / 2; }
    showLayer("aeste", K.branches + 1.2); showLayer("laub", K.leaves_w); showLayer("komp", K.compost_w); showLayer("erde", K.soil_w);
    const ek = t >= K.topup ? fill(t, K.topup, 1.0) : 0;
    extraKomp.visible = ek > 0.001; const ea = HB - sink, eb = ea + sink * ek; extraKomp.scale.y = Math.max(0.001, eb - ea); extraKomp.position.y = (ea + eb) / 2;
    sticks.forEach((s) => { const u = s.userData, st = K.branches + u.d * 1.2, k = clamp((t - st) / 0.45, 0, 1);
      s.visible = t >= st && t < K.leaves_w + 0.6; s.position.set(u.x, u.y + (1 - k * k) * 1.4, u.z); s.rotation.set(u.rx, u.ry, u.rz + (1 - k) * 1.5); });
    leaves.forEach((l) => { const u = l.userData, st = K.leaves_w + u.d * 1.0, k = clamp((t - st) / 0.7, 0, 1);
      l.visible = t >= st && t < K.compost_w + 0.6; l.position.set(u.x + Math.sin(k * 6 + u.r) * 0.08 * (1 - k), u.y + (1 - k) * 1.2, u.z); l.rotation.set(-Math.PI / 2 + (1 - k) * Math.sin(u.r * 3) * 1.2, u.r, 0); });
    lumps.forEach((l) => { const u = l.userData, st = K.compost_w + u.d * 0.9, k = clamp((t - st) / 0.4, 0, 1);
      l.visible = t >= st && t < K.soil_w + 0.5; l.position.set(u.x, u.y + (1 - k * k) * 1.2, u.z); });
    drops.forEach((d) => { const u = d.userData, ph = (t - K.runs) / 1.2 + u.o;
      d.visible = t >= K.runs && t < K.leaves_w; d.position.set(u.x, 0.32 - (ph % 1) * 0.75, u.z); });
    const wa = t >= K.heats && t < K.soil_w + 0.6 ? 1 : 0;
    glow.visible = wa > 0; glow.material.opacity = wa * (0.25 + 0.15 * Math.sin(t * 6));
    heat.forEach((h) => { const u = h.userData, ph = ((t - K.heats) * 0.6 + u.o) % 1;
      h.visible = wa > 0; h.position.set(u.x, 0.7 + ph * 0.6, u.z); h.rotation.x = Math.PI / 2; h.material.opacity = Math.sin(ph * 3.14) * 0.9; });
    // Pflanzen: wachsen früh, bei „like crazy“ noch größer
    const pk = ["tomate", "zucchini", "kohl"];
    plants.forEach((p, i) => { const st = K.earlier - 0.3 + i * 0.12, k = t >= K.grow ? outBack((t - st) / 0.6) : 0, boost = 1 + 0.45 * ease((t - K.crazy) / 0.8);
      p.g.visible = k > 0.001; p.g.scale.setScalar(Math.max(0.001, k * boost)); p.g.position.y = HB - sink + sink * ek; });

    renderer.render(scene, camera);

    LABELS.forEach((l, i) => { const el = labelEls[i]; v3.set(l[3], l[4], l[5]).project(camera);
      const on = t >= l[6] && t < l[7] && v3.z < 1;
      el.style.display = on ? "block" : "none";
      if (on) { el.style.left = ((v3.x + 1) / 2 * W) + "px"; el.style.top = ((1 - v3.y) / 2 * H) + "px"; } });
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
for key, f, v in [("mud", "error.mp3", 0.35), ("back", "error.mp3", 0.3), ("voles_w", "glitch-1.mp3", 0.2), ("rot_w", "error.mp3", 0.3),
                  ("bottom_w", "error.mp3", 0.3), ("mesh_w", "click.mp3", 0.4), ("foil_w", "whoosh.mp3", 0.3), ("soil1", "pop.mp3", 0.4),
                  ("branches", "impact-bass-2.mp3", 0.3), ("leaves_w", "whoosh.mp3", 0.25), ("compost_w", "impact-bass-2.mp3", 0.3),
                  ("soil_w", "impact-bass-2.mp3", 0.3), ("earlier", "pop.mp3", 0.4), ("crazy", "sparkle.mp3", 0.35), ("topup", "pop.mp3", 0.4),
                  ("congrats", "sparkle.mp3", 0.5)]:
    SFX.append((K[key], f, v))
SFX += [(K["frame_w"] + 0.1 + i * 0.35 + 0.25, "click-soft.mp3", 0.5) for i in range(2)]
SFX += [(K["tall90"] - 0.2 + i * 0.35 + 0.25, "click-soft.mp3", 0.5) for i in range(3)]


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
    <title>How to build a raised bed the right way</title>
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
