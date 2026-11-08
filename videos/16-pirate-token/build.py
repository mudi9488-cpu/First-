#!/usr/bin/env python3
"""Builds "The Pirate Token" (English) – blocky-3D storytime in the style of references/storytime.md:
"In this town …" hook, first-person narrator (Leo), a hard cut on every voice line (~85 shots),
one word per caption (neon yellow, Lilita One), diegetic text (billboard, clock, phone), cliffhanger ending.

1. Stimme: python3 ../../tools/tts.py .  (Platzhalter Piper en-us-ryan-high)
   oder eigene Aufnahme: python3 ../../tools/align.py . assets/source/<datei>.mp3
2. python3 build.py
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "tools"))
from simkit import load_timings, fmt, audio_len  # noqa: E402

SFX_ROOT = Path.home() / ".claude/plugins/cache/hyperframes/hyperframes/0.9.25/skills/media-use/audio/assets/sfx"
W, H = 1080, 1920
TITLE = "The Pirate Token"

T = load_timings(HERE)
LINES = [l for b in T["beats"] for l in b["lines"]]
VOICE_END = T["beats"][-1]["end"]
TOTAL = round(VOICE_END + 1.4, 2)
# Shot i startet kurz vor Zeile i (harter Schnitt pro Sprechzeile)
LS = [0.0] + [round(l["start"] - 0.08, 3) for l in LINES[1:]]
assert len(LS) == 85, len(LS)

WORLD_JS = r"""
const LS = __LS__, DUR = __DUR__;
window.__hf = window.__hf || {}; window.__hf.buildReady = window.__hf.buildReady || {};
window.__hf.buildReady.world = import("./assets/three.module.min.js").then((THREE) => {
  const W = 1080, H = 1920, HX = 200, RX = -200, VZ = 400;
  const canvas = document.getElementById("w-canvas");
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1); renderer.setSize(W, H, false);
  renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.1;

  function mulberry(a) { return function () { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
  const R = mulberry(7);
  const rr = (a, b) => a + (b - a) * R();
  const pick = (arr) => arr[Math.floor(R() * arr.length)];
  const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
  const ease = (x) => { x = clamp(x, 0, 1); return x * x * (3 - 2 * x); };
  const outBack = (x) => { x = clamp(x, 0, 1); const c = 1.7; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
  const D2R = Math.PI / 180;

  // ---------- Texturen
  function cv(w, h) { const c = document.createElement("canvas"); c.width = w; c.height = h; return c; }
  function tex(w, h, seed, draw, rep) {
    const c = cv(w, h); const g = c.getContext("2d"); draw(g, mulberry(seed), w, h);
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace;
    t.wrapS = t.wrapT = THREE.RepeatWrapping; if (rep) t.repeat.set(rep[0], rep[1]); t.anisotropy = 4; return t;
  }
  const speck = (g, r, w, h, n, cols, s0, s1) => { for (let i = 0; i < n; i++) { g.fillStyle = cols[Math.floor(r() * cols.length)];
    const s = s0 + r() * (s1 - s0); g.fillRect(r() * w, r() * h, s, s); } };
  const grassT = tex(256, 256, 1, (g, r, w, h) => { g.fillStyle = "#5FA83A"; g.fillRect(0, 0, w, h); speck(g, r, w, h, 2500, ["#559C33", "#6BB544", "#4E9030"], 2, 5); }, [30, 30]);
  const roadT = tex(256, 256, 2, (g, r, w, h) => { g.fillStyle = "#3A3F4B"; g.fillRect(0, 0, w, h); speck(g, r, w, h, 1500, ["#343944", "#424854", "#2F333D"], 1, 3);
    g.fillStyle = "#F2C230"; g.fillRect(w / 2 - 4, 0, 8, h * 0.55); }, [1, 20]);
  const walkT = tex(128, 128, 3, (g, r, w, h) => { g.fillStyle = "#C9CCD3"; g.fillRect(0, 0, w, h); speck(g, r, w, h, 400, ["#BFC2C9", "#D3D6DC"], 1, 3);
    g.strokeStyle = "#A9ADB6"; g.lineWidth = 3; g.strokeRect(0, 0, w, h); }, [2, 40]);
  const woodT = tex(256, 128, 4, (g, r, w, h) => { g.fillStyle = "#9A5F2E"; g.fillRect(0, 0, w, h);
    for (let i = 0; i < 36; i++) { g.strokeStyle = ["#87512A", "#AE6F3A", "#7A4723"][Math.floor(r() * 3)]; g.lineWidth = 1 + r() * 2;
      const y = r() * h; g.beginPath(); g.moveTo(0, y); g.bezierCurveTo(w * 0.3, y + (r() - 0.5) * 8, w * 0.7, y + (r() - 0.5) * 8, w, y); g.stroke(); }
    g.fillStyle = "rgba(50,25,10,0.55)"; for (let y = 0; y < h; y += 32) g.fillRect(0, y, w, 3); }, [1, 1]);
  const floorT = tex(256, 256, 5, (g, r, w, h) => { g.fillStyle = "#C88F55"; g.fillRect(0, 0, w, h);
    for (let y = 0; y < h; y += 32) { g.fillStyle = ["#C0854B", "#D29C62", "#B97D45"][Math.floor(r() * 3)]; g.fillRect(0, y, w, 30); g.fillStyle = "rgba(80,45,15,0.5)"; g.fillRect(0, y + 30, w, 2);
      g.fillRect(Math.floor(r() * w), y, 2, 30); } }, [4, 4]);
  const hallFloorT = tex(256, 256, 6, (g, r, w, h) => { for (let y = 0; y < 4; y++) for (let x = 0; x < 4; x++) {
    g.fillStyle = (x + y) % 2 ? "#2B2350" : "#352C62"; g.fillRect(x * 64, y * 64, 64, 64); } g.strokeStyle = "#C9A23A"; g.lineWidth = 2;
    for (let i = 0; i <= 256; i += 64) { g.beginPath(); g.moveTo(i, 0); g.lineTo(i, 256); g.stroke(); g.beginPath(); g.moveTo(0, i); g.lineTo(256, i); g.stroke(); } }, [8, 8]);
  const sidingT = (col, seed) => tex(128, 128, seed, (g, r, w, h) => { g.fillStyle = col; g.fillRect(0, 0, w, h);
    for (let y = 0; y < h; y += 16) { g.fillStyle = "rgba(0,0,0,0.13)"; g.fillRect(0, y + 13, w, 3); g.fillStyle = "rgba(255,255,255,0.08)"; g.fillRect(0, y, w, 3); } }, [3, 3]);
  const brickT = tex(256, 256, 8, (g, r, w, h) => { g.fillStyle = "#D8D2C8"; g.fillRect(0, 0, w, h);
    for (let y = 0; y < h; y += 20) for (let x = (y / 20) % 2 * 24; x < w + 48; x += 48) { g.fillStyle = ["#B4553E", "#A84B36", "#BF6249", "#9E4632"][Math.floor(r() * 4)]; g.fillRect(x - 46, y + 2, 44, 16); } }, [3, 3]);
  const roofT = tex(128, 128, 9, (g, r, w, h) => { g.fillStyle = "#4A4F63"; g.fillRect(0, 0, w, h);
    for (let y = 0; y < h; y += 16) { g.fillStyle = "rgba(0,0,0,0.22)"; g.fillRect(0, y, w, 3); } }, [4, 4]);
  const wallpT = tex(128, 128, 10, (g, r, w, h) => { g.fillStyle = "#7FB7D8"; g.fillRect(0, 0, w, h);
    for (let x = 0; x < w; x += 32) { g.fillStyle = "rgba(255,255,255,0.18)"; g.fillRect(x, 0, 12, h); } }, [3, 2]);

  // Gesichter (Klötzchen-Decals)
  const FACE = {};
  function faceTex(ex, o) {
    const key = ex + "|" + (o.glasses ? 1 : 0) + "|" + (o.stache ? 1 : 0) + "|" + (o.blush ? 1 : 0);
    if (FACE[key]) return FACE[key];
    const c = cv(256, 256), g = c.getContext("2d");
    const ink = "#1B1410"; g.lineCap = "round"; g.lineJoin = "round";
    const eye = (x, y, big) => { if (big) { g.fillStyle = "#FFF"; g.beginPath(); g.ellipse(x, y, 26, 30, 0, 0, 6.3); g.fill(); g.lineWidth = 6; g.strokeStyle = ink; g.stroke();
        g.fillStyle = ink; g.beginPath(); g.arc(x, y + 4, 9, 0, 6.3); g.fill(); }
      else { g.fillStyle = ink; g.beginPath(); g.ellipse(x, y, 15, 22, 0, 0, 6.3); g.fill(); g.fillStyle = "#FFF"; g.beginPath(); g.arc(x - 4, y - 8, 5, 0, 6.3); g.fill(); } };
    const happyEye = (x, y) => { g.strokeStyle = ink; g.lineWidth = 9; g.beginPath(); g.arc(x, y + 8, 16, Math.PI * 1.15, Math.PI * 1.85); g.stroke(); };
    const brow = (x, y, a) => { g.strokeStyle = ink; g.lineWidth = 9; g.beginPath(); g.moveTo(x - 20 * Math.cos(a), y - 20 * Math.sin(a)); g.lineTo(x + 20 * Math.cos(a), y + 20 * Math.sin(a)); g.stroke(); };
    const L = 92, Rr = 164, EY = 112;
    const big = ["shock", "scared", "wide"].includes(ex);
    if (ex === "grin" || ex === "evil" && false) { happyEye(L, EY); happyEye(Rr, EY); }
    else if (ex === "evil") { g.fillStyle = ink; g.fillRect(L - 18, EY - 4, 36, 12); g.fillRect(Rr - 18, EY - 4, 36, 12); }
    else if (ex === "sleep") { happyEye(L, EY - 14); }
    else { eye(L, EY, big); eye(Rr, EY, big); }
    if (ex === "angry" || ex === "evil") { brow(L, EY - 38, 0.45); brow(Rr, EY - 38, -0.45); }
    if (ex === "sad" || ex === "cry" || ex === "scared") { brow(L, EY - 40, -0.35); brow(Rr, EY - 40, 0.35); }
    if (ex === "smirk") { brow(L, EY - 36, 0); brow(Rr, EY - 46, -0.25); }
    if (ex === "serious") { brow(L, EY - 36, 0.15); brow(Rr, EY - 36, -0.15); }
    if (ex === "shock" || ex === "wide") { brow(L, EY - 50, -0.15); brow(Rr, EY - 50, 0.15); }
    g.strokeStyle = ink; g.lineWidth = 8; const MY = 182;
    if (ex === "neutral") { g.beginPath(); g.arc(128, MY - 22, 24, 0.25 * Math.PI, 0.75 * Math.PI); g.stroke(); }
    else if (ex === "smile") { g.beginPath(); g.arc(128, MY - 30, 36, 0.2 * Math.PI, 0.8 * Math.PI); g.stroke(); }
    else if (ex === "grin" || ex === "evil") { g.fillStyle = "#5A1414"; g.beginPath(); g.moveTo(80, MY - 14); g.quadraticCurveTo(128, MY + 44, 176, MY - 14); g.closePath(); g.fill();
      g.fillStyle = "#FFF"; g.fillRect(88, MY - 14, 80, 10); }
    else if (ex === "shock") { g.fillStyle = "#5A1414"; g.beginPath(); g.ellipse(128, MY, 16, 22, 0, 0, 6.3); g.fill(); }
    else if (ex === "wide") { g.fillStyle = "#5A1414"; g.beginPath(); g.ellipse(128, MY + 2, 30, 34, 0, 0, 6.3); g.fill(); }
    else if (ex === "sad" || ex === "cry") { g.beginPath(); g.arc(128, MY + 18, 26, 1.2 * Math.PI, 1.8 * Math.PI); g.stroke(); }
    else if (ex === "scared") { g.beginPath(); g.moveTo(96, MY); for (let i = 0; i <= 8; i++) g.lineTo(96 + i * 8, MY + (i % 2 ? -7 : 7)); g.stroke(); }
    else if (ex === "angry") { g.beginPath(); g.arc(128, MY + 22, 28, 1.2 * Math.PI, 1.8 * Math.PI); g.stroke(); }
    else if (ex === "smirk") { g.beginPath(); g.moveTo(100, MY - 2); g.quadraticCurveTo(140, MY + 6, 166, MY - 18); g.stroke(); }
    else if (ex === "serious") { g.beginPath(); g.moveTo(104, MY - 2); g.lineTo(152, MY - 2); g.stroke(); }
    else if (ex === "sleep") { g.beginPath(); g.moveTo(110, MY - 4); g.lineTo(146, MY - 4); g.stroke(); }
    if (ex === "cry") { g.fillStyle = "rgba(80,170,255,0.9)"; g.fillRect(L - 8, EY + 20, 16, 90); g.fillRect(Rr - 8, EY + 20, 16, 90); }
    if (o.blush) { g.fillStyle = "rgba(255,110,110,0.35)"; g.beginPath(); g.ellipse(58, 160, 20, 12, 0, 0, 6.3); g.ellipse(198, 160, 20, 12, 0, 0, 6.3); g.fill(); }
    if (o.glasses) { g.strokeStyle = "#222"; g.lineWidth = 7; g.strokeRect(L - 32, EY - 30, 64, 58); g.strokeRect(Rr - 32, EY - 30, 64, 58); g.beginPath(); g.moveTo(L + 32, EY - 4); g.lineTo(Rr - 32, EY - 4); g.stroke(); }
    if (o.stache) { g.fillStyle = "#2A1A10"; g.beginPath(); g.ellipse(108, MY - 34, 26, 10, 0.2, 0, 6.3); g.ellipse(148, MY - 34, 26, 10, -0.2, 0, 6.3); g.fill(); }
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; FACE[key] = t; return t;
  }

  const std = (o) => new THREE.MeshStandardMaterial(Object.assign({ roughness: 0.75, metalness: 0 }, o));
  const basic = (o) => new THREE.MeshBasicMaterial(o);
  const scene = new THREE.Scene();
  const add = (m, par, cast = true, recv = true) => { m.castShadow = cast; m.receiveShadow = recv; (par || scene).add(m); return m; };
  const box = (w, h, d, mat, x, y, z, par, cast = true) => { const m = add(new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat), par, cast, true); m.position.set(x, y, z); return m; };

  // ---------- Schilder / Bildschirme (Canvas, nur neu zeichnen bei Moduswechsel)
  function screen(w, h, cw, ch, draw, lit = true) {
    const c = cv(cw, ch), g = c.getContext("2d"), t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace;
    const mat = lit ? basic({ map: t, toneMapped: false }) : std({ map: t, roughness: 0.6 });
    const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), mat); let key = null;
    m.userData.set = (k, extra) => { if (k === key) return; key = k; g.clearRect(0, 0, cw, ch); draw(g, k, cw, ch, extra); t.needsUpdate = true; };
    return m;
  }
  const big = (g, txt, x, y, size, col, stroke) => { g.font = `${size}px Lilita, 'Inter', sans-serif`; g.textAlign = "center"; g.textBaseline = "middle";
    if (stroke) { g.lineWidth = size * 0.16; g.strokeStyle = stroke; g.lineJoin = "round"; g.strokeText(txt, x, y); } g.fillStyle = col; g.fillText(txt, x, y); };
  const glowText = (g, txt, x, y, size, col) => { g.save(); g.shadowColor = col; g.shadowBlur = size * 0.35; big(g, txt, x, y, size, col); g.restore(); big(g, txt, x, y, size, "#FFFFFF"); g.globalAlpha = 0.55; big(g, txt, x, y, size, col); g.globalAlpha = 1; };
  function drawMayor(g, cx, cy, s) {
    g.fillStyle = "#1E3A8A"; g.fillRect(cx - 1.1 * s, cy + 0.55 * s, 2.2 * s, 1.2 * s); g.fillStyle = "#C81E3A"; g.beginPath(); g.moveTo(cx - 0.9 * s, cy + 0.55 * s); g.lineTo(cx - 0.6 * s, cy + 0.55 * s); g.lineTo(cx + 0.9 * s, cy + 1.75 * s); g.lineTo(cx + 0.55 * s, cy + 1.75 * s); g.fill();
    g.fillStyle = "#F0C49A"; g.fillRect(cx - 0.55 * s, cy - 0.55 * s, 1.1 * s, 1.1 * s); g.fillStyle = "#D9DDE3"; g.fillRect(cx - 0.6 * s, cy - 0.65 * s, 1.2 * s, 0.25 * s); g.fillRect(cx - 0.6 * s, cy - 0.65 * s, 0.15 * s, 0.6 * s); g.fillRect(cx + 0.45 * s, cy - 0.65 * s, 0.15 * s, 0.6 * s);
    g.fillStyle = "#1B1410"; g.fillRect(cx - 0.3 * s, cy - 0.15 * s, 0.12 * s, 0.18 * s); g.fillRect(cx + 0.18 * s, cy - 0.15 * s, 0.12 * s, 0.18 * s);
    g.strokeStyle = "#1B1410"; g.lineWidth = s * 0.06; g.beginPath(); g.arc(cx, cy + 0.12 * s, 0.22 * s, 0.2 * Math.PI, 0.8 * Math.PI); g.stroke(); }
  function drawBillboard(g, k, w, h) {
    const bg = { mayor: "#0E1638", treasure: "#2A1640", x15: "#0F2A1C", odds: "#2A0C14", rule: "#14142A", sold: "#2A0C14", d14: "#10223A", off: "#0A0C12" }[k] || "#0A0C12";
    g.fillStyle = bg; g.fillRect(0, 0, w, h);
    g.fillStyle = "rgba(255,255,255,0.04)"; for (let y = 0; y < h; y += 6) g.fillRect(0, y, w, 2);
    if (k === "mayor") { drawMayor(g, w * 0.3, h * 0.42, h * 0.33); g.fillStyle = "#E11D48"; g.fillRect(w * 0.55, h * 0.18, w * 0.38, h * 0.14); big(g, "LIVE", w * 0.74, h * 0.25, h * 0.11, "#FFF");
      big(g, "BREAKING", w * 0.74, h * 0.5, h * 0.12, "#FFD23F"); big(g, "NEWS", w * 0.74, h * 0.66, h * 0.12, "#FFD23F"); }
    if (k === "treasure") { glowText(g, "TREASURE", w / 2, h * 0.36, h * 0.24, "#FFC531"); glowText(g, "HOUR", w / 2, h * 0.66, h * 0.24, "#FFC531"); }
    if (k === "x15") { glowText(g, "1.5x", w / 2, h * 0.4, h * 0.38, "#3DDC84"); big(g, "CHANCE · 1 HOUR", w / 2, h * 0.78, h * 0.1, "#FFF"); }
    if (k === "odds") { big(g, "YOUR CHANCE", w / 2, h * 0.2, h * 0.1, "#FFF"); glowText(g, "1 IN", w / 2, h * 0.42, h * 0.18, "#FF3B5C"); glowText(g, "137,500", w / 2, h * 0.7, h * 0.24, "#FF3B5C"); }
    if (k === "rule") { big(g, "PIRATE TOKEN", w / 2, h * 0.3, h * 0.12, "#FFD23F"); glowText(g, "RULE #1", w / 2, h * 0.62, h * 0.26, "#FFFFFF"); }
    if (k === "d14") { big(g, "SHOP", w / 2, h * 0.24, h * 0.13, "#FFF"); glowText(g, "FREE", w / 2, h * 0.5, h * 0.24, "#3DDC84"); big(g, "FOR 14 DAYS", w / 2, h * 0.78, h * 0.12, "#FFD23F"); }
    g.strokeStyle = "#FFC531"; g.lineWidth = 10; g.strokeRect(5, 5, w - 10, h - 10);
  }
  function drawPhone(g, k, w, h) {
    g.fillStyle = k === "unlock" || k === "d14" ? "#0B2A1A" : "#11162A"; g.fillRect(0, 0, w, h);
    if (k === "ping") { g.fillStyle = "#FFC531"; g.beginPath(); g.arc(w / 2, h * 0.42, w * 0.26, 0, 6.3); g.fill(); big(g, "!", w / 2, h * 0.43, w * 0.36, "#11162A"); big(g, "NEW ITEM", w / 2, h * 0.72, w * 0.13, "#FFF"); }
    if (k === "unlock") { big(g, "SHOP", w / 2, h * 0.3, w * 0.2, "#FFF"); glowText(g, "UNLOCKED", w / 2, h * 0.46, w * 0.16, "#3DDC84");
      g.strokeStyle = "#3DDC84"; g.lineWidth = 14; g.beginPath(); g.moveTo(w * 0.36, h * 0.66); g.lineTo(w * 0.47, h * 0.75); g.lineTo(w * 0.66, h * 0.58); g.stroke(); }
    if (k === "d14") { big(g, "FREE FOR", w / 2, h * 0.3, w * 0.14, "#FFF"); glowText(g, "14", w / 2, h * 0.5, w * 0.42, "#FFC531"); big(g, "DAYS", w / 2, h * 0.7, w * 0.16, "#FFC531"); }
  }
  function drawClock(g, k, w, h) { g.fillStyle = "#101320"; g.fillRect(0, 0, w, h); glowText(g, k, w / 2, h / 2 + 4, h * 0.62, "#FF6B3D"); g.strokeStyle = "#C9A23A"; g.lineWidth = 8; g.strokeRect(4, 4, w - 8, h - 8); }
  function drawShopSign(g, k, w, h) { g.fillStyle = "#1A1030"; g.fillRect(0, 0, w, h);
    if (k === "free") { glowText(g, "FREE", w / 2, h / 2, h * 0.6, "#3DDC84"); } else { glowText(g, "$$$", w / 2, h / 2, h * 0.6, "#FF3B9A"); } }
  function drawCount(g, k, w, h) { g.clearRect(0, 0, w, h); g.fillStyle = "rgba(20,0,4,0.75)"; g.fillRect(0, 0, w, h); glowText(g, k, w / 2, h / 2 + 4, h * 0.55, "#FF2A3D"); }

  // ---------- Bauteile
  const woodM = std({ map: woodT }), goldM = std({ color: 0xF2B632, metalness: 0.8, roughness: 0.3, emissive: 0x2A1A00 });
  const darkWin = std({ color: 0x223044, roughness: 0.2, metalness: 0.2 });
  const litWin = std({ color: 0xFFD98A, emissive: 0xFFC060, emissiveIntensity: 0, roughness: 0.4 });
  const nightWins = [];
  function chest(par, x, y, z, ry = 0, s = 1) {
    const g = new THREE.Group(); g.position.set(x, y, z); g.rotation.y = ry; g.scale.setScalar(s); (par || scene).add(g);
    const bm = woodM.clone(); const lm = goldM.clone();
    box(1.2, 0.62, 0.8, bm, 0, 0.31, 0, g); for (const xx of [-0.45, 0.45]) box(0.12, 0.64, 0.82, lm, xx, 0.31, 0, g, false);
    const glow = new THREE.Mesh(new THREE.PlaneGeometry(1.1, 0.7), basic({ color: 0xFFD45A, toneMapped: false })); glow.rotation.x = -Math.PI / 2; glow.position.set(0, 0.6, 0); glow.visible = false; g.add(glow);
    const lid = new THREE.Group(); lid.position.set(0, 0.62, -0.4); g.add(lid);
    box(1.2, 0.26, 0.8, bm, 0, 0.13, 0.4, lid); for (const xx of [-0.45, 0.45]) box(0.12, 0.28, 0.82, lm, xx, 0.13, 0.4, lid, false);
    box(0.2, 0.22, 0.06, lm, 0, 0.0, 0.82, lid, false);
    g.userData = { lid, glow, bm, lm }; return g;
  }
  function setChest(c, open, glow, warm) {
    c.userData.lid.rotation.x = -open * 1.95;
    c.userData.glow.visible = open > 0.15 && glow > 0;
    c.userData.lm.emissive.setHex(glow > 0 ? 0xFFB020 : 0x2A1A00); c.userData.lm.emissiveIntensity = glow > 0 ? 0.6 * glow : 1;
    c.userData.bm.emissive.setHex(warm > 0 ? 0xFF4A10 : 0x000000); c.userData.bm.emissiveIntensity = warm;
  }
  function tokenMesh(s = 1) {
    const c = cv(256, 256), g = c.getContext("2d");
    const gr = g.createRadialGradient(128, 128, 20, 128, 128, 128); gr.addColorStop(0, "#2A2A30"); gr.addColorStop(1, "#08080A"); g.fillStyle = gr; g.fillRect(0, 0, 256, 256);
    g.strokeStyle = "#F2B632"; g.lineWidth = 14; g.beginPath(); g.arc(128, 128, 112, 0, 6.3); g.stroke(); g.lineWidth = 4; g.beginPath(); g.arc(128, 128, 96, 0, 6.3); g.stroke();
    g.fillStyle = "#F2B632"; g.beginPath(); g.ellipse(128, 112, 44, 40, 0, 0, 6.3); g.fill(); g.fillRect(104, 130, 48, 30);
    g.fillStyle = "#0A0A0C"; g.beginPath(); g.ellipse(110, 112, 12, 14, 0, 0, 6.3); g.ellipse(146, 112, 12, 14, 0, 0, 6.3); g.fill();
    g.beginPath(); g.moveTo(128, 124); g.lineTo(121, 136); g.lineTo(135, 136); g.fill(); for (let i = 0; i < 3; i++) g.fillRect(110 + i * 14, 146, 4, 14);
    g.strokeStyle = "#F2B632"; g.lineWidth = 12; g.lineCap = "round"; g.beginPath(); g.moveTo(70, 168); g.lineTo(186, 206); g.moveTo(186, 168); g.lineTo(70, 206); g.stroke();
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace;
    const face = std({ map: t, metalness: 0.5, roughness: 0.35, emissive: 0xFFFFFF, emissiveMap: t, emissiveIntensity: 0.25 });
    const rim = std({ color: 0xF2B632, metalness: 0.9, roughness: 0.25, emissive: 0x3A2400 });
    const m = new THREE.Mesh(new THREE.CylinderGeometry(0.32 * s, 0.32 * s, 0.07 * s, 40), [rim, face, face]);
    m.rotation.x = Math.PI / 2; const g2 = new THREE.Group(); g2.add(m); m.castShadow = true; g2.userData = { face, rim }; return g2;
  }

  // ---------- Klötzchen-Figuren
  function makeChar(o) {
    const root = new THREE.Group(); scene.add(root);
    const sk = std({ color: o.skin || 0xF1C27D }), sh = std({ color: o.shirt }), pa = std({ color: o.pants || 0x2E3A59 }), shoe = std({ color: o.shoe || 0x222222 });
    if (o.dark) { [sk, sh, pa, shoe].forEach((m) => { m.color.setHex(0x0B0B0F); m.roughness = 1; }); }
    // Torso mit Shirt-Design vorn
    const c = cv(128, 128), g = c.getContext("2d"); g.fillStyle = "#" + new THREE.Color(o.dark ? 0x0B0B0F : o.shirt).getHexString(); g.fillRect(0, 0, 128, 128);
    if (o.design === "hoodie") { g.fillStyle = "rgba(255,255,255,0.85)"; g.fillRect(0, 70, 128, 10); g.fillStyle = "rgba(0,0,0,0.18)"; g.fillRect(40, 84, 48, 34); g.strokeStyle = "#FFF"; g.lineWidth = 4; g.beginPath(); g.moveTo(52, 0); g.lineTo(52, 30); g.moveTo(76, 0); g.lineTo(76, 30); g.stroke(); }
    if (o.design === "suit") { g.fillStyle = "#F4F4F4"; g.beginPath(); g.moveTo(44, 0); g.lineTo(84, 0); g.lineTo(64, 60); g.fill(); g.fillStyle = "#C81E3A"; g.fillRect(59, 8, 10, 46); g.strokeStyle = "#F2B632"; g.lineWidth = 6; g.beginPath(); g.arc(64, 30, 34, 0.15 * Math.PI, 0.85 * Math.PI); g.stroke(); g.fillStyle = "#F2B632"; g.beginPath(); g.arc(64, 66, 8, 0, 6.3); g.fill(); }
    if (o.design === "star") { g.fillStyle = "#FFF"; g.font = "bold 64px sans-serif"; g.textAlign = "center"; g.fillText("★", 64, 86); }
    if (o.design === "stripe") { g.fillStyle = "rgba(255,255,255,0.7)"; for (let y = 20; y < 128; y += 30) g.fillRect(0, y, 128, 10); }
    const ct = new THREE.CanvasTexture(c); ct.colorSpace = THREE.SRGBColorSpace; const front = std({ map: ct });
    const torso = add(new THREE.Mesh(new THREE.BoxGeometry(1, 1, 0.5), [sh, sh, sh, sh, front, sh]), root); torso.position.y = 1.5;
    const limb = (x, y, mats) => { const p = new THREE.Group(); p.position.set(x, y, 0); root.add(p); return p; };
    const armL = limb(0.75, 1.97), armR = limb(-0.75, 1.97), legL = limb(0.25, 1.0), legR = limb(-0.25, 1.0);
    for (const a of [armL, armR]) { box(0.48, 0.62, 0.48, sh, 0, -0.28, 0, a); box(0.46, 0.4, 0.46, sk, 0, -0.78, 0, a); }
    for (const l of [legL, legR]) { box(0.49, 0.86, 0.5, pa, 0, -0.43, 0, l); box(0.5, 0.16, 0.54, shoe, 0, -0.92, 0.02, l); }
    const head = new THREE.Group(); head.position.y = 2.0; root.add(head);
    box(0.62, 0.62, 0.62, sk, 0, 0.31, 0, head);
    const faceM = basic({ map: faceTex("neutral", o), transparent: true }); if (o.dark) faceM.visible = false;
    const face = new THREE.Mesh(new THREE.PlaneGeometry(0.6, 0.6), faceM); face.position.set(0, 0.31, 0.312); head.add(face);
    const hm = std({ color: o.hairCol || 0x4A2E1A, roughness: 0.9 });
    const hs = o.hair || "short";
    if (hs === "short" || hs === "messy" || hs === "long" || hs === "pony") { box(0.68, 0.18, 0.68, hm, 0, 0.66, -0.01, head); box(0.68, 0.36, 0.14, hm, 0, 0.5, -0.29, head); box(0.12, 0.3, 0.6, hm, 0.31, 0.52, -0.02, head); box(0.12, 0.3, 0.6, hm, -0.31, 0.52, -0.02, head); }
    if (hs === "messy") for (let i = 0; i < 6; i++) { const b = box(0.2, 0.16, 0.2, hm, -0.25 + i * 0.1, 0.76, -0.2 + (i % 3) * 0.17, head); b.rotation.set(rr(-0.5, 0.5), rr(0, 1), rr(-0.5, 0.5)); }
    if (hs === "messy") box(0.5, 0.1, 0.12, hm, -0.06, 0.6, 0.3, head);
    if (hs === "long") { box(0.7, 0.8, 0.16, hm, 0, 0.22, -0.3, head); box(0.14, 0.75, 0.3, hm, 0.32, 0.25, 0.08, head); box(0.14, 0.75, 0.3, hm, -0.32, 0.25, 0.08, head); }
    if (hs === "pony") { box(0.2, 0.55, 0.2, hm, 0, 0.35, -0.42, head); box(0.24, 0.24, 0.24, std({ color: 0xFF5FA2 }), 0, 0.66, -0.36, head); }
    if (hs === "bald") box(0.66, 0.2, 0.66, hm, 0, 0.32, -0.02, head);
    if (hs === "tophat") { const hat = std({ color: 0x15121C, roughness: 0.6 }); const c1 = add(new THREE.Mesh(new THREE.CylinderGeometry(0.5, 0.5, 0.05, 24), hat), head); c1.position.y = 0.64;
      const c2 = add(new THREE.Mesh(new THREE.CylinderGeometry(0.32, 0.32, 0.55, 24), hat), head); c2.position.y = 0.92; const band = add(new THREE.Mesh(new THREE.CylinderGeometry(0.325, 0.325, 0.1, 24), std({ color: 0x7C3AED })), head); band.position.y = 0.72; }
    if (hs === "cap") { const cm = std({ color: o.capCol || 0xD62828 }); box(0.68, 0.2, 0.68, cm, 0, 0.7, 0, head); box(0.6, 0.05, 0.3, cm, 0, 0.62, 0.42, head); }
    if (o.dark) { root.scale.setScalar(1.18); }
    const ch = { root, armL, armR, legL, legR, head, faceM, o, ex: null };
    ch.setEx = (ex) => { if (ex !== ch.ex) { ch.ex = ex; faceM.map = faceTex(ex, o); faceM.needsUpdate = true; } };
    return ch;
  }
  function pose(ch, p, u) {
    const { armL, armR, legL, legR, head, root } = ch;
    for (const q of [armL, armR, legL, legR, head]) q.rotation.set(0, 0, 0);
    root.rotation.x = 0; root.rotation.z = 0; let bob = 0;
    const sw = Math.sin(u * 2.2) * 0.04;
    armL.rotation.z = 0.06 + sw; armR.rotation.z = -0.06 - sw; head.rotation.y = Math.sin(u * 0.9) * 0.06;
    if (p === "walk" || p === "run") { const sp = p === "run" ? 13 : 8, am = p === "run" ? 0.9 : 0.55, s = Math.sin(u * sp);
      legL.rotation.x = s * am; legR.rotation.x = -s * am; armL.rotation.x = -s * am; armR.rotation.x = s * am; bob = Math.abs(Math.cos(u * sp)) * 0.06; }
    if (p === "cheer") { const s = Math.sin(u * 13); legL.rotation.x = s * 0.8; legR.rotation.x = -s * 0.8; armL.rotation.z = 2.7 + s * 0.2; armR.rotation.z = -2.7 + s * 0.2; bob = Math.abs(Math.cos(u * 13)) * 0.08; }
    if (p === "wave") { armR.rotation.z = -2.5 + Math.sin(u * 9) * 0.35; }
    if (p === "up") { armL.rotation.z = 2.6 + Math.sin(u * 10) * 0.12; armR.rotation.z = -2.6 - Math.sin(u * 10) * 0.12; bob = Math.abs(Math.sin(u * 10)) * 0.12; }
    if (p === "point") { armR.rotation.x = -1.5; armL.rotation.x = -0.4 + Math.sin(u * 14) * 0.15; root.rotation.z = Math.sin(u * 14) * 0.03; }
    if (p === "hold") { armL.rotation.x = -1.35; armR.rotation.x = -1.35; armL.rotation.z = -0.25; armR.rotation.z = 0.25; }
    if (p === "shake") { armL.rotation.x = -1.35 + Math.sin(u * 47) * 0.05; armR.rotation.x = -1.35 + Math.sin(u * 53) * 0.05; armL.rotation.z = -0.25; armR.rotation.z = 0.25; head.rotation.z = Math.sin(u * 31) * 0.03; }
    if (p === "phone") { armR.rotation.x = -1.25; armR.rotation.z = 0.35; armL.rotation.x = -0.5; head.rotation.x = 0.35; }
    if (p === "money") { armR.rotation.x = -1.3; armR.rotation.z = 0.1; }
    if (p === "holdUp") { armR.rotation.x = -2.9 - Math.sin(u * 3) * 0.05; armR.rotation.z = 0.1; armL.rotation.z = 0.5; head.rotation.x = -0.25; }
    if (p === "reach") { armR.rotation.x = -1.0; armL.rotation.x = -1.0; armR.rotation.z = 0.15; armL.rotation.z = -0.15; head.rotation.x = 0.35; }
    if (p === "sad") { head.rotation.x = 0.32; armL.rotation.z = 0.02; armR.rotation.z = -0.02; root.rotation.x = 0.05; }
    if (p === "hands") { armL.rotation.x = -2.6; armR.rotation.x = -2.6; armL.rotation.z = -0.55; armR.rotation.z = 0.55; }
    if (p === "kick") { const k = Math.sin(clamp(u * 3.2, 0, Math.PI)); legR.rotation.x = -1.4 * k; armL.rotation.z = 0.9; armR.rotation.z = -0.9; root.rotation.x = 0.12 * k; }
    if (p === "lean") { root.rotation.x = 0.16; armR.rotation.x = -0.3; head.rotation.x = 0.1; }
    if (p === "knock") { armR.rotation.x = -1.7 + Math.max(0, Math.sin(u * 18)) * 0.35; }
    if (p === "sit") { legL.rotation.x = -1.5; legR.rotation.x = -1.5; bob = -0.5; }
    root.position.y += bob;
  }

  const SKIN = [0xF1C27D, 0xE0AC69, 0xC68642, 0x8D5524, 0xFFDBAC, 0xD8A06A];
  const SHIRT = [0x2B7BE4, 0xE63946, 0x2A9D8F, 0xF4A261, 0x8338EC, 0x06D6A0, 0xFFBE0B, 0xFB5607, 0x3A86FF, 0xEF476F, 0x118AB2, 0x7B2CBF];
  const HAIRC = [0x2B1A10, 0x4A2E1A, 0x1A1A1A, 0xC98B3C, 0x6B3E1E, 0xE8C66A];
  const A = {
    leo: makeChar({ shirt: 0xF77F00, pants: 0x2E3A59, design: "hoodie", hair: "messy", hairCol: 0x5A3215, skin: 0xF1C27D, shoe: 0xEEEEEE }),
    mia: makeChar({ shirt: 0xFF5FA2, pants: 0x6C8EBF, design: "star", hair: "long", hairCol: 0x3A2214, skin: 0xF1C27D, blush: true }),
    vance: makeChar({ shirt: 0x5B2A86, pants: 0x3B1C5A, design: "suit", hair: "tophat", skin: 0xE8B98F, stache: true, shoe: 0x111111 }),
    old: makeChar({ shirt: 0x8A7F70, pants: 0x4A4A4A, design: "stripe", hair: "bald", hairCol: 0xDADADA, skin: 0xE0AC69, glasses: true }),
    girl: makeChar({ shirt: 0xFFD23F, pants: 0x3A86FF, hair: "pony", hairCol: 0xC98B3C, skin: 0xFFDBAC, blush: true }),
    npc1: makeChar({ shirt: 0x2B7BE4, pants: 0x22304A, design: "stripe", hair: "short", hairCol: 0x1A1A1A, skin: 0xC68642 }),
    npc2: makeChar({ shirt: 0xE63946, pants: 0x2E2E2E, hair: "cap", capCol: 0x111111, skin: 0xE0AC69 }),
    npc3: makeChar({ shirt: 0x2A9D8F, pants: 0x3D3D5C, hair: "short", hairCol: 0xC98B3C, skin: 0xFFDBAC }),
    fig: makeChar({ shirt: 0x000000, dark: true, hair: "bald" }),
  };
  const CROWD = [];
  for (let i = 0; i < 30; i++) CROWD.push(makeChar({ shirt: pick(SHIRT), pants: pick([0x2E3A59, 0x22304A, 0x3D3D5C, 0x4A4A4A, 0x5C4033]), skin: pick(SKIN),
    hair: pick(["short", "short", "messy", "cap", "long", "pony", "bald"]), hairCol: pick(HAIRC), capCol: pick(SHIRT), design: pick([null, "stripe", "star", null]) }));
  // Requisiten an Händen
  const handTok = tokenMesh(0.5); handTok.position.set(0, -1.05, 0.05); A.leo.armR.add(handTok);
  const girlTok = tokenMesh(0.5); girlTok.position.set(0, -1.05, 0.05); A.girl.armR.add(girlTok);
  const phone = new THREE.Group(); phone.position.set(0.0, -1.0, 0.18); phone.rotation.x = 1.25; A.leo.armR.add(phone);
  box(0.36, 0.64, 0.05, std({ color: 0x111111, roughness: 0.3 }), 0, 0, 0, phone, false);
  const phoneScr = screen(0.32, 0.58, 256, 464, drawPhone); phoneScr.position.z = 0.03; phone.add(phoneScr);
  const money = new THREE.Group(); money.position.set(0, -1.05, 0.15); A.vance.armR.add(money);
  for (let i = 0; i < 4; i++) box(0.5, 0.06, 0.26, std({ color: 0x3DAA5C }), 0, -0.05 + i * 0.065, 0, money, false);
  box(0.12, 0.27, 0.28, std({ color: 0xF2E8C9 }), 0, 0.04, 0, money, false);

  // ---------- STADT (Straße entlang z, Halle am Ende bei z=-40)
  const street = new THREE.Group(); scene.add(street);
  { const g = add(new THREE.Mesh(new THREE.PlaneGeometry(200, 200), std({ map: grassT })), street, false, true); g.rotation.x = -Math.PI / 2; g.position.y = -0.02;
    const rd = add(new THREE.Mesh(new THREE.PlaneGeometry(8, 140), std({ map: roadT, roughness: 0.95 })), street, false, true); rd.rotation.x = -Math.PI / 2; rd.position.set(0, 0, -5);
    for (const s of [-1, 1]) { const w = box(2.5, 0.16, 140, std({ map: walkT }), s * 5.25, 0.08, -5, street, false); } }
  const HOUSES = [];
  function house(side, z, opt) {
    const g = new THREE.Group(); g.position.set(side * 7, 0, z); g.rotation.y = side > 0 ? -Math.PI / 2 : Math.PI / 2; street.add(g);
    const wd = opt.w || 7, ht = opt.h || 5.5, dp = 7;
    const wall = opt.wall || std({ map: sidingT(opt.col || "#E9E2D0", 20 + Math.floor(z)) });
    box(wd, ht, dp, wall, 0, ht / 2, -dp / 2, g);
    if (!opt.flat) { const s = new THREE.Shape(); s.moveTo(-wd / 2 - 0.4, 0); s.lineTo(wd / 2 + 0.4, 0); s.lineTo(0, 2.6); s.lineTo(-wd / 2 - 0.4, 0);
      const rg = new THREE.ExtrudeGeometry(s, { depth: dp + 0.6, bevelEnabled: false }); const roof = add(new THREE.Mesh(rg, opt.roof || std({ map: roofT })), g); roof.position.set(0, ht, -dp - 0.3); }
    else box(wd + 0.3, 0.4, dp + 0.3, std({ color: 0x5A5F73 }), 0, ht + 0.2, -dp / 2, g);
    const door = box(1.2, 2.3, 0.12, std({ color: opt.door || 0x5A3A22 }), opt.doorX || 0, 1.15, 0.05, g); box(0.1, 0.1, 0.1, goldM, (opt.doorX || 0) + 0.42, 1.15, 0.15, g, false);
    box(1.6, 0.2, 0.9, std({ color: 0xBFC2C9 }), opt.doorX || 0, 0.1, 0.5, g);
    const wins = [];
    for (const [x, y] of opt.wins || [[-2.2, 1.6], [2.2, 1.6], [-2.2, 4.0], [2.2, 4.0], [0, 4.0]]) {
      const wm = opt.darkW ? darkWin : litWin.clone(); const w = box(1.3, 1.2, 0.08, wm, x, y, 0.03, g, false); box(1.5, 0.12, 0.2, std({ color: 0xFFFFFF }), x, y - 0.66, 0.08, g, false);
      if (!opt.darkW) nightWins.push(wm); wins.push(w); }
    g.userData = { door, wins }; HOUSES.push(g); return g;
  }
  const leoHouse = house(-1, 10, { col: "#BFD7EA", door: 0x7A2E1E });
  const vanceHouse = house(1, 16, { w: 9, h: 7, wall: std({ color: 0xF5E6B8 }), roof: std({ color: 0xD9A520, metalness: 0.5, roughness: 0.35 }), door: 0x3B1C5A,
    wins: [[-3, 1.8], [3, 1.8], [-3, 4.8], [0, 4.8], [3, 4.8]] });
  for (const xx of [-2, 2]) { const col = add(new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.22, 7, 16), std({ color: 0xFFFFFF })), vanceHouse); col.position.set(xx, 3.5, 0.6); }
  const girlHouse = house(-1, -14, { col: "#F2C6C2", door: 0x3A5A40 });
  const girlWinM = girlHouse.userData.wins.map((w) => w.material);
  house(-1, 1, { col: "#D8E2C6" }); house(-1, 19, { col: "#F3E3B5" }); house(-1, -5, { col: "#C9C3E6" }); house(-1, -23, { col: "#E6D3C3" }); house(1, 25, { col: "#CFE8E0" });
  house(1, 7, { col: "#F0D7A8" }); house(-1, 28, { col: "#E9E2D0" }); house(-1, -32, { col: "#D2DCE8" }); house(1, -32, { col: "#EAD2DC" });
  // Shop (rechts, z = -2)
  const shop = house(1, -2, { w: 8, h: 5, flat: true, wall: std({ map: brickT }), door: 0x2B2B2B, wins: [[-2.6, 1.7], [2.6, 1.7]] });
  const shopSign = screen(4.2, 1.2, 512, 146, drawShopSign); shopSign.position.set(0, 3.9, 0.12); shop.add(shopSign);
  const SHOPNAME = screen(3, 0.8, 384, 102, (g, k, w, h) => { g.fillStyle = "#101320"; g.fillRect(0, 0, w, h); glowText(g, "ITEM SHOP", w / 2, h / 2 + 3, h * 0.6, "#FFC531"); }); SHOPNAME.position.set(0, 5.4, 0.15); shop.add(SHOPNAME); SHOPNAME.userData.set("x");
  for (let i = 0; i < 6; i++) { const it = box(0.4, 0.4, 0.4, std({ color: SHIRT[i], emissive: SHIRT[i], emissiveIntensity: 0.2 }), (i < 3 ? -2.6 : 2.6) + ((i % 3) - 1) * 0.42, 1.5, 0.2, shop, false); it.rotation.y = 0.6; }
  // Billboard (rechts, z = -24)
  const bbB = new THREE.Group(); bbB.position.set(7.2, 0, -24); bbB.rotation.y = -Math.PI / 2; street.add(bbB);
  box(9, 5, 8, std({ map: brickT }), 0, 2.5, -4, bbB); box(9.4, 0.3, 8.4, std({ color: 0x5A5F73 }), 0, 5.15, -4, bbB);
  for (const xx of [-2.5, 2.5]) box(0.3, 2.4, 0.3, std({ color: 0x2B2B33, metalness: 0.6 }), xx, 6.4, -1, bbB);
  box(8.6, 5.3, 0.3, std({ color: 0x1C1C24 }), 0, 9.9, -1.1, bbB);
  const billboard = screen(8.2, 4.9, 820, 490, drawBillboard); billboard.position.set(0, 9.9, -0.93); bbB.add(billboard);
  // Truhenhalle
  const hallB = new THREE.Group(); hallB.position.set(0, 0, -40); street.add(hallB);
  box(26, 10, 14, std({ color: 0x3B2A6E }), 0, 5, -7, hallB); box(27, 0.8, 15, goldM, 0, 10.2, -7, hallB);
  for (let i = -5; i <= 5; i += 2) { if (Math.abs(i) < 2) continue; const c = add(new THREE.Mesh(new THREE.CylinderGeometry(0.4, 0.45, 9.6, 20), std({ color: 0xF4EEDC })), hallB); c.position.set(i * 1.15, 4.8, 0.6); }
  box(6.4, 0.5, 2.6, std({ color: 0xBFC2C9 }), 0, 0.25, 1.2, hallB);
  const doorGlow = box(4.0, 4.6, 0.05, basic({ color: 0xFFC860, toneMapped: false }), 0, 2.55, 0.02, hallB, false);
  const doorL = box(2.0, 4.6, 0.2, std({ color: 0x2A1E4A, metalness: 0.3 }), -1.0, 2.55, 0.12, hallB); const doorR = box(2.0, 4.6, 0.2, std({ color: 0x2A1E4A, metalness: 0.3 }), 1.0, 2.55, 0.12, hallB);
  box(4.6, 0.3, 0.4, goldM, 0, 5.0, 0.2, hallB);
  const hallSign = screen(10, 1.6, 900, 144, (g, k, w, h) => { g.fillStyle = "#151030"; g.fillRect(0, 0, w, h); glowText(g, "CHEST HALL", w / 2, h / 2 + 4, h * 0.62, "#FFC531"); }); hallSign.position.set(0, 8.4, 0.08); hallB.add(hallSign); hallSign.userData.set("x");
  const clock = screen(2.8, 1.1, 336, 132, drawClock); clock.position.set(0, 6.3, 0.08); hallB.add(clock);
  const chestDeco = chest(hallB, 0, 10.6, -1.5, 0, 2.2); setChest(chestDeco, 0, 1, 0);
  // Laternen, Bäume, Schild "FOR SALE"
  const lampLights = [];
  for (const [x, z] of [[-4.6, 14], [4.6, 4], [-4.6, -6], [4.6, -16], [-4.6, -26], [4.6, -34], [-4.6, 24]]) {
    box(0.18, 4.4, 0.18, std({ color: 0x2B2B33, metalness: 0.5 }), x, 2.2, z, street); box(0.9 * Math.sign(-x), 0.14, 0.14, std({ color: 0x2B2B33 }), x - 0.45 * Math.sign(x), 4.35, z, street);
    const bulb = box(0.4, 0.2, 0.4, litWin.clone(), x - 0.85 * Math.sign(x), 4.2, z, street, false); nightWins.push(bulb.material);
    const pl = new THREE.PointLight(0xFFB566, 0, 14, 1.6); pl.position.set(x - 0.85 * Math.sign(x), 4.0, z); street.add(pl); lampLights.push(pl); }
  const barkM = std({ color: 0x6B4A2F }), leafMs = [0x4E9A3A, 0x5DAF45, 0x438A33].map((c) => std({ color: c, flatShading: true }));
  for (const [x, z, s] of [[-4.4, 6, 1], [4.4, 11, 1.1], [-4.4, -10, 0.9], [4.4, -9, 1], [-4.4, -19, 1.1], [4.4, 21, 0.9], [-4.4, 31, 1]]) {
    const t = new THREE.Group(); t.position.set(x, 0, z); t.scale.setScalar(s); street.add(t);
    const tr = add(new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.22, 2.6, 8), barkM), t); tr.position.y = 1.3;
    for (let i = 0; i < 5; i++) { const b = add(new THREE.Mesh(new THREE.IcosahedronGeometry(rr(0.7, 1.0), 1), leafMs[i % 3]), t); b.position.set(rr(-0.6, 0.6), 2.9 + rr(-0.2, 0.7), rr(-0.6, 0.6)); } }
  const porch = new THREE.PointLight(0xFFB566, 0, 7, 1.4); porch.position.set(-5.9, 3.0, 10); street.add(porch);
  const sale = new THREE.Group(); sale.position.set(-5.7, 0, -16.2); sale.rotation.y = Math.PI / 2; street.add(sale);
  box(0.1, 1.5, 0.1, woodM, 0, 0.75, 0, sale); const saleS = screen(1.3, 0.8, 260, 160, (g, k, w, h) => { g.fillStyle = "#F4F1EA"; g.fillRect(0, 0, w, h); g.fillStyle = "#C81E3A"; g.fillRect(0, 0, w, 40);
    big(g, "MOVED", w / 2, 20, 30, "#FFF"); big(g, "FOR SALE", w / 2, 100, 50, "#C81E3A"); }, false); saleS.position.set(0, 1.4, 0.06); sale.add(saleS); saleS.userData.set("x");
  const clouds = [];
  for (const [x, y, z, s] of [[-30, 26, -70, 4], [10, 30, -80, 5], [35, 24, -60, 3.5], [-12, 34, -95, 5]]) {
    const cl = new THREE.Group(); cl.position.set(x, y, z); street.add(cl); clouds.push(cl);
    for (let i = 0; i < 6; i++) { const p = new THREE.Mesh(new THREE.SphereGeometry(s * rr(0.5, 0.9), 12, 10), basic({ color: 0xFFFFFF, fog: false })); p.position.set(rr(-1.5, 1.5) * s, rr(-0.2, 0.4) * s, rr(-0.4, 0.4) * s); cl.add(p); } }
  const moon = new THREE.Mesh(new THREE.SphereGeometry(4, 24, 16), basic({ color: 0xFFF4D6, fog: false })); moon.position.set(-25, 40, -90); street.add(moon);

  // ---------- HALLE innen (x = 200)
  const hall = new THREE.Group(); scene.add(hall);
  { const f = add(new THREE.Mesh(new THREE.PlaneGeometry(30, 34), std({ map: hallFloorT, roughness: 0.35, metalness: 0.2 })), hall, false, true); f.rotation.x = -Math.PI / 2; f.position.set(HX, 0, 0);
    const wm = std({ color: 0x2A2250 }); box(30, 14, 0.5, wm, HX, 7, -16, hall); box(0.5, 14, 34, wm, HX - 15, 7, 0, hall); box(0.5, 14, 34, wm, HX + 15, 7, 0, hall); box(30, 14, 0.5, wm, HX, 7, 16.5, hall);
    for (let i = -12; i <= 12; i += 4) { box(0.6, 14, 0.6, goldM, HX + i, 7, -15.6, hall, false); }
    for (const s of [-1, 1]) for (let z = -12; z <= 12; z += 6) { const n = box(0.2, 10, 0.3, basic({ color: 0xB06BFF, toneMapped: false }), HX + s * 14.7, 6, z, hall, false); } }
  const hallScreen = screen(12, 4.5, 960, 360, (g, k, w, h) => { g.fillStyle = "#120E2A"; g.fillRect(0, 0, w, h); glowText(g, k === "x15" ? "TREASURE HOUR · 1.5x" : "OPEN ONE CHEST", w / 2, h * 0.5, h * 0.2, "#FFC531"); g.strokeStyle = "#FFC531"; g.lineWidth = 8; g.strokeRect(4, 4, w - 8, h - 8); });
  hallScreen.position.set(HX, 9, -15.7); hall.add(hallScreen);
  const GRID = []; const COLS = [-7.5, -4.5, -1.5, 1.5, 4.5, 7.5], ROWS = [-10, -6.5, -3];
  for (const z of ROWS) for (const x of COLS) { box(1.5, 0.6, 1.1, std({ color: 0x3E3470, metalness: 0.3 }), HX + x, 0.3, z, hall); const c = chest(hall, HX + x, 0.6, z); GRID.push(c); }
  box(1.7, 0.7, 1.3, std({ color: 0xC9A23A, metalness: 0.7, roughness: 0.3 }), HX, 0.35, 3, hall);
  const hero = chest(hall, HX, 0.7, 3);
  const heroLight = new THREE.PointLight(0xFFC040, 0, 9, 1.5); heroLight.position.set(HX, 1.6, 3); hall.add(heroLight);
  const hallLights = [];
  for (const [x, z] of [[-6, -6], [6, -6], [-6, 8], [6, 8]]) { const l = new THREE.PointLight(0xC59BFF, 0, 30, 1.2); l.position.set(HX + x, 9, z); hall.add(l); hallLights.push(l); }
  const plank = box(0.7, 0.12, 0.25, woodM, HX, 1.2, 3, hall); plank.visible = false;

  // ---------- ZIMMER (x = -200)
  const room = new THREE.Group(); scene.add(room);
  { const f = add(new THREE.Mesh(new THREE.PlaneGeometry(8, 8), std({ map: floorT })), room, false, true); f.rotation.x = -Math.PI / 2; f.position.set(RX, 0, 0);
    const wm = std({ map: wallpT });
    // Rückwand mit Fensteröffnung
    box(8, 1.6, 0.2, wm, RX, 0.8, -4, room); box(8, 1.2, 0.2, wm, RX, 3.4, -4, room); box(3.2, 1.2, 0.2, wm, RX - 2.4, 2.2, -4, room); box(3.2, 1.2, 0.2, wm, RX + 2.4, 2.2, -4, room);
    box(0.2, 4, 8, wm, RX - 4, 2, 0, room); box(0.2, 4, 8, wm, RX + 4, 2, 0, room);
    for (const [w, h, d, x, y, z] of [[8, 0.2, 0.25, RX, 0.1, -3.9], [0.25, 0.2, 8, RX - 3.9, 0.1, 0], [0.25, 0.2, 8, RX + 3.9, 0.1, 0]]) box(w, h, d, std({ color: 0xFFFFFF }), x, y, z, room, false);
    box(1.8, 0.12, 0.3, std({ color: 0xFFFFFF }), RX, 1.55, -3.85, room); }
  const roomDoor = box(0.12, 2.6, 1.3, std({ color: 0xF4F4F4 }), RX - 3.88, 1.3, 1.6, room);
  const winSky = add(new THREE.Mesh(new THREE.PlaneGeometry(3, 2.2), basic({ color: 0x8CC8FF })), room, false, false); winSky.position.set(RX, 2.3, -4.6);
  const winTree = add(new THREE.Mesh(new THREE.IcosahedronGeometry(0.7, 1), leafMs[0]), room, false, false); winTree.position.set(RX + 0.7, 2.0, -5.2);
  { const bed = new THREE.Group(); bed.position.set(RX - 2.4, 0, -2.2); room.add(bed);
    box(1.9, 0.5, 3.0, woodM, 0, 0.25, 0, bed); box(1.8, 0.25, 2.9, std({ color: 0xFFFFFF }), 0, 0.62, 0, bed); box(1.85, 0.2, 1.9, std({ color: 0x3A86FF }), 0, 0.78, 0.5, bed);
    box(1.0, 0.2, 0.5, std({ color: 0xFFFFFF }), 0, 0.85, -1.1, bed); box(1.9, 1.2, 0.15, woodM, 0, 0.6, -1.5, bed); }
  box(0.9, 0.75, 0.7, woodM, RX - 0.8, 0.375, -3.3, room);
  box(1.8, 0.1, 0.9, woodM, RX + 2.8, 1.0, -3.2, room); for (const [x, z] of [[2.0, -3.6], [3.6, -3.6], [2.0, -2.8], [3.6, -2.8]]) box(0.1, 1.0, 0.1, woodM, RX + x, 0.5, z, room, false);
  box(0.9, 0.6, 0.06, std({ color: 0x111111 }), RX + 2.8, 1.4, -3.55, room);
  const PILE = [];
  for (const [x, y, z, r] of [[2.6, 0, 1.0, 0.3], [3.2, 0, 2.1, -0.4], [2.4, 0, 2.7, 0.9], [3.0, 0.62, 1.5, 0.1], [3.3, 0, 0.0, -0.2], [2.7, 0.62, 0.3, 0.6], [3.1, 1.24, 0.9, -0.5]]) {
    const c = chest(room, RX + x, y, z, r, 0.85); setChest(c, 0.75, 0, 0); PILE.push(c); }
  const poster = screen(1.6, 1.2, 320, 240, (g, k, w, h) => { g.fillStyle = "#FFF7E0"; g.fillRect(0, 0, w, h); g.strokeStyle = "#222"; g.lineWidth = 4;
    for (let i = 0; i < 9; i++) for (let j = 0; j < 4; j++) { const x = 28 + i * 31, y = 30 + j * 32; g.beginPath(); g.moveTo(x, y); g.lineTo(x, y + 22); g.moveTo(x + 6, y); g.lineTo(x + 6, y + 22); g.moveTo(x + 12, y); g.lineTo(x + 12, y + 22); g.moveTo(x + 18, y); g.lineTo(x + 18, y + 22); g.moveTo(x - 4, y + 18); g.lineTo(x + 22, y + 4); g.stroke(); }
    big(g, "412", w / 2, h * 0.83, 52, "#E11D48"); }, false);
  poster.position.set(RX + 3.88, 2.3, -1.0); poster.rotation.y = -Math.PI / 2; room.add(poster); poster.userData.set("x");
  const roomLamp = new THREE.PointLight(0xFFE2B0, 0, 12, 1.4); roomLamp.position.set(RX, 3.6, 0.5); room.add(roomLamp);
  const moonL = new THREE.PointLight(0x7A9CFF, 0, 10, 1.2); moonL.position.set(RX, 2.6, -3.2); room.add(moonL);
  const nightLamp = new THREE.PointLight(0xFF3040, 0, 4, 1.5); nightLamp.position.set(RX - 0.8, 1.3, -2.9); room.add(nightLamp);

  // ---------- VOID (Token-Bühne, z = 400)
  const voidG = new THREE.Group(); scene.add(voidG);
  { const f = add(new THREE.Mesh(new THREE.CircleGeometry(6, 48), std({ color: 0x1A1430, roughness: 0.4, metalness: 0.3 })), voidG, false, true); f.rotation.x = -Math.PI / 2; f.position.set(0, 0, VZ);
    const ped = add(new THREE.Mesh(new THREE.CylinderGeometry(0.7, 0.85, 1.0, 32), std({ color: 0x2A2148, metalness: 0.4, roughness: 0.4 })), voidG); ped.position.set(0, 0.5, VZ);
    const ring = add(new THREE.Mesh(new THREE.TorusGeometry(0.78, 0.04, 8, 48), basic({ color: 0xFFC531, toneMapped: false })), voidG, false, false); ring.rotation.x = Math.PI / 2; ring.position.set(0, 1.0, VZ); }
  const voidLight = new THREE.SpotLight(0xFFE0A0, 0, 20, 0.5, 0.5, 1.2); voidLight.position.set(0, 7, VZ + 1); voidLight.target.position.set(0, 1, VZ); voidG.add(voidLight); voidG.add(voidLight.target);
  const voidFill = new THREE.PointLight(0xFFC040, 0, 6, 1.5); voidFill.position.set(0, 1.8, VZ + 0.8); voidG.add(voidFill);
  const SPARK = []; for (let i = 0; i < 40; i++) { const s = new THREE.Mesh(new THREE.OctahedronGeometry(0.03, 0), basic({ color: 0xFFD45A, toneMapped: false })); s.userData = { a: R() * 6.3, r: rr(0.5, 2.2), y: rr(0.5, 3.5), o: R() }; voidG.add(s); SPARK.push(s); }

  const bigPhone = new THREE.Group(); bigPhone.position.set(HX + 0.3, 1.9, 3.45); bigPhone.rotation.x = -0.45; hall.add(bigPhone);
  box(0.36, 0.64, 0.05, std({ color: 0x111111, roughness: 0.3 }), 0, 0, 0, bigPhone, false);
  const bigScr = screen(0.32, 0.58, 256, 464, drawPhone); bigScr.position.z = 0.03; bigPhone.add(bigScr);
  const phoneGlow = new THREE.PointLight(0x9CFFB8, 0, 3, 1.5); phoneGlow.position.set(0, 0, 0.3); bigPhone.add(phoneGlow);
  // Haupt-Token (wird pro Einstellung platziert)
  const token = tokenMesh(1); scene.add(token);
  const countdown = screen(1.1, 0.34, 440, 136, drawCount); scene.add(countdown);
  const giftTok = tokenMesh(0.5); scene.add(giftTok);

  // ---------- Licht
  const hemi = new THREE.HemisphereLight(0xD8E8FF, 0x6B5A40, 0.9); scene.add(hemi);
  const sun = new THREE.DirectionalLight(0xFFF1D8, 2.6); sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048);
  Object.assign(sun.shadow.camera, { left: -14, right: 14, top: 14, bottom: -14, near: 1, far: 80 }); sun.shadow.bias = -0.0005; scene.add(sun); scene.add(sun.target);
  const skyDay = new THREE.Color(0x7EC4F5), skyNight = new THREE.Color(0x0B1030);
  scene.fog = new THREE.Fog(0xBFE0F8, 40, 120);

  // ---------- Einstellungen (eine pro Sprechzeile). cast: [x, z, ry(deg), pose, ex, {to:[x,z], dur, y}]
  const LEO = (x, z, r, p, e, o) => ["leo", x, z, r, p, e, o];
  const S = [
    /* 1 hook   */ { m: "day", cr: "street", cam: { p: [7, 24, 40], p2: [5, 19, 30], t: [0, 0, -30], fov: 50 } },
    /* 2        */ { m: "hall", cast: [["npc1", HX, 4.3, 180, "reach", "neutral"]], hero: { open: 0.35 }, cam: { p: [HX + 2.7, 2.5, 2.0], t: [HX, 1.7, 3.8], fov: 46 } },
    /* 3        */ { m: "day", cr: "street", cam: { p: [-3, 0.6, 4], t: [2, 2.2, -10], fov: 55 } },
    /* 4        */ { m: "void", tok: "void", cam: { p: [0, 1.95, VZ + 3.2], p2: [0, 1.85, VZ + 2.2], t: [0, 1.8, VZ], fov: 40 } },
    /* 5 rule   */ { m: "day", shop: "price", cast: [["npc1", 4.4, -1.6, 90, "idle", "smile"]], cam: { p: [0.2, 2.1, 4], t: [7, 2.6, -2], fov: 50 } },
    /* 6        */ { m: "day", shop: "free", cast: [["npc1", 4.6, -2.2, -45, "up", "grin"]], cam: { p: [2.0, 2.2, 1.0], t: [5.4, 2.3, -2.8], fov: 50 } },
    /* 7        */ { m: "day", bb: "d14", cam: { p: [-3, 1.5, -13], t: [7, 9.5, -24], fov: 50 } },
    /* 8 daily  */ { m: "day", clock: "8:00", doors: "open", cam: { p: [0, 3, -23], p2: [0, 2.8, -27], t: [0, 5, -40], fov: 50 } },
    /* 9        */ { m: "hall", cast: [["npc1", HX, 10, 180, "walk", "neutral", { to: [HX, 4.5], dur: 1.6 }]], cam: { p: [HX + 0.9, 2.7, 12], t: [HX, 1.2, 3], fov: 50 } },
    /* 10       */ { m: "hall", cast: [["npc1", HX, 4.3, 180, "reach", "sad"]], hero: { open: 0.1 }, cam: { p: [HX - 2.7, 2.5, 2.2], t: [HX, 1.6, 3.8], fov: 46 } },
    /* 11       */ { m: "hall", cast: [["npc1", HX, 4.3, 180, "sad", "sad"]], hero: { open: -1 }, cam: { face: "npc1", d: 1.4, dx: 0.2, fov: 42 } },
    /* 12       */ { m: "day", doors: "isopen", cast: [["npc1", 0.3, -36.4, 0, "walk", "sad", { to: [0.3, -31], dur: 3 }]], cam: { p: [0.8, 2.4, -39.2], t: [0.2, 1.6, -30], fov: 50 } },
    /* 13 odds  */ { m: "day", bb: "odds", cam: { p: [-4, 1, -15], p2: [-3.4, 1.4, -16.5], t: [7, 9.5, -24], fov: 45 } },
    /* 14       */ { m: "hall", cast: [["old", HX - 4.5, -1.8, 180, "reach", "neutral"]], grid: [[13, 0.3]], cam: { p: [HX - 2.2, 2.4, -0.6], t: [HX - 4.5, 1.7, -2.4], fov: 45 } },
    /* 15       */ { m: "hall", cast: [["old", HX - 4.5, -1.8, 180, "sad", "sad"]], grid: [[13, -1]], cam: { face: "old", d: 1.3, dx: -0.25, fov: 40 } },
    /* 16 law   */ { m: "day", bb: "rule", cam: { p: [-2, 2, -12], p2: [-1, 2.6, -15], t: [7, 9.5, -24], fov: 42 } },
    /* 17       */ { m: "void", tok: "void", lab: ["✕ CAN'T BE SOLD", "r", [0, 2.75, VZ]], cam: { p: [1.2, 2.1, VZ + 2.8], t: [0, 2.0, VZ], fov: 42 } },
    /* 18       */ { m: "day", gift: [-1.4, 1.45, 6], cast: [["npc1", -2.1, 6, 90, "hold", "smile"], ["npc2", -0.7, 6, -90, "reach", "shock"]], lab: ["✕ CAN'T BE GIFTED", "r", [-1.4, 3.4, 6]], cam: { p: [-1.2, 2.0, 9.4], t: [-1.4, 1.7, 6], fov: 45 } },
    /* 19       */ { m: "hall", hero: { open: 0.15, glow: 1 }, cam: { p: [HX + 0.8, 1.2, 5.6], t: [HX, 1.4, 3], fov: 48 } },
    /* 20       */ { m: "void", tok: "void", cam: { p: [-1.6, 2.3, VZ + 2.4], p2: [-0.5, 2.0, VZ + 2.8], t: [0, 1.8, VZ], fov: 40 } },
    /* 21 rich  */ { m: "day", cr: "street", cam: { p: [3, 2.5, 22], t: [-1, 1.5, 2], fov: 50 } },
    /* 22       */ { m: "day", cast: [["vance", 5.0, 16, -90, "idle", "smirk"]], cam: { p: [1.4, 0.6, 14.6], t: [6, 3.0, 16.3], fov: 55 } },
    /* 23       */ { m: "day", cast: [["vance", 5.0, 16, -90, "money", "smirk"]], money: 1, lab: ["$10,000", "g", [5.0, 3.5, 16]], cam: { p: [2.4, 2.2, 17.2], t: [5.0, 1.9, 16], fov: 45 } },
    /* 24       */ { m: "day", cast: [["vance", 5.0, 16, -90, "money", "smirk"]], money: 1, cam: { face: "vance", d: 1.4, dx: 0.35, fov: 40 } },
    /* 25 vance */ { m: "day", cast: [["vance", 5.0, 16, -90, "idle", "smirk"]], lab: ["MR. VANCE", "y", [5.0, 3.55, 16]], cam: { face: "vance", d: 1.6, dx: -0.3, dy: -0.25, fov: 44 } },
    /* 26       */ { m: "day", cr: "street", gold: 1, cam: { p: [-14, 16, 32], p2: [-12, 15, 24], t: [6, 0, -4], fov: 50 } },
    /* 27       */ { m: "void", tok: "void", cam: { p: [0, 2.8, VZ + 2.2], t: [0, 1.8, VZ], fov: 38 } },
    /* 28 me    */ { m: "room", cast: [LEO(RX, 0.5, 0, "wave", "smile")], lab: ["LEO", "y", [RX, 3.35, 0.5]], cam: { face: "leo", d: 1.5, dx: 0.25, fov: 44 } },
    /* 29       */ { m: "room", cast: [LEO(RX, 0.5, 15, "idle", "neutral")], lab: ["13", "y", [RX, 3.35, 0.5]], cam: { p: [RX + 1.4, 1.9, 4.6], t: [RX, 1.4, 0.5], fov: 50 } },
    /* 30       */ { m: "room", cast: [LEO(RX + 0.6, 0.2, 60, "idle", "sad")], lab: ["412", "r", [RX + 3.6, 3.4, -1.0]], cam: { p: [RX - 1.6, 2.4, 3.8], t: [RX + 2.3, 1.2, 0.3], fov: 52 } },
    /* 31       */ { m: "hall", cast: [LEO(HX, 4.3, 180, "reach", "sad")], hero: { open: 0.05 }, plank: 1, cam: { p: [HX + 2.6, 2.6, 2.4], t: [HX, 1.7, 3.6], fov: 46 } },
    /* 32 mia   */ { m: "room", cast: [["mia", RX - 2.6, 2.3, 120, "point", "grin"], LEO(RX + 0.6, 0.1, -100, "sad", "sad")], lab: ["MIA", "y", [RX - 2.6, 3.35, 2.3]], cam: { p: [RX + 1.6, 2.0, 3.8], t: [RX - 2.4, 1.8, 1.8], fov: 46 } },
    /* 33       */ { m: "room", cast: [["mia", RX - 1.3, 1.3, 115, "point", "smirk"], LEO(RX + 0.6, 0.3, -70, "sad", "sad")], cam: { p: [RX + 0.4, 2.0, 5.0], t: [RX - 0.4, 1.8, 0.7], fov: 45 } },
    /* 34 girl  */ { m: "day", cast: [["girl", -5.8, -14, 90, "wave", "smile"]], cam: { p: [-1, 2.2, -10], t: [-7, 2, -15], fov: 48 } },
    /* 35       */ { m: "day", cast: [["girl", -5.8, -14, 60, "holdUp", "grin"]], girlTok: 1, cam: { p: [-3.4, 1.6, -12.6], t: [-5.8, 2.6, -14], fov: 45 } },
    /* 36       */ { m: "dusk", sale: 1, girlDark: 1, cam: { p: [-1, 1.8, -9], p2: [-1.6, 1.8, -11], t: [-8, 2.5, -15], fov: 48 } },
    /* 37       */ { m: "night", sale: 1, girlDark: 1, cam: { p: [-3, 2.6, -12.6], p2: [-4.4, 2.9, -13.4], t: [-8, 3.6, -14.8], fov: 40 } },
    /* 38 mayor */ { m: "day", bb: "mayor", cr: "look", cam: { p: [-5, 1.4, -13], t: [7, 9.5, -24], fov: 55 } },
    /* 39       */ { m: "day", bb: "treasure", cam: { p: [1, 4, -18.5], p2: [2, 5, -20.5], t: [7, 9.9, -24], fov: 45 } },
    /* 40       */ { m: "day", bb: "x15", cam: { p: [-2, 2.4, -17], t: [7, 9.9, -24], fov: 45 } },
    /* 41 line  */ { m: "day", cr: "run", cam: { p: [0, 1.3, -31], t: [0, 2.2, 0], fov: 55 } },
    /* 42       */ { m: "night", cr: "queue", clock: "4:00", cam: { p: [9, 9, -18], t: [0, 1, -36], fov: 50 } },
    /* 43       */ { m: "night", cr: "queue", clock: "4:00", cam: { p: [0, 4, -29], p2: [0, 5, -32], t: [0, 6.5, -40], fov: 40 } },
    /* 44 paid  */ { m: "night", cr: "queue", money: 1, cast: [["vance", 2.4, -28, -90, "money", "smirk"], ["npc2", 1.1, -28, 90, "reach", "grin"]], cam: { p: [4.6, 2.2, -25.2], t: [1.7, 1.8, -28], fov: 48 } },
    /* 45       */ { m: "hall", cr: "hall", crPose: "reach", grid: "opening", cam: { p: [HX + 6, 4, 6], t: [HX - 2, 1, -6], fov: 50 } },
    /* 46       */ { m: "night", cr: "queue", cam: { p: [0, 22, -8], p2: [0, 24, -2], t: [0, 0, -30], fov: 50 } },
    /* 47 three */ { m: "night", clock: "3:00", cast: [LEO(0, -37.8, 180, "idle", "neutral")], cam: { p: [3.2, 2.2, -30.5], t: [0, 2.8, -40], fov: 45 } },
    /* 48 hall  */ { m: "night", cr: "queue", qOff: 1.2, clock: "4:00", doors: "open", cast: [LEO(0, -37.4, 180, "idle", "shock")], cam: { p: [3.6, 2.0, -33.2], t: [0, 2.5, -40], fov: 48 } },
    /* 49       */ { m: "hall", grid: "glow", cam: { p: [HX + 9, 6, 13], p2: [HX + 7, 5.5, 11], t: [HX - 1, 0.5, -4], fov: 55 } },
    /* 50       */ { m: "hall", grid: "opening", cr: "hall", crPose: "reach", cam: { p: [HX - 8, 3.5, 4], t: [HX + 1, 1, -6], fov: 50 } },
    /* 51       */ { m: "hall", grid: "open", cr: "hall", crTurn: 1, crPose: "sad", crEx: "sad", cam: { p: [HX - 8, 2.5, 2.0], p2: [HX + 2, 2.5, 2.0], t: [HX - 6, 2.1, -1.8], t2: [HX + 4, 2.1, -1.8], fov: 45 } },
    /* 52       */ { m: "hall", grid: "open", cr: "hall", crPose: "sad", crEx: "sad", cast: [["npc3", HX - 1.5, -1.6, 0, "sad", "cry"]], cam: { face: "npc3", d: 1.4, dx: 0.2, fov: 42 } },
    /* 53       */ { m: "hall", grid: "open", kick: 16, cast: [["npc2", HX + 4.5, -1.6, 180, "kick", "angry"]], cam: { p: [HX + 6.6, 1.7, -0.4], t: [HX + 4.5, 1.1, -2.6], fov: 50 } },
    /* 54 turn  */ { m: "hall", grid: "open", cr: "hall", crPose: "idle", crEx: "sad", cast: [LEO(HX, 8.5, 180, "walk", "neutral", { to: [HX, 4.4], dur: 1.6 })], cam: { p: [HX + 1, 2.5, 11], t: [HX, 1.4, 3], fov: 48 } },
    /* 55       */ { m: "hall", cast: [LEO(HX, 4.3, 180, "reach", "neutral")], cam: { p: [HX + 2.2, 3.0, 1.9], t: [HX, 1.3, 3.3], fov: 44, tight: 1 } },
    /* 56       */ { m: "hall", warm: 1, cast: [LEO(HX, 4.3, 180, "reach", "neutral")], cam: { p: [HX + 1.5, 1.6, 1.4], p2: [HX + 1.3, 1.55, 1.7], t: [HX, 1.2, 3], fov: 42, tight: 1 } },
    /* 57       */ { m: "hall", warm: 1, cast: [LEO(HX, 4.3, 180, "reach", "scared")], cam: { face: "leo", d: 1.35, dx: -0.2, dy: -0.15, fov: 40 } },
    /* 58 open  */ { m: "hall", hero: { open: 0.15, glow: 1 }, cast: [LEO(HX, 4.3, 180, "reach", "shock")], cam: { p: [HX + 2.4, 1.3, 1.6], t: [HX, 1.7, 3.4], fov: 50 } },
    /* 59       */ { m: "hall", hero: { open: -1, glow: 1 }, grid: "open", cr: "hallStare", crEx: "shock", cast: [LEO(HX, 4.3, 180, "idle", "shock")], cam: { p: [HX - 7, 5, 12], t: [HX, 1, 1], fov: 50 } },
    /* 60 coin  */ { m: "hall", hero: { open: -1, glow: 1 }, tok: "chest", cam: { p: [HX, 3.0, 4.1], t: [HX, 1.36, 3.0], fov: 38, tight: 1 } },
    /* 61       */ { m: "hall", hero: { open: -1, glow: 1 }, tok: "rise", cam: { p: [HX + 0.5, 2.0, 4.7], t: [HX, 1.85, 3], fov: 36, tight: 1 } },
    /* 62       */ { m: "hall", hero: { open: -1, glow: 1 }, tok: "face", cam: { p: [HX, 1.95, 4.0], p2: [HX, 1.95, 3.8], t: [HX, 1.95, 3], fov: 34, tight: 1 } },
    /* 63 token */ { m: "hall", hero: { open: -1, glow: 1 }, handTok: 1, cast: [LEO(HX, 4.7, 0, "holdUp", "wide")], lab: ["PIRATE TOKEN", "y", [HX - 0.75, 4.6, 4.7]], cam: { p: [HX + 0.9, 0.9, 7.6], t: [HX, 2.8, 4.7], fov: 52 } },
    /* 64 shake */ { m: "hall", hero: { open: -1, glow: 1 }, handTok: 1, cast: [LEO(HX, 4.7, 0, "shake", "scared")], cam: { p: [HX + 0.4, 2.1, 6.6], t: [HX, 1.9, 4.7], fov: 44 } },
    /* 65       */ { m: "hall", hero: { open: -1, glow: 1 }, handTok: 1, cast: [LEO(HX, 4.7, 0, "shake", "scared"), ["mia", HX + 1.25, 3.5, 15, "idle", "shock"]], cam: { p: [HX - 0.8, 2.3, 8.2], t: [HX + 0.5, 2.0, 4.0], fov: 46 } },
    /* 66       */ { m: "hall", hero: { open: -1, glow: 1 }, cast: [["mia", HX + 1.25, 3.5, 15, "hands", "wide"]], cam: { face: "mia", d: 1.3, dx: 0.15, fov: 42 } },
    /* 67 screen*/ { m: "hall", hero: { open: -1, glow: 1 }, bigPhone: "ping", cast: [LEO(HX, 4.3, 180, "phone", "shock")], cam: { p: [HX + 1.0, 2.7, 5.1], t: [HX + 0.3, 1.9, 3.45], fov: 42, tight: 1 } },
    /* 68       */ { m: "hall", hero: { open: -1, glow: 1 }, bigPhone: "unlock", cam: { p: [HX + 0.33, 2.15, 4.25], p2: [HX + 0.33, 2.1, 4.1], t: [HX + 0.3, 1.9, 3.45], fov: 38, tight: 1 } },
    /* 69       */ { m: "hall", hero: { open: -1, glow: 1 }, bigPhone: "d14", cam: { p: [HX + 0.45, 2.2, 4.3], p2: [HX + 0.4, 2.15, 4.1], t: [HX + 0.3, 1.9, 3.45], fov: 38, tight: 1 } },
    /* 70 stare */ { m: "hall", hero: { open: -1, glow: 1 }, cr: "stare", crEx: "shock", cast: [LEO(HX, 4.3, 0, "idle", "scared")], cam: { p: [HX, 2.35, 4.7], p2: [HX, 2.35, 5.2], t: [HX, 2.1, 11], fov: 55 } },
    /* 71       */ { m: "hall", hero: { open: -1, glow: 1 }, cr: "stare", crEx: "shock", cast: [LEO(HX, 4.3, 0, "idle", "scared"), ["vance", HX + 0.4, 12, 180, "walk", "serious", { to: [HX + 0.3, 6.4], dur: 2.4 }]], cam: { p: [HX - 0.4, 2.2, 4.8], t: [HX + 0.4, 2.2, 10], fov: 46 } },
    /* 72 whisp */ { m: "hall", dim: 1, hero: { open: -1, glow: 1 }, cr: "stare", crEx: "shock", cast: [LEO(HX, 4.3, 0, "idle", "scared"), ["vance", HX + 0.25, 6.0, 185, "idle", "serious"]], cam: { p: [HX - 1.1, 2.6, 3.2], t: [HX + 0.25, 2.25, 6.0], fov: 42 } },
    /* 73       */ { m: "hall", dim: 1, cast: [LEO(HX - 0.1, 4.3, 0, "idle", "scared"), ["vance", HX + 0.1, 5.25, 180, "lean", "serious"]], cam: { p: [HX + 2.6, 2.3, 4.8], t: [HX, 2.2, 4.8], fov: 42 } },
    /* 74       */ { m: "hall", dim: 1, cast: [["vance", HX + 0.1, 5.25, 180, "lean", "serious"]], cam: { face: "vance", d: 0.95, dx: 0.1, dy: -0.05, fov: 40 } },
    /* 75       */ { m: "void", tok: "void", tokRed: 1, cam: { p: [0, 1.8, VZ + 2.3], p2: [0, 1.8, VZ + 1.3], t: [0, 1.8, VZ], fov: 40 } },
    /* 76 smile */ { m: "hall", dim: 1, cast: [["mia", HX + 0.95, 5.5, 220, "idle", "scared"]], cam: { face: "mia", d: 1.3, dx: -0.15, fov: 42 } },
    /* 77       */ { m: "hall", dim: 1, cast: [["vance", HX + 0.25, 6.0, 140, "idle", "evil"]], cam: { face: "vance", d: 1.1, dx: 0.1, dy: -0.1, fov: 40 } },
    /* 78 night */ { m: "night", cast: [["fig", -5.6, 10, -90, "idle", "neutral"]], cam: { p: [-1, 1.6, 14.5], t: [-6.5, 2.2, 10], fov: 45 } },
    /* 79       */ { m: "night", knock: 1, cast: [["fig", -5.9, 10, -90, "knock", "neutral"]], cam: { p: [-4.4, 2.0, 7.4], t: [-6.8, 2.0, 10], fov: 42, tight: 1 } },
    /* 80       */ { m: "roomNight", cast: [["mia", RX - 3.4, 1.6, 110, "run", "scared", { to: [RX - 1.4, 0.8], dur: 1.2 }], LEO(RX - 1.4, -1.4, 60, "idle", "scared")], cam: { p: [RX + 2.6, 2.0, 3.6], t: [RX - 2, 1.5, 0], fov: 48 } },
    /* 81       */ { m: "roomNight", cast: [["mia", RX - 1.4, 0.8, 120, "idle", "scared"]], cam: { face: "mia", d: 1.25, dx: 0.15, fov: 42 } },
    /* 82       */ { m: "roomNight", cast: [LEO(RX - 0.6, -0.9, 200, "idle", "scared")], cam: { face: "leo", d: 1.3, dx: -0.15, fov: 42 } },
    /* 83       */ { m: "night", sale: 1, girlDark: 1, cam: { p: [-2, 1.4, -10], p2: [-2.6, 1.5, -11], t: [-7.5, 2.4, -14.5], fov: 42 } },
    /* 84       */ { m: "roomNight", tok: "stand", cast: [LEO(RX - 0.7, -1.7, 180, "idle", "scared")], cam: { p: [RX + 1.0, 1.9, -0.7], t: [RX - 0.8, 1.0, -3.2], fov: 50, tight: 1 } },
    /* 85       */ { m: "roomNight", tok: "stand", count: 1, cam: { p: [RX - 0.5, 1.4, -1.2], p2: [RX - 0.65, 1.35, -1.8], t: [RX - 0.8, 1.25, -3.3], fov: 45, tight: 1 } },
  ];

  // Crowd-Positionen
  const HALLSKIP = [13, 14, 16];
  function placeCrowd(mode, u, s) {
    CROWD.forEach((c) => (c.root.visible = false));
    if (!mode) return;
    const ex = s.crEx || "neutral";
    CROWD.forEach((c, i) => {
      const r = mulberry(100 + i), a = r(), b = r(), d = r();
      let x, z, ry, p = "idle", e = ex, on = true;
      if (mode === "street" || mode === "run" || mode === "look") {
        if (i >= 16) { on = false; } else {
          const side = i % 2 ? 1 : -1; x = side * (4.6 + b * 1.0); const sp = mode === "run" ? 4.5 : 1.3 + b * 0.5;
          z = 30 - a * 62; ry = 180; p = "walk";
          if (mode === "run") { x = (b - 0.5) * 7; z = 2 - a * 22 - u * sp * 0; p = d > 0.5 ? "cheer" : "run"; e = "grin"; z = -6 - a * 18 + u * sp; ry = 0; }
          else if (mode === "look") { p = "idle"; ry = 90 + (b - 0.5) * 40; z = -8 - a * 14; x = (b - 0.5) * 7; e = "shock"; }
          else z -= u * sp;
        }
      } else if (mode === "queue") {
        const k = i + (s.qOff || 0); x = (i % 2 ? 0.35 : -0.35) * (1 + d * 0.3); z = -37 + k * 1.1; ry = 180 + (b - 0.5) * 30; p = "idle"; e = d > 0.6 ? "neutral" : "smile";
      } else if (mode === "hall" || mode === "hallStare") {
        const idx = [...Array(18).keys()].filter((q) => !HALLSKIP.includes(q))[i];
        if (idx === undefined) on = false; else { const g = GRID[idx]; x = g.position.x; z = g.position.z + 1.2; ry = s.crTurn ? 0 : 180; p = s.crPose || "idle";
          if (mode === "hallStare") { ry = Math.atan2(HX - x, 3 - z) / D2R; p = "idle"; } }
      } else if (mode === "stare") {
        if (i >= 22) on = false; else { const row = Math.floor(i / 7), col = i % 7; x = HX + (col - 3) * 1.25 + (row % 2) * 0.6; z = 7.5 + row * 1.5; ry = Math.atan2(HX - x, 4.3 - z) / D2R; if (Math.abs(x - HX - 0.35) < 0.7 && row < 2 && s.cast && s.cast.some((q) => q[0] === "vance")) x += 1.4; }
      }
      c.root.visible = on; if (!on) return;
      c.root.position.set(x, 0, z); c.root.rotation.y = ry * D2R; c.setEx(e); pose(c, p, u + a * 3);
    });
  }

  const camera = new THREE.PerspectiveCamera(50, W / H, 0.05, 400);
  const lab = document.getElementById("lab"), labSpan = lab.querySelector("span");
  const LABCOL = { r: "#FF4D5E", y: "#FFD23F", g: "#5CF08C" };
  const v3 = new THREE.Vector3(), look = new THREE.Vector3();
  const blackC = new THREE.Color(0x05060A);

  function setMode(m, s) {
    const night = m === "night" || m === "roomNight", dusk = m === "dusk";
    street.visible = m === "day" || m === "night" || m === "dusk"; hall.visible = m === "hall"; room.visible = m === "room" || m === "roomNight"; voidG.visible = m === "void";
    scene.fog.color.set(night ? 0x0B1030 : dusk ? 0xF2A66B : 0xBFE0F8);
    scene.fog.near = m === "hall" || m.startsWith("room") ? 300 : 40; scene.fog.far = m === "hall" || m.startsWith("room") ? 600 : 120;
    scene.background = m === "void" ? blackC : m === "hall" ? new THREE.Color(0x120E2A) : night ? skyNight : dusk ? new THREE.Color(0xF0A060) : skyDay;
    hemi.intensity = { day: 0.9, dusk: 0.6, night: 0.4, hall: 0.35, room: 0.75, roomNight: 0.55, void: 0.08 }[m];
    hemi.color.set(night ? 0x5C74D6 : m === "hall" ? 0xB89BFF : 0xD8E8FF);
    sun.intensity = { day: 2.6, dusk: 1.6, night: 0.35, hall: 0.5, room: 2.0, roomNight: 0.25, void: 0 }[m];
    sun.color.set(night ? 0x9DB4FF : dusk ? 0xFF9A55 : 0xFFF1D8);
    nightWins.forEach((w) => (w.emissiveIntensity = night || dusk ? 1.6 : 0));
    lampLights.forEach((l) => (l.intensity = m === "night" ? 45 : dusk ? 10 : 0)); porch.intensity = m === "night" ? 14 : 0; moonL.intensity = m === "roomNight" ? 10 : 0;
    hallLights.forEach((l) => (l.intensity = m === "hall" ? (s.dim ? 40 : 70) : 0));
    roomLamp.intensity = m === "room" ? 8 : 0; winSky.material.color.set(m === "roomNight" ? 0x0B1030 : 0x8CC8FF);
    voidLight.intensity = m === "void" ? 160 : 0; voidFill.intensity = m === "void" ? 4 : 0;
    moon.visible = night; clouds.forEach((c) => (c.visible = !night));
    renderer.toneMappingExposure = m === "hall" && s.dim ? 0.92 : 1.1;
  }

  function render(t) {
    let i = 0; for (let k = 0; k < LS.length; k++) if (t >= LS[k]) i = k;
    const s = S[i], t0 = LS[i], t1 = i + 1 < LS.length ? LS[i + 1] : DUR, u = t - t0, dur = t1 - t0, p = ease(u / dur);
    setMode(s.m, s);
    // Figuren
    for (const k in A) A[k].root.visible = false;
    const castPos = {};
    (s.cast || []).forEach(([name, x, z, r, ps, ex, o]) => {
      const ch = A[name]; ch.root.visible = true; let X = x, Z = z, P = ps;
      if (o && o.to) { const q = clamp(u / o.dur, 0, 1); X = x + (o.to[0] - x) * q; Z = z + (o.to[1] - z) * q; if (q >= 1) P = "idle"; }
      ch.root.position.set(X, (o && o.y) || 0, Z); ch.root.rotation.y = r * D2R; ch.setEx(ex); pose(ch, P, u); castPos[name] = [X, Z, r];
    });
    placeCrowd(s.cr, u, s);
    // Requisiten
    money.visible = !!s.money; handTok.visible = !!s.handTok; girlTok.visible = !!s.girlTok; phone.visible = false; bigPhone.visible = !!s.bigPhone; if (s.bigPhone) bigScr.userData.set(s.bigPhone); phoneGlow.intensity = s.bigPhone ? 3 : 0;
    plank.visible = false; if (s.plank) { const q = clamp((u - 0.5) / 0.5, 0, 1); plank.visible = q > 0; plank.position.set(HX, 1.0 + outBack(q) * 0.9, 3); plank.rotation.set(0, u * 2, 0.3); }
    giftTok.visible = !!s.gift; if (s.gift) { giftTok.position.set(...s.gift); giftTok.rotation.y = u * 2; }
    sale.visible = !!s.sale; girlWinM.forEach((m) => { m.emissiveIntensity = s.girlDark ? 0 : m.emissiveIntensity; if (s.girlDark) m.color.set(0x1A1E2A); else m.color.set(0xFFD98A); });
    billboard.userData.set(s.bb || "mayor"); shopSign.userData.set(s.shop || "price"); clock.userData.set(s.clock || "8:00"); hallScreen.userData.set("x");
    // Hallentüren
    let dq = 0; if (s.doors === "open") dq = ease((u - 0.3) / 1.0); if (s.doors === "isopen") dq = 1;
    doorL.position.x = -1.0 - dq * 1.9; doorR.position.x = 1.0 + dq * 1.9; doorGlow.visible = dq > 0;
    // Truhen
    const hs = s.hero || {}; let ho = 0; if (hs.open === -1) ho = 1; else if (hs.open !== undefined) ho = outBack((u - hs.open) / 0.45);
    const warm = s.warm ? 0.5 + 0.35 * Math.sin(u * 7) : 0;
    setChest(hero, clamp(ho, 0, 1.08), hs.glow ? 1 : 0, warm);
    heroLight.intensity = hs.glow && ho > 0.1 ? (hs.open === -1 ? 14 : 30 * clamp((u - hs.open) / 0.4, 0, 1) + 8) : s.warm ? 10 + 6 * Math.sin(u * 7) : 0;
    heroLight.color.set(s.warm ? 0xFF5A20 : 0xFFC040);
    GRID.forEach((c, k) => { let o = 0, gl = s.grid === "glow" ? 1 : 0;
      if (s.grid === "open") o = 1; if (s.grid === "opening") o = outBack((u - 0.2 - mulberry(k + 9)() * 0.5) / 0.45);
      if (Array.isArray(s.grid)) s.grid.forEach(([idx, dl]) => { if (idx === k) o = dl < 0 ? 1 : outBack((u - dl) / 0.45); });
      setChest(c, clamp(o, 0, 1.08), gl, 0); c.rotation.z = 0; c.position.y = 0.6;
      if (s.kick === k) { const q = Math.max(0, Math.sin(clamp((u - 0.25) * 6, 0, Math.PI))); c.rotation.z = -0.25 * q; c.position.y = 0.6 + 0.12 * q; } });
    // Gold-Glanz (Vance besitzt halbe Stadt)
    // Token
    token.visible = !!s.tok; countdown.visible = false;
    if (s.tok) { const tf = token.userData.face; tf.emissive.set(s.tokRed ? 0xFF2030 : 0xFFFFFF); tf.emissiveIntensity = s.tokRed ? 0.8 + 0.4 * Math.sin(u * 9) : 0.25;
      token.rotation.set(0, 0, 0); token.scale.setScalar(1);
      if (s.tok === "void") { token.position.set(0, 1.8 + Math.sin(u * 2) * 0.05, VZ); token.rotation.y = 0.6 * Math.sin(u * 1.4) + (s.tokRed ? 0 : u * 0.8); }
      if (s.tok === "chest") { token.position.set(HX, 1.36, 3); token.rotation.x = -Math.PI / 2; token.scale.setScalar(0.55); token.rotation.z = u * 0.4; }
      if (s.tok === "rise") { token.position.set(HX, 1.4 + ease(u / 1.2) * 0.5, 3); token.scale.setScalar(0.55); token.rotation.y = u * 2.2; }
      if (s.tok === "face") { token.position.set(HX, 1.95, 3); token.scale.setScalar(0.55); token.rotation.y = Math.sin(u * 1.5) * 0.25; }
      if (s.tok === "stand") { token.position.set(RX - 0.8, 0.95, -3.3); token.scale.setScalar(0.6); tf.emissive.set(0xFF2030); tf.emissiveIntensity = 0.5 + 0.4 * Math.sin(u * 6); }
    }
    nightLamp.intensity = s.tok === "stand" ? 3 + 2 * Math.sin(u * 6) : 0;
    if (s.count) { countdown.visible = true; const left = 14 * 86400 - 1 - Math.floor(u); const d = Math.floor(left / 86400), h = Math.floor(left % 86400 / 3600), mi = Math.floor(left % 3600 / 60), se = left % 60;
      countdown.userData.set(`${d}d ${String(h).padStart(2, "0")}:${String(mi).padStart(2, "0")}:${String(se).padStart(2, "0")}`);
      countdown.position.set(RX - 0.8, 1.55, -3.3); countdown.scale.setScalar(0.5 * outBack(u / 0.4) + 0.001); }
    SPARK.forEach((sp) => { const d = sp.userData, a = d.a + u * 0.4; sp.position.set(Math.cos(a) * d.r, d.y + Math.sin(u + d.o * 6) * 0.2, VZ + Math.sin(a) * d.r); sp.rotation.y = u * 2; sp.material.color.set(s.tokRed ? 0xFF3040 : 0xFFD45A); });
    // Klopfen: Tür zittert
    leoHouse.userData.door.position.z = 0.05; if (s.knock) { for (const kt of [0.05, 0.42, 0.79]) { const q = u - kt; if (q > 0 && q < 0.15) leoHouse.userData.door.position.z = 0.05 - 0.04 * Math.sin(q / 0.15 * Math.PI); } }
    // Kamera
    const c = s.cam; let P, Tg;
    if (c.face) { const [x, z, r] = castPos[c.face]; const ch = A[c.face]; const hy = 2.31 * ch.root.scale.y + (ch.root.position.y || 0);
      const f = [Math.sin(r * D2R), Math.cos(r * D2R)], rt = [Math.cos(r * D2R), -Math.sin(r * D2R)], d = c.d * 1.55 * (1 - 0.06 * p);
      P = [x + f[0] * d + rt[0] * (c.dx || 0), hy + (c.dy || 0), z + f[1] * d + rt[1] * (c.dx || 0)]; Tg = [x, hy - 0.02, z]; }
    else if (c.pPhone) { phone.updateWorldMatrix(true, false); const pw = new THREE.Vector3(); phone.getWorldPosition(pw); const q = (1 - 0.08 * p);
      P = [pw.x + c.pPhone[0], pw.y + c.pPhone[1] * q, pw.z + c.pPhone[2] * q]; Tg = [pw.x, pw.y, pw.z]; }
    else { const p2 = c.p2 || [c.p[0] + (c.t[0] - c.p[0]) * 0.08, c.p[1] + (c.t[1] - c.p[1]) * 0.08, c.p[2] + (c.t[2] - c.p[2]) * 0.08];
      P = [0, 1, 2].map((k) => c.p[k] + (p2[k] - c.p[k]) * p); const t2 = c.t2 || c.t; Tg = [0, 1, 2].map((k) => c.t[k] + (t2[k] - c.t[k]) * p);
      const dd = Math.hypot(P[0] - Tg[0], P[1] - Tg[1], P[2] - Tg[2]); if (!c.tight && s.m !== "void" && dd < 3.2) { const f = 1.5; P = [0, 1, 2].map((k) => Tg[k] + (P[k] - Tg[k]) * f); } }
    camera.position.set(...P); look.set(...Tg); camera.fov = c.fov; camera.updateProjectionMatrix(); camera.lookAt(look);
    sun.position.set(Tg[0] - 8, Tg[1] + 14, Tg[2] + 9); sun.target.position.set(Tg[0], Tg[1], Tg[2]);
    renderer.render(scene, camera);
    // Schwebendes Label
    if (s.lab) { v3.set(...s.lab[2]).project(camera); const on = v3.z < 1; lab.style.display = on ? "block" : "none";
      if (on) { labSpan.textContent = s.lab[0]; labSpan.style.color = LABCOL[s.lab[1]]; lab.style.left = clamp((v3.x + 1) / 2 * W, 300, W - 300) + "px";
        lab.style.top = clamp((1 - v3.y) / 2 * H, 330, 1050) + "px"; const q = clamp(u / 0.22, 0, 1); labSpan.style.transform = `scale(${0.4 + 0.6 * outBack(q)})`; labSpan.style.opacity = q > 0 ? 1 : 0; } }
    else lab.style.display = "none";
  }

  const st = { t: 0 };
  const tl = gsap.timeline({ paused: true });
  tl.to(st, { t: DUR, duration: DUR, ease: "none", onUpdate: () => render(st.t) }, 0);
  window.__timelines["world"] = tl;
  return document.fonts.load("80px Lilita").then(() => render(0));
}).catch((e) => { console.error("world build failed", e); throw e; });
"""


def world_html():
    js = WORLD_JS.replace("__LS__", json.dumps(LS)).replace("__DUR__", str(TOTAL))
    return f"""<template>
  <style>
    @font-face {{ font-family: 'Lilita'; src: url('assets/LilitaOne-Regular.ttf') format('truetype'); }}
    #root {{ position:absolute; inset:0; background:#0B1030; }}
    #w-canvas {{ position:absolute; left:0; top:0; width:{W}px; height:{H}px; }}
    #lab {{ position:absolute; display:none; transform:translate(-50%,-50%); white-space:nowrap; }}
    #lab span {{ display:inline-block; font-family:'Lilita',sans-serif; font-size:76px; letter-spacing:0.01em;
      -webkit-text-stroke:12px #000; paint-order:stroke fill; text-shadow:0 6px 0 #000; }}
  </style>
  <div id="root" data-composition-id="world" data-width="{W}" data-height="{H}" data-duration="{fmt(TOTAL)}" data-layout-allow-overlap>
    <canvas id="w-canvas" width="{W}" height="{H}"></canvas>
    <div id="lab"><span>LABEL</span></div>
  </div>
  <script>
{js}
  </script>
