#!/usr/bin/env python3
"""Builds "The Storm Egg" (English) – blocky-3D storytime in the style of references/storytime.md:
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
TITLE = "The Storm Egg"

T = load_timings(HERE)
LINES = [l for b in T["beats"] for l in b["lines"]]
VOICE_END = T["beats"][-1]["end"]
TOTAL = round(VOICE_END + 1.8, 2)
# Einstellungen: Startzeile je Schnitt (mehrere kurze Zeilen = eine Einstellung, ~2 s wie in den Referenzen)
SHOT_LINES = [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 13, 14, 15, 16, 18, 20, 21, 23, 26, 28, 30, 31, 33, 35, 36, 38, 39, 40, 41, 43, 44,
              46, 48, 51, 53, 55, 56, 58, 60, 61, 63, 64, 65, 66, 67, 68, 69, 70, 72, 73, 76, 77, 79, 82, 85, 87, 89, 91, 94, 96, 97, 99, 100]
LS = [0.0] + [round(LINES[i]["start"] - 0.06, 3) for i in SHOT_LINES[1:]]


def wt(line, prefix, n=1):
    k = 0
    for w in LINES[line]["words"]:
        if re.sub(r"[^\w']", "", w["text"]).lower().startswith(prefix.lower()):
            k += 1
            if k == n:
                return round(w["start"], 3)
    raise KeyError((line, prefix))


KW = {"hatched": wt(19, "hatched"), "icecream": wt(31, "dropped"), "lightning": wt(60, "struck"), "crack": wt(68, "crack"), "ate": wt(78, "ate"),
      "b1": wt(79, "one"), "b2": wt(80, "two"), "b3": wt(81, "three"), "fire": wt(4, "fire"), "ice": wt(5, "ice"), "bubbles": wt(7, "bubbles"),
      "sun": wt(12, "sun"), "red": wt(14, "red"), "green": wt(15, "green"), "didnt": wt(20, "didn"), "plane": wt(22, "plane"), "titan": wt(28, "titan"),
      "dryer": wt(34, "hair"), "micro": wt(41, "microwave"), "bad": wt(43, "bad"), "stairs": wt(46, "stairs"), "backpack": wt(50, "backpack"),
      "race": wt(52, "great"), "saddle": wt(53, "golden"), "finish": wt(57, "finish"), "storm": wt(59, "storm"), "away": wt(62, "away"),
      "dark": wt(64, "dark"), "glowing": wt(69, "glowing"), "potato": wt(72, "potato"), "nice": wt(75, "nice"), "bigger": wt(83, "bigger"),
      "flew": wt(88, "flew"), "home": wt(90, "home"), "won": wt(95, "won"), "miles": wt(96, "three"), "weather": wt(101, "weather")}

WORLD_JS = r"""
const LS = __LS__, DUR = __DUR__, KW = __KW__;
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
  let drawBillboard = function (g, k, w, h) {
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
  let drawShopSign = function (g, k, w, h) { g.fillStyle = "#1A1030"; g.fillRect(0, 0, w, h);
    if (k === "free") { glowText(g, "FREE", w / 2, h / 2, h * 0.6, "#3DDC84"); } else { glowText(g, "$$$", w / 2, h / 2, h * 0.6, "#FF3B9A"); } }
  function drawCount(g, k, w, h) { g.clearRect(0, 0, w, h); g.fillStyle = "rgba(20,0,4,0.75)"; g.fillRect(0, 0, w, h); glowText(g, k, w / 2, h / 2 + 4, h * 0.55, "#FF2A3D"); }
  function drawHead(g, cx, cy, s, skin, hair, shirt, grin) {
    g.fillStyle = shirt; g.fillRect(cx - 1.1 * s, cy + 0.55 * s, 2.2 * s, 1.2 * s);
    g.fillStyle = skin; g.fillRect(cx - 0.55 * s, cy - 0.55 * s, 1.1 * s, 1.1 * s); g.fillStyle = hair; g.fillRect(cx - 0.6 * s, cy - 0.68 * s, 1.2 * s, 0.3 * s);
    g.fillStyle = "#1B1410"; g.fillRect(cx - 0.3 * s, cy - 0.12 * s, 0.12 * s, 0.18 * s); g.fillRect(cx + 0.18 * s, cy - 0.12 * s, 0.12 * s, 0.18 * s);
    g.strokeStyle = "#1B1410"; g.lineWidth = s * 0.06; g.beginPath(); g.arc(cx, cy + 0.14 * s, 0.22 * s, 0.2 * Math.PI, 0.8 * Math.PI); g.stroke(); }
  const drawBillboard0 = drawBillboard;
  drawBillboard = function (g, k, w, h) {
    if (k === "games") { g.fillStyle = "#1A0F3A"; g.fillRect(0, 0, w, h); drawMayor(g, w * 0.2, h * 0.42, h * 0.24); glowText(g, "GIANT", w * 0.64, h * 0.24, h * 0.17, "#FFC531"); glowText(g, "GAMES", w * 0.64, h * 0.44, h * 0.17, "#FFC531");
      big(g, "WINNER GETS", w * 0.64, h * 0.62, h * 0.08, "#FFFFFF"); glowText(g, "$10,000,000", w * 0.62, h * 0.8, h * 0.14, "#5CF08C"); g.strokeStyle = "#FFC531"; g.lineWidth = 10; g.strokeRect(5, 5, w - 10, h - 10); return; }
    if (!["h24", "honest", "stay", "mayorTV"].includes(k)) return drawBillboard0(g, k, w, h);
    g.fillStyle = { h24: "#2A0C14", honest: "#10223A", stay: "#2A0C14", mayorTV: "#0E1638" }[k]; g.fillRect(0, 0, w, h);
    g.fillStyle = "rgba(255,255,255,0.04)"; for (let y = 0; y < h; y += 6) g.fillRect(0, y, w, 2);
    if (k === "h24") { g.save(); g.shadowColor = "#FF2A2A"; g.shadowBlur = 60; g.fillStyle = "#FF3B3B"; g.beginPath(); g.arc(w / 2, h * 0.3, h * 0.13, 0, 6.3); g.fill(); g.restore();
      glowText(g, "1 LIE =", w / 2, h * 0.6, h * 0.14, "#FFFFFF"); glowText(g, "24 HOURS", w / 2, h * 0.82, h * 0.2, "#FF3B5C"); }
    if (k === "honest") { drawHead(g, w * 0.27, h * 0.45, h * 0.3, "#F1C27D", "#3A2214", "#3A86FF"); g.fillStyle = "#F2B632"; g.beginPath(); g.arc(w * 0.27, h * 0.85, h * 0.07, 0, 6.3); g.fill();
      big(g, "MOST HONEST", w * 0.68, h * 0.36, h * 0.12, "#FFD23F"); big(g, "KID IN TOWN", w * 0.68, h * 0.54, h * 0.12, "#FFD23F"); glowText(g, "NOAH", w * 0.68, h * 0.76, h * 0.15, "#5CF08C"); }
    if (k === "stay" || k === "mayorTV") { drawMayor(g, w * 0.27, h * 0.42, h * 0.3); g.fillStyle = "#E11D48"; g.fillRect(w * 0.55, h * 0.14, w * 0.38, h * 0.13); big(g, "LIVE", w * 0.74, h * 0.205, h * 0.1, "#FFF");
      if (k === "stay") { glowText(g, "STAY", w * 0.74, h * 0.48, h * 0.2, "#FF3B5C"); glowText(g, "INSIDE", w * 0.74, h * 0.72, h * 0.2, "#FF3B5C"); }
      else { big(g, "MAYOR", w * 0.74, h * 0.5, h * 0.12, "#FFD23F"); big(g, "ADDRESS", w * 0.74, h * 0.68, h * 0.12, "#FFD23F"); } }
    g.strokeStyle = "#FFC531"; g.lineWidth = 10; g.strokeRect(5, 5, w - 10, h - 10);
  };
  const drawShop0 = drawShopSign;
  drawShopSign = function (g, k, w, h) { if (k !== "nolight") return drawShop0(g, k, w, h); g.fillStyle = "#1A1030"; g.fillRect(0, 0, w, h);
    g.save(); g.shadowColor = "#FF2A2A"; g.shadowBlur = 30; g.strokeStyle = "#FF3B3B"; g.lineWidth = 10; g.beginPath(); g.arc(h * 0.6, h / 2, h * 0.32, 0, 6.3); g.stroke();
    g.beginPath(); g.moveTo(h * 0.37, h * 0.27); g.lineTo(h * 0.83, h * 0.73); g.stroke(); g.restore(); glowText(g, "NO RED LIGHTS", w * 0.58, h / 2 + 3, h * 0.36, "#FF3B5C"); };
  function drawMsg(g, k, w, h) {
    g.fillStyle = "#0F1320"; g.fillRect(0, 0, w, h); big(g, "UNKNOWN", w / 2, h * 0.08, w * 0.11, "#FF5A6A"); big(g, "NUMBER", w / 2, h * 0.15, w * 0.11, "#FF5A6A");
    const n = +k; if (n === 0) { g.fillStyle = "#3A86FF"; g.beginPath(); g.arc(w / 2, h * 0.5, w * 0.18, 0, 6.3); g.fill(); big(g, "1", w / 2, h * 0.505, w * 0.2, "#FFF"); big(g, "NEW MESSAGE", w / 2, h * 0.7, w * 0.09, "#FFF"); return; }
    const msgs = [["Your light", "is off."], ["Don't let", "them see you."]];
    for (let i = 0; i < Math.min(n - 1, 2); i++) { const y = h * (0.26 + i * 0.22); g.fillStyle = "#2A2F45"; g.beginPath(); g.roundRect(w * 0.08, y, w * 0.84, h * 0.17, 18); g.fill();
      big(g, msgs[i][0], w / 2, y + h * 0.055, w * 0.1, i ? "#FF5A6A" : "#FFFFFF"); big(g, msgs[i][1], w / 2, y + h * 0.115, w * 0.1, i ? "#FF5A6A" : "#FFFFFF"); } }

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
  const GLOW = (() => { const c = cv(128, 128), g = c.getContext("2d"); const gr = g.createRadialGradient(64, 64, 4, 64, 64, 64);
    gr.addColorStop(0, "rgba(255,255,255,1)"); gr.addColorStop(0.25, "rgba(255,120,120,0.7)"); gr.addColorStop(1, "rgba(255,0,0,0)"); g.fillStyle = gr; g.fillRect(0, 0, 128, 128);
    const t = new THREE.CanvasTexture(c); return t; })();
  function lampSet(ch, on, at, u) { ch.lamp.visible = on && (at === undefined || u >= at); if (ch.lamp.visible) { const q = at === undefined ? 1 : outBack((u - at) / 0.25);
      ch.lamp.scale.setScalar(Math.max(0.01, q) * (1 + 0.06 * Math.sin(u * 8))); } }
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
    if (hs === "bowl") { box(0.76, 0.3, 0.76, hm, 0, 0.66, 0, head); box(0.76, 0.16, 0.12, hm, 0, 0.5, 0.33, head); box(0.12, 0.3, 0.7, hm, 0.35, 0.48, 0, head); box(0.12, 0.3, 0.7, hm, -0.35, 0.48, 0, head);
      for (let i = 0; i < 5; i++) { const b = box(0.12, 0.34, 0.12, hm, -0.24 + i * 0.12, 0.92, -0.05 + (i % 2) * 0.1, head); b.rotation.z = (i - 2) * 0.3; } }
    if (hs === "bun") { box(0.68, 0.16, 0.68, hm, 0, 0.66, -0.01, head); box(0.68, 0.36, 0.14, hm, 0, 0.5, -0.29, head); box(0.12, 0.3, 0.6, hm, 0.31, 0.52, -0.02, head); box(0.12, 0.3, 0.6, hm, -0.31, 0.52, -0.02, head); box(0.3, 0.3, 0.3, hm, 0, 0.82, -0.2, head); }
    if (hs === "chef") { const cm = std({ color: 0xFFFFFF }); box(0.68, 0.16, 0.68, cm, 0, 0.68, 0, head); const c2 = add(new THREE.Mesh(new THREE.CylinderGeometry(0.4, 0.32, 0.5, 20), cm), head); c2.position.y = 1.0; }
    if (o.dark) { root.scale.setScalar(1.18); }
    // rotes Licht über dem Kopf
    const lamp = new THREE.Group(); lamp.position.y = hs === "chef" || hs === "tophat" ? 1.62 : 1.18; head.add(lamp);
    const core = new THREE.Mesh(new THREE.SphereGeometry(0.12, 16, 12), basic({ color: 0xFF2A2A, toneMapped: false })); lamp.add(core);
    const halo = new THREE.Sprite(new THREE.SpriteMaterial({ map: GLOW, color: 0xFF3030, blending: THREE.AdditiveBlending, depthWrite: false, transparent: true, toneMapped: false })); halo.scale.set(1.1, 1.1, 1); lamp.add(halo);
    lamp.visible = false;
    const ch = { root, armL, armR, legL, legR, head, faceM, o, ex: null, lamp };
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
    if (p === "sit") { legL.rotation.x = -1.5; legR.rotation.x = -1.5; bob = -0.5; armL.rotation.x = -0.9; armR.rotation.x = -0.9; }
    if (p === "no") { head.rotation.y = Math.sin(u * 9) * 0.4; head.rotation.x = 0.15; }
    if (p === "lookUp") { head.rotation.x = -0.55; }
    if (p === "sad2") { head.rotation.x = 0.3; armL.rotation.x = -0.2; armR.rotation.x = -0.2; }
    root.position.y += bob;
  }

  const SKIN = [0xF1C27D, 0xE0AC69, 0xC68642, 0x8D5524, 0xFFDBAC, 0xD8A06A];
  const SHIRT = [0x2B7BE4, 0xE63946, 0x2A9D8F, 0xF4A261, 0x8338EC, 0x06D6A0, 0xFFBE0B, 0xFB5607, 0x3A86FF, 0xEF476F, 0x118AB2, 0x7B2CBF];
  const HAIRC = [0x2B1A10, 0x4A2E1A, 0x1A1A1A, 0xC98B3C, 0x6B3E1E, 0xE8C66A];
  const A = {
    kai: makeChar({ shirt: 0x2A9D8F, pants: 0x22304A, design: "hoodie", hair: "messy", hairCol: 0x3A2214, skin: 0xF1C27D, shoe: 0xEEEEEE }),
    friend: makeChar({ shirt: 0xE63946, pants: 0x2E3A59, design: "star", hair: "short", hairCol: 0x6B3E1E, skin: 0xE0AC69 }),
    blake: makeChar({ shirt: 0x6A1B9A, pants: 0x22304A, design: "suit", hair: "short", hairCol: 0xF2D16B, skin: 0xFFDBAC, shoe: 0x111111 }),
    k1: makeChar({ shirt: 0xFFBE0B, pants: 0x3D3D5C, hair: "pony", hairCol: 0xC98B3C, skin: 0xFFDBAC, blush: true }),
    k2: makeChar({ shirt: 0x3A86FF, pants: 0x22304A, hair: "cap", capCol: 0xE63946, skin: 0x8D5524 }),
    k3: makeChar({ shirt: 0x06D6A0, pants: 0x2E2E2E, hair: "bun", hairCol: 0x2B1A10, skin: 0xC68642 }),
    mayor: makeChar({ shirt: 0x1E3A8A, pants: 0x14234F, design: "suit", hair: "short", hairCol: 0xD9DDE3, skin: 0xF0C49A, stache: true }),
  };
  const CROWD = [];
  for (let i = 0; i < 24; i++) CROWD.push(makeChar({ shirt: pick(SHIRT), pants: pick([0x2E3A59, 0x22304A, 0x3D3D5C, 0x4A4A4A, 0x5C4033]), skin: pick(SKIN),
    hair: pick(["short", "short", "messy", "cap", "long", "pony", "bun"]), hairCol: pick(HAIRC), capCol: pick(SHIRT), design: pick([null, "stripe", "star", null]) }));

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
  const shop = house(1, -2, { w: 8, h: 5, flat: true, wall: std({ map: brickT }), door: 0x2B2B2B, darkW: true, wins: [[-2.6, 1.7], [2.6, 1.7]] });
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
  const hallSign = screen(10, 1.6, 900, 144, (g, k, w, h) => { g.fillStyle = "#151030"; g.fillRect(0, 0, w, h); glowText(g, "TOWN HALL", w / 2, h / 2 + 4, h * 0.62, "#FFC531"); }); hallSign.position.set(0, 8.4, 0.08); hallB.add(hallSign); hallSign.userData.set("x");
  const clock = screen(2.8, 1.1, 336, 132, drawClock); clock.position.set(0, 6.3, 0.08); hallB.add(clock);
  // Laternen, Bäume, Schild "FOR SALE"
  const lampLights = [];
  for (const [x, z] of [[-4.6, 14], [4.6, -11], [-4.6, -6], [4.6, -16], [-4.6, -26], [4.6, -34], [-4.6, 24]]) {
    box(0.18, 4.4, 0.18, std({ color: 0x2B2B33, metalness: 0.5 }), x, 2.2, z, street); box(0.9 * Math.sign(-x), 0.14, 0.14, std({ color: 0x2B2B33 }), x - 0.45 * Math.sign(x), 4.35, z, street);
    const bulb = box(0.4, 0.2, 0.4, litWin.clone(), x - 0.85 * Math.sign(x), 4.2, z, street, false); nightWins.push(bulb.material);
    const pl = new THREE.PointLight(0xFFB566, 0, 14, 1.6); pl.position.set(x - 0.85 * Math.sign(x), 4.0, z); street.add(pl); lampLights.push(pl); }
  const barkM = std({ color: 0x6B4A2F }), leafMs = [0x4E9A3A, 0x5DAF45, 0x438A33].map((c) => std({ color: c, flatShading: true }));
  for (const [x, z, s] of [[-4.4, 17.5, 1], [4.4, 11, 1.1], [-4.4, -10, 0.9], [4.4, -9, 1], [-4.4, -19, 1.1], [4.4, 21, 0.9], [-4.4, 31, 1]]) {
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
  const poster = screen(1.6, 1.2, 320, 240, (g, k, w, h) => { g.fillStyle = "#FFF7E0"; g.fillRect(0, 0, w, h); g.strokeStyle = "#C9A23A"; g.lineWidth = 10; g.strokeRect(8, 8, w - 16, h - 16);
    big(g, "MOST HONEST", w / 2, h * 0.3, 34, "#1E3A8A"); big(g, "KID IN TOWN", w / 2, h * 0.5, 34, "#1E3A8A"); g.fillStyle = "#F2B632"; g.beginPath(); g.arc(w / 2, h * 0.75, 22, 0, 6.3); g.fill(); }, false);
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

  // ---------- KÜCHE (x = -400)
  const KX = -400;
  const kitchen = new THREE.Group(); scene.add(kitchen);
  const tileT = tex(128, 128, 61, (g, r, w, h) => { for (let y = 0; y < 2; y++) for (let x = 0; x < 2; x++) { g.fillStyle = (x + y) % 2 ? "#E8E2D6" : "#C9C2B4"; g.fillRect(x * 64, y * 64, 64, 64); } }, [6, 6]);
  { const f = add(new THREE.Mesh(new THREE.PlaneGeometry(9, 9), std({ map: tileT })), kitchen, false, true); f.rotation.x = -Math.PI / 2; f.position.set(KX, 0, 0);
    const wm = std({ color: 0xF2E3B8 });
    box(9, 1.6, 0.2, wm, KX, 0.8, -4.5, kitchen); box(9, 1.1, 0.2, wm, KX, 3.45, -4.5, kitchen); box(3.4, 1.3, 0.2, wm, KX - 2.8, 2.25, -4.5, kitchen); box(3.4, 1.3, 0.2, wm, KX + 2.8, 2.25, -4.5, kitchen);
    box(0.2, 4, 9, wm, KX - 4.5, 2, 0, kitchen); box(0.2, 4, 9, wm, KX + 4.5, 2, 0, kitchen);
    box(2.2, 0.12, 0.3, std({ color: 0xFFFFFF }), KX, 1.55, -4.35, kitchen);
    // Küchenzeile, Kühlschrank
    box(4.2, 1.0, 0.8, std({ color: 0x7FB7A0 }), KX + 2.2, 0.5, -4.0, kitchen); box(4.3, 0.08, 0.85, std({ color: 0xEDEDED }), KX + 2.2, 1.04, -4.0, kitchen);
    box(1.1, 2.4, 0.9, std({ color: 0xF4F4F4, roughness: 0.3 }), KX - 3.7, 1.2, -3.8, kitchen); box(0.06, 0.6, 0.06, std({ color: 0x999999 }), KX - 3.3, 1.5, -3.33, kitchen);
    // Tisch + Stühle
    box(2.2, 0.1, 1.3, woodM, KX, 1.0, -0.6, kitchen); for (const [x, z] of [[-1, -1.15], [1, -1.15], [-1, -0.05], [1, -0.05]]) box(0.1, 1.0, 0.1, woodM, KX + x, 0.5, z, kitchen, false);
    for (const z of [-1.75, 0.55]) { box(0.7, 0.08, 0.6, woodM, KX, 0.5, z, kitchen); box(0.7, 0.8, 0.08, woodM, KX, 0.9, z + (z < 0 ? -0.28 : 0.28), kitchen); }
    box(0.5, 0.2, 0.5, std({ color: 0xFFFFFF }), KX - 0.6, 1.15, -0.7, kitchen); }
  const kSky = add(new THREE.Mesh(new THREE.PlaneGeometry(4, 2), basic({ color: 0xA9B1C0 })), kitchen, false, false); kSky.position.set(KX, 2.3, -5.0);
  const kLamp = new THREE.PointLight(0xFFE2B0, 0, 12, 1.4); kLamp.position.set(KX, 3.6, 0); kitchen.add(kLamp);
  const tvB = box(0.1, 1.05, 1.8, std({ color: 0x111111 }), KX - 4.38, 2.2, -0.6, kitchen, false);
  const tv = screen(1.68, 0.95, 640, 362, (g, k, w, h) => drawBillboard(g, k, w, h)); tv.position.set(KX - 4.32, 2.2, -0.6); tv.rotation.y = Math.PI / 2; kitchen.add(tv);
  // Handy auf dem Tisch
  const phoneT = new THREE.Group(); phoneT.position.set(KX + 0.55, 1.07, -0.45); phoneT.rotation.x = -Math.PI / 2; kitchen.add(phoneT);
  box(0.36, 0.64, 0.04, std({ color: 0x111111, roughness: 0.3 }), 0, 0, 0, phoneT, false);
  const phoneS = screen(0.32, 0.58, 320, 580, drawMsg); phoneS.position.z = 0.025; phoneT.add(phoneS);
  const phoneGlow = new THREE.PointLight(0xBFD8FF, 0, 2.5, 1.5); phoneGlow.position.set(0, 0, 0.4); phoneT.add(phoneGlow);

  // ---------- Bus und schwarzes Auto (Straße)
  const bus = new THREE.Group(); street.add(bus);
  { const yb = std({ color: 0xF6C026 }); box(2.4, 2.4, 7, yb, 0, 1.6, 0, bus); box(2.42, 0.7, 6.2, darkWin, 0, 2.25, -0.2, bus, false);
    box(2.5, 0.2, 7.1, std({ color: 0x2B2B33 }), 0, 0.5, 0, bus); box(2.3, 0.9, 0.06, darkWin, 0, 2.2, 3.51, bus, false);
    const sign = screen(1.6, 0.35, 320, 70, (g, k, w, h) => { g.fillStyle = "#111"; g.fillRect(0, 0, w, h); glowText(g, "TOWN LINE 4", w / 2, h / 2 + 2, h * 0.6, "#FFB020"); }); sign.position.set(0, 2.85, 3.52); bus.add(sign); sign.userData.set("x");
    for (const [x, z] of [[-1.15, 2.3], [1.15, 2.3], [-1.15, -2.3], [1.15, -2.3]]) { const w = add(new THREE.Mesh(new THREE.CylinderGeometry(0.45, 0.45, 0.3, 16), std({ color: 0x1A1A1A })), bus); w.rotation.z = Math.PI / 2; w.position.set(x, 0.45, z); } }
  const busDoor = box(0.06, 1.9, 1.0, darkWin, 1.22, 1.35, 2.3, bus, false);
  const car = new THREE.Group(); street.add(car);
  const carDoor = new THREE.Group();
  { const cb = std({ color: 0x0E0F14, metalness: 0.6, roughness: 0.25 }); box(1.9, 0.7, 4.2, cb, 0, 0.75, 0, car); box(1.7, 0.6, 2.2, cb, 0, 1.38, -0.2, car);
    box(1.72, 0.45, 2.0, darkWin, 0, 1.4, -0.2, car, false); box(1.6, 0.2, 0.1, basic({ color: 0xFFF2C0, toneMapped: false }), 0, 0.85, 2.11, car, false);
    for (const [x, z] of [[-0.95, 1.35], [0.95, 1.35], [-0.95, -1.35], [0.95, -1.35]]) { const w = add(new THREE.Mesh(new THREE.CylinderGeometry(0.38, 0.38, 0.28, 16), std({ color: 0x111111 })), car); w.rotation.z = Math.PI / 2; w.position.set(x, 0.38, z); }
    carDoor.position.set(-0.96, 0, 0.5); car.add(carDoor); box(0.06, 1.1, 1.2, cb, 0, 1.0, -0.6, carDoor); }

  // ---------- STADION (x = 600)
  const SX = 600;
  const stadium = new THREE.Group(); scene.add(stadium);
  { const f = add(new THREE.Mesh(new THREE.CircleGeometry(1, 64), std({ map: grassT, color: 0x8FD16A })), stadium, false, true); f.rotation.x = -Math.PI / 2; f.scale.set(26, 18, 1); f.position.set(SX, 0.01, 0);
    const lineM = basic({ color: 0xFFFFFF }); const l1 = add(new THREE.Mesh(new THREE.RingGeometry(4.6, 4.9, 48), lineM), stadium, false, false); l1.rotation.x = -Math.PI / 2; l1.position.set(SX, 0.03, 0);
    box(0.3, 0.02, 34, lineM, SX, 0.03, 0, stadium, false);
    for (let r = 0; r < 14; r++) { const c = add(new THREE.Mesh(new THREE.CylinderGeometry(1, 1, 1, 72, 1, true), std({ color: r % 2 ? 0x6A5ACD : 0x5145A8, side: THREE.DoubleSide })), stadium, false, true);
      const h = 0.9 * (r + 1); c.scale.set(27 + r * 1.3, h, 19 + r * 1.3); c.position.set(SX, h / 2, 0);
      const top = add(new THREE.Mesh(new THREE.RingGeometry(1, 1 + 1.3 / (27 + r * 1.3), 72), std({ color: r % 2 ? 0x7B6CE0 : 0x6155C0, side: THREE.DoubleSide })), stadium, false, true);
      top.rotation.x = -Math.PI / 2; top.scale.set(27 + r * 1.3, 19 + r * 1.3, 1); top.position.set(SX, h + 0.01, 0); } }
  // Publikum (instanziert)
  const NCROWD = 1900, crowdBody = new THREE.InstancedMesh(new THREE.BoxGeometry(0.55, 0.8, 0.35), std({ color: 0xFFFFFF }), NCROWD);
  const crowdHead = new THREE.InstancedMesh(new THREE.BoxGeometry(0.42, 0.42, 0.42), std({ color: 0xF1C27D }), NCROWD);
  const CR = []; { const Rc = mulberry(55); let k = 0; for (let r = 0; r < 14 && k < NCROWD; r++) { const n = Math.floor(120 + r * 6);
      for (let i = 0; i < n && k < NCROWD; i++) { const a = (i + Rc() * 0.5) / n * Math.PI * 2; const rx = 27.6 + r * 1.3, rz = 19.6 + r * 1.3;
        CR.push({ x: SX + Math.cos(a) * rx, z: Math.sin(a) * rz, y: 0.9 * (r + 1), ry: Math.atan2(-Math.cos(a) * rx, -Math.sin(a) * rz), o: Rc() });
        crowdBody.setColorAt(k, new THREE.Color(SHIRT[Math.floor(Rc() * SHIRT.length)])); crowdHead.setColorAt(k, new THREE.Color(SKIN[Math.floor(Rc() * SKIN.length)])); k++; } } }
  stadium.add(crowdBody); stadium.add(crowdHead);
  const dummy = new THREE.Object3D();
  function crowdUpdate(u, cheer) { CR.forEach((c, k) => { const j = cheer ? Math.abs(Math.sin(u * 9 + c.o * 20)) * 0.35 : Math.sin(u * 2 + c.o * 9) * 0.03;
      dummy.position.set(c.x, c.y + 0.4 + j, c.z); dummy.rotation.set(0, c.ry, 0); dummy.updateMatrix(); crowdBody.setMatrixAt(k, dummy.matrix);
      dummy.position.y = c.y + 1.02 + j; dummy.updateMatrix(); crowdHead.setMatrixAt(k, dummy.matrix); });
    crowdBody.instanceMatrix.needsUpdate = true; crowdHead.instanceMatrix.needsUpdate = true; }
  crowdUpdate(0, false);
  // Großbildschirm
  for (const xx of [-7, 7]) box(0.6, 22, 0.6, std({ color: 0x2B2B33 }), SX + xx, 11, -36, stadium);
  box(19, 11, 0.6, std({ color: 0x15121C }), SX, 24, -36.2, stadium);
  const bigScreen = screen(18, 10, 900, 500, (g, k, w, h) => { g.fillStyle = "#0E1638"; g.fillRect(0, 0, w, h);
    if (k.startsWith("$")) { big(g, "SAM'S BANK", w / 2, h * 0.2, h * 0.1, "#FFFFFF"); glowText(g, k, w / 2, h * 0.55, h * (k.length > 9 ? 0.2 : 0.26), "#5CF08C"); }
    else if (k === "final") { glowText(g, "FINAL CHALLENGE", w / 2, h * 0.28, h * 0.12, "#FF4D8D"); big(g, "FIND THE", w / 2, h * 0.5, h * 0.1, "#FFFFFF"); glowText(g, "GOLDEN KEY", w / 2, h * 0.7, h * 0.16, "#FFC531"); }
    else { glowText(g, "GIANT GAMES", w / 2, h * 0.3, h * 0.18, "#FFC531"); big(g, "GRAND PRIZE", w / 2, h * 0.55, h * 0.09, "#FFFFFF"); glowText(g, "$10,000,000", w / 2, h * 0.75, h * 0.17, "#5CF08C"); }
    g.strokeStyle = "#FFC531"; g.lineWidth = 12; g.strokeRect(6, 6, w - 12, h - 12); });
  bigScreen.position.set(SX, 24, -35.85); stadium.add(bigScreen);
  // Tresor auf Podest
  box(4, 0.8, 4, std({ color: 0xC9A23A, metalness: 0.7, roughness: 0.3 }), SX, 0.4, -6, stadium);
  const safeM = std({ color: 0x8A9099, metalness: 0.8, roughness: 0.35 });
  box(2.6, 3, 2.2, safeM, SX, 2.3, -6, stadium);
  const safeDoor = new THREE.Group(); safeDoor.position.set(SX - 1.2, 2.3, -4.85); stadium.add(safeDoor);
  box(2.3, 2.7, 0.2, std({ color: 0x9AA2AD, metalness: 0.85, roughness: 0.3 }), 1.15, 0, 0, safeDoor);
  { const wh = add(new THREE.Mesh(new THREE.TorusGeometry(0.45, 0.07, 8, 24), goldM), safeDoor, false, false); wh.position.set(1.15, 0.2, 0.15);
    box(0.12, 0.3, 0.05, std({ color: 0x111111 }), 1.15, -0.6, 0.13, safeDoor, false); }
  const safeGlow = add(new THREE.Mesh(new THREE.PlaneGeometry(2.2, 2.5), basic({ color: 0x5CF08C, toneMapped: false })), stadium, false, false); safeGlow.position.set(SX, 2.3, -4.98); safeGlow.visible = false;
  // Riss im Boden mit goldenem Schlüssel
  const crack = new THREE.Group(); crack.position.set(SX + 7, 0.02, 3); crack.rotation.y = 0.5; stadium.add(crack);
  { const s = new THREE.Shape(); s.moveTo(-3, 0); for (let i = 0; i <= 12; i++) s.lineTo(-3 + i * 0.5, (i % 2 ? 0.16 : 0.08)); for (let i = 12; i >= 0; i--) s.lineTo(-3 + i * 0.5, (i % 2 ? -0.1 : -0.18)); s.closePath();
    const m = add(new THREE.Mesh(new THREE.ShapeGeometry(s), basic({ color: 0x0A0705 })), crack, false, false); m.rotation.x = -Math.PI / 2; }
  const keyGlow = new THREE.Sprite(new THREE.SpriteMaterial({ map: GLOW, color: 0xFFD45A, blending: THREE.AdditiveBlending, depthWrite: false, transparent: true, toneMapped: false })); keyGlow.scale.set(1.2, 1.2, 1); keyGlow.position.set(0.6, 0.03, 0); crack.add(keyGlow);
  const keyM = new THREE.Group(); { const k1 = add(new THREE.Mesh(new THREE.TorusGeometry(0.05, 0.015, 6, 16), goldM), keyM, false, false); box(0.12, 0.02, 0.02, goldM, 0.1, 0, 0, keyM, false); box(0.02, 0.04, 0.02, goldM, 0.15, -0.02, 0, keyM, false); }
  // Basketballkorb, Seil, Bänke, Auto zum Hochheben
  const hoop = new THREE.Group(); hoop.position.set(SX - 14, 0, -2); stadium.add(hoop);
  box(0.5, 16, 0.5, std({ color: 0x2B2B33 }), 0, 8, 0, hoop); box(6, 4, 0.3, std({ color: 0xFFFFFF }), 0, 16, 1, hoop);
  { const r = add(new THREE.Mesh(new THREE.TorusGeometry(1.5, 0.12, 8, 24), std({ color: 0xFF6A00 })), hoop); r.rotation.x = Math.PI / 2; r.position.set(0, 14.5, 2.6); }
  const ball = add(new THREE.Mesh(new THREE.SphereGeometry(1.1, 20, 16), std({ color: 0xE86A1A })), stadium); ball.visible = false;
  const rope = box(0.25, 0.25, 30, std({ color: 0xC9A06A }), SX, 6, 4, stadium); rope.visible = false;
  const benches = []; for (let i = 0; i < 4; i++) { const b = box(5, 0.5, 1.2, std({ color: 0x3A86FF }), SX - 8 + i * 5, 0.25, 12, stadium); benches.push(b); }
  const liftCar = car.clone(); liftCar.scale.setScalar(1); stadium.add(liftCar); liftCar.visible = false;
  // Konfetti + Geldregen
  const NCF = 500, conf = new THREE.InstancedMesh(new THREE.PlaneGeometry(0.35, 0.22), basic({ color: 0xFFFFFF, side: THREE.DoubleSide }), NCF);
  const CF = []; { const Rr = mulberry(77); for (let i = 0; i < NCF; i++) { CF.push({ x: (Rr() - 0.5) * 30, z: (Rr() - 0.5) * 24, s: 2 + Rr() * 3, o: Rr() * 20, r: Rr() * 6 });
      conf.setColorAt(i, new THREE.Color(i % 3 === 0 ? 0x3DAA5C : [0xFFC531, 0xFF4D8D, 0x3A86FF, 0x5CF08C, 0xFFFFFF][i % 5])); } }
  scene.add(conf); conf.frustumCulled = false; conf.visible = false;
  function confUpdate(u, cx, cy, cz) { CF.forEach((c, i) => { const y = cy + 18 - ((u * c.s + c.o) % 20); dummy.position.set(cx + c.x + Math.sin(u * 2 + c.o) * 0.5, y, cz + c.z);
      dummy.rotation.set(u * 3 + c.r, u * 2 + c.o, c.r); dummy.scale.setScalar(i % 3 === 0 ? 1.6 : 1); dummy.updateMatrix(); conf.setMatrixAt(i, dummy.matrix); }); conf.instanceMatrix.needsUpdate = true; dummy.scale.setScalar(1); }
  // Vögel / Nest / Taube / Flugzeug
  function bird(col, sc) { const g = new THREE.Group(); const m = std({ color: col }); box(0.5, 0.35, 0.8, m, 0, 0, 0, g); box(0.3, 0.3, 0.3, m, 0, 0.2, 0.45, g);
    box(0.12, 0.08, 0.2, std({ color: 0xF2A23A }), 0, 0.18, 0.66, g); const wl = box(0.7, 0.06, 0.4, m, 0.5, 0.05, 0, g), wr = box(0.7, 0.06, 0.4, m, -0.5, 0.05, 0, g);
    g.userData = { wl, wr }; g.scale.setScalar(sc); scene.add(g); return g; }
  const flap = (b, u) => { b.userData.wl.rotation.z = Math.sin(u * 18) * 0.7; b.userData.wr.rotation.z = -Math.sin(u * 18) * 0.7; };
  const birds = [bird(0x8A6E4B, 1), bird(0x5A7FA8, 1), bird(0xC0392B, 1)];
  const nest = add(new THREE.Mesh(new THREE.TorusGeometry(0.45, 0.16, 8, 20), std({ map: woodT, color: 0xA07850 })), scene); nest.rotation.x = Math.PI / 2;
  const pigeon = bird(0x9AA0A8, 1);
  const plane = new THREE.Group(); scene.add(plane);
  { const pm = std({ color: 0xF4F4F4 }); box(1.2, 1.2, 9, pm, 0, 0, 0, plane); box(10, 0.2, 1.8, pm, 0, 0, 0.5, plane); box(3, 0.2, 1, pm, 0, 0, -3.8, plane); box(0.2, 1.8, 1.2, std({ color: 0xE63946 }), 0, 1.0, -3.8, plane);
    box(1.0, 0.4, 0.1, darkWin, 0, 0.3, 4.5, plane, false); }
  // Riesenkrümel, Erdnuss, Münze, Limonadenstand, Lineal
  const crumb = add(new THREE.Mesh(new THREE.DodecahedronGeometry(0.05, 0), std({ color: 0xD9A05B, flatShading: true })), scene);
  const peanut = add(new THREE.Mesh(new THREE.CapsuleGeometry(0.09, 0.14, 4, 8), std({ color: 0xC9A06A })), scene); peanut.rotation.z = Math.PI / 2;
  const coin = add(new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.12, 0.02, 24), std({ color: 0xC0C4CC, metalness: 0.9, roughness: 0.3 })), scene);
  const stand = new THREE.Group(); scene.add(stand);
  { box(0.5, 0.25, 0.25, woodM, 0, 0.125, 0, stand); box(0.04, 0.3, 0.04, woodM, -0.22, 0.4, 0, stand); box(0.04, 0.3, 0.04, woodM, 0.22, 0.4, 0, stand);
    const sg = screen(0.5, 0.16, 300, 96, (g, k, w, h) => { g.fillStyle = "#FFF3B0"; g.fillRect(0, 0, w, h); big(g, "LEMONADE 20¢", w / 2, h / 2 + 2, h * 0.5, "#E63946"); }, false); sg.position.set(0, 0.55, 0.02); stand.add(sg); sg.userData.set("x"); }
  const ruler = screen(1.2, 12, 120, 1200, (g, k, w, h) => { g.fillStyle = "#FFD23F"; g.fillRect(0, 0, w, h); g.fillStyle = "#1B1410";
    for (let i = 0; i < 60; i++) { const y = h - i * 20; g.fillRect(0, y, i % 5 ? 30 : 60, 3); }
    const marks = [["$10", 0.035], ["$1K", 0.2], ["$100K", 0.45], ["$1M", 0.75]]; marks.forEach(([t, f]) => big(g, t, w * 0.66, h - h * f - 14, 26, "#C81E3A")); }, false);
  scene.add(ruler); ruler.userData.set("x");
  const debris = []; for (let i = 0; i < 24; i++) { const d = box(0.4, 0.15, 0.5, std({ map: roofT }), 0, 0, 0, scene, false); d.userData = { a: R() * 6.3, v: 2 + R() * 4, s: R() }; debris.push(d); }
  // Schule: Riesentreppe + Flur
  const school = new THREE.Group(); scene.add(school); const SCZ = -800;
  { const f = add(new THREE.Mesh(new THREE.PlaneGeometry(14, 14), std({ map: tileT })), school, false, true); f.rotation.x = -Math.PI / 2; f.position.set(0, 0, SCZ);
    for (let i = 0; i < 8; i++) box(5, 0.35 * (i + 1), 0.6, std({ color: 0xBDB5A6 }), 0, 0.175 * (i + 1), SCZ - 2 - i * 0.6, school);
    for (let i = 0; i < 7; i++) { box(1, 3, 0.8, std({ color: [0x3A86FF, 0x2B7BE4][i % 2] }), -6 + i * 1.05, 1.5, SCZ - 6.6, school); }
    box(14, 5, 0.3, std({ color: 0xF2E3B8 }), 0, 2.5, SCZ - 7.2, school);
    box(1.8, 0.08, 1.0, woodM, 3.5, 1.0, SCZ + 2, school); for (const [x, z] of [[2.7, 1.6], [4.3, 1.6], [2.7, 2.4], [4.3, 2.4]]) box(0.08, 1, 0.08, woodM, x, 0.5, SCZ + z, school, false); }

  // =================== FANTASY-DORF (x = 1000) ===================
  const VX = 1000;
  const village = new THREE.Group(); scene.add(village);
  const vAdd = (m, cast = true) => add(m, village, cast, true);
  const cobT = tex(256, 256, 81, (g, r, w, h) => { g.fillStyle = "#9C958A"; g.fillRect(0, 0, w, h);
    for (let y = 0; y < h; y += 32) for (let x = (y / 32) % 2 * 20; x < w + 40; x += 40) { g.fillStyle = ["#B3AB9E", "#A39B8F", "#C2BAAD", "#8F887D"][Math.floor(r() * 4)];
      g.beginPath(); g.roundRect(x - 38, y + 2, 36, 28, 7); g.fill(); } }, [2, 14]);
  const timberT = (base, seed) => tex(256, 256, seed, (g, r, w, h) => { g.fillStyle = base; g.fillRect(0, 0, w, h); g.fillStyle = "#5A3A22";
    g.fillRect(0, 0, w, 14); g.fillRect(0, h - 14, w, 14); g.fillRect(0, h / 2 - 7, w, 14); g.fillRect(0, 0, 14, h); g.fillRect(w - 14, 0, 14, h);
    g.save(); g.lineWidth = 12; g.strokeStyle = "#5A3A22"; g.beginPath(); g.moveTo(14, h / 2); g.lineTo(w / 2, 14); g.lineTo(w - 14, h / 2); g.moveTo(w / 2, h / 2); g.lineTo(w / 2, h - 14); g.stroke(); g.restore(); }, [1, 1]);
  const rockT = tex(256, 256, 82, (g, r, w, h) => { g.fillStyle = "#8C8F96"; g.fillRect(0, 0, w, h); speck(g, r, w, h, 1500, ["#7A7D84", "#9EA1A8", "#6E7178", "#B0B3B9"], 3, 9); }, [3, 3]);
  const shingleT = (col, seed) => tex(128, 128, seed, (g, r, w, h) => { g.fillStyle = col; g.fillRect(0, 0, w, h);
    for (let y = 0; y < h; y += 16) for (let x = (y / 16) % 2 * 8; x < w; x += 16) { g.fillStyle = "rgba(0,0,0,0.18)"; g.fillRect(x, y + 12, 15, 4); g.fillStyle = "rgba(255,255,255,0.08)"; g.fillRect(x, y, 15, 3); } }, [5, 5]);
  // Boden, Hügel, Berge
  { const g = vAdd(new THREE.Mesh(new THREE.PlaneGeometry(700, 700), std({ map: grassT, color: 0xB5E38A })), false); g.rotation.x = -Math.PI / 2; g.position.set(VX, 0, 0);
    const road = vAdd(new THREE.Mesh(new THREE.PlaneGeometry(6, 120), std({ map: cobT })), false); road.rotation.x = -Math.PI / 2; road.position.set(VX, 0.02, -10);
    const road2 = vAdd(new THREE.Mesh(new THREE.PlaneGeometry(60, 5), std({ map: cobT })), false); road2.rotation.x = -Math.PI / 2; road2.position.set(VX, 0.025, -6); }
  const hillM = [0x7FC45A, 0x8ACF63, 0x74B850].map((c) => std({ color: c, flatShading: true }));
  for (let i = 0; i < 26; i++) { const a = i / 26 * Math.PI * 2, rad = 105 + (i % 3) * 18; const h = vAdd(new THREE.Mesh(new THREE.IcosahedronGeometry(1, 2), hillM[i % 3]), false);
    h.scale.set(28 + (i % 4) * 6, 12 + (i % 5) * 4, 24); h.position.set(VX + Math.cos(a) * rad, -4, Math.sin(a) * rad - 70); }
  const mtnM = std({ color: 0x7D8AA6, flatShading: true }), snowM = std({ color: 0xF4F7FB, flatShading: true });
  for (const [x, z, r, hgt] of [[-120, -230, 70, 120], [-20, -260, 85, 150], [90, -240, 75, 130], [190, -210, 60, 100], [-210, -200, 55, 90], [40, -200, 50, 85]]) {
    const m = vAdd(new THREE.Mesh(new THREE.ConeGeometry(r, hgt, 7), mtnM), false); m.position.set(VX + x, hgt / 2 - 10, z);
    const s = vAdd(new THREE.Mesh(new THREE.ConeGeometry(r * 0.32, hgt * 0.32, 7), snowM), false); s.position.set(VX + x, hgt - 10 - hgt * 0.16 + 0.5, z); }
  // Wasserfall an der Klippe (links hinten)
  const cliff = vAdd(new THREE.Mesh(new THREE.BoxGeometry(30, 34, 16), std({ map: rockT, flatShading: true }))); cliff.position.set(VX - 42, 17, -48);
  const fallT = tex(64, 256, 83, (g, r, w, h) => { g.fillStyle = "#6EC6F0"; g.fillRect(0, 0, w, h); for (let i = 0; i < 70; i++) { g.fillStyle = ["#A9E2FA", "#FFFFFF", "#5AB8E8"][i % 3]; g.fillRect(r() * w, r() * h, 2 + r() * 3, 20 + r() * 40); } }, [3, 2]);
  const fall = vAdd(new THREE.Mesh(new THREE.PlaneGeometry(8, 34), basic({ map: fallT, transparent: true, opacity: 0.92 })), false); fall.position.set(VX - 36, 17, -39.9);
  const pool = vAdd(new THREE.Mesh(new THREE.CircleGeometry(9, 32), std({ color: 0x4FA8D8, roughness: 0.15, metalness: 0.2 })), false); pool.rotation.x = -Math.PI / 2; pool.position.set(VX - 36, 0.05, -34);
  const foam = []; for (let i = 0; i < 14; i++) { const f = vAdd(new THREE.Mesh(new THREE.SphereGeometry(1, 10, 8), basic({ color: 0xFFFFFF, transparent: true, opacity: 0.85 })), false); f.userData = { a: R() * 6.3, o: R() }; foam.push(f); }
  // Fluss mit Brücke
  const river = vAdd(new THREE.Mesh(new THREE.PlaneGeometry(200, 7), std({ color: 0x4FA8D8, roughness: 0.15, metalness: 0.2 })), false); river.rotation.x = -Math.PI / 2; river.position.set(VX, 0.04, -30);
  { const br = vAdd(new THREE.Mesh(new THREE.CylinderGeometry(5, 5, 6, 24, 1, false, -Math.PI / 2, Math.PI), std({ map: rockT }))); br.rotation.set(0, 0, 0); br.rotation.z = Math.PI / 2; br.rotation.y = Math.PI / 2;
    br.scale.set(1, 1, 0.35); br.position.set(VX, -3.4, -30); }
  // Fachwerkhäuser entlang der Straße
  const roofCols = ["#C0392B", "#2E6DB4", "#1F8A70", "#8E44AD", "#D35400"];
  const wallCols = ["#F4EBD9", "#F7E3C6", "#EFE6F2", "#E8F1E4"];
  const vHouses = [];
  function vHouse(x, z, ry, sc, k) {
    const g = new THREE.Group(); g.position.set(VX + x, 0, z); g.rotation.y = ry; g.scale.setScalar(sc); village.add(g);
    const wall = std({ map: timberT(wallCols[k % 4], 90 + k) });
    box(5, 3, 4.4, std({ map: rockT }), 0, 1.5, 0, g); box(5.6, 3.2, 5, wall, 0, 4.6, 0, g);
    const s = new THREE.Shape(); s.moveTo(-3.3, 0); s.lineTo(3.3, 0); s.lineTo(0, 3.6); s.lineTo(-3.3, 0);
    const rg = new THREE.ExtrudeGeometry(s, { depth: 5.8, bevelEnabled: false }); const roof = add(new THREE.Mesh(rg, std({ map: shingleT(roofCols[k % 5], 120 + k) })), g); roof.position.set(0, 6.2, -2.9);
    box(0.7, 2.2, 0.7, std({ map: rockT }), 1.5, 8.6, -0.8, g);
    box(1.1, 2.0, 0.12, std({ color: 0x6B3E1E }), 0, 1.0, 2.24, g);
    for (const [wx, wy] of [[-1.6, 1.7], [1.6, 1.7], [-1.4, 4.6], [1.4, 4.6]]) { const wm = litWin.clone(); box(0.95, 0.95, 0.1, wm, wx, wy, wy < 3 ? 2.24 : 2.54, g, false); nightWins.push(wm);
      box(1.15, 0.12, 0.25, std({ color: 0x6B3E1E }), wx, wy - 0.55, wy < 3 ? 2.3 : 2.6, g, false);
      if (wy > 3) for (let f = 0; f < 3; f++) box(0.2, 0.2, 0.2, std({ color: [0xFF5FA2, 0xFFD23F, 0xFF7043][f] }), wx - 0.3 + f * 0.3, wy - 0.42, 2.72, g, false); }
    vHouses.push(g); return g; }
  [[-9, -2, 0.15, 1], [-10, -16, 0.05, 1.05], [-9.5, 10, -0.1, 0.95], [-11, 22, 0.2, 1.1], [9, -3, -0.12, 1], [10, -17, 0.1, 1.1], [9.5, 9, 0.05, 0.95], [11, 21, -0.2, 1.05],
   [-22, -4, 0.6, 1.2], [22, -6, -0.5, 1.15], [-24, 14, 0.3, 1], [24, 12, -0.4, 1.1], [-6, -46, 0, 1], [8, -48, 0.3, 1.1]].forEach(([x, z, r, sc], k) => { const h = vHouse(x, z, (x < 0 ? Math.PI / 2 : -Math.PI / 2) + r, sc, k); });
  const kaiHouse = vHouses[0];
  // Laternen + Wimpelketten
  const vLamps = [];
  for (let i = 0; i < 8; i++) { const x = (i % 2 ? 5.8 : -5.8), z = [28, 21, -14, -27][Math.floor(i / 2)]; box(0.16, 3.6, 0.16, std({ color: 0x2B2B33 }), VX + x, 1.8, z, village);
    const lb = box(0.45, 0.6, 0.45, litWin.clone(), VX + x, 3.8, z, village, false); nightWins.push(lb.material);
    const pl = new THREE.PointLight(0xFFB566, 0, 12, 1.6); pl.position.set(VX + x, 3.6, z); village.add(pl); vLamps.push(pl); }
  const flagCols = [0xFF4D8D, 0xFFD23F, 0x3A86FF, 0x5CF08C, 0xFF7043];
  for (const z of [16, 4, -10]) { for (let i = 0; i < 14; i++) { const x = -6.5 + i; const y = 7.2 - Math.sin(i / 13 * Math.PI) * 1.2;
      const f = vAdd(new THREE.Mesh(new THREE.ConeGeometry(0.28, 0.6, 3), std({ color: flagCols[i % 5] })), false); f.rotation.x = Math.PI; f.position.set(VX + x, y - 0.3, z); } }
  // Bäume (Tannen + runde) und Blumen
  const pineM = [0x2E7D4F, 0x358A57, 0x27704A].map((c) => std({ color: c, flatShading: true }));
  function pine(x, z, s) { const g = new THREE.Group(); g.position.set(VX + x, 0, z); g.scale.setScalar(s); village.add(g);
    box(0.4, 1.4, 0.4, std({ color: 0x6B4A2F }), 0, 0.7, 0, g); for (let k = 0; k < 3; k++) { const c = add(new THREE.Mesh(new THREE.ConeGeometry(1.8 - k * 0.45, 2.2, 7), pineM[k % 3]), g); c.position.y = 2 + k * 1.2; } }
  for (let i = 0; i < 40; i++) { const a = R() * 6.28, r0 = 28 + R() * 30; pine(Math.cos(a) * r0, Math.sin(a) * r0 * 0.8 - 8, rr(1.1, 2.2)); }
  for (let i = 0; i < 70; i++) { const x = rr(-20, 20), z = rr(-25, 30); if (Math.abs(x) < 4) continue; const f = vAdd(new THREE.Mesh(new THREE.BoxGeometry(0.25, 0.25, 0.25), std({ color: [0xFF5FA2, 0xFFD23F, 0xFFFFFF, 0xB06BFF][i % 4] })), false); f.position.set(VX + x, 0.13, z); }
  // Drachenturm auf dem Hügel
  const tower = new THREE.Group(); tower.position.set(VX + 26, 0, -34); village.add(tower);
  { const tm = std({ map: rockT }); const c = add(new THREE.Mesh(new THREE.CylinderGeometry(4, 5, 30, 12), tm), tower); c.position.y = 15;
    const rf = add(new THREE.Mesh(new THREE.ConeGeometry(6, 9, 12), std({ map: shingleT("#2E6DB4", 140) })), tower); rf.position.y = 34.5;
    box(0.2, 5, 0.2, std({ color: 0x333333 }), 0, 41, 0, tower); const fl = box(2.6, 1.4, 0.06, std({ color: 0xFF4D8D }), 1.3, 42.6, 0, tower, false);
    for (let k = 0; k < 6; k++) { const a = k / 6 * Math.PI * 2; box(1.2, 1.6, 0.2, litWin.clone(), Math.cos(a) * 4.5, 22, Math.sin(a) * 4.5, tower, false).rotation.y = -a + Math.PI / 2; }
    box(14, 1, 14, tm, 0, 0.5, 0, tower); }
  // Schule oben auf dem Hügel mit endloser Treppe
  const school19 = new THREE.Group(); school19.position.set(VX - 20, 0, 40); village.add(school19);
  { const sm = std({ map: rockT }); for (let i = 0; i < 40; i++) box(4, 0.5, 1.1, sm, 0, 0.25 + i * 0.5, -i * 1.0, school19);
    box(4.4, 20, 40, std({ color: 0x8FC46A }), 0, -0.2, -20, school19).visible = false;
    const top = new THREE.Group(); top.position.set(0, 20, -44); school19.add(top);
    box(16, 7, 10, std({ map: timberT("#F4EBD9", 160) }), 0, 3.5, 0, top); const s = new THREE.Shape(); s.moveTo(-9, 0); s.lineTo(9, 0); s.lineTo(0, 5); s.lineTo(-9, 0);
    const rf = add(new THREE.Mesh(new THREE.ExtrudeGeometry(s, { depth: 11, bevelEnabled: false }), std({ map: shingleT("#C0392B", 161) })), top); rf.position.set(0, 7, -5.5);
  }
  const schoolSign = screen(6, 1.2, 600, 120, (g, k, w, h) => { g.fillStyle = "#3B2A1A"; g.fillRect(0, 0, w, h); big(g, "DRAGON ACADEMY", w / 2, h / 2 + 3, h * 0.55, "#FFD23F"); }, false);
  schoolSign.position.set(VX - 20, 26.5, -3.9 + 40 - 44 + 5.05); village.add(schoolSign); schoolSign.userData.set("x");
  // Drachen-Ampel
  const dLight = new THREE.Group(); dLight.position.set(VX + 4.2, 0, 1); dLight.rotation.y = -Math.PI / 2; village.add(dLight);
  { box(0.25, 6, 0.25, std({ color: 0x2B2B33 }), 0, 3, 0, dLight); box(1.4, 2.6, 0.6, std({ color: 0x1A1A1A }), 0, 6.8, 0, dLight); }
  const dRed = add(new THREE.Mesh(new THREE.CircleGeometry(0.42, 20), basic({ color: 0x551111, toneMapped: false })), dLight, false, false); dRed.position.set(0, 7.5, 0.31);
  const dGreen = add(new THREE.Mesh(new THREE.CircleGeometry(0.42, 20), basic({ color: 0x114411, toneMapped: false })), dLight, false, false); dGreen.position.set(0, 6.2, 0.31);
  const dSign = screen(2.6, 0.8, 300, 92, (g, k, w, h) => { g.fillStyle = "#FFD23F"; g.fillRect(0, 0, w, h); big(g, "DRAGON CROSSING", w / 2, h / 2 + 2, h * 0.38, "#1B1410"); }, false); dSign.position.set(0, 4.6, 0.15); dLight.add(dSign); dSign.userData.set("x");
  // Rennbanner (Start/Ziel)
  const raceArch = new THREE.Group(); raceArch.position.set(VX, 0, -20); village.add(raceArch);
  { for (const x of [-4.5, 4.5]) box(0.5, 9, 0.5, std({ color: 0xC9A23A, metalness: 0.6, roughness: 0.3 }), x, 4.5, 0, raceArch); }
  const raceBanner = screen(9.5, 2.2, 950, 220, (g, k, w, h) => { g.fillStyle = "#2A1640"; g.fillRect(0, 0, w, h); glowText(g, "GREAT DRAGON RACE", w / 2, h * 0.42, h * 0.36, "#FFC531"); big(g, "WIN THE GOLDEN SADDLE", w / 2, h * 0.8, h * 0.16, "#FFFFFF"); });
  raceBanner.position.set(0, 8.2, 0.3); raceArch.add(raceBanner); raceBanner.userData.set("x");
  const saddle = new THREE.Group(); village.add(saddle); { const sg = std({ color: 0xFFC531, metalness: 0.3, roughness: 0.3, emissive: 0x7A4A00, emissiveIntensity: 0.6 }); box(1.4, 0.4, 1.1, sg, 0, 0, 0, saddle); box(0.3, 0.5, 1.1, sg, -0.55, 0.3, 0, saddle); box(0.3, 0.5, 1.1, sg, 0.55, 0.3, 0, saddle); }
  // Blüten/Blätter in der Luft
  const NP = 220, petals = new THREE.InstancedMesh(new THREE.PlaneGeometry(0.16, 0.12), basic({ color: 0xFFFFFF, side: THREE.DoubleSide, transparent: true, opacity: 0.9 }), NP);
  const PT = []; { const Rr = mulberry(91); for (let i = 0; i < NP; i++) { PT.push({ x: (Rr() - 0.5) * 40, y: Rr() * 14, z: (Rr() - 0.5) * 60, o: Rr() * 9, s: 0.4 + Rr() * 0.6 }); petals.setColorAt(i, new THREE.Color([0xFFB7D5, 0xFFFFFF, 0xFFD6E8][i % 3])); } }
  petals.frustumCulled = false; village.add(petals);
  function petalUpdate(t) { PT.forEach((p, i) => { const y = ((p.y - t * p.s) % 14 + 14) % 14; dummy.position.set(VX + p.x + Math.sin(t * 0.7 + p.o) * 1.5, y, p.z + Math.cos(t * 0.5 + p.o) * 1.0);
      dummy.rotation.set(t * 1.3 + p.o, t + p.o, p.o); dummy.scale.setScalar(1); dummy.updateMatrix(); petals.setMatrixAt(i, dummy.matrix); }); petals.instanceMatrix.needsUpdate = true; }
  // Regen + Blitze (Sturm)
  const NRAIN = 900, rainPos = new Float32Array(NRAIN * 6), rainB = [];
  for (let i = 0; i < NRAIN; i++) rainB.push([rr(-30, 30), rr(0, 1), rr(-40, 40), rr(0.9, 1.3)]);
  const rainGeo = new THREE.BufferGeometry(); rainGeo.setAttribute("position", new THREE.BufferAttribute(rainPos, 3));
  const rain = new THREE.LineSegments(rainGeo, new THREE.LineBasicMaterial({ color: 0xBFD0E8, transparent: true, opacity: 0.55 })); rain.frustumCulled = false; scene.add(rain);
  function rainUpdate(t, cx, cz) { for (let i = 0; i < NRAIN; i++) { const [x, o, z, sp] = rainB[i], y = 30 - ((t * 26 * sp + o * 30) % 30);
      rainPos.set([cx + x, y, cz + z, cx + x - 0.15, y - 0.9, cz + z], i * 6); } rainGeo.attributes.position.needsUpdate = true; }
  function makeBolt(seed) { const g = new THREE.Group(); const r0 = mulberry(seed); let x = 0, y = 40; const m = basic({ color: 0xE8F4FF, toneMapped: false });
    while (y > 0) { const nx = x + (r0() - 0.5) * 5, ny = y - 3 - r0() * 3; const len = Math.hypot(nx - x, ny - y); const b = new THREE.Mesh(new THREE.BoxGeometry(0.35, len, 0.35), m);
      b.position.set((x + nx) / 2, (y + ny) / 2, 0); b.rotation.z = Math.atan2(-(nx - x), ny - y) + Math.PI; g.add(b); x = nx; y = ny; }
    const gl = new THREE.Sprite(new THREE.SpriteMaterial({ map: GLOW, color: 0x9FCBFF, blending: THREE.AdditiveBlending, depthWrite: false, transparent: true, toneMapped: false })); gl.scale.set(30, 50, 1); gl.position.y = 20; g.add(gl);
    g.visible = false; scene.add(g); return g; }
  const bolts = [makeBolt(5), makeBolt(9), makeBolt(13)];
  const flashL = new THREE.PointLight(0xCFE3FF, 0, 200, 1.0); scene.add(flashL);

  // =================== DRACHEN ===================
  function makeDragon(col, belly, o = {}) {
    const root = new THREE.Group(); scene.add(root);
    const bm = std({ color: col, flatShading: true }), lm = std({ color: belly, flatShading: true }), hm = std({ color: 0xF4EBD0 });
    const body = new THREE.Group(); body.position.y = 1.6; root.add(body);
    box(1.6, 1.3, 2.8, bm, 0, 0, 0, body); box(1.3, 0.5, 2.4, lm, 0, -0.55, 0.05, body);
    for (let i = 0; i < 4; i++) { const sp = add(new THREE.Mesh(new THREE.ConeGeometry(0.22, 0.5, 4), lm), body); sp.position.set(0, 0.8, 1.0 - i * 0.7); }
    const neck = new THREE.Group(); neck.position.set(0, 0.4, 1.3); body.add(neck); box(0.8, 0.8, 1.4, bm, 0, 0.5, 0.5, neck).rotation.x = -0.6;
    const head = new THREE.Group(); head.position.set(0, 1.25, 1.2); neck.add(head);
    box(1.1, 0.95, 1.2, bm, 0, 0, 0, head); box(0.85, 0.55, 0.8, bm, 0, -0.15, 0.85, head); box(0.75, 0.15, 0.7, lm, 0, -0.45, 0.85, head);
    for (const sx of [-1, 1]) { box(0.28, 0.28, 0.05, basic({ color: 0xFFFFFF }), sx * 0.32, 0.15, 0.61, head, false); box(0.14, 0.2, 0.06, basic({ color: 0x111111 }), sx * 0.32, 0.13, 0.63, head, false);
      const hr = add(new THREE.Mesh(new THREE.ConeGeometry(0.13, 0.6, 5), hm), head); hr.position.set(sx * 0.32, 0.7, -0.3); hr.rotation.x = -0.5;
      box(0.08, 0.08, 0.05, std({ color: 0x111111 }), sx * 0.18, -0.08, 1.26, head, false); }
    const jaw = new THREE.Group(); jaw.position.set(0, -0.4, 0.5); head.add(jaw); box(0.75, 0.18, 0.75, bm, 0, -0.05, 0.35, jaw);
    const wingShape = new THREE.Shape(); wingShape.moveTo(0, 0); wingShape.lineTo(3.2, 0.6); wingShape.lineTo(3.6, -0.3); wingShape.lineTo(2.6, -0.7); wingShape.lineTo(1.8, -1.6); wingShape.lineTo(0.9, -1.2); wingShape.lineTo(0, -1.4); wingShape.lineTo(0, 0);
    const wg = new THREE.ShapeGeometry(wingShape); const wmM = std({ color: belly, side: THREE.DoubleSide, flatShading: true });
    const wingL = new THREE.Group(); wingL.position.set(0.7, 0.55, 0.4); body.add(wingL); const wl = add(new THREE.Mesh(wg, wmM), wingL); wl.rotation.x = Math.PI / 2;
    const wingR = new THREE.Group(); wingR.position.set(-0.7, 0.55, 0.4); body.add(wingR); const wr = add(new THREE.Mesh(wg, wmM), wingR); wr.rotation.x = Math.PI / 2; wr.scale.x = -1;
    const tail = []; let par = body, tz = -1.4; for (let i = 0; i < 4; i++) { const tg = new THREE.Group(); tg.position.set(0, 0, i === 0 ? -1.4 : -0.9); par.add(tg);
      box(0.7 - i * 0.14, 0.6 - i * 0.12, 1.0, bm, 0, 0, -0.45, tg); tail.push(tg); par = tg; }
    const tip = add(new THREE.Mesh(new THREE.ConeGeometry(0.3, 0.6, 4), lm), tail[3]); tip.rotation.x = -Math.PI / 2; tip.position.z = -1.1;
    const legs = []; for (const [x, z] of [[0.6, 0.9], [-0.6, 0.9], [0.6, -0.9], [-0.6, -0.9]]) { const lg = new THREE.Group(); lg.position.set(x, -0.5, z); body.add(lg); box(0.42, 1.2, 0.5, bm, 0, -0.5, 0, lg); legs.push(lg); }
    const seat = new THREE.Group(); seat.position.set(0, 0.75, 0.1); body.add(seat);
    const d = { root, body, neck, head, jaw, wingL, wingR, tail, legs, seat };
    d.pose = (mode, u) => { const fl = mode === "fly" || mode === "hover"; const sp = mode === "fly" ? 7 : mode === "hover" ? 9 : 2;
      const wa = fl ? Math.sin(u * sp) * 0.75 : 0.15 + Math.sin(u * 1.5) * 0.05;
      wingL.rotation.z = fl ? wa : 0.9; wingR.rotation.z = fl ? -wa : -0.9; wingL.rotation.y = fl ? 0 : -0.6; wingR.rotation.y = fl ? 0 : 0.6;
      tail.forEach((tg, i) => { tg.rotation.y = Math.sin(u * 2.2 - i * 0.7) * 0.18; tg.rotation.x = fl ? 0.05 : 0.12; });
      legs.forEach((lg, i) => { lg.rotation.x = fl ? 0.9 : (mode === "walk" ? Math.sin(u * 7 + i * Math.PI) * 0.5 : 0); });
      body.position.y = fl ? 1.6 + Math.sin(u * sp) * 0.15 : 1.6 + Math.sin(u * 1.5) * 0.04;
      neck.rotation.x = mode === "roar" ? -0.5 : Math.sin(u * 1.2) * 0.05; head.rotation.x = mode === "roar" ? -0.3 : 0; jaw.rotation.x = mode === "roar" || mode === "breath" ? 0.6 : 0.05;
      head.rotation.y = Math.sin(u * 0.8) * 0.15; };
    return d; }
  const D = {
    fire: makeDragon(0xD64545, 0xF2A23A), ice: makeDragon(0x5AB8E8, 0xD8F3FF), bub: makeDragon(0xFF8FC8, 0xFFE0F0), red: makeDragon(0xE63946, 0xFFC531),
    titan: makeDragon(0x2B2D42, 0x8D99AE), storm: makeDragon(0x3A4FD8, 0x8EE3FF), g1: makeDragon(0x2A9D8F, 0xE9C46A), g2: makeDragon(0x8338EC, 0xFFBE0B),
  };
  // Atem-Effekte (Feuer, Eis, Blasen)
  const NB = 60, breath = new THREE.InstancedMesh(new THREE.IcosahedronGeometry(0.25, 0), basic({ color: 0xFFFFFF, transparent: true, opacity: 0.9, toneMapped: false }), NB); breath.frustumCulled = false; scene.add(breath);
  const breathCol = { fire: [0xFF7A1A, 0xFFD23F, 0xFF3B1A], ice: [0xBFE9FF, 0xFFFFFF, 0x7FD0FF], bub: [0xFFB7E3, 0xBFE9FF, 0xFFFFFF] };
  function breathUpdate(drg, kind, u) { breath.visible = !!kind; if (!kind) return; drg.head.updateWorldMatrix(true, false); const hp = new THREE.Vector3(0, -0.2, 1.3).applyMatrix4(drg.head.matrixWorld);
    const dir = new THREE.Vector3(0, -0.15, 1).transformDirection(drg.head.matrixWorld); const sc = drg.root.scale.x;
    for (let i = 0; i < NB; i++) { const q = ((u * (kind === "bub" ? 0.6 : 1.4) + i / NB) % 1); const spread = q * (kind === "bub" ? 1.2 : 0.8) * sc;
      dummy.position.copy(hp).addScaledVector(dir, q * 6 * sc); dummy.position.x += Math.sin(i * 12.9) * spread; dummy.position.y += Math.cos(i * 7.3) * spread + (kind === "bub" ? q * 2 * sc : 0);
      dummy.rotation.set(i, i * 2, 0); dummy.scale.setScalar(sc * (kind === "bub" ? 0.9 + Math.sin(i) * 0.4 : (0.6 + q * 1.6) * (1 - q * 0.5))); dummy.updateMatrix(); breath.setMatrixAt(i, dummy.matrix);
      breath.setColorAt(i, new THREE.Color(breathCol[kind][i % 3])); } breath.instanceMatrix.needsUpdate = true; breath.instanceColor.needsUpdate = true; }
  breath.setColorAt(0, new THREE.Color(0xFFFFFF));
  // Ei
  const eggTex = tex(256, 256, 95, (g, r, w, h) => { g.fillStyle = "#6C7CE0"; g.fillRect(0, 0, w, h); for (let i = 0; i < 40; i++) { g.fillStyle = ["#9DB4FF", "#4A5BC4", "#C9D6FF"][i % 3]; g.beginPath(); g.ellipse(r() * w, r() * h, 6 + r() * 14, 5 + r() * 10, r() * 3, 0, 6.3); g.fill(); }
    g.strokeStyle = "#8EE3FF"; g.lineWidth = 5; g.beginPath(); for (let x = 0; x <= w; x += 16) g.lineTo(x, h * 0.5 + Math.sin(x * 0.2) * 12); g.stroke(); }, [1, 1]);
  const eggMat = std({ map: eggTex, roughness: 0.4, emissive: 0x8EE3FF, emissiveIntensity: 0 });
  const egg = add(new THREE.Mesh(new THREE.SphereGeometry(0.32, 24, 18), eggMat), scene); egg.scale.set(1, 1.3, 1);
  const eggCrack = new THREE.Group(); egg.add(eggCrack); { const cm = basic({ color: 0xFFFFFF, toneMapped: false }); for (let i = 0; i < 6; i++) { const b = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.12, 0.02), cm); const a = i / 6 * Math.PI * 2; b.position.set(Math.sin(a) * 0.31, 0.05 + (i % 2) * 0.06, Math.cos(a) * 0.31); b.rotation.set(0, a, (i % 2 ? 0.6 : -0.6)); eggCrack.add(b); } }
  const eggLight = new THREE.PointLight(0x8EE3FF, 0, 6, 1.5); egg.add(eggLight);
  const eggs = []; for (let i = 0; i < 6; i++) { const e = add(new THREE.Mesh(new THREE.SphereGeometry(0.32, 16, 12), std({ color: [0xD64545, 0x5AB8E8, 0xFF8FC8, 0xFFC531, 0x2A9D8F, 0x8338EC][i] })), scene); e.scale.set(1, 1.3, 1); eggs.push(e); }
  const shell = []; for (let i = 0; i < 8; i++) { const s = add(new THREE.Mesh(new THREE.SphereGeometry(0.32, 8, 6, 0, 1.4, 0, 1.2), std({ map: eggTex, side: THREE.DoubleSide })), scene); s.userData = { a: i / 8 * 6.28 }; shell.push(s); }
  // Requisiten: Föhn, Buch, Mikrowelle, Eis, Rucksack, Tisch
  const dryer = new THREE.Group(); scene.add(dryer); { const dm = std({ color: 0xFF5FA2 }); box(0.18, 0.18, 0.5, dm, 0, 0, 0, dryer); box(0.12, 0.35, 0.12, dm, 0, -0.22, -0.12, dryer); }
  const hot = []; for (let i = 0; i < 10; i++) { const h = add(new THREE.Mesh(new THREE.TorusGeometry(0.06, 0.012, 4, 12), basic({ color: 0xFFB070, transparent: true, opacity: 0.7 })), scene, false, false); hot.push(h); }
  const book = new THREE.Group(); scene.add(book); { box(0.5, 0.06, 0.36, std({ color: 0x2E6DB4 }), 0, 0, 0, book); box(0.48, 0.07, 0.34, std({ color: 0xFFFFFF }), 0, 0.01, 0, book); }
  const micro = new THREE.Group(); scene.add(micro); { box(1.2, 0.7, 0.8, std({ color: 0xEDEDED }), 0, 0.35, 0, micro); box(0.75, 0.5, 0.05, darkWin, -0.15, 0.37, 0.41, micro, false); box(0.2, 0.5, 0.05, std({ color: 0x333333 }), 0.45, 0.37, 0.41, micro, false); }
  const microGlow = new THREE.PointLight(0xFFE08A, 0, 2, 1.5); microGlow.position.set(-0.15, 0.37, 0.2); micro.add(microGlow);
  const iceCream = new THREE.Group(); scene.add(iceCream); { const cone = add(new THREE.Mesh(new THREE.ConeGeometry(0.12, 0.35, 10), std({ color: 0xD9A05B })), iceCream); cone.rotation.x = Math.PI; const sc = add(new THREE.Mesh(new THREE.SphereGeometry(0.15, 12, 10), std({ color: 0xFF9FC8 })), iceCream); sc.position.y = 0.22; }
  const backpack = new THREE.Group(); scene.add(backpack); { box(0.5, 0.65, 0.3, std({ color: 0xE63946 }), 0, 0.33, 0, backpack); box(0.42, 0.25, 0.08, std({ color: 0xC62828 }), 0, 0.25, 0.18, backpack); }
  const parkSign = screen(1.1, 0.5, 220, 100, (g, k, w, h) => { g.fillStyle = "#2E6DB4"; g.fillRect(0, 0, w, h); big(g, "P", w * 0.2, h / 2 + 2, h * 0.7, "#FFF"); big(g, "BACKPACK", w * 0.62, h / 2 + 2, h * 0.24, "#FFF"); }, false); scene.add(parkSign); parkSign.userData.set("x");
  const photo = screen(0.5, 0.36, 200, 144, (g, k, w, h) => { g.fillStyle = "#FFF"; g.fillRect(0, 0, w, h); g.fillStyle = "#7EC4F5"; g.fillRect(10, 10, w - 20, h - 20); g.fillStyle = "#D64545"; g.fillRect(70, 50, 70, 40); g.fillRect(130, 40, 30, 30); }, false); scene.add(photo); photo.userData.set("x");
  const bigTable = new THREE.Group(); scene.add(bigTable); { box(2.2, 0.1, 1.3, woodM, 0, 1.0, 0, bigTable); for (const [x, z] of [[-1, -0.55], [1, -0.55], [-1, 0.55], [1, 0.55]]) box(0.1, 1.0, 0.1, woodM, x, 0.5, z, bigTable, false); }
  // Bürgermeister-Plakat am Rathausplatz (Holzbrett)
  const raceBoard = screen(4, 2.6, 600, 390, (g, k, w, h) => { g.fillStyle = "#F4E2B8"; g.fillRect(0, 0, w, h); g.strokeStyle = "#6B3E1E"; g.lineWidth = 14; g.strokeRect(7, 7, w - 14, h - 14);
    big(g, "THE GREAT", w / 2, h * 0.2, h * 0.12, "#6B3E1E"); big(g, "DRAGON RACE", w / 2, h * 0.38, h * 0.15, "#C0392B"); big(g, "TOMORROW!", w / 2, h * 0.58, h * 0.12, "#6B3E1E");
    g.fillStyle = "#F2B632"; g.beginPath(); g.ellipse(w / 2, h * 0.8, 70, 26, 0, 0, 6.3); g.fill(); big(g, "GOLDEN SADDLE", w / 2, h * 0.8, h * 0.06, "#6B3E1E"); }, false);
  const boardG = new THREE.Group(); village.add(boardG); raceBoard.position.set(VX - 3.0, 2.8, 6); raceBoard.rotation.y = Math.PI / 2; boardG.add(raceBoard); raceBoard.userData.set("x");
  box(0.2, 4, 0.2, woodM, VX - 3.1, 2, 4.2, boardG); box(0.2, 4, 0.2, woodM, VX - 3.1, 2, 7.8, boardG);

  // ---------- Licht
  const hemi = new THREE.HemisphereLight(0xD8E8FF, 0x6B5A40, 0.9); scene.add(hemi);
  const sun = new THREE.DirectionalLight(0xFFF1D8, 2.6); sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048);
  Object.assign(sun.shadow.camera, { left: -14, right: 14, top: 14, bottom: -14, near: 1, far: 80 }); sun.shadow.bias = -0.0005; scene.add(sun); scene.add(sun.target);
  const skyDay = new THREE.Color(0x7EC4F5), skyNight = new THREE.Color(0x0B1030);
  scene.fog = new THREE.Fog(0xBFE0F8, 40, 120);

  // Sonne am Himmel
  const sunDisc = new THREE.Mesh(new THREE.SphereGeometry(10, 24, 16), basic({ color: 0xFFF2B0, fog: false, toneMapped: false })); sunDisc.position.set(VX + 30, 150, -330); village.add(sunDisc);
  const sunGlow = new THREE.Sprite(new THREE.SpriteMaterial({ map: GLOW, color: 0xFFE9A0, blending: THREE.AdditiveBlending, depthWrite: false, transparent: true, fog: false, toneMapped: false })); sunGlow.scale.set(90, 90, 1); sunGlow.position.copy(sunDisc.position); village.add(sunGlow);
  { const b = box(20, 20, 14, std({ map: rockT }), VX - 20, 10, -4, village); }

  // ---------- Einstellungen
  // dr: [name, x, y, z, ry, mode, scale, {to:[x,y,z], dur, from, sTo:[s, from, dur], breath, roll, pitch, shake}]
  // cast: [name, x, z, ry, pose, ex, {y, to, dur, from, ride: dragon, exAfter, s}]
  // cam: {p, p2, t, t2, fov, fov2, roll, roll2, follow:{d|c, off, off2, look}}
  const X = VX, KH = [VX - 6.2, -2];
  const S = [
    /* 1  */ { m: "day", dr: [["g1", X - 12, 18, 10, 160, "fly", 1.6, { to: [X + 4, 22, -30], dur: 2 }], ["g2", X + 8, 24, 30, 170, "fly", 1.6, { to: [X + 14, 26, -10], dur: 2 }]], cast: [["k1", 0, 0, 0, "sit", "grin", { ride: "g1" }], ["k2", 0, 0, 0, "sit", "grin", { ride: "g2" }]], cam: { p: [X + 6, 46, 80], p2: [X + 2, 30, 46], t: [X, 4, -50], t2: [X, 2, -60], fov: 55 } },
    /* 2  */ { m: "day", dr: [["g1", X + 2.5, 0, 9, -140, "idle", 0.9, {}]], cast: [["k1", X + 0.6, 7.8, 60, "wave", "grin"]], cam: { p: [X - 6, 2.4, 17], p2: [X - 4.5, 2.6, 15], t: [X + 1.5, 1.8, 8.5], fov: 50, roll: 0.06, roll2: 0.02 } },
    /* 3  */ { m: "day", table: [X + 2.5, 12], eggs: "table", cast: [["k2", X + 1.2, 13.4, 200, "up", "grin"], ["k3", X + 3.9, 13.6, 160, "wave", "smile"]], cam: { p: [X + 2.5, 3.4, 4.5], p2: [X + 1.5, 3.0, 6.0], t: [X + 2.5, 1.6, 12], fov: 50 } },
    /* 4  */ { m: "day", egg: [KH[0] + 0.7, 0.32, KH[1] + 0.6], cast: [["kai", KH[0], KH[1], 100, "sad2", "sad"]], cam: { p: [KH[0] + 5.5, 2.4, KH[1] + 2.5], p2: [KH[0] + 3.0, 2.3, KH[1] + 1.0], t: [KH[0], 2.0, KH[1]], fov: 46 } },
    /* 5  */ { m: "day", dr: [["fire", X + 3, 0, 4, -100, "breath", 1.0, { breath: "fire" }]], cam: { p: [X - 6, 1.0, 11], p2: [X - 4.5, 1.4, 9], t: [X + 1.5, 2.0, 4], fov: 56, roll: -0.08, roll2: -0.03 } },
    /* 6  */ { m: "day", dr: [["ice", X - 2, 0, 0, 80, "breath", 1.0, { breath: "ice" }]], cam: { p: [X + 7, 1.4, 8], p2: [X + 5.5, 1.8, 6], t: [X - 0.5, 2.0, 0], fov: 54 } },
    /* 7  */ { m: "day", dr: [["bub", X + 1, 0, 6, 200, "breath", 0.9, { breath: "bub" }]], cast: [["k3", X - 1.6, 4.0, 30, "up", "grin"]], cam: { p: [X - 5, 1.6, 14], p2: [X - 3.5, 2.2, 12], t: [X, 2, 5], fov: 52 } },
    /* 8  */ { m: "day", dr: [["g1", X - 10, 9, 24, 200, "fly", 1.0, { to: [X - 18, 22, -2], dur: 1.6 }]], cast: [["k1", 0, 0, 0, "sit", "grin", { ride: "g1" }]], cam: { follow: { d: "g1", off: [7, 3, 9], off2: [5, 4, 8], look: [0, 1.5, 0] }, fov: 52, roll: 0.1, roll2: 0.04 } },
    /* 9  */ { m: "day", dr: [["g2", X + 14, 7, 10, -100, "fly", 1.0, { to: [X - 6, 7.5, 6], dur: 1.4 }]], cam: { p: [X + 1, 2.2, 20], p2: [X - 1, 2.6, 19], t: [X + 4, 6.5, 8], t2: [X - 3, 7, 6], fov: 54 } },
    /* 10 */ { m: "day", sunDim: 1, dr: [["titan", X + 30, 34, -20, -95, "fly", 10, { to: [X - 25, 36, -26], dur: 3.2 }]], cam: { p: [X + 2, 1.0, 12], p2: [X + 1, 1.2, 10], t: [X, 30, -20], t2: [X - 6, 32, -24], fov: 66 } },
    /* 11 */ { m: "day", sunDim: 2, dr: [["titan", X + 18, 70, -160, -95, "fly", 10, { to: [X + 40, 72, -170], dur: 1.6 }]], cam: { p: [X, 2, 20], p2: [X, 1.6, 16], t: [X + 30, 150, -330], fov: 45 } },
    /* 12 */ { m: "day", light: "red", cam: { p: [X + 0.5, 4.2, 6.5], p2: [X + 1.6, 5.4, 3.6], t: [X + 4.2, 6.6, 1], fov: 48 } },
    /* 13 */ { m: "day", light: "red", dr: [["g2", X + 0.5, 7, -2, 160, "hover", 1.0, { to: [X + 0.5, 0, -2], dur: 1.0 }]], cam: { p: [X - 5, 1.6, 9], p2: [X - 4, 1.4, 7.6], t: [X + 0.5, 3, -2], fov: 54 } },
    /* 14 */ { m: "day", light: "green", dr: [["g2", X + 0.5, 0, -2, 160, "fly", 1.0, { to: [X - 1, 12, -12], dur: 1.0 }]], cam: { p: [X - 5, 1.6, 9], p2: [X - 4.6, 1.2, 8], t: [X + 0.5, 3, -2], t2: [X, 8, -8], fov: 54 } },
    /* 15 */ { m: "day", lab: ["KAI · 12", "y", [KH[0], 3.3, KH[1]]], cast: [["kai", KH[0], KH[1], 90, "wave", "smile"]], cam: { face: "kai", d: 1.9, dx: 0.4, fov: 46, orbit: 0.35 } },
    /* 16 */ { m: "day", table: [X + 2.5, 12], eggs: "hatch", cast: [["k2", X + 1.2, 13.4, 200, "up", "grin"], ["k3", X + 3.9, 13.6, 160, "up", "grin"]], cam: { p: [X + 2.5, 3.2, 5.0], p2: [X + 2.5, 2.6, 6.6], t: [X + 2.5, 1.4, 12], fov: 50 } },
    /* 17 */ { m: "day", table: [X + 2.5, 12], egg: [X + 2.5, 1.47, 12], cast: [["kai", X + 2.5, 13.7, 180, "sad2", "sad"]], cam: { p: [X + 2.4, 1.6, 9.6], p2: [X + 2.45, 1.55, 10.6], t: [X + 2.5, 1.5, 12], fov: 44, tight: 1 } },
    /* 18 */ { m: "day", dr: [["red", X + 30, 6, 2, -90, "fly", 1.0, { to: [X - 30, 7, 2], dur: 1.6 }]], cast: [["friend", 0, 0, 0, "sit", "grin", { ride: "red" }], ["kai", X - 2, 6, 180, "idle", "shock"]], cam: { p: [X - 1, 1.6, 12], p2: [X - 1.6, 2.0, 12.4], t: [X + 2, 5, 2], t2: [X - 6, 5, 2], fov: 56 } },
    /* 19 */ { m: "room", egg: [RX - 2.4, 1.15, -2.7], cam: { p: [RX - 1.2, 1.6, -0.6], p2: [RX - 1.9, 1.35, -1.8], t: [RX - 2.4, 1.15, -2.7], fov: 44, tight: 1 } },
    /* 20 */ { m: "day", lab: ["BLAKE", "r", [X + 0.5, 3.4, -10]], cast: [["blake", X + 0.5, -10, 10, "idle", "smirk"]], cam: { face: "blake", d: 2.0, dx: -0.5, fov: 46, orbit: -0.4 } },
    /* 21 */ { m: "day", lab: ["TITAN", "r", [X + 18, 30, -40]], dr: [["titan", X + 16, 0, -40, -30, "roar", 9, {}]], cast: [["blake", X + 4, -14, -30, "idle", "smirk"]], cam: { p: [X - 2, 1.4, 6], p2: [X - 3.5, 1.2, 9], t: [X + 14, 16, -40], fov: 64 } },
    /* 22 */ { m: "day", dr: [["titan", X - 30, 34, -6, 90, "fly", 5, { to: [X + 10, 32, -2], dur: 1.8 }]], cast: [["blake", 0, 0, 0, "sit", "smirk", { ride: "titan" }]], cam: { p: [KH[0] + 3, 1.2, KH[1] + 6], p2: [KH[0] + 4, 1.0, KH[1] + 5], t: [X - 8, 26, -4], t2: [X + 2, 26, -3], fov: 62 } },
    /* 23 */ { m: "day", ice: [KH[0], KH[1], KW.icecream], cast: [["kai", KH[0], KH[1], 90, "idle", "neutral", { exAfter: [KW.icecream + 0.6, "angry"] }]], cam: { p: [KH[0] + 3.4, 2.3, KH[1] + 0.8], p2: [KH[0] + 2.4, 2.4, KH[1] + 0.5], t: [KH[0], 2.3, KH[1]], fov: 48 } },
    /* 24 */ { m: "room", egg: [RX - 2.4, 1.15, -2.7], dryer: 1, cast: [["kai", RX - 1.0, -1.4, -110, "reach", "neutral"]], cam: { p: [RX + 0.3, 2.0, -3.5], p2: [RX - 0.1, 1.8, -3.3], t: [RX - 2.2, 1.25, -2.5], fov: 52 } },
    /* 25 */ { m: "room", egg: [RX - 2.4, 1.15, -2.7], book: 1, cast: [["kai", RX - 1.0, -1.4, -110, "hold", "smile"]], cam: { p: [RX + 0.3, 2.0, -3.5], p2: [RX - 0.1, 1.8, -3.3], t: [RX - 2.2, 1.25, -2.5], fov: 52 } },
    /* 26 */ { m: "room", egg: [RX - 2.4, 1.15, -2.7], lab: ["DAY 3", "y", [RX - 2.4, 3.6, -2.7]], cast: [["kai", RX - 2.4, -2.7, 20, "sit", "sad", { y: 1.35 }]], cam: { p: [RX + 0.6, 2.4, 0.8], p2: [RX - 0.2, 2.2, 0.0], t: [RX - 2.4, 2.0, -2.6], fov: 50 } },
    /* 27 */ { m: "room", egg: [RX - 2.4, 1.15, -2.7], cam: { p: [RX - 2.0, 1.4, -1.6], p2: [RX - 2.25, 1.3, -2.1], t: [RX - 2.4, 1.15, -2.7], fov: 40, tight: 1 } },
    /* 28 */ { m: "room", egg: [RX - 2.4, 1.15, -2.7], cast: [["kai", RX - 1.3, -1.6, -130, "up", "grin"]], cam: { face: "kai", d: 1.9, dx: 0.3, fov: 48, orbit: 0.3 } },
    /* 29 */ { m: "room", egg: [RX - 2.4, 1.15, -2.7], photo: 1, cast: [["kai", RX - 1.0, -1.4, -110, "hold", "smile"]], cam: { p: [RX + 0.3, 2.0, -3.5], p2: [RX - 0.1, 1.8, -3.3], t: [RX - 2.2, 1.25, -2.5], fov: 52 } },
    /* 30 */ { m: "kitchen", micro: 1, cast: [["kai", KX + 0.9, -3.2, 110, "idle", "smirk"]], cam: { p: [KX + 2.6, 1.8, -1.2], p2: [KX + 2.4, 1.6, -2.2], t: [KX + 2.2, 1.35, -3.9], fov: 48, tight: 1 } },
    /* 31 */ { m: "kitchen", micro: 2, cast: [["kai", KX + 0.9, -3.2, 30, "hands", "shock"]], cam: { face: "kai", d: 1.6, dx: -0.2, fov: 46, orbit: -0.3 } },
    /* 32 */ { m: "day", dr: [["g1", X - 6, 6, 30, 200, "fly", 1.0, { to: [X - 16, 18, 4], dur: 2 }], ["g2", X - 2, 8, 34, 195, "fly", 1.0, { to: [X - 13, 20, 8], dur: 2 }]], cast: [["k1", 0, 0, 0, "sit", "grin", { ride: "g1" }], ["k2", 0, 0, 0, "sit", "grin", { ride: "g2" }]], cam: { follow: { d: "g2", off: [-6, 2, 8], off2: [-7, 3.5, 6], look: [0, 1.5, -2] }, fov: 54, roll: -0.08 } },
    /* 33 */ { m: "day", lab: ["400 STAIRS", "r", [X - 20, 9, 18]], cast: [["kai", X - 20, 36, 180, "walk", "sad", { y: 2.5, to: [X - 20, 34], dur: 3 }]], cam: { p: [X - 14, 2, 44], p2: [X - 13, 12, 40], t: [X - 20, 3, 34], t2: [X - 20, 18, 4], fov: 60 } },
    /* 34 */ { m: "day", park: 1, cam: { p: [X - 15.5, 21.5, 6.5], p2: [X - 16.8, 21.2, 4.8], t: [X - 18.5, 20.6, 2.4], fov: 46, tight: 1 } },
    /* 35 */ { m: "day", board: 1, cast: [["mayor", X - 2.0, 8.8, -60, "point", "smile"]], cam: { p: [X + 3.5, 2.6, 7.5], p2: [X + 1.6, 2.8, 6.6], t: [X - 3, 2.8, 6.4], fov: 50 } },
    /* 36 */ { m: "day", saddle: 1, cam: { p: [X + 3.2, 2.6, -15.5], p2: [X + 2.2, 2.2, -17], t: [X, 1.6, -20], fov: 46, roll: 0.05, roll2: -0.03 } },
    /* 37 */ { m: "day", dr: [["fire", X - 6, 0, -24, 180, "idle", 1.0, {}], ["ice", X - 2, 0, -25, 180, "idle", 1.0, {}], ["bub", X + 2, 0, -24, 180, "idle", 0.9, {}], ["red", X + 6, 0, -25, 180, "idle", 1.0, {}]], cam: { p: [X + 12, 3.5, -12], p2: [X - 12, 3.5, -12], t: [X + 4, 2, -24], t2: [X - 4, 2, -24], fov: 54 } },
    /* 38 */ { m: "day", lab: ["FINISH LINE?", "r", [X, 3.3, -16]], dr: [["titan", X + 8, 0, -30, -150, "idle", 6, {}]], cast: [["kai", X, -16, 160, "sad2", "sad"], ["blake", 0, 0, 0, "sit", "evil", { ride: "titan" }]], cam: { p: [X - 2.5, 1.0, -10.5], p2: [X - 1.4, 1.2, -12], t: [X + 2, 6, -22], fov: 60 } },
    /* 39 */ { m: "storm", cam: { p: [X + 10, 40, 70], p2: [X + 4, 32, 48], t: [X, 4, -40], fov: 56 } },
    /* 40 */ { m: "storm", bolts: [[KW.lightning + 0.25, X + 26, -34]], cam: { p: [X + 8, 3, 0], p2: [X + 9, 3.6, -2], t: [X + 26, 26, -34], fov: 58 } },
    /* 41 */ { m: "storm", dr: [["fire", X - 6, 8, -20, 20, "fly", 1.0, { to: [X - 20, 26, -70], dur: 1.6 }], ["ice", X + 2, 10, -18, 0, "fly", 1.0, { to: [X + 4, 30, -80], dur: 1.6 }], ["bub", X + 8, 6, -16, -20, "fly", 0.9, { to: [X + 22, 24, -70], dur: 1.6 }]], cam: { p: [X, 2.5, 8], p2: [X, 2, 10], t: [X, 10, -20], t2: [X, 18, -40], fov: 60, roll: 0.05 } },
    /* 42 */ { m: "storm", dr: [["titan", X + 10, 20, -40, 20, "fly", 8, { to: [X + 20, 40, -120], dur: 1.3 }]], cam: { p: [X, 3, 10], p2: [X, 2.5, 12], t: [X + 10, 22, -40], t2: [X + 18, 34, -100], fov: 62 } },
    /* 43 */ { m: "storm", dark: 1, cam: { p: [X + 14, 22, 34], p2: [X + 10, 18, 26], t: [X, 2, -8], fov: 56 } },
    /* 44 */ { m: "storm", dark: 1, cr: "run", cam: { p: [X + 2.5, 1.8, 18], p2: [X + 1.5, 2.0, 15], t: [X, 1.6, 4], fov: 54 } },
    /* 45 */ { m: "kitchenStorm", cast: [["blake", KX, -0.2, 0, "sit", "cry", { y: -0.25 }]], cam: { p: [KX + 0.3, 1.2, 2.4], p2: [KX + 0.2, 1.0, 1.8], t: [KX, 0.6, -0.4], fov: 50, tight: 1, roll: 0.06 } },
    /* 46 */ { m: "roomStorm", egg: [RX - 2.4, 1.15, -2.7], bolts: [[LS0(45) + 0.6, RX, -12]], cast: [["kai", RX - 0.4, -2.2, -100, "idle", "scared"]], cam: { p: [RX + 1.6, 2.2, 1.6], p2: [RX + 0.8, 2.0, 0.6], t: [RX - 2.0, 1.3, -2.4], fov: 50 } },
    /* 47 */ { m: "roomStorm", egg: [RX - 2.4, 1.15, -2.7, { crack: KW.crack, shake: 1 }], cam: { p: [RX - 2.0, 1.45, -1.5], p2: [RX - 2.2, 1.35, -2.0], t: [RX - 2.4, 1.15, -2.7], fov: 42, tight: 1 } },
    /* 48 */ { m: "roomStorm", egg: [RX - 2.4, 1.15, -2.7, { crack: 0, glow: 1, shake: 1 }], cast: [["kai", RX - 1.0, -1.4, -110, "hands", "shock"]], cam: { p: [RX + 0.3, 2.0, -3.5], p2: [RX - 0.1, 1.8, -3.3], t: [RX - 2.2, 1.25, -2.5], fov: 52 } },
    /* 49 */ { m: "roomStorm", shells: [RX - 2.4, 1.15, -2.7, LS0(48) + 0.2], dr: [["storm", RX - 2.4, 0.83, -2.7, 30, "idle", 0.13, {}]], cam: { p: [RX - 1.2, 1.5, -1.5], p2: [RX - 1.6, 1.4, -1.9], t: [RX - 2.4, 1.15, -2.7], fov: 46, tight: 1 } },
    /* 50 */ { m: "roomStorm", lab: ["POTATO SIZE", "y", [RX - 2.4, 1.75, -2.7]], dr: [["storm", RX - 2.4, 0.83, -2.7, 30, "roar", 0.13, {}]], cam: { p: [RX - 1.9, 1.3, -2.15], p2: [RX - 2.05, 1.25, -2.35], t: [RX - 2.4, 1.1, -2.7], fov: 46, tight: 1 } },
    /* 51 */ { m: "storm", cast: [["blake", X + 4.5, 3, -100, "point", "grin"]], cam: { face: "blake", d: 1.8, dx: 0.4, fov: 46, orbit: 0.4 } },
    /* 52 */ { m: "storm", dr: [["storm", X, 0, 2, 180, "roar", 0.35, {}]], cast: [["kai", X + 2.6, 3.0, 220, "idle", "shock"]], cam: { p: [X + 1.2, 0.6, 4.6], p2: [X + 1.0, 0.7, 4.2], t: [X, 0.6, 2], t2: [X, 1.6, 1], fov: 56, tight: 1 } },
    /* 53 */ { m: "storm", bolts: [[KW.ate, X, 2]], dr: [["storm", X, 0, 2, 180, "roar", 0.35, { sTo: [0.6, KW.ate + 0.1, 0.4] }]], cam: { p: [X + 3, 1.0, 5], p2: [X + 2.4, 1.6, 4.4], t: [X, 1.5, 2], t2: [X, 4, 2], fov: 58 } },
    /* 54 */ { m: "storm", bolts: [[KW.b1, X, 2], [KW.b2, X, 2], [KW.b3, X, 2]], dr: [["storm", X, 0, 2, 180, "roar", 0.6, { steps: [[KW.b1, 1.1], [KW.b2, 1.8], [KW.b3, 2.6]] }]], cam: { p: [X + 7, 2, 10], p2: [X + 8, 2.5, 12], t: [X, 3, 2], fov: 58 } },
    /* 55 */ { m: "storm", bolts: [[LS0(54) + 0.2, X, 2]], dr: [["storm", X, 0, 2, 180, "roar", 2.6, { sTo: [7, LS0(54), 2.6] }]], cast: [["kai", X + 2.5, 8, 180, "hands", "shock"]], cam: { p: [X + 4, 1.2, 14], p2: [X + 5, 0.8, 18], t: [X, 4, 2], t2: [X, 12, 2], fov: 62 } },
    /* 56 */ { m: "storm", dr: [["storm", X - 6, 0, -10, 150, "roar", 9, {}], ["titan", X + 12, 0, -16, -150, "idle", 7, { shake: 1 }]], cam: { p: [X + 2, 2, 22], p2: [X + 2, 4, 28], t: [X + 2, 14, -12], fov: 64 } },
    /* 57 */ { m: "storm", dr: [["storm", X, 10, 10, 180, "fly", 2.2, { to: [X - 4, 22, -50], dur: 3 }]], cast: [["kai", 0, 0, 0, "sit", "angry", { ride: "storm", s: 1.0 }]], cam: { follow: { d: "storm", off: [5, 5, 16], off2: [3, 6, 13], look: [0, 3, -4] }, fov: 58, roll: 0.08, roll2: -0.06 } },
    /* 58 */ { m: "storm", dr: [["storm", X - 4, 20, -20, 160, "fly", 3, { to: [X, 14, 14], dur: 2.6 }], ["fire", X - 8, 22, -28, 160, "fly", 1.5, { to: [X - 4, 15, 8], dur: 2.6 }], ["ice", X + 2, 21, -30, 160, "fly", 1.5, { to: [X + 6, 14, 6], dur: 2.6 }], ["bub", X - 1, 24, -34, 160, "fly", 1.4, { to: [X + 2, 16, 2], dur: 2.6 }]], cast: [["kai", 0, 0, 0, "sit", "grin", { ride: "storm", s: 1.3 }]], cam: { p: [X + 10, 12, 24], p2: [X + 8, 13, 22], t: [X - 2, 16, -6], t2: [X, 15, 6], fov: 60 } },
    /* 59 */ { m: "storm", dr: [["titan", X - 30, 0, -33, 30, "idle", 3, { shake: 1 }]], cam: { p: [X - 14, 6, -16], p2: [X - 15, 5.5, -18], t: [X - 30, 6, -34], fov: 56 } },
    /* 60 */ { m: "day", conf: 1, dr: [["storm", X, 2, -10, 180, "fly", 3, { to: [X, 4, -34], dur: 1.8 }]], cast: [["kai", 0, 0, 0, "sit", "grin", { ride: "storm", s: 1.3 }]], cam: { p: [X - 6, 3, -26], p2: [X - 5, 3.6, -27], t: [X, 6, -20], fov: 58, roll: -0.05 } },
    /* 61 */ { m: "day", conf: 1, lab: ["+3 MILES", "g", [X, 12, -24]], dr: [["storm", X, 0, -24, 200, "roar", 3, {}]], cast: [["kai", 0, 0, 0, "sit", "grin", { ride: "storm", s: 1.3 }]], cam: { p: [X - 3, 3.5, -10], p2: [X - 2.4, 3.9, -11.5], t: [X, 7, -24], fov: 56 } },
    /* 62 */ { m: "day", dr: [["titan", X + 2, 0, -32, 200, "idle", 5, { pitch: 0.12 }]], cast: [["blake", X - 2, -27, 160, "sad2", "sad"]], cam: { p: [X - 4, 1.8, -16], p2: [X - 3, 2.0, -17.5], t: [X + 1, 4, -30], fov: 58 } },
    /* 63 */ { m: "day", conf: 1, saddle: 2, dr: [["storm", X, 0, -24, 200, "idle", 3, {}]], cast: [["kai", 0, 0, 0, "sit", "grin", { ride: "storm", s: 1.3 }]], cam: { p: [X + 5, 3.5, -13], p2: [X + 4, 4.2, -14.5], t: [X, 5, -24], fov: 56 } },
    /* 64 */ { m: "day", conf: 1, dr: [["storm", X, 0, -24, 200, "roar", 3, {}]], cast: [["kai", 0, 0, 0, "sit", "grin", { ride: "storm", s: 1.3 }]], cam: { p: [X - 3, 3, -12], p2: [X - 7, 10, -6], t: [X, 7, -24], fov: 56, roll: 0.04 } },
  ];
  function LS0(i) { return LS[i]; }

  function placeCrowd(mode, u, s, t, camP) {
    CROWD.forEach((c) => { c.root.visible = false; c.lamp.visible = false; c.root.scale.setScalar(1); });
    if (!mode) return;
    CROWD.forEach((c, i) => { const r = mulberry(100 + i), a = r(), b = r(), d = r(); if (i >= 14) return;
      let x = X + (b - 0.5) * 8, z = 20 - a * 30, ry = 180, p = "walk", e = "smile";
      if (mode === "run") { p = "run"; e = "scared"; ry = b > 0.5 ? 90 : -90; x = X + (b - 0.5) * 6 + (b > 0.5 ? 1 : -1) * u * 4; }
      if (camP && Math.hypot(x - camP[0], 1.3 - camP[1], z - camP[2]) < 5) return;
      c.root.visible = true; c.root.position.set(x, 0, z); c.root.rotation.y = ry * D2R; c.setEx(e); pose(c, p, u + a * 3); });
  }

  const camera = new THREE.PerspectiveCamera(50, W / H, 0.02, 900);
  const lab = document.getElementById("lab"), labSpan = lab.querySelector("span");
  const LABCOL = { r: "#FF4D5E", y: "#FFD23F", g: "#5CF08C" };
  const v3 = new THREE.Vector3(), look = new THREE.Vector3(), tmpV = new THREE.Vector3();
  const skyV = new THREE.Color(0x8CCBF7), skyStorm = new THREE.Color(0x232B3D);

  function setMode(m, s, t) {
    const storm = m === "storm" || m === "roomStorm" || m === "kitchenStorm";
    village.visible = m === "day" || m === "storm"; room.visible = m === "room" || m === "roomStorm"; kitchen.visible = m === "kitchen" || m === "kitchenStorm";
    street.visible = false; stadium.visible = false; school.visible = false; voidG.visible = false;
    scene.fog.color.set(storm ? 0x2A3346 : 0xCFE6F7); scene.fog.near = m === "day" || m === "storm" ? 50 : 300; scene.fog.far = m === "day" ? 380 : m === "storm" ? 160 : 600;
    scene.background = storm ? skyStorm : skyV;
    hemi.intensity = storm ? 0.7 : 1.0; hemi.color.set(storm ? 0x6F80A8 : 0xCFE6FF); hemi.groundColor.set(storm ? 0x2A2A3A : 0x8FB06A);
    sun.intensity = storm ? 0.35 : (s.sunDim === 1 ? 1.2 : s.sunDim === 2 ? 0.6 : 2.7); sun.color.set(storm ? 0x9DB4FF : 0xFFE8C8);
    const lit = storm && !s.dark; nightWins.forEach((w) => (w.emissiveIntensity = lit ? 1.4 : 0)); vLamps.forEach((l) => (l.intensity = lit ? 40 : 0));
    lampLights.forEach((l) => (l.intensity = 0)); porch.intensity = 0;
    roomLamp.intensity = m === "room" ? 8 : m === "roomStorm" ? 0.8 : 0; winSky.material.color.set(storm ? 0x1A2233 : 0x8CC8FF);
    kLamp.intensity = m === "kitchen" ? 9 : m === "kitchenStorm" ? 5 : 0; kSky.material.color.set(storm ? 0x1A2233 : 0xA9D7F5);
    voidLight.intensity = 0; voidFill.intensity = 0; moon.visible = false;
    rain.visible = m === "storm"; sunDisc.visible = !storm; sunGlow.visible = !storm; sunGlow.material.opacity = s.sunDim === 2 ? 0.25 : 1;
    renderer.toneMappingExposure = 1.1;
  }
  const scaleAt = (o, t) => { let sc = o.s || 1; if (o.sTo) { const q = ease((t - o.sTo[1]) / o.sTo[2]); sc = sc + (o.sTo[0] - sc) * q; } return sc; };
  const smooth = (x) => { x = clamp(x, 0, 1); return 0.5 - 0.5 * Math.cos(Math.PI * x); };

  function render(t) {
    let i = 0; for (let k = 0; k < LS.length; k++) if (t >= LS[k]) i = k;
    const s = S[i], t0 = LS[i], t1 = i + 1 < LS.length ? LS[i + 1] : DUR, u = t - t0, dur = t1 - t0, p = smooth(u / dur);
    setMode(s.m, s, t);
    for (const k in A) { A[k].root.visible = false; A[k].lamp.visible = false; }
    for (const k in D) D[k].root.visible = false;
    let breathed = false;
    const dPos = {};
    (s.dr || []).forEach(([name, x, y, z, ry, mode, sc0, o]) => { const d = D[name]; o = o || {}; d.root.visible = true;
      let X0 = x, Y0 = y, Z0 = z; if (o.to) { const q = smooth((t - (o.from || t0)) / o.dur); X0 = x + (o.to[0] - x) * q; Y0 = y + (o.to[1] - y) * q; Z0 = z + (o.to[2] - z) * q; }
      let sc = sc0; if (o.sTo) { const q = ease((t - o.sTo[1]) / o.sTo[2]); sc = sc0 + (o.sTo[0] - sc0) * q; }
      if (o.steps) o.steps.forEach(([tt, ss]) => { if (t >= tt) sc = sc + (ss - sc) * outBack((t - tt) / 0.35); });
      d.root.scale.setScalar(sc); d.root.position.set(X0 + (o.shake ? Math.sin(u * 45) * 0.04 * sc : 0), Y0, Z0);
      let yaw = ry * D2R; if (o.to) { const dx = o.to[0] - x, dz = o.to[2] - z; if (Math.hypot(dx, dz) > 1) yaw = Math.atan2(dx, dz); }
      d.root.rotation.set(o.pitch || 0, yaw, (o.roll || 0) + (mode === "fly" ? Math.sin(u * 1.3) * 0.08 : 0));
      d.pose(mode, u + x); if (o.breath && !breathed) { d.root.updateMatrixWorld(true); breathUpdate(d, o.breath, u); breathed = true; }
      dPos[name] = [X0, Y0, Z0, sc]; });
    if (!breathed) breath.visible = false;
    const castPos = {};
    (s.cast || []).forEach(([name, x, z, r, ps, ex, o]) => {
      const ch = A[name]; ch.root.visible = true; o = o || {}; let X0 = x, Z0 = z, P = ps, Y0 = o.y || 0;
      if (o.to) { const q = clamp((t - (o.from || t0)) / o.dur, 0, 1); X0 = x + (o.to[0] - x) * q; Z0 = z + (o.to[1] - z) * q; if (o.y) Y0 = o.y + (Z0 - z) * -0.5; }
      const sc = o.s || 1; ch.root.scale.setScalar(sc);
      if (o.ride) { const d = D[o.ride]; d.root.updateMatrixWorld(true); d.seat.getWorldPosition(tmpV); X0 = tmpV.x; Z0 = tmpV.z; Y0 = tmpV.y - 0.5 * sc; r = d.root.rotation.y / D2R; ch.root.scale.setScalar(sc); }
      ch.root.position.set(X0, Y0, Z0); ch.root.rotation.y = r * D2R;
      ch.setEx(o.exAfter && t >= o.exAfter[0] ? o.exAfter[1] : ex); pose(ch, P, u);
      castPos[name] = [X0, Z0, r, sc, Y0]; });
    // Requisiten
    bigTable.visible = !!s.table; if (s.table) bigTable.position.set(s.table[0], 0, s.table[1]);
    eggs.forEach((e, k) => { e.visible = false; }); shell.forEach((sh) => (sh.visible = false));
    if (s.eggs) { const hatched = s.eggs === "hatch" && t >= KW.hatched; eggs.forEach((e, k) => { e.visible = !hatched; e.position.set(s.table[0] - 0.9 + (k % 3) * 0.9, 1.47, s.table[1] - 0.3 + Math.floor(k / 3) * 0.6); e.rotation.z = Math.sin(u * 12 + k) * 0.08; });
      if (hatched) { const q = t - KW.hatched; ["g1", "g2", "bub"].forEach((nm, k) => { const d = D[nm]; d.root.visible = true; d.root.scale.setScalar(0.18 * outBack(q / 0.4)); d.root.position.set(s.table[0] - 0.9 + k * 0.9, 1.05, s.table[1]); d.root.rotation.set(0, 0.3 * k, 0); d.pose("roar", u); }); } }
    egg.visible = !!s.egg; eggCrack.visible = false; eggMat.emissiveIntensity = 0; eggLight.intensity = 0;
    if (s.egg) { const o = s.egg[3] || {}; egg.position.set(s.egg[0], s.egg[1] + 0.1, s.egg[2]); egg.rotation.set(0, 0, o.shake ? Math.sin(u * 30) * 0.08 : 0);
      if (o.crack !== undefined) eggCrack.visible = t >= o.crack; if (o.glow) { eggMat.emissiveIntensity = 0.6 + 0.4 * Math.sin(u * 8); eggLight.intensity = 4 + 2 * Math.sin(u * 8); }
      if (s.micro === 1) {} }
    if (s.shells) { const q = t - s.shells[3]; if (q > 0) shell.forEach((sh) => { const a = sh.userData.a; sh.visible = true; sh.position.set(s.shells[0] + Math.cos(a) * q * 0.9, s.shells[1] + 0.1 + q * 1.2 - 3 * q * q, s.shells[2] + Math.sin(a) * q * 0.9); sh.rotation.set(q * 6, a, q * 4); }); }
    dryer.visible = !!s.dryer; hot.forEach((h) => (h.visible = !!s.dryer)); if (s.dryer) { dryer.position.set(RX - 1.75, 1.5, -2.35); dryer.rotation.set(0, -2.4, 0.3);
      hot.forEach((h, k) => { const q = (u * 1.2 + k / 10) % 1; h.position.set(RX - 1.85 - q * 0.5, 1.45 - q * 0.25, -2.45 - q * 0.3); h.scale.setScalar(1 + q * 2); h.rotation.y = -2.4; }); }
    book.visible = !!s.book; if (s.book) { book.position.set(RX - 1.75, 1.45, -2.0); book.rotation.set(-0.6, -2.2, 0); }
    photo.visible = !!s.photo; if (s.photo) { photo.position.set(RX - 1.85, 1.5, -2.2); photo.rotation.y = -2.2; }
    micro.visible = !!s.micro; microGlow.intensity = 0; if (s.micro) { micro.position.set(KX + 2.2, 1.08, -4.0); microGlow.intensity = s.micro === 1 ? 3 : 0;
      egg.visible = true; egg.position.set(KX + 2.05, 1.45, -3.8); egg.rotation.y = u * 2; egg.scale.set(0.7, 0.9, 0.7); } else egg.scale.set(1, 1.3, 1);
    if (s.micro === 2) { egg.visible = false; }
    iceCream.visible = !!s.ice; if (s.ice) { const q = clamp((t - s.ice[2]) / 0.6, 0, 1); iceCream.position.set(s.ice[0], 20 - q * 17.1, s.ice[1]); iceCream.rotation.set(0, 0, q > 0.99 ? 0 : u * 6); }
    backpack.visible = !!s.park; parkSign.visible = !!s.park; if (s.park) { backpack.position.set(X - 18.5, 20, 2.4); parkSign.position.set(X - 18.5, 21.5, 1.9); }
    saddle.visible = !!s.saddle; if (s.saddle === 1) { saddle.position.set(X, 1.6 + Math.sin(u * 2) * 0.05, -20); saddle.rotation.y = u * 0.8; saddle.scale.setScalar(1); }
    if (s.saddle === 2) { const d = D.storm; d.seat.getWorldPosition(tmpV); saddle.position.set(tmpV.x, tmpV.y - 0.15 * 3, tmpV.z); saddle.rotation.y = d.root.rotation.y; saddle.scale.setScalar(2.2); }
    boardG.visible = !!s.board;
    dRed.material.color.set(s.light === "red" ? 0xFF2A2A : 0x551111); dGreen.material.color.set(s.light === "green" ? 0x2AFF6A : 0x114411);
    // Wasserfall, Blüten, Regen, Konfetti
    fallT.offset.y = -t * 0.8; foam.forEach((f) => { const a = f.userData.a + t * 0.6; f.position.set(VX - 36 + Math.cos(a) * 3, 0.3 + Math.abs(Math.sin(t * 3 + f.userData.o * 9)) * 0.6, -36 + Math.sin(a) * 1.5); });
    petals.visible = s.m === "day"; if (petals.visible) petalUpdate(t);
    conf.visible = !!s.conf; if (s.conf) confUpdate(u, X, 0, -20);
    // Blitze
    bolts.forEach((b) => (b.visible = false)); flashL.intensity = 0; let flash = 0;
    (s.bolts || []).forEach(([bt, bx, bz], k) => { const q = t - bt; if (q >= 0 && q < 0.35) { const b = bolts[k % 3]; b.visible = q < 0.22 || (q > 0.27 && q < 0.33); b.position.set(bx, 0, bz); b.scale.setScalar(bx < 0 && s.m === "roomStorm" ? 0.6 : 1); flash = Math.max(flash, 1 - q / 0.35); } });
    if (flash > 0) { flashL.position.set(look.x || 0, 30, (look.z || 0) + 10); flashL.intensity = 600 * flash; renderer.toneMappingExposure = 1.1 + flash * 0.8; if (s.m !== "day") scene.background = new THREE.Color(0x232B3D).lerp(new THREE.Color(0xB8C8E8), flash * 0.7); }
    // Kamera
    const c = s.cam; let P, Tg;
    if (c.follow) { const fp = c.follow.d ? dPos[c.follow.d] : castPos[c.follow.c]; const off = c.follow.off2 ? c.follow.off.map((v, k) => v + (c.follow.off2[k] - v) * p) : c.follow.off;
      P = [fp[0] + off[0], fp[1] + off[1], fp[2] + off[2]]; Tg = [fp[0] + c.follow.look[0], fp[1] + c.follow.look[1], fp[2] + c.follow.look[2]]; }
    else if (c.face) { const [x, z, r, sc, y0] = castPos[c.face]; const hy = 2.31 * sc + y0; const ra = (r * D2R) + (c.orbit || 0) * (p - 0.5);
      const f = [Math.sin(ra), Math.cos(ra)], rt = [Math.cos(ra), -Math.sin(ra)], d = c.d * 1.55 * sc * (1.12 - 0.24 * p);
      P = [x + f[0] * d + rt[0] * (c.dx || 0) * sc, hy + (c.dy || 0) * sc, z + f[1] * d + rt[1] * (c.dx || 0) * sc]; Tg = [x, hy - 0.05 * sc, z]; }
    else { const p2 = c.p2 || [c.p[0] + (c.t[0] - c.p[0]) * 0.22, c.p[1] + (c.t[1] - c.p[1]) * 0.22, c.p[2] + (c.t[2] - c.p[2]) * 0.22];
      P = [0, 1, 2].map((k) => c.p[k] + (p2[k] - c.p[k]) * p); const t2 = c.t2 || c.t; Tg = [0, 1, 2].map((k) => c.t[k] + (t2[k] - c.t[k]) * p); }
    camera.position.set(...P); look.set(...Tg); camera.fov = c.fov + ((c.fov2 || c.fov) - c.fov) * p; camera.updateProjectionMatrix(); camera.lookAt(look);
    const roll = (c.roll || 0) + (((c.roll2 !== undefined ? c.roll2 : (c.roll || 0))) - (c.roll || 0)) * p; if (roll) camera.rotateZ(roll);
    placeCrowd(s.cr, u, s, t0, P);
    const sd = Math.max(16, Math.hypot(P[0] - Tg[0], P[1] - Tg[1], P[2] - Tg[2]) * 0.9);
    Object.assign(sun.shadow.camera, { left: -sd, right: sd, top: sd, bottom: -sd, far: sd * 6 }); sun.shadow.camera.updateProjectionMatrix();
    sun.position.set(Tg[0] - sd * 0.6, Tg[1] + sd * 1.1, Tg[2] + sd * 0.7); sun.target.position.set(Tg[0], Tg[1], Tg[2]);
    if (s.m === "storm") rainUpdate(t, P[0], P[2] - 15);
    renderer.render(scene, camera);
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
    js = WORLD_JS.replace("__LS__", json.dumps(LS)).replace("__DUR__", str(TOTAL)).replace("__KW__", json.dumps(KW))
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


# Ton: Whoosh bei Beat-Wechseln, Effekte an Story-Momenten
SFX = []
beat_first, n = [], 0
for b in T["beats"]:
    beat_first.append(n)
    n += len(b["lines"])
for li in beat_first[1:]:
    SFX.append((round(LINES[li]["start"] - 0.12, 3), "whoosh-short.mp3", 0.24))
for t, f, v in [
    (0.0, "whoosh-cinematic.mp3", 0.35), (KW["fire"], "whoosh-short.mp3", 0.45), (KW["fire"] + 0.05, "impact-bass-1.mp3", 0.3), (KW["ice"], "sparkle.mp3", 0.4),
    (KW["bubbles"], "pop.mp3", 0.45), (KW["bubbles"] + 0.3, "pop.mp3", 0.35), (LS[9] + 0.2, "whoosh-cinematic.mp3", 0.4), (KW["sun"], "impact-bass-2.mp3", 0.4),
    (KW["red"], "click.mp3", 0.5), (KW["green"], "click.mp3", 0.5), (KW["green"] + 0.1, "whoosh-short.mp3", 0.4), (LS[14], "pop.mp3", 0.35),
    (KW["hatched"], "pop.mp3", 0.5), (KW["hatched"] + 0.12, "pop.mp3", 0.45), (KW["hatched"] + 0.25, "pop.mp3", 0.45), (KW["didnt"], "error.mp3", 0.35),
    (KW["plane"] - 0.6, "whoosh-cinematic.mp3", 0.45), (KW["titan"], "impact-bass-2.mp3", 0.45), (KW["icecream"] + 0.6, "pop.mp3", 0.55),
    (KW["dryer"], "riser.mp3", 0.25), (KW["micro"], "notification.mp3", 0.45), (KW["bad"], "impact-bass-1.mp3", 0.4), (KW["stairs"], "click-soft.mp3", 0.35),
    (KW["backpack"], "pop.mp3", 0.4), (KW["race"], "chime.mp3", 0.45), (KW["saddle"], "sparkle.mp3", 0.45), (KW["finish"], "error.mp3", 0.35),
    (KW["storm"], "impact-bass-2.mp3", 0.5), (KW["lightning"] + 0.25, "impact-bass-2.mp3", 0.6), (KW["lightning"] + 0.25, "glitch-1.mp3", 0.35),
    (KW["away"], "whoosh-cinematic.mp3", 0.4), (KW["dark"], "impact-bass-1.mp3", 0.4), (LS[45] + 0.6, "impact-bass-1.mp3", 0.4),
    (KW["crack"], "click.mp3", 0.6), (KW["crack"] + 0.05, "impact-bass-1.mp3", 0.45), (KW["glowing"], "riser.mp3", 0.35), (LS[48] + 0.2, "pop.mp3", 0.5),
    (KW["potato"], "sparkle.mp3", 0.35), (KW["nice"], "error.mp3", 0.25), (KW["ate"], "impact-bass-2.mp3", 0.55), (KW["ate"], "glitch-2.mp3", 0.3),
    (KW["b1"], "impact-bass-2.mp3", 0.5), (KW["b2"], "impact-bass-2.mp3", 0.5), (KW["b3"], "impact-bass-2.mp3", 0.55), (KW["bigger"], "riser.mp3", 0.35),
    (KW["flew"], "whoosh-cinematic.mp3", 0.45), (KW["home"], "chime.mp3", 0.4), (KW["won"], "chime.mp3", 0.5), (KW["won"] + 0.1, "sparkle.mp3", 0.5),
    (KW["miles"], "pop.mp3", 0.4), (KW["weather"], "sparkle.mp3", 0.45),
]:
    SFX.append((round(t, 3), f, v))


def write():
    comp = HERE / "compositions"
    comp.mkdir(exist_ok=True)
    (comp / "world.html").write_text(world_html())
    (comp / "captions.html").write_text(captions_html())
    (HERE / "assets" / "sfx").mkdir(parents=True, exist_ok=True)
    audio = []
    if (HERE / "assets" / "voice.wav").exists():
        audio.append('      <audio id="voice" class="clip" src="assets/voice.wav" data-start="0" data-track-index="10" data-volume="1"></audio>')
    music = HERE / "assets" / "source" / "music-ref.mp3"
    if music.exists():
        fade = TOTAL - 2.5
        import subprocess
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(music), "-t", str(TOTAL), "-af",
                        f"afade=t=in:d=0.4,afade=t=out:st={fade}:d=2.5,loudnorm=I=-23:TP=-4:LRA=9", "-ar", "44100", str(HERE / "assets" / "music.wav")], check=True)
        audio.append(f'      <audio id="music" class="clip" src="assets/music.wav" data-start="0" data-duration="{fmt(TOTAL)}" data-track-index="9" data-volume="1"></audio>')
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
