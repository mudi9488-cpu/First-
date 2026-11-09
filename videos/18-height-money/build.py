#!/usr/bin/env python3
"""Builds "Height = Money" (English) – blocky-3D storytime in the style of references/storytime.md:
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
TITLE = "Height = Money"

T = load_timings(HERE)
LINES = [l for b in T["beats"] for l in b["lines"]]
VOICE_END = T["beats"][-1]["end"]
TOTAL = round(VOICE_END + 1.8, 2)
# Einstellungen: Startzeile je Schnitt (mehrere kurze Zeilen = eine Einstellung, ~2 s wie in den Referenzen)
SHOT_LINES = [0, 1, 2, 4, 6, 8, 10, 11, 13, 14, 17, 19, 21, 24, 26, 29, 31, 32, 34, 35, 37, 39, 42, 43, 44, 45, 47, 48, 50, 53,
              54, 55, 56, 59, 61, 62, 63, 64, 66, 68, 70, 72, 73, 74, 76, 78, 79, 82, 83, 84, 85, 88, 89, 91, 93, 95, 98, 100, 101, 102]
LS = [0.0] + [round(LINES[i]["start"] - 0.06, 3) for i in SHOT_LINES[1:]]


def wt(line, prefix, n=1):
    k = 0
    for w in LINES[line]["words"]:
        if re.sub(r"[^\w']", "", w["text"]).lower().startswith(prefix.lower()):
            k += 1
            if k == n:
                return round(w["start"], 3)
    raise KeyError((line, prefix))


KW = {"taller": wt(3, "taller"), "shrink": wt(20, "shrink"), "shoot": wt(22, "shoot"), "crash": wt(23, "crash"), "pigeon": wt(44, "pigeon"),
      "dropped": wt(51, "dropped"), "jumped": wt(76, "jumped"), "click": wt(83, "click"), "onek": wt(85, "one"), "onem": wt(86, "one"),
      "tenm": wt(87, "ten"), "growing": wt(88, "growing"), "shrank": wt(98, "shrank"), "fell": wt(99, "fell"), "stepped": wt(54, "stepped"),
      "silent": wt(82, "silent"), "money": wt(1, "money"), "cat": wt(5, "cat"), "house": wt(9, "house"), "airplanes": wt(16, "airplanes"),
      "measure": wt(25, "measure"), "lemonade": wt(40, "lemonade"), "games": wt(46, "giant"), "million10": wt(49, "ten"), "key": wt(57, "golden"),
      "cars": wt(62, "cars"), "shine": wt(68, "shine"), "hand": wt(75, "giant"), "crumb": wt(101, "crumb"), "days": wt(103, "three")}

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
    sam: makeChar({ shirt: 0x2A9D8F, pants: 0x22304A, design: "hoodie", hair: "messy", hairCol: 0x6B3E1E, skin: 0xF1C27D, shoe: 0xEEEEEE }),
    gold: makeChar({ shirt: 0xD9A520, pants: 0x8A6A10, design: "suit", hair: "tophat", skin: 0xF0C49A, stache: true, shoe: 0x111111 }),
    grandpa: makeChar({ shirt: 0x8A7F70, pants: 0x4A4A4A, design: "stripe", hair: "bald", hairCol: 0xDADADA, skin: 0xE0AC69, glasses: true }),
    baby: makeChar({ shirt: 0xFFFFFF, pants: 0xFFFFFF, hair: "bald", hairCol: 0xE8C66A, skin: 0xFFDBAC, blush: true }),
    rich: makeChar({ shirt: 0x8338EC, pants: 0x22304A, design: "star", hair: "cap", capCol: 0xFFC531, skin: 0xF1C27D }),
    shopper: makeChar({ shirt: 0xE07A9B, pants: 0x4A4A6A, hair: "long", hairCol: 0x5A3215, skin: 0xC68642 }),
    winner: makeChar({ shirt: 0xFB5607, pants: 0x2E2E2E, design: "stripe", hair: "short", hairCol: 0x1A1A1A, skin: 0xE0AC69 }),
    npc1: makeChar({ shirt: 0x2B7BE4, pants: 0x22304A, design: "star", hair: "short", hairCol: 0x1A1A1A, skin: 0xC68642 }),
    npc2: makeChar({ shirt: 0xE63946, pants: 0x2E2E2E, hair: "cap", capCol: 0x111111, skin: 0xE0AC69 }),
    g1: makeChar({ shirt: 0x06D6A0, pants: 0x3D3D5C, hair: "messy", hairCol: 0x2B1A10, skin: 0xD8A06A }),
    g2: makeChar({ shirt: 0xFFBE0B, pants: 0x22304A, hair: "pony", hairCol: 0xC98B3C, skin: 0xFFDBAC }),
  };
  const CROWD = [];
  for (let i = 0; i < 30; i++) CROWD.push(makeChar({ shirt: pick(SHIRT), pants: pick([0x2E3A59, 0x22304A, 0x3D3D5C, 0x4A4A4A, 0x5C4033]), skin: pick(SKIN),
    hair: pick(["short", "short", "messy", "cap", "long", "pony", "bun"]), hairCol: pick(HAIRC), capCol: pick(SHIRT), design: pick([null, "stripe", "star", null]) }));
  // Katze
  const cat = new THREE.Group(); scene.add(cat);
  { const cm = std({ color: 0xF2A23A }); box(0.25, 0.22, 0.55, cm, 0, 0.28, 0, cat); box(0.24, 0.22, 0.22, cm, 0, 0.45, 0.32, cat);
    box(0.06, 0.08, 0.04, cm, -0.08, 0.6, 0.32, cat); box(0.06, 0.08, 0.04, cm, 0.08, 0.6, 0.32, cat); box(0.05, 0.35, 0.05, cm, 0, 0.45, -0.3, cat).rotation.x = -0.5;
    for (const [x, z] of [[-0.08, 0.2], [0.08, 0.2], [-0.08, -0.2], [0.08, -0.2]]) box(0.06, 0.18, 0.06, cm, x, 0.09, z, cat);
    box(0.04, 0.04, 0.01, std({ color: 0x111111 }), -0.06, 0.48, 0.435, cat); box(0.04, 0.04, 0.01, std({ color: 0x111111 }), 0.06, 0.48, 0.435, cat); }
  const keyHand = new THREE.Group(); A.sam.armR.add(keyHand); keyHand.position.set(0, -1.05, 0.1); keyHand.scale.setScalar(4);

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

  // ---------- Licht
  const hemi = new THREE.HemisphereLight(0xD8E8FF, 0x6B5A40, 0.9); scene.add(hemi);
  const sun = new THREE.DirectionalLight(0xFFF1D8, 2.6); sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048);
  Object.assign(sun.shadow.camera, { left: -14, right: 14, top: 14, bottom: -14, near: 1, far: 80 }); sun.shadow.bias = -0.0005; scene.add(sun); scene.add(sun.target);
  const skyDay = new THREE.Color(0x7EC4F5), skyNight = new THREE.Color(0x0B1030);
  scene.fog = new THREE.Fog(0xBFE0F8, 40, 120);

  // ---------- Einstellungen. cast: [name, x, z, ry, pose, ex, {s, sTo:[s, from(abs), dur], y, yTo:[y, from, dur], to, dur, from, exAfter}]
  const SAM = 0.15, GOLD = 9;
  const S = [
    /* 1  */ { m: "day", cr: "sizes", cam: { p: [8, 22, 38], p2: [6, 18, 29], t: [0, 0, -25], fov: 50 } },
    /* 2  */ { m: "day", ruler: [6.6, 2.75], cast: [["npc1", 5.4, 2.75, -90, "idle", "smile"]], cam: { p: [1.4, 2.6, 6.4], t: [5.9, 2.6, 2.75], fov: 50 } },
    /* 3  */ { m: "day", ruler: [6.6, 2.75], lab: ["+$1,000", "g", [5.4, 5.0, 2.75]], cast: [["npc1", 5.4, 2.75, -90, "up", "grin", { s: 1, sTo: [1.6, KW.taller - 0.6, 0.9] }]], cam: { p: [1.0, 3.0, 6.8], t: [5.9, 3.0, 2.75], fov: 52 } },
    /* 4  */ { m: "day", cat: [-3.4, 4.6, 40], lab: ["$10", "r", [-3.0, 1.3, 4.4]], cast: [["npc2", -2.8, 4.3, -30, "idle", "sad", { s: 0.24 }]], cam: { p: [-1.6, 0.5, 6.2], t: [-3.1, 0.45, 4.4], fov: 46, tight: 1 } },
    /* 5  */ { m: "day", lab: ["$1,000", "y", [-3.0, 3.6, 4.4]], cast: [["npc2", -3.0, 4.4, 20, "idle", "neutral"]], cam: { p: [-1.2, 2.2, 8.6], t: [-3.0, 1.8, 4.4], fov: 46 } },
    /* 6  */ { m: "day", lab: ["$1,000,000", "g", [-5, 13, 2]], cast: [["winner", -5, 2, 60, "idle", "smirk", { s: 4.4 }]], cam: { p: [6, 1.5, 16], t: [-5, 7, 0], fov: 60 } },
    /* 7  */ { m: "day", lab: ["MR. GOLD", "y", [4.2, 24.5, 16]], cast: [["gold", 4.2, 16, -90, "idle", "smirk", { s: GOLD }]], cam: { p: [-12, 2, -6], t: [4, 16, 16], fov: 66 } },
    /* 8  */ { m: "day", nest: 1, cast: [["gold", 4.2, 16, -90, "idle", "neutral", { s: GOLD }]], cam: { p: [-11, 30, 28], p2: [-10, 30.5, 27], t: [4.2, 27, 16], fov: 50, tight: 1 } },
    /* 9  */ { m: "day", peanut: [-1.15, 5.0], lab: ["NEWBORN", "y", [-1.0, 0.55, 5.0]], cast: [["baby", -0.85, 5.0, -20, "idle", "smile", { s: 0.07 }]], cam: { p: [-0.6, 0.22, 5.75], t: [-0.95, 0.12, 5.0], fov: 44, tight: 1 } },
    /* 10 */ { m: "day", plane: 1, cast: [["grandpa", -2, -6, 30, "idle", "scared", { s: 10 }]], cam: { p: [10, 6, 24], t: [-1, 18, -6], fov: 62 } },
    /* 11 */ { m: "day", cast: [["rich", 1.6, 1.0, -120, "idle", "smirk", { s: 3 }], ["npc1", -0.4, 0.1, 70, "idle", "sad"]], cam: { p: [-1.5, 0.6, 2.2], t: [1.4, 5.5, 1.0], fov: 58, tight: 1 } },
    /* 12 */ { m: "day", shop: "price", lab: ["-$80", "r", [4.6, 3.2, -2.2]], cast: [["shopper", 4.6, -2.2, -60, "sad2", "shock", { s: 1, sTo: [0.5, KW.shrink, 0.6] }]], cam: { p: [1.0, 2.4, 2.4], t: [4.8, 2.2, -2.2], fov: 52 } },
    /* 13 */ { m: "day", debris: [-6.4, 5.5, -5], lab: ["+$1,000,000", "g", [-5.4, 13, -5]], cast: [["winner", -5.4, -5, 90, "up", "grin", { s: 1, sTo: [5, KW.shoot, 0.7] }]], cam: { p: [3, 2, 7], t: [-5, 6, -5], fov: 60 } },
    /* 14 */ { m: "day", ruler: [6.6, 2.75], cast: [["npc2", 5.5, 2.75, -90, "idle", "neutral", { s: 1.3 }]], lab: ["$12,400", "g", [6.5, 4.4, 2.75]], cam: { p: [1.2, 2.5, 6.2], t: [6.0, 2.8, 2.75], fov: 52 } },
    /* 15 */ { m: "day", cr: "sizes", cam: { p: [-3, 3, 14], p2: [-2, 3.6, 11], t: [1, 3, -8], fov: 55 } },
    /* 16 */ { m: "day", lab: ["SAM · 15", "y", [-3.0, 0.65, 4.4]], cast: [["sam", -3.0, 4.4, 20, "wave", "smile", { s: SAM }]], cam: { face: "sam", d: 1.6, dx: 0.2, fov: 46 } },
    /* 17 */ { m: "day", lab: ["4 INCHES", "r", [-3.0, 0.7, 4.4]], cast: [["sam", -3.0, 4.4, 20, "idle", "sad", { s: SAM }], ["npc1", -2.0, 4.2, -80, "walk", "neutral", { to: [-4.6, 4.2], dur: 2 }]], cam: { p: [-2.2, 0.35, 6.4], t: [-3.0, 0.6, 4.2], fov: 54, tight: 1 } },
    /* 18 */ { m: "day", coin: [-2.75, 4.5], lab: ["$9.50", "r", [-3.0, 0.6, 4.4]], cast: [["sam", -3.0, 4.4, 30, "sad2", "sad", { s: SAM }]], cam: { p: [-2.6, 0.35, 5.3], t: [-2.9, 0.2, 4.4], fov: 46, tight: 1 } },
    /* 19 */ { m: "school", lab: ["SAM", "y", [0.3, 0.7, SCZ - 1.4]], cast: [["sam", 0.3, SCZ - 1.4, 180, "idle", "scared", { s: SAM }]], cam: { p: [3.2, 0.5, SCZ - 0.2], t: [0, 1.4, SCZ - 3.5], fov: 60, tight: 1 } },
    /* 20 */ { m: "school", cast: [["sam", 0.3, SCZ - 1.0, 0, "hands", "scared", { s: SAM }], ["g1", 1.2, SCZ + 3, 200, "walk", "neutral", { to: [0.7, SCZ - 1.3], dur: 2.2 }], ["g2", -0.6, SCZ + 4, 170, "walk", "smile", { to: [-0.3, SCZ - 0.6], dur: 2.4 }]], cam: { p: [0.6, 0.2, SCZ - 2.2], t: [0.3, 0.4, SCZ + 1], fov: 62, tight: 1 } },
    /* 21 */ { m: "school", crumb: [3.62, 1.08, SCZ + 2.05], lab: ["LUNCH", "y", [3.5, 1.5, SCZ + 2]], cast: [["sam", 3.5, SCZ + 2, 30, "hold", "sad", { s: SAM, y: 1.04 }]], cam: { p: [3.75, 1.2, SCZ + 2.7], t: [3.52, 1.13, SCZ + 2.0], fov: 44, tight: 1 } },
    /* 22 */ { m: "day", stand: [-3.2, 4.3], lab: ["20¢", "r", [-3.2, 0.75, 4.3]], cast: [["sam", -3.0, 4.55, 10, "wave", "smile", { s: SAM }]], cam: { p: [-2.4, 0.4, 5.9], t: [-3.1, 0.3, 4.4], fov: 46, tight: 1 } },
    /* 23 */ { m: "day", ruler: [-3.4, 4.0, true], lab: ["+1 MM", "g", [-3.0, 0.7, 4.4]], cast: [["sam", -3.0, 4.2, 20, "up", "grin", { s: SAM, sTo: [SAM * 1.02, LS0(22) + 0.4, 0.3] }]], cam: { p: [-2.5, 0.35, 5.3], t: [-3.1, 0.35, 4.2], fov: 46, tight: 1 } },
    /* 24 */ { m: "day", coin: [-2.0, 4.6], cast: [["sam", -3.2, 4.6, 90, "walk", "grin", { s: SAM, to: [-2.25, 4.6], dur: 1.0 }]], cam: { p: [-2.6, 0.25, 5.7], t: [-2.5, 0.15, 4.6], fov: 48, tight: 1 } },
    /* 25 */ { m: "day", pigeon: 1, cast: [["sam", -2.25, 4.6, 0, "up", "scared", { s: SAM, y: 0, yTo: [1.6, KW.pigeon + 0.2, 1.2] }]], cam: { p: [-1.2, 0.6, 7.2], t: [-2.3, 1.0, 4.6], fov: 52, tight: 1 } },
    /* 26 */ { m: "day", bb: "games", cr: "look", cam: { p: [-4, 1.4, -13], p2: [-3.4, 1.8, -14.5], t: [7, 9.5, -24], fov: 54 } },
    /* 27 */ { m: "stadium", cheer: 1, cam: { p: [SX + 30, 22, 30], p2: [SX + 24, 20, 26], t: [SX, 0, -4], fov: 55 } },
    /* 28 */ { m: "stadium", cheer: 1, screen: "x", cam: { p: [SX + 2, 14, 2], p2: [SX + 1.5, 16, -2], t: [SX, 24, -36], fov: 48 } },
    /* 29 */ { m: "stadium", ball: 1, cast: [["g1", SX - 14, 2.5, 180, "hold", "smirk", { s: 4.2 }]], cam: { p: [SX - 4, 4, 16], t: [SX - 14, 9, 0], fov: 58 } },
    /* 30 */ { m: "stadium", rope: 1, cast: [["g1", SX - 4, 4, 90, "hold", "angry", { s: 3.5 }], ["g2", SX + 4, 4, -90, "hold", "angry", { s: 3.5 }], ["winner", SX - 7, 4, 90, "hold", "angry", { s: 3.2 }], ["rich", SX + 7, 4, -90, "hold", "angry", { s: 3.2 }]], cam: { p: [SX, 5, 24], t: [SX, 5, 4], fov: 58 } },
    /* 31 */ { m: "stadium", stomp: [SX + 0.6, 9.4], cast: [["sam", SX, 9.4, 0, "hands", "scared", { s: SAM }]], cam: { p: [SX + 0.4, 0.25, 10.8], t: [SX + 0.3, 0.6, 9.2], fov: 62, tight: 1 } },
    /* 32 */ { m: "stadium", cast: [["sam", SX, 9.4, 0, "idle", "angry", { s: SAM }]], cam: { face: "sam", d: 1.5, dx: 0.2, fov: 46 } },
    /* 33 */ { m: "stadium", cheer: 1, screen: "final", cam: { p: [SX + 2, 12, 2], t: [SX, 24, -36], fov: 46 } },
    /* 34 */ { m: "stadium", cam: { p: [SX + 4, 3, 4], p2: [SX + 3.2, 3, 2.5], t: [SX, 2.3, -6], fov: 50 } },
    /* 35 */ { m: "stadium", cheer: 1, benchFlip: 1, cast: [["g1", SX - 6, 8, 150, "walk", "angry", { s: 4 }], ["g2", SX + 6, 9, 210, "walk", "angry", { s: 4 }]], cam: { p: [SX, 9, 16], t: [SX, 5, 4], fov: 60 } },
    /* 36 */ { m: "stadium", liftCar: 1, cast: [["winner", SX - 8, -2, 40, "up", "angry", { s: 4 }]], cam: { p: [SX + 2, 3, 12], t: [SX - 8, 14, -2], fov: 60 } },
    /* 37 */ { m: "stadium", benchFlip: 2, cast: [["rich", SX + 4, 10, -20, "kick", "angry", { s: 3.5 }]], cam: { p: [SX - 6, 4, 22], t: [SX + 3, 4, 11], fov: 58 } },
    /* 38 */ { m: "stadium", clouds: 1, cast: [["gold", SX - 4, -14, 20, "lookUp", "serious", { s: GOLD }]], cam: { p: [SX + 24, 6, 26], t: [SX - 4, 18, -14], fov: 66 } },
    /* 39 */ { m: "stadium", cast: [["sam", SX + 6.2, 4.6, 120, "idle", "shock", { s: SAM }]], cam: { face: "sam", d: 1.5, dx: -0.2, fov: 46 } },
    /* 40 */ { m: "stadium", keyOn: 1, cam: { p: [SX + 8.3, 0.7, 3.6], p2: [SX + 8.0, 0.5, 3.3], t: [SX + 7.53, 0.05, 2.71], fov: 44, tight: 1 } },
    /* 41 */ { m: "stadium", keyOn: 1, cast: [["g2", SX + 9, 6.5, 200, "reach", "angry", { s: 4 }]], cam: { p: [SX + 5, 0.4, 0.5], t: [SX + 7.5, 3, 4], fov: 60, tight: 1 } },
    /* 42 */ { m: "stadium", keyOn: 1, cast: [["sam", SX + 6.9, 3.5, 160, "idle", "grin", { s: SAM }]], cam: { face: "sam", d: 1.5, dx: 0.2, fov: 46 } },
    /* 43 */ { m: "stadium", cast: [["gold", SX + 2, -6, 60, "idle", "angry", { s: GOLD }]], cam: { p: [SX + 9, 1, 4], t: [SX + 2, 21, -6], fov: 58 } },
    /* 44 */ { m: "stadium", keyOn: 1, cast: [["gold", SX + 2, -6, 60, "reach", "angry", { s: GOLD }], ["sam", SX + 6.9, 3.5, -120, "run", "scared", { s: SAM }]], cam: { p: [SX + 7.8, 0.35, 4.9], t: [SX + 5, 6, -2], fov: 64, tight: 1 } },
    /* 45 */ { m: "stadium", keyOn: 1, cast: [["sam", SX + 6.6, 3.8, -60, "run", "scared", { s: SAM, to: [SX + 7.3, 3.2], dur: 0.6, yTo: [-0.6, KW.jumped + 0.4, 0.4] }]], cam: { p: [SX + 7.8, 0.5, 4.9], t: [SX + 7.1, 0.1, 3.4], fov: 52, tight: 1 } },
    /* 46 */ { m: "stadium", keyOn: 1, hand: 1, cam: { p: [SX + 9.5, 1.2, 6.2], t: [SX + 7.3, 0.4, 3.2], fov: 54, tight: 1 } },
    /* 47 */ { m: "stadium", keyHand: 1, cast: [["sam", SX + 5.5, 1, -150, "walk", "grin", { s: SAM, to: [SX + 0.5, -4.4], dur: 2.8 }]], cam: { p: [SX + 6.2, 0.25, 2.2], t: [SX + 1, 1.0, -5], fov: 56, tight: 1 } },
    /* 48 */ { m: "stadium", cam: { p: [SX + 28, 20, 26], p2: [SX + 26, 19, 23], t: [SX, 0, -4], fov: 55 } },
    /* 49 */ { m: "stadium", safeOpen: KW.click, keyHand: 1, cast: [["sam", SX + 0.4, -4.4, 180, "reach", "shock", { s: SAM, y: 0.8 }]], cam: { p: [SX - 3, 4.5, 1], t: [SX, 2.2, -5], fov: 50 } },
    /* 50 */ { m: "stadium", safeOpen: -1, screen: "$9.50", cam: { p: [SX + 1, 12, 0], t: [SX, 24, -36], fov: 44 } },
    /* 51 */ { m: "stadium", safeOpen: -1, cheer: 1, conf: 1, screen: "count", cam: { p: [SX + 1, 12, 0], p2: [SX + 0.6, 14, -6], t: [SX, 24, -36], fov: 44 } },
    /* 52 */ { m: "stadium", safeOpen: -1, cheer: 1, conf: 1, cast: [["sam", SX + 0.4, -2.6, 0, "up", "grin", { s: SAM, sTo: [1.2, KW.growing - 0.1, 1.4] }]], cam: { p: [SX + 0.6, 2.5, 6], t: [SX + 0.4, 1.4, -2.6], fov: 52 } },
    /* 53 */ { m: "stadium", safeOpen: -1, cheer: 1, conf: 1, cast: [["sam", SX + 0.4, -2.6, 0, "up", "grin", { s: 1.2, sTo: [7, LS0(52), 1.6] }]], cam: { p: [SX + 1, 1, 12], t: [SX + 0.4, 9, -2.6], fov: 62 } },
    /* 54 */ { m: "day", cr: "sizes", cast: [["sam", 0, -8, 180, "idle", "grin", { s: 12 }]], cam: { p: [10, 44, -2], p2: [9.5, 44.5, -3], t: [0, 0, -50], fov: 60, tight: 1 } },
    /* 55 */ { m: "day", cast: [["sam", 0, -14, 0, "idle", "smirk", { s: 7 }], ["rich", -1.2, -6, 180, "lookUp", "shock"], ["npc2", 1.2, -6.4, 190, "lookUp", "shock"]], cam: { p: [0, 1.2, -1.5], t: [0, 8, -12], fov: 62 } },
    /* 56 */ { m: "stadium", lab: ["BET: ALL HIS MONEY", "r", [SX - 4, 25, -14]], cast: [["gold", SX - 4, -14, 30, "idle", "shock", { s: GOLD }]], cam: { face: "gold", d: 1.6, dx: 0.3, fov: 46 } },
    /* 57 */ { m: "stadium", cast: [["gold", SX + 7.4, 3.1, -60, "hands", "scared", { s: GOLD, sTo: [SAM, KW.shrank, 0.9], yTo: [-0.5, KW.fell, 0.5] }]], cam: { p: [SX + 14, 6, 12], p2: [SX + 10.5, 1.5, 6.5], t: [SX + 7.4, 3, 3.1], fov: 60, tight: 1 } },
    /* 58 */ { m: "stadium", crumb: [SX + 7.45, 0.06, 3.25], cast: [["sam", SX + 1, -2, 120, "hold", "smirk", { s: 7 }]], cam: { p: [SX + 14, 4, 10], t: [SX + 5, 5, 1], fov: 62 } },
    /* 59 */ { m: "stadium", crumb: [SX + 7.47, 0.08, 3.25], lab: ["1 CRUMB", "y", [SX + 7.4, 0.55, 3.1]], cast: [["gold", SX + 7.4, 3.1, 30, "hold", "sad", { s: SAM }]], cam: { p: [SX + 7.75, 0.3, 3.75], t: [SX + 7.4, 0.25, 3.1], fov: 46, tight: 1 } },
    /* 60 */ { m: "stadium", crumb: [SX + 7.47, 0.08, 3.25], conf: 1, cheer: 1, cast: [["gold", SX + 7.4, 3.1, 30, "hold", "sad", { s: SAM }]], cam: { face: "gold", d: 1.3, dx: 0.15, fov: 44 } },
  ];
  function LS0(i) { return LS[i]; }

  function placeCrowd(mode, u, s, t, camP) {
    CROWD.forEach((c) => { c.root.visible = false; c.lamp.visible = false; c.root.scale.setScalar(1); });
    if (!mode) return;
    CROWD.forEach((c, i) => {
      const r = mulberry(100 + i), a = r(), b = r(), d = r();
      if (i >= 18) return;
      const side = i % 2 ? 1 : -1; let x = side * (4.6 + b * 1.0), z = 30 - a * 62, ry = 180, p = "walk", e = "smile", sc = 1;
      if (mode === "sizes") { sc = [0.3, 0.6, 1, 1, 1.6, 2.5, 4][Math.floor(d * 7)]; x = side * (2.5 + b * 2.5); z -= u * (1 + b * 0.5) * Math.sqrt(sc); e = sc > 2 ? "smirk" : sc < 0.7 ? "sad" : "smile"; }
      if (mode === "look") { p = "idle"; ry = 90 + (b - 0.5) * 40; z = -8 - a * 14; x = (b - 0.5) * 7; e = "shock"; }
      if (camP && Math.hypot(x - camP[0], 1.3 * sc - camP[1], z - camP[2]) < 9 + 3 * sc + (camP[1] > 10 ? 16 : 0)) return;
      c.root.visible = true; c.root.position.set(x, 0, z); c.root.rotation.y = ry * D2R; c.root.scale.setScalar(sc); c.setEx(e); pose(c, p, u + a * 3);
    });
  }

  const camera = new THREE.PerspectiveCamera(50, W / H, 0.02, 600);
  const lab = document.getElementById("lab"), labSpan = lab.querySelector("span");
  const LABCOL = { r: "#FF4D5E", y: "#FFD23F", g: "#5CF08C" };
  const v3 = new THREE.Vector3(), look = new THREE.Vector3(), tmpV = new THREE.Vector3();

  function setMode(m, s) {
    street.visible = m === "day"; stadium.visible = m === "stadium"; school.visible = m === "school"; room.visible = false; kitchen.visible = false; voidG.visible = false;
    scene.fog.color.set(0xBFE0F8); scene.fog.near = m === "school" ? 300 : 60; scene.fog.far = m === "school" ? 600 : 220;
    scene.background = m === "school" ? new THREE.Color(0xF2E3B8) : skyDay;
    hemi.intensity = m === "school" ? 0.8 : 0.95; hemi.color.set(0xD8E8FF);
    sun.intensity = m === "school" ? 1.6 : 2.6; sun.color.set(0xFFF1D8);
    nightWins.forEach((w) => (w.emissiveIntensity = 0)); lampLights.forEach((l) => (l.intensity = 0)); porch.intensity = 0;
    roomLamp.intensity = 0; kLamp.intensity = 0; voidLight.intensity = 0; voidFill.intensity = 0;
    moon.visible = false; clouds.forEach((c) => (c.visible = m === "day"));
    renderer.toneMappingExposure = 1.1;
  }
  const scaleAt = (o, t) => { let sc = o.s || 1; if (o.sTo) { const q = ease((t - o.sTo[1]) / o.sTo[2]); sc = sc + (o.sTo[0] - sc) * q; } return sc; };
  const yAt = (o, t) => { let y = o.y || 0; if (o.yTo) { const q = ease((t - o.yTo[1]) / o.yTo[2]); y = y + (o.yTo[0] - y) * q; } return y; };

  function render(t) {
    let i = 0; for (let k = 0; k < LS.length; k++) if (t >= LS[k]) i = k;
    const s = S[i], t0 = LS[i], t1 = i + 1 < LS.length ? LS[i + 1] : DUR, u = t - t0, dur = t1 - t0, p = ease(u / dur);
    setMode(s.m, s);
    for (const k in A) { A[k].root.visible = false; A[k].lamp.visible = false; }
    const castPos = {};
    (s.cast || []).forEach(([name, x, z, r, ps, ex, o]) => {
      const ch = A[name]; ch.root.visible = true; let X = x, Z = z, P = ps; o = o || {};
      if (o.to) { const q = clamp((t - (o.from || t0)) / o.dur, 0, 1); X = x + (o.to[0] - x) * q; Z = z + (o.to[1] - z) * q; if (q >= 1 || t < (o.from || t0)) P = ps === "walk" || ps === "run" ? "idle" : ps; }
      const sc = scaleAt(o, t); ch.root.scale.setScalar(sc);
      ch.root.position.set(X, yAt(o, t), Z); ch.root.rotation.y = r * D2R;
      ch.setEx(o.exAfter && t >= o.exAfter[0] ? o.exAfter[1] : ex); pose(ch, P, u);
      castPos[name] = [X, Z, r, sc, ch.root.position.y];
    });
    billboard.userData.set(s.bb || "games"); shopSign.userData.set(s.shop || "price"); clock.userData.set("8:00");
    doorL.position.x = -1.0; doorR.position.x = 1.0; doorGlow.visible = false; bus.visible = false; car.visible = false;
    // Requisiten
    cat.visible = !!s.cat; if (s.cat) { cat.position.set(s.cat[0], 0, s.cat[1]); cat.rotation.y = s.cat[2] * D2R; }
    peanut.visible = !!s.peanut; if (s.peanut) peanut.position.set(s.peanut[0], 0.09, s.peanut[1]);
    coin.visible = !!s.coin; if (s.coin) coin.position.set(s.coin[0], 0.01, s.coin[1]);
    stand.visible = !!s.stand; if (s.stand) stand.position.set(s.stand[0], 0, s.stand[1]);
    crumb.visible = !!s.crumb; if (s.crumb) { crumb.position.set(...s.crumb); crumb.scale.setScalar(s.m === "stadium" ? 0.8 : 0.45); }
    ruler.visible = !!s.ruler; if (s.ruler) { const tiny = s.ruler[2]; ruler.scale.setScalar(tiny ? 0.06 : 1); ruler.position.set(s.ruler[0], (tiny ? 0.06 : 1) * 6, s.ruler[1]); ruler.rotation.y = tiny ? 0 : -Math.PI / 2; }
    // Nest + Vögel um Mr. Gold
    nest.visible = !!s.nest; birds.forEach((b) => (b.visible = !!s.nest));
    if (s.nest) { const g = A.gold; g.head.updateWorldMatrix(true, false); g.head.getWorldPosition(tmpV); const top = tmpV.y + 0.78 * GOLD * 1.0;
      nest.position.set(tmpV.x, tmpV.y + 1.22 * GOLD, tmpV.z); nest.scale.setScalar(2.6);
      birds.forEach((b, k) => { const a = u * 1.6 + k * 2.1; b.position.set(tmpV.x + Math.cos(a) * 3.5, tmpV.y + 1.3 * GOLD + k * 0.6 + Math.sin(u * 3 + k) * 0.4, tmpV.z + Math.sin(a) * 3.5); b.rotation.y = -a; b.scale.setScalar(1.2); flap(b, u + k); }); }
    plane.visible = !!s.plane; if (s.plane) { plane.position.set(-30 + u * 18, 26, -3); plane.rotation.y = Math.PI / 2; }
    pigeon.visible = !!s.pigeon; if (s.pigeon) { const q = ease((t - KW.pigeon) / 0.5); const ly = yAt({ y: 0, yTo: [1.6, KW.pigeon + 0.2, 1.2] }, t);
      pigeon.position.set(-2.25 - (1 - q) * 4, 0.55 + ly + (1 - q) * 3, 4.6); pigeon.rotation.y = Math.PI / 2; pigeon.scale.setScalar(0.5); flap(pigeon, u); }
    debris.forEach((d) => (d.visible = false));
    if (s.debris) { const q = t - KW.crash; if (q > 0) debris.forEach((d) => { const v = d.userData; d.visible = true; d.position.set(s.debris[0] + Math.cos(v.a) * v.v * q, s.debris[1] + v.v * 1.5 * q - 4.9 * q * q, s.debris[2] + Math.sin(v.a) * v.v * q); d.rotation.set(q * 5 * v.s, q * 3, q * 4); }); }
    // Stadion
    crowdUpdate(u, !!s.cheer);
    bigScreen.userData.set(s.screen === "count" ? (t >= KW.tenm ? "$10,000,000" : t >= KW.onem ? "$1,000,000" : t >= KW.onek ? "$1,000" : "$9.50") : s.screen || "x");
    keyGlow.visible = !!s.keyOn; keyGlow.material.opacity = 0.6 + 0.4 * Math.sin(u * 6); keyHand.visible = !!s.keyHand; if (s.keyHand && !keyHand.children.length) keyHand.add(keyM);
    ball.visible = !!s.ball; if (s.ball) { const q = ease((t - KW.dropped) / 0.8); ball.position.set(SX - 14, 12 + (1 - q) * 3 - Math.max(0, t - KW.dropped - 0.8) * 6, 2.6 + (1 - q) * -0.5); }
    rope.visible = !!s.rope; if (s.rope) { rope.position.set(SX + Math.sin(u * 3) * 0.6, 6.4, 4); rope.rotation.y = Math.PI / 2; }
    benches.forEach((b, k) => { b.rotation.set(0, 0, 0); b.position.y = 0.25; if (s.benchFlip) { const q = ease((u - 0.2 - k * 0.15) / 0.6); b.rotation.x = q * Math.PI * (k % 2 ? 1 : -1); b.position.y = 0.25 + Math.sin(q * Math.PI) * 3; } });
    liftCar.visible = !!s.liftCar; if (s.liftCar) { liftCar.position.set(SX - 8, 2 + 4 * 4 + Math.sin(u * 4) * 0.3, -2); liftCar.scale.setScalar(1.6); liftCar.rotation.z = Math.sin(u * 3) * 0.1; }
    safeDoor.rotation.y = 0; safeGlow.visible = false;
    if (s.safeOpen !== undefined) { const q = s.safeOpen === -1 ? 1 : ease((t - s.safeOpen) / 0.6); safeDoor.rotation.y = -1.6 * q; safeGlow.visible = q > 0.1; }
    conf.visible = !!s.conf; if (s.conf) confUpdate(u, s.m === "stadium" ? SX : 0, 0, 0);
    // Riesenhand / Stampfen
    if (s.hand) { const g = A.gold; g.root.visible = true; g.root.scale.setScalar(GOLD); g.root.position.set(SX + 9.5, 0, -4); g.root.rotation.y = -0.3; pose(g, "reach", u); g.armR.rotation.x = -0.9 + Math.sin(u * 3) * 0.05; g.armL.rotation.x = -0.6; }
    if (s.stomp) { const g = A.g1; g.root.visible = true; g.root.scale.setScalar(4); const q = Math.max(0, Math.sin(clamp((u - 0.2) * 2.2, 0, Math.PI))); g.root.position.set(s.stomp[0] + 1.2, 0, s.stomp[1] - 3.2); g.root.rotation.y = 0; pose(g, "idle", u); g.legR.rotation.x = -0.25 * q; }
    // Kamera
    const c = s.cam; let P, Tg;
    if (c.face) { const [x, z, r, sc, y0] = castPos[c.face]; const hy = 2.31 * sc + y0;
      const f = [Math.sin(r * D2R), Math.cos(r * D2R)], rt = [Math.cos(r * D2R), -Math.sin(r * D2R)], d = c.d * 1.55 * sc * (1 - 0.06 * p);
      P = [x + f[0] * d + rt[0] * (c.dx || 0) * sc, hy + (c.dy || 0) * sc, z + f[1] * d + rt[1] * (c.dx || 0) * sc]; Tg = [x, hy - 0.02 * sc, z]; }
    else { const p2 = c.p2 || [c.p[0] + (c.t[0] - c.p[0]) * 0.08, c.p[1] + (c.t[1] - c.p[1]) * 0.08, c.p[2] + (c.t[2] - c.p[2]) * 0.08];
      P = [0, 1, 2].map((k) => c.p[k] + (p2[k] - c.p[k]) * p); const t2 = c.t2 || c.t; Tg = [0, 1, 2].map((k) => c.t[k] + (t2[k] - c.t[k]) * p);
      const dd = Math.hypot(P[0] - Tg[0], P[1] - Tg[1], P[2] - Tg[2]); if (!c.tight && dd < 3.2) { const f = 1.5; P = [0, 1, 2].map((k) => Tg[k] + (P[k] - Tg[k]) * f); } }
    placeCrowd(s.cr, u, s, t0, P);
    camera.position.set(...P); look.set(...Tg); camera.fov = c.fov; camera.updateProjectionMatrix(); camera.lookAt(look);
    const sd = Math.max(14, Math.hypot(P[0] - Tg[0], P[1] - Tg[1], P[2] - Tg[2]) * 0.9);
    Object.assign(sun.shadow.camera, { left: -sd, right: sd, top: sd, bottom: -sd, far: sd * 6 }); sun.shadow.camera.updateProjectionMatrix();
    sun.position.set(Tg[0] - sd * 0.6, Tg[1] + sd * 1.1, Tg[2] + sd * 0.7); sun.target.position.set(Tg[0], Tg[1], Tg[2]);
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
    SFX.append((round(LINES[li]["start"] - 0.12, 3), "whoosh-short.mp3", 0.26))
for t, f, v in [
    (KW["taller"] - 0.5, "riser.mp3", 0.25), (KW["taller"], "pop.mp3", 0.45), (KW["cat"], "pop.mp3", 0.4), (KW["house"], "impact-bass-1.mp3", 0.4),
    (LS[6] + 0.1, "impact-bass-2.mp3", 0.4), (LS[7], "sparkle.mp3", 0.3), (KW["airplanes"], "whoosh-cinematic.mp3", 0.4),
    (KW["shrink"], "error.mp3", 0.35), (KW["shoot"], "riser.mp3", 0.3), (KW["crash"], "impact-bass-2.mp3", 0.5), (KW["measure"], "click.mp3", 0.4),
    (LS[16], "pop.mp3", 0.35), (LS[17], "error.mp3", 0.3), (KW["lemonade"] + 0.6, "click-soft.mp3", 0.4), (LS[22] + 0.4, "sparkle.mp3", 0.35),
    (KW["pigeon"], "whoosh-short.mp3", 0.45), (KW["games"], "notification.mp3", 0.4), (LS[26], "whoosh-cinematic.mp3", 0.35),
    (KW["million10"], "chime.mp3", 0.45), (KW["dropped"] + 0.8, "impact-bass-1.mp3", 0.4), (KW["stepped"], "impact-bass-2.mp3", 0.5),
    (KW["key"], "sparkle.mp3", 0.35), (KW["cars"], "impact-bass-1.mp3", 0.4), (LS[36] + 0.3, "impact-bass-1.mp3", 0.35),
    (KW["shine"], "sparkle.mp3", 0.45), (KW["hand"], "whoosh-cinematic.mp3", 0.4), (KW["jumped"], "whoosh-short.mp3", 0.4), (LS[45], "impact-bass-2.mp3", 0.4),
    (KW["silent"], "riser.mp3", 0.2), (KW["click"], "click.mp3", 0.6), (KW["click"] + 0.1, "impact-bass-2.mp3", 0.4),
    (KW["onek"], "chime.mp3", 0.4), (KW["onem"], "chime.mp3", 0.45), (KW["tenm"], "chime.mp3", 0.5), (KW["tenm"] + 0.1, "sparkle.mp3", 0.5),
    (KW["growing"], "riser.mp3", 0.35), (LS[52], "impact-bass-1.mp3", 0.4), (KW["shrank"], "error.mp3", 0.35), (KW["fell"] + 0.3, "pop.mp3", 0.45),
    (KW["crumb"], "pop.mp3", 0.45), (KW["days"] + 0.4, "sparkle.mp3", 0.4),
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
