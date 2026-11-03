#!/usr/bin/env python3
"""Builds "How to lay a lawn from scratch" (English) – same structure as videos/07–11:
one growing world (new lawn next to the house, ground cut open at the front), a chain of problem → fix (red problem words,
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
TITLE = "How to lay a lawn from scratch"

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
    "lawn_w": word("want", "lawn"), "weeds": word("throw", "weeds"), "nothing": word("throw", "Nothing"),
    "clear_w": word("clear", "clear"), "loosen": word("clear", "loosen"), "cm": word("clear", "15"),
    "bumpy": word("bumps", "bumpy"), "hollows": word("bumps", "hollows"), "rake1": word("bumps", "rake"), "roll1": word("bumps", "roll"),
    "spread": word("seed", "spread"), "cross": word("seed", "crosswise"), "rake2": word("seed", "rake"), "roll2": word("seed", "roll"),
    "dry_w": word("dry", "dry"), "water_w": word("dry", "water"), "every": word("dry", "every"), "grass_up": word("dry", "grass"),
    "early": word("walk", "early"), "rope": word("walk", "rope"), "weeks": word("walk", "weeks"),
    "ten": word("mow", "ten"), "mow_w": word("mow", "mow"), "third": word("mow", "third"),
    "congrats": word("end", "Congratulations"), "green_end": word("end", "green"),
})
# (Start, Kamera von, Kamera nach, Ziel, FOV); None = Kamerafahrt
SHOTS = [
    (K["want"], (4.2, 2.2, 6.0), (3.5, 1.9, 5.3), (0.4, 0.3, -0.8), 50),
    (K["throw"], (1.9, 1.05, 3.1), (1.55, 0.9, 2.7), (0.4, 0.0, -0.5), 50),
    (K["clear"], (1.0, 0.4, 2.5), (0.8, 0.32, 2.15), (0.4, -0.08, 0.0), 50),
    (K["bumps"], (2.5, 0.85, 3.3), (2.15, 0.72, 2.9), (0.4, 0.0, -0.6), 50),
    (K["seed"], (1.7, 1.35, 2.9), (1.35, 1.15, 2.5), (0.4, 0.0, -0.7), 50),
    (K["dry"], (1.0, 0.5, 2.3), (0.85, 0.44, 2.0), (0.4, 0.0, -0.2), 50),
    (K["walk"], (2.6, 1.3, 3.6), (2.2, 1.1, 3.1), (0.4, 0.1, -0.7), 50),
    (K["mow"], (2.2, 0.6, 2.9), (1.9, 0.5, 2.5), (0.5, 0.05, -0.5), 50),
    (K["end"], None, None, (0.4, 0.3, -0.8), 50),
]

# Schwebende 3D-Wörter: rot = Problem, gelb = Lösung
LABELS = [
    ("l-lawn", "PERFECT LAWN?", "g", 0.4, 0.8, -0.6, K["lawn_w"], K["throw"]),
    ("l-weeds", "SEED ON WEEDS", "r", 0.4, 0.4, -0.5, K["weeds"] - 0.3, K["nothing"]),
    ("l-nothing", "NOTHING GROWS!", "r", 0.4, 0.4, -0.5, K["nothing"], K["clear"]),
    ("l-clear", "WEEDS OUT", "y", 0.4, 0.35, -0.3, K["clear_w"], K["cm"]),
    ("l-cm", "LOOSEN 15 CM", "y", 0.4, -0.08, 0.5, K["cm"] - 0.3, K["bumps"]),
    ("l-bumpy", "PUDDLES!", "r", 0.6, 0.35, -0.5, K["bumpy"] - 0.2, K["rake1"]),
    ("l-level", "RAKE + ROLL", "y", 0.4, 0.4, -0.5, K["rake1"], K["seed"]),
    ("l-cross", "SPREAD CROSSWISE", "y", 0.4, 0.5, -0.6, K["cross"] - 0.3, K["dry"]),
    ("l-dry", "DRIED OUT!", "r", 0.4, 0.3, -0.2, K["dry_w"] - 0.2, K["every"]),
    ("l-water", "WATER DAILY", "b", 0.4, 0.45, -0.2, K["every"], K["walk"]),
    ("l-early", "TOO EARLY!", "r", 0.4, 0.5, -0.7, K["early"] - 0.3, K["rope"]),
    ("l-rope", "KEEP OFF · FEW WEEKS", "y", 0.4, 0.55, -0.7, K["rope"], K["mow"]),
    ("l-ten", "10 CM", "y", 0.4, 0.35, -0.3, K["ten"], K["mow_w"]),
    ("l-third", "TOP 1/3 ONLY", "y", 0.4, 0.35, -0.3, K["third"] - 0.3, K["end"]),
    ("l-congrats", "CONGRATULATIONS!", "y", 0.4, 1.6, -0.8, K["congrats"], TOTAL),
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




  // ---------- Rasenfläche (x LX0..LX1, z LZ0..LZ1; Front = Schnittkante)
  const LX0 = -1.2, LX1 = 2.0, LZ0 = -2.0, LZ1 = 0.5, LW = LX1 - LX0, LD = LZ1 - LZ0;
  const bareT = tex(256, 256, 71, (g, r, w, h) => { g.fillStyle = "#4A3424"; g.fillRect(0, 0, w, h); speck(g, r, w, h, 2400, ["#3A281B", "#5A402C", "#664A33", "#2E2016"], 1, 3); }, [4, 3]);
  const patchT = tex(256, 256, 72, (g, r, w, h) => { g.fillStyle = "#5C4A30"; g.fillRect(0, 0, w, h); speck(g, r, w, h, 1600, ["#4A3424", "#6B5A3A", "#6E8A3A", "#56702E"], 2, 7); }, [3, 2]);
  const compactT = tex(512, 64, 73, (g, r, w, h) => { g.fillStyle = "#6A5038"; g.fillRect(0, 0, w, h);
    for (let y = 2; y < h; y += 5) { g.fillStyle = ["#5A4430", "#76593E", "#4E3A28"][Math.floor(r() * 3)]; g.fillRect(0, y, w, 2); } }, [3, 1]);
  const looseT = tex(512, 64, 74, (g, r, w, h) => { g.fillStyle = "#3A281B"; g.fillRect(0, 0, w, h); speck(g, r, w, h, 900, ["#5A402C", "#2A1C12", "#6B4C33", "#4A3424"], 2, 6);
    speck(g, r, w, h, 120, ["#1A110B"], 1.5, 3); }, [3, 1]);
  // Oberfläche als verformbares Gitter (Buckel / Mulden)
  const surfG = new THREE.PlaneGeometry(LW, LD, 48, 36); surfG.rotateX(-Math.PI / 2);
  const sp = surfG.attributes.position, baseXZ = [];
  for (let i = 0; i < sp.count; i++) baseXZ.push([sp.getX(i), sp.getZ(i)]);
  const bumpF = (x, z) => 0.08 + 0.05 * Math.sin(x * 3.1 + 0.7) * Math.cos(z * 2.6) + 0.03 * Math.sin(x * 7.3 + z * 4.1);
  const surfM = std({ map: patchT, roughness: 0.95 });
  const surf = add(new THREE.Mesh(surfG, surfM), false, true); surf.position.set((LX0 + LX1) / 2, 0.006, (LZ0 + LZ1) / 2);
  // Schürze an der Schnittkante (folgt der Buckel-Oberkante)
  const NSK = 49, skPos = new Float32Array(NSK * 2 * 3), skIdx = [];
  for (let i = 0; i < NSK - 1; i++) { const a = i * 2; skIdx.push(a, a + 1, a + 2, a + 1, a + 3, a + 2); }
  const skG = new THREE.BufferGeometry(); skG.setAttribute("position", new THREE.BufferAttribute(skPos, 3)); skG.setIndex(skIdx);
  const skirt = add(new THREE.Mesh(skG, new THREE.MeshBasicMaterial({ color: 0x3A281B, side: THREE.DoubleSide })), false, false); skirt.frustumCulled = false;
  const puddles = [[-0.73, 0.1], [0.28, -1.21], [1.29, 0.1]].map(([x, z]) => {
    const p = add(new THREE.Mesh(new THREE.CircleGeometry(0.22, 24), new THREE.MeshStandardMaterial({ color: 0x4A8ED0, roughness: 0.05, transparent: true, opacity: 0.85 })), false, false);
    p.rotation.x = -Math.PI / 2; p.userData = { x, z }; return p; });
  // Schnitt: oberste 15 cm verdichtet → gelockert; Wurzeln
  const sec = (mat, z) => { const m = add(new THREE.Mesh(new THREE.PlaneGeometry(1, 1), mat), false, false); m.position.z = z; return m; };
  function rect(m, x0, x1, y0, y1) { const ok = x1 - x0 > 0.002 && y1 - y0 > 0.002; m.visible = ok;
    if (ok) { m.scale.set(x1 - x0, y1 - y0, 1); m.position.x = (x0 + x1) / 2; m.position.y = (y0 + y1) / 2; } }
  const compSec = sec(std({ map: compactT }), 0.503), looseSec = sec(std({ map: looseT }), 0.504);
  const roots = [];
  for (let i = 0; i < 60; i++) { const m = add(new THREE.Mesh(new THREE.PlaneGeometry(0.006, 1), new THREE.MeshBasicMaterial({ color: 0xE6D2A8 })), false, false);
    m.userData = { x: rr(LX0 + 0.05, LX1 - 0.05), L: rr(0.06, 0.13), a: rr(-0.3, 0.3) }; m.position.z = 0.506; roots.push(m); }
  // Unkraut
  const weeds = [];
  for (let i = 0; i < 30; i++) { const g = new THREE.Group(); g.position.set(rr(LX0 + 0.1, LX1 - 0.1), 0.0, rr(LZ0 + 0.1, LZ1 - 0.1)); scene.add(g);
    const kind = i % 3;
    if (kind === 0) { for (let k = 0; k < 6; k++) { const lf = new THREE.Mesh(new THREE.ConeGeometry(0.025, 0.16, 4), std({ color: 0x4F7A2A, flatShading: true }));
        lf.rotation.set(Math.PI / 2 - 0.25, 0, 0); lf.rotation.y = k; const p = new THREE.Group(); p.rotation.y = k * 1.05; lf.position.z = 0.07; p.add(lf); g.add(p); }
      const st = new THREE.Mesh(new THREE.CylinderGeometry(0.004, 0.004, 0.18, 5), std({ color: 0x5C8A33 })); st.position.y = 0.09; g.add(st);
      const fl = new THREE.Mesh(new THREE.SphereGeometry(0.03, 10, 8), std({ color: 0xF2C514 })); fl.position.y = 0.19; g.add(fl); }
    else { for (let k = 0; k < 7; k++) { const b = new THREE.Mesh(new THREE.ConeGeometry(0.012, rr(0.15, 0.3), 4), std({ color: [0x6E8A33, 0x8A9A3A][k % 2], flatShading: true }));
        b.position.set(rr(-0.04, 0.04), 0.1, rr(-0.04, 0.04)); b.rotation.set(rr(-0.4, 0.4), 0, rr(-0.4, 0.4)); g.add(b); } }
    g.traverse((o) => { o.castShadow = true; }); g.userData = { o: R() }; weeds.push(g); }
  // Saatkörner (InstancedMesh) und Grashalme
  const NS = 500, seeds = new THREE.InstancedMesh(new THREE.SphereGeometry(0.007, 5, 4), std({ color: 0xD9C27A }), NS);
  seeds.frustumCulled = false; scene.add(seeds);
  const seedP = []; for (let i = 0; i < NS; i++) seedP.push([rr(LX0, LX1), rr(LZ0, LZ1), R(), R()]);
  const NB = 2600, blades = new THREE.InstancedMesh(new THREE.ConeGeometry(0.006, 1, 3), std({ color: 0x5E9A36, roughness: 0.8 }), NB);
  blades.frustumCulled = false; blades.castShadow = false; blades.receiveShadow = true; scene.add(blades);
  const bladeP = []; for (let i = 0; i < NB; i++) bladeP.push([rr(LX0 + 0.01, LX1 - 0.01), rr(LZ0 + 0.01, LZ1 - 0.01), R(), rr(-0.25, 0.25), rr(-0.25, 0.25)]);
  const bc = new THREE.Color(); bladeP.forEach((b, i) => blades.setColorAt(i, bc.setHSL(0.27 + b[2] * 0.05, 0.6, 0.4 + b[2] * 0.14)));
  const dummy = new THREE.Object3D();
  // Geräte: Rechen, Walze, Streuwagen, Regner, Mäher; Absperrung; Fußspuren
  const rake = new THREE.Group(); scene.add(rake);
  { const h = new THREE.Mesh(new THREE.CylinderGeometry(0.014, 0.014, 1.4, 8), std({ map: woodT })); h.rotation.x = 0.9; h.position.set(0, 0.45, 0.5); rake.add(h);
    const hd = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.03, 0.03), std({ color: 0x777C82, metalness: 0.6 })); rake.add(hd);
    for (let i = 0; i < 12; i++) { const t = new THREE.Mesh(new THREE.BoxGeometry(0.008, 0.06, 0.008), std({ color: 0x777C82, metalness: 0.6 })); t.position.set(-0.23 + i * 0.042, -0.03, 0); rake.add(t); } }
  const roller = new THREE.Group(); scene.add(roller);
  { const c = new THREE.Mesh(new THREE.CylinderGeometry(0.15, 0.15, 0.6, 20), std({ color: 0x3E7A4A, metalness: 0.3, roughness: 0.5 })); c.rotation.x = Math.PI / 2; c.position.y = 0.15; c.castShadow = true; roller.add(c);
    const h = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 1.1, 8), std({ color: 0x333333 })); h.rotation.z = 1.0; h.position.set(-0.45, 0.5, 0); roller.add(h); }
  const spreader = new THREE.Group(); scene.add(spreader);
  { const b = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.1, 0.22, 16), std({ color: 0xE24A2E, roughness: 0.5 })); b.position.y = 0.32; b.castShadow = true; spreader.add(b);
    for (const s of [-1, 1]) { const w = new THREE.Mesh(new THREE.CylinderGeometry(0.07, 0.07, 0.03, 14), std({ color: 0x222222 })); w.rotation.x = Math.PI / 2; w.position.set(0, 0.07, s * 0.14); spreader.add(w); }
    const h = new THREE.Mesh(new THREE.CylinderGeometry(0.01, 0.01, 0.9, 8), std({ color: 0x333333 })); h.rotation.z = 1.0; h.position.set(-0.35, 0.6, 0); spreader.add(h); }
  const crossA = new THREE.Group(); scene.add(crossA);
  for (const rot of [0, Math.PI / 2]) { const m = new THREE.MeshBasicMaterial({ color: 0xFFD23F }); const g = new THREE.Group(); g.rotation.y = rot;
    const sh = new THREE.Mesh(new THREE.BoxGeometry(1.6, 0.01, 0.05), m); g.add(sh);
    for (const s of [-1, 1]) { const hd = new THREE.Mesh(new THREE.ConeGeometry(0.08, 0.18, 3), m); hd.rotation.z = -s * Math.PI / 2; hd.position.x = s * 0.85; g.add(hd); } crossA.add(g); }
  crossA.position.set(0.4, 0.04, -0.75);
  const sprk = new THREE.Group(); sprk.position.set(0.4, 0, -0.75); scene.add(sprk);
  { const p = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.03, 0.18, 10), std({ color: 0xF2B51A })); p.position.y = 0.09; sprk.add(p); }
  const wdrops = [];
  for (let i = 0; i < 60; i++) { const d = add(new THREE.Mesh(new THREE.SphereGeometry(0.012, 6, 5), new THREE.MeshStandardMaterial({ color: 0x6FB8F5, roughness: 0.1 })), false, false);
    d.userData = { a: R() * 6.28, o: R(), r: rr(0.6, 1.4) }; wdrops.push(d); }
  const mower = new THREE.Group(); scene.add(mower);
  { const b = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.14, 0.4), std({ color: 0xD32F2F, roughness: 0.5 })); b.position.y = 0.13; b.castShadow = true; mower.add(b);
    const e = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.1, 0.12, 14), std({ color: 0x333333 })); e.position.y = 0.26; mower.add(e);
    for (const [x, z] of [[-0.17, -0.18], [0.17, -0.18], [-0.17, 0.18], [0.17, 0.18]]) { const w = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 0.03, 12), std({ color: 0x222222 })); w.rotation.x = Math.PI / 2; w.position.set(x, 0.05, z); mower.add(w); }
    const h = new THREE.Mesh(new THREE.CylinderGeometry(0.01, 0.01, 0.9, 8), std({ color: 0x333333 })); h.rotation.z = 0.95; h.position.set(-0.4, 0.5, 0); mower.add(h); }
  const rope = new THREE.Group(); scene.add(rope);
  { const pm = std({ map: woodT }), rm = new THREE.MeshBasicMaterial({ color: 0xF2D23A });
    const cs = [[LX0 - 0.05, LZ1 - 0.05], [LX1 + 0.05, LZ1 - 0.05], [LX1 + 0.05, LZ0 - 0.05], [LX0 - 0.05, LZ0 - 0.05]];
    cs.forEach(([x, z], i) => { const p = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.45, 0.04), pm); p.position.set(x, 0.22, z); p.castShadow = true; rope.add(p);
      const [x2, z2] = cs[(i + 1) % 4], len = Math.hypot(x2 - x, z2 - z); const r = new THREE.Mesh(new THREE.BoxGeometry(len, 0.012, 0.012), rm);
      r.position.set((x + x2) / 2, 0.38, (z + z2) / 2); r.rotation.y = -Math.atan2(z2 - z, x2 - x); rope.add(r); }); }
  const steps = [];
  for (let i = 0; i < 10; i++) { const s = add(new THREE.Mesh(new THREE.CircleGeometry(1, 16), new THREE.MeshBasicMaterial({ color: 0x3A2A1A, transparent: true, opacity: 0.85 })), false, false);
    s.rotation.x = -Math.PI / 2; s.scale.set(0.05, 0.11, 1); s.position.set(-1.0 + i * 0.3, 0.02, -0.5 + (i % 2) * 0.16); steps.push(s); }
  // Person (Anfang: Samen werfen; später läuft jemand drüber)
  const person = new THREE.Group(); scene.add(person);
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
    if (!s[1]) { const a = 0.5 - p * 0.55, r = 5.4; camera.position.set(Math.sin(a) * r + 0.4, 2.0 + p * 0.3, Math.cos(a) * r - 0.8); }
    else camera.position.set(s[1][0] + (s[2][0] - s[1][0]) * p, s[1][1] + (s[2][1] - s[1][1]) * p, s[1][2] + (s[2][2] - s[1][2]) * p);
    look.set(s[3][0], s[3][1], s[3][2]); camera.fov = s[4]; camera.updateProjectionMatrix(); camera.lookAt(look);
  }
  const E = (t, t0, d) => ease((t - t0) / (d || 0.6));
  const sweep = (t, t0, t1) => clamp((t - t0) / (t1 - t0), 0, 1);

  function render(t) {
    shotAt(t);
    // Oberfläche: fleckig → nackte Erde (gelockert) → mit Buckeln → glatt; trocken heller
    const clearK = E(t, K.clear_w, 0.6), bump = E(t, K.bumpy - 0.4, 0.6) * (1 - E(t, K.rake1, 1.4));
    surfM.map = t >= K.walk ? grassT : clearK > 0.5 ? bareT : patchT; surf.position.y = 0.006;
    for (let i = 0; i < sp.count; i++) { const [x, z] = baseXZ[i]; sp.setY(i, bump * bumpF(x, z)); } sp.needsUpdate = true; surfG.computeVertexNormals();
    for (let i = 0; i < NSK; i++) { const x = LX0 + LW * i / (NSK - 1), h = 0.006 + bump * bumpF(x - (LX0 + LX1) / 2, LD / 2);
      skPos.set([x, h, 0.505, x, 0, 0.505], i * 6); } skG.attributes.position.needsUpdate = true; skirt.visible = bump > 0.01;
    const dryK = E(t, K.dry_w - 0.4, 0.8) * (1 - E(t, K.every, 1.2));
    surfM.color.set(0xFFFFFF).lerp(new THREE.Color(0xE8C9A0), dryK);
    puddles.forEach((p) => { const k = E(t, K.hollows - 0.3, 0.6) * (1 - E(t, K.rake1, 0.8)); p.visible = k > 0.01;
      p.scale.setScalar(Math.max(0.01, k)); p.position.set(p.userData.x + 0.0, 0.006 + bump * bumpF(p.userData.x, p.userData.z) + 0.012, p.userData.z); });
    // Schnitt: verdichtet bis "loosen", dann locker
    const lk = E(t, K.loosen, 0.9);
    rect(compSec, LX0, LX1, -0.15, 0); compSec.visible = lk < 0.99;
    rect(looseSec, LX0, LX0 + LW * lk, -0.15, 0); if (lk < 0.01) looseSec.visible = false;
    // Unkraut weg
    weeds.forEach((g) => { const k = E(t, K.clear_w - 0.2 + g.userData.o * 0.5, 0.35); g.visible = k < 0.99; g.scale.setScalar(Math.max(0.01, 1 - k)); g.position.y = k * 0.3; });
    // Saat: erst auf das Unkraut geworfen (verschwindet), dann kreuzweise gestreut, trocknet, keimt
    let seedVis = 0;
    seedP.forEach((s, i) => { let vis = false, y = 0.012;
      if (t >= K.throw && t < K.clear_w) { const k = E(t, K.throw + 0.3 + s[2] * 0.6, 0.3); vis = k > 0.01 && t < K.nothing + 0.6 + s[3]; y = 0.012 + (1 - k) * 0.5; }
      else if (t >= K.spread && t < K.grass_up + 0.5) { const pass = s[3] < 0.5 ? sweep(t, K.spread, K.cross + 0.3) : sweep(t, K.cross + 0.2, K.rake2);
        const pos = s[3] < 0.5 ? (s[0] - LX0) / LW : (LZ1 - s[1]) / LD; vis = pos < pass; }
      dummy.position.set(s[0], y, s[1]); dummy.scale.setScalar(vis ? 1 : 0.0001); dummy.updateMatrix(); seeds.setMatrixAt(i, dummy.matrix); if (vis) seedVis++; });
    seeds.instanceMatrix.needsUpdate = true;
    // Gras keimt, wächst auf 10 cm; Trampelpfad; Mähen auf 2/3
    const grow = E(t, K.water_w + 0.6, 2.6), toTen = E(t, K.ten - 0.6, 0.8);
    let H = 0.012 + 0.04 * grow + 0.05 * toTen; const mowX = LX0 - 0.3 + (LW + 0.6) * sweep(t, K.mow_w - 0.2, K.third + 0.4);
    const trampled = E(t, K.early - 0.5, 0.5) * (1 - E(t, K.rope + 0.5, 1.5));
    bladeP.forEach((b, i) => { let h = H * (0.75 + 0.5 * b[2]); const on = t >= K.water_w + 0.6;
      if (t >= K.mow_w - 0.2 && b[0] < mowX) h *= 0.66; if (t >= K.end) h = Math.max(h, 0.07 * (0.75 + 0.5 * b[2]));
      const nearPath = Math.abs(b[1] - (-0.42)) < 0.18 && trampled > 0; const flat = nearPath ? trampled : 0;
      dummy.position.set(b[0], h / 2 * (1 - flat * 0.7), b[1]); dummy.rotation.set(b[3] + flat * 1.2, 0, b[4]); dummy.scale.set(1, on ? h : 0.0001, 1); dummy.updateMatrix(); blades.setMatrixAt(i, dummy.matrix); });
    blades.instanceMatrix.needsUpdate = true;
    if (t >= K.grass_up && t < K.walk) surfM.color.lerp(new THREE.Color(0x6E8A4A), E(t, K.grass_up, 2.0) * 0.6);
    // Wurzeln im Schnitt
    const rk = E(t, K.water_w + 0.8, 3.0);
    roots.forEach((m) => { const u = m.userData, L = u.L * rk; m.visible = L > 0.004; m.scale.y = Math.max(0.001, L); m.rotation.z = u.a; m.position.set(u.x + Math.sin(u.a) * L / 2, -L / 2, 0.506); });
    // Geräte
    const rakeOn = t >= K.rake1 - 0.2 && t < K.roll1 + 0.2 || t >= K.rake2 - 0.2 && t < K.roll2;
    rake.visible = rakeOn; if (rakeOn) { const ph = t * 1.8; rake.position.set(0.4 + Math.sin(ph) * 0.8, 0.04, -0.75 + Math.sin(ph * 0.5) * 0.6); }
    const rollOn = t >= K.roll1 - 0.1 && t < K.seed || t >= K.roll2 - 0.1 && t < K.dry;
    roller.visible = rollOn; if (rollOn) { const t0 = t < K.seed ? K.roll1 : K.roll2, k = sweep(t, t0 - 0.1, t0 + 1.3); roller.position.set(LX0 + 0.2 + k * (LW - 0.4), 0, -0.75 + Math.sin(k * 9) * 0.5); }
    const spOn = t >= K.spread - 0.1 && t < K.rake2;
    spreader.visible = spOn; if (spOn) { if (t < K.cross + 0.2) spreader.position.set(LX0 + LW * sweep(t, K.spread, K.cross + 0.3), 0, -0.2); else { spreader.position.set(0.9, 0, LZ1 - LD * sweep(t, K.cross + 0.2, K.rake2)); } spreader.rotation.y = t < K.cross + 0.2 ? 0 : Math.PI / 2; }
    crossA.visible = t >= K.cross - 0.3 && t < K.rake2;
    const wOn = t >= K.water_w - 0.1 && t < K.walk; sprk.visible = wOn;
    wdrops.forEach((d) => { const u = d.userData, ph = ((t - K.water_w) * 0.9 + u.o) % 1; d.visible = wOn;
      d.position.set(0.4 + Math.cos(u.a) * u.r * ph, 0.18 + Math.sin(Math.PI * ph) * 0.45, -0.75 + Math.sin(u.a) * u.r * ph * 0.8); });
    const mOn = t >= K.mow_w - 0.3 && t < K.end; mower.visible = mOn; if (mOn) mower.position.set(mowX, 0, -0.5);
    rope.visible = t >= K.rope - 0.1; rope.position.y = (1 - E(t, K.rope - 0.1, 0.4)) * 0.6;
    steps.forEach((s, i) => { s.visible = t >= K.early - 0.6 + i * 0.08 && t < K.weeks; });
    // Person: wirft Samen am Anfang, läuft später über den Rasen
    const walkOn = t >= K.walk && t < K.rope;
    person.visible = t < K.clear || walkOn;
    if (t < K.clear) { person.position.set(1.4, 0, -1.3); person.rotation.y = -0.8; }
    else { const k = sweep(t, K.walk, K.rope + 0.1); person.position.set(-1.3 + k * 3.4, 0, -0.42); person.rotation.y = Math.PI / 2; }
    sunBall.visible = false;

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
for key, f, v in [("nothing", "error.mp3", 0.35), ("bumpy", "error.mp3", 0.3), ("dry_w", "error.mp3", 0.3), ("early", "error.mp3", 0.3),
                  ("clear_w", "whoosh.mp3", 0.3), ("loosen", "impact-bass-2.mp3", 0.3), ("rake1", "pop.mp3", 0.35), ("roll1", "impact-bass-1.mp3", 0.25),
                  ("cross", "pop.mp3", 0.4), ("every", "pop.mp3", 0.4), ("rope", "click.mp3", 0.4), ("mow_w", "glitch-1.mp3", 0.15),
                  ("third", "pop.mp3", 0.4), ("green_end", "sparkle.mp3", 0.4), ("congrats", "sparkle.mp3", 0.5)]:
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