</template>
"""


def captions_html():
    """Genau ein Wort pro Untertitel – Neon-Gelb, Lilita One, dicke Kontur (Referenz B/C). Markierte Wörter größer."""
    items = []
    for l in LINES:
        marks = []
        for m in re.finditer(r"\{(\w):([^}]*)\}|([^{}\s]+)", l["show"]):
            marks += [False] * len(m.group(3).split()) if m.group(3) else [True] * len(m.group(2).split())
        for w, mk in zip(l["words"], marks):
            items.append((w["text"].strip(".,:;!?"), w["start"], w["end"], mk))
    groups, js = [], []
    for i, (txt, s, e, mk) in enumerate(items):
        nxt = items[i + 1][1] if i + 1 < len(items) else TOTAL
        end = min(nxt - 0.02, e + 0.45)
        st = max(0.03, s - 0.02)
        gid = f"wd{i}"
        cls = "wd big" if mk else "wd"
        groups.append(f'<div id="{gid}" class="clip {cls}" data-start="{fmt(st)}" data-duration="{fmt(max(0.08, end - st))}" data-track-index="1">'
                      f'<span>{txt}</span></div>')
        js.append(f'    tl.fromTo("#{gid} span", {{scale:0.82}}, {{scale:1, duration:0.1, ease:"back.out(3)"}}, {fmt(st)});')
    return f"""<template>
  <style>
    @font-face {{ font-family: 'Lilita'; src: url('assets/LilitaOne-Regular.ttf') format('truetype'); }}
    #root {{ position:absolute; inset:0; }}
    .wd {{ position:absolute; left:40px; right:40px; top:1290px; text-align:center; overflow:visible; }}
    .wd span {{ display:inline-block; font-family:'Lilita',sans-serif; font-size:100px; line-height:1; color:#E8FF3A;
      -webkit-text-stroke:18px #000; paint-order:stroke fill; text-shadow:0 7px 0 #000, 0 0 24px rgba(0,0,0,0.45); }}
    .wd.big span {{ font-size:122px; }}
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


def line_word(i, prefix, n=1):
    k = 0
    for w in LINES[i]["words"]:
        if re.sub(r"[^\w'-]", "", w["text"]).lower().startswith(prefix.lower()):
            k += 1
            if k == n:
                return w["start"]
    raise KeyError((i, prefix))


# Ton: Whoosh bei Beat-Wechsel, Effekte an Story-Momenten (Zeilen-Index 0-basiert)
SFX = []
beat_first = []
n = 0
for b in T["beats"]:
    beat_first.append(n)
    n += len(b["lines"])
for i in beat_first[1:]:
    SFX.append((LS[i] - 0.1, "whoosh-short.mp3", 0.3))
for i, f, v, off in [
    (1, "pop.mp3", 0.45, 0.4), (3, "sparkle.mp3", 0.5, 0.0), (5, "chime.mp3", 0.4, 0.1), (9, "pop.mp3", 0.4, 0.15),
    (12, "impact-bass-2.mp3", 0.4, 0.2), (16, "error.mp3", 0.35, 0.3), (17, "error.mp3", 0.35, 0.3), (19, "sparkle.mp3", 0.4, 0.0),
    (22, "chime.mp3", 0.45, 0.1), (29, "impact-bass-1.mp3", 0.35, 0.2), (30, "pop.mp3", 0.4, 0.5), (34, "sparkle.mp3", 0.4, 0.2),
    (37, "notification.mp3", 0.45, 0.0), (38, "riser.mp3", 0.3, 0.0), (39, "chime.mp3", 0.4, 0.1), (43, "chime.mp3", 0.35, 0.2),
    (47, "whoosh-cinematic.mp3", 0.4, 0.2), (48, "sparkle.mp3", 0.4, 0.0), (49, "pop.mp3", 0.4, 0.2), (50, "error.mp3", 0.3, 0.0),
    (52, "impact-bass-1.mp3", 0.4, 0.3), (56, "riser.mp3", 0.35, 0.0), (57, "impact-bass-2.mp3", 0.5, 0.15), (57, "sparkle.mp3", 0.5, 0.2),
    (60, "sparkle.mp3", 0.4, 0.0), (62, "impact-bass-2.mp3", 0.45, 0.0), (66, "notification.mp3", 0.5, 0.0), (67, "chime.mp3", 0.45, 0.0),
    (74, "glitch-1.mp3", 0.35, 0.0), (76, "impact-bass-1.mp3", 0.35, 0.0), (83, "impact-bass-2.mp3", 0.4, 0.0), (84, "glitch-2.mp3", 0.35, 0.3),
]:
    SFX.append((LS[i] + off, f, v))
for kt in (0.05, 0.42, 0.79):  # Klopfen: drei Schläge
    SFX.append((LS[78] + kt, "impact-bass-1.mp3", 0.55))
for k in range(int(TOTAL - LS[84]) + 1):  # Countdown-Ticken
    if LS[84] + k + 0.3 < TOTAL - 0.2:
        SFX.append((LS[84] + k + 0.3, "click.mp3", 0.35))


def write():
    comp = HERE / "compositions"
    comp.mkdir(exist_ok=True)
    (comp / "world.html").write_text(world_html())
    (comp / "captions.html").write_text(captions_html())
    (HERE / "assets" / "sfx").mkdir(parents=True, exist_ok=True)
    audio = []
    if (HERE / "assets" / "voice.wav").exists():
        audio.append('      <audio id="voice" class="clip" src="assets/voice.wav" data-start="0" data-track-index="10" data-volume="1"></audio>')
    for j, (t, f, vol) in enumerate(sorted(SFX)):
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
      @font-face {{ font-family: 'Lilita'; src: url('assets/LilitaOne-Regular.ttf') format('truetype'); }}
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:#0B1030; }}
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
    print("total", TOTAL, "shots", len(LS), "sfx", len(SFX))


if __name__ == "__main__":
    write()
