#!/usr/bin/env python3
"""Baut „Was wäre, wenn die Erde 5 Sekunden lang stoppt?“ – 3D-Stil wie Referenz C (Elektronen-Video).

Eine durchgehende Three.js-Welt (compositions/world.html) + HTML-Overlays (Titel, Countdown, Serifen-Untertitel).
1. Stimme: python3 ../../tools/align.py . assets/source/<aufnahme>.mp3   (Platzhalter: tools/tts.py)
2. python3 build.py
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "tools"))
from simkit import load_timings, fmt, audio_len, plain  # noqa: E402

SFX_ROOT = Path("/root/.claude/plugins/cache/hyperframes/hyperframes/0.8.197/skills/media-use/audio/assets/sfx")
W, H = 1080, 1920

T = load_timings(HERE)
B = {b["id"]: b for b in T["beats"]}
VOICE_END = T["beats"][-1]["end"]
END_CARD = round(VOICE_END + 0.4, 3)
TOTAL = round(END_CARD + 2.8, 2)


def wa(bid, li, wi=0):
    return round(B[bid]["lines"][li]["words"][wi]["start"], 3)


K = {
    "stop": round(B["platz"]["lines"][3]["end"] - 0.1, 3),   # das „t“ von „stoppt“ (Zeilenende)
    "turn": wa("stopp", 2, 0),                 # Kamera dreht nach Osten
    "roofs": wa("sturm", 2, 1),                # „Dächer“
    "space": round(B["ozean"]["start"] - 0.7, 3),
    "globe": round(B["ozean"]["start"] + 0.5, 3),
    "restart": wa("zurueck", 0, 4),            # „wieder“
    "back": round(wa("zurueck", 1, 0) - 0.25, 3),
    "yank": wa("zurueck", 2, 2),               # „andere Richtung“
    "end": END_CARD,
}
SLOW = round((K["restart"] - K["stop"]) / 5.0, 1)   # wie stark die 5 Sekunden gedehnt sind

# ------------------------------------------------------------------ 3D-Welt

WORLD_JS = r"""
const K = __K__;
window.__hf = window.__hf || {}; window.__hf.buildReady = window.__hf.buildReady || {};
window.__hf.buildReady.world = import("./assets/three.module.min.js").then((THREE) => {
  const W = 1080, H = 1920, DUR = __DUR__;
  const canvas = document.getElementById("w-canvas");
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1); renderer.setSize(W, H, false);
  renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;

  function mulberry(a) { return function () { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
  const R = mulberry(7);
  const rr = (a, b) => a + (b - a) * R();
  const pick = (arr) => arr[Math.floor(R() * arr.length)];
  const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
  const ease = (x) => { x = clamp(x, 0, 1); return x * x * (3 - 2 * x); };
  const easeIn3 = (x) => { x = clamp(x, 0, 1); return x * x * x; };

  // ---------------- Stadt
  const city = new THREE.Scene();
  const SKY = new THREE.Color("#9FB0C8"), BLACK = new THREE.Color("#000000");
  const lineMat = new THREE.LineBasicMaterial({ color: 0xDCE6FF, transparent: true, opacity: 0.9, fog: true });
  const blackMat = new THREE.MeshBasicMaterial({ color: 0x000000, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 });
  const solids = [];
  function solid(geo, color, x, y, z, parent) {
    const mat = new THREE.MeshLambertMaterial({ color });
    const m = new THREE.Mesh(geo, mat);
    m.position.set(x, y, z); m.castShadow = true; m.receiveShadow = true;
    const e = new THREE.LineSegments(new THREE.EdgesGeometry(geo, 25), lineMat); e.visible = false; m.add(e);
    (parent || city).add(m); solids.push({ m, e, mat }); return m;
  }
  const box = (w, h, d) => new THREE.BoxGeometry(w, h, d);
  function roofGeo(w, h, d) {  // Satteldach (Prisma)
    const s = new THREE.Shape(); s.moveTo(-d / 2, 0); s.lineTo(d / 2, 0); s.lineTo(0, h); s.lineTo(-d / 2, 0);
    const g = new THREE.ExtrudeGeometry(s, { depth: w, bevelEnabled: false }); g.translate(0, 0, -w / 2); g.rotateY(Math.PI / 2); return g;
  }

  // Boden
  const ground = solid(new THREE.BoxGeometry(4600, 1, 600), "#8E8A80", 2000, -0.5, 0);
  solid(new THREE.BoxGeometry(110, 0.2, 90), "#BDB4A4", 0, 0.05, 0);              // Platz-Pflaster
  for (let i = -5; i <= 5; i++) solid(new THREE.BoxGeometry(0.3, 0.22, 90), "#A99F8E", i * 10, 0.06, 0);

  // Neues Rathaus (Nordseite) mit Turm
  const RH = "#6F6A63";
  solid(box(90, 28, 18), RH, 0, 14, -55);
  for (let i = -4; i <= 4; i++) solid(new THREE.ConeGeometry(2.2, 7, 4), RH, i * 10, 31.5, -47);
  solid(box(11, 78, 11), "#66615A", 8, 39, -50);
  solid(new THREE.ConeGeometry(7, 18, 4), "#3F5A55", 8, 87, -50);
  solid(box(13, 3, 13), "#5D5852", 8, 70, -50);
  // Häuser West/Süd/Ost um den Platz
  const pastel = ["#D8C3A5", "#C9A27E", "#E6D8B8", "#B7C4C8", "#D9B8A0", "#E9E1C9", "#C7B49A"];
  const dyn = [];
  function house(x, z, w, d, h, ry) {
    const g = new THREE.Group(); g.position.set(x, 0, z); g.rotation.y = ry || 0; city.add(g);
    solid(box(w, h, d), pick(pastel), 0, h / 2, 0, g);
    const roof = solid(roofGeo(w, rr(5, 8), d), "#8C4B3A", 0, h, 0, g);
    return { g, roof, h };
  }
  for (let i = 0; i < 6; i++) house(-45 + i * 18, 55, 17, 16, rr(16, 24));
  for (let i = 0; i < 4; i++) house(-68, -30 + i * 20, 18, 16, rr(16, 22), Math.PI / 2);
  // Straße „Tal“ nach Osten: zwei Häuserzeilen
  const streetRoofs = [];
  for (const side of [-1, 1]) {
    let x = 62;
    while (x < 2300) {
      const w = rr(14, 26), h = rr(14, 34);
      const hs = house(x + w / 2, side * rr(19, 22) - side * 0 + side * 8, w, 14, h);
      streetRoofs.push({ roof: hs.roof, base: hs.roof.position.clone(), gx: x + w / 2, gz: hs.g.position.z, h: hs.h, s: R() });
      x += w + rr(0.5, 3);
    }
  }
  // Mariensäule
  solid(box(5, 3, 5), "#9C978E", 0, 1.5, 0);
  solid(new THREE.CylinderGeometry(0.7, 0.8, 14, 8), "#C9C2B4", 0, 10, 0);
  const madonna = solid(new THREE.ConeGeometry(0.9, 2.6, 6), "#D4AF37", 0, 18.3, 0);
  // Bäume, Laternen, Bänke (bleiben liegen → werden am Ende zurückgerissen)
  const leftovers = [];
  function tree(x, z) {
    const g = new THREE.Group(); g.position.set(x, 0, z); city.add(g);
    solid(new THREE.CylinderGeometry(0.3, 0.4, 3, 6), "#6B4B33", 0, 1.5, 0, g);
    solid(new THREE.IcosahedronGeometry(rr(2.2, 3), 0), pick(["#4F7A3A", "#5C8A42", "#46703A"]), 0, 4.6, 0, g);
    leftovers.push({ g, base: g.position.clone(), s: R() }); return g;
  }
  for (let i = 0; i < 7; i++) tree(-48 + i * 16, 40);
  for (let i = 0; i < 5; i++) { const g = new THREE.Group(); g.position.set(-40 + i * 20, 0, -30); city.add(g);
    solid(new THREE.CylinderGeometry(0.12, 0.12, 5, 6), "#2E3338", 0, 2.5, 0, g); solid(box(0.7, 0.5, 0.7), "#F2E2A0", 0, 5.2, 0, g);
    leftovers.push({ g, base: g.position.clone(), s: R() }); }
  for (let i = 0; i < 6; i++) { const g = new THREE.Group(); g.position.set(-35 + i * 14, 0, 28); city.add(g);
    solid(box(3, 0.25, 0.9), "#7A5638", 0, 0.9, 0, g); solid(box(3, 0.9, 0.2), "#7A5638", 0, 1.4, -0.35, g);
    leftovers.push({ g, base: g.position.clone(), s: R() }); }

  // Menschen (Block-Figuren wie in der Referenz) und Autos
  const shirts = ["#E6E1D3", "#2F4C8F", "#C9B037", "#B03A2E", "#3C8D6E", "#E8E8E8", "#8A5A9E", "#D97B29"];
  function person(x, z, ry) {
    const g = new THREE.Group(); g.position.set(x, 0, z); g.rotation.y = ry; city.add(g);
    const pants = pick(["#2B3448", "#3D3A36", "#4A5A78"]);
    solid(box(0.28, 0.9, 0.28), pants, -0.16, 0.45, 0, g); solid(box(0.28, 0.9, 0.28), pants, 0.16, 0.45, 0, g);
    solid(box(0.62, 0.75, 0.34), pick(shirts), 0, 1.28, 0, g);
    solid(box(0.34, 0.36, 0.34), pick(["#E8C39E", "#C68E62", "#8D5A3B", "#F1D2B4"]), 0, 1.86, 0, g);
    return g;
  }
  for (let i = 0; i < 46; i++) {
    const x = rr(-45, 50), z = rr(-35, 38);
    if (Math.abs(x) < 4 && Math.abs(z) < 4) continue;
    dyn.push({ g: person(x, z, rr(0, 6.28)), kind: "p", s: R() });
  }
  function car(x, z) {
    const g = new THREE.Group(); g.position.set(x, 0, z); city.add(g);
    const c = pick(["#B03A2E", "#2F4C8F", "#E8E8E8", "#2E3338", "#C9B037"]);
    solid(box(4.2, 1.0, 1.8), c, 0, 0.75, 0, g); solid(box(2.2, 0.8, 1.6), c, -0.2, 1.65, 0, g);
    return g;
  }
  // ein paar Menschen direkt vor dir: sie fliegen sichtbar neben dir her
  for (const [x, z] of [[-18, 16], [-11, 14], [-6, 19], [-15, 9], [-3, 12], [-20, 21], [-9, 6], [-1, 17]])
    dyn.push({ g: person(x, z, rr(0, 6.28)), kind: "p", s: R() });
  for (let i = 0; i < 14; i++) dyn.push({ g: car(rr(65, 700), pick([-4, 4])), kind: "c", s: R() });

  // Licht (Abenddämmerung)
  city.add(new THREE.HemisphereLight(0xCFDCF2, 0x5B5248, 0.9));
  const sun = new THREE.DirectionalLight(0xFFE2C0, 1.6);
  sun.position.set(-80, 120, 90); sun.castShadow = true;
  sun.shadow.mapSize.set(2048, 2048);
  Object.assign(sun.shadow.camera, { left: -110, right: 110, top: 110, bottom: -110, near: 10, far: 400 });
  city.add(sun); city.add(sun.target);
  city.fog = new THREE.Fog(SKY, 180, 900);

  // Bodenraster (nur im Drahtgitter-Modus) – zeigt, wie schnell der Boden unter dir wegzieht
  const gp = [];
  for (let z = -150; z <= 150; z += 10) gp.push(new THREE.Vector3(-300, 0.05, z), new THREE.Vector3(2600, 0.05, z));
  for (let x = -300; x <= 2600; x += 10) gp.push(new THREE.Vector3(x, 0.05, -150), new THREE.Vector3(x, 0.05, 150));
  const groundGrid = new THREE.LineSegments(new THREE.BufferGeometry().setFromPoints(gp),
    new THREE.LineBasicMaterial({ color: 0x5A6A8C, transparent: true, opacity: 0.55, fog: true }));
  city.add(groundGrid);

  // Sterne + Windstreifen (nur im Drahtgitter-Modus)
  const starGeo = new THREE.BufferGeometry(); const sp = [];
  for (let i = 0; i < 1800; i++) { const a = rr(0, 6.28), b = rr(-0.2, 1.2), r = 1500;
    sp.push(Math.cos(a) * Math.cos(b) * r, Math.sin(b) * r + 50, Math.sin(a) * Math.cos(b) * r); }
  starGeo.setAttribute("position", new THREE.Float32BufferAttribute(sp, 3));
  const stars = new THREE.Points(starGeo, new THREE.PointsMaterial({ color: 0xFFFFFF, size: 2.2, sizeAttenuation: false, fog: false }));
  city.add(stars);
  const NW = 700, windBase = [];
  const windGeo = new THREE.BufferGeometry(); const windPos = new Float32Array(NW * 6);
  for (let i = 0; i < NW; i++) windBase.push([rr(0, 400), rr(0.3, 40), rr(-60, 60), rr(2, 9), rr(0.6, 1.4)]);
  windGeo.setAttribute("position", new THREE.BufferAttribute(windPos, 3));
  const wind = new THREE.LineSegments(windGeo, new THREE.LineBasicMaterial({ color: 0xBFD3FF, transparent: true, opacity: 0.55, fog: true }));
  wind.frustumCulled = false; city.add(wind);

  // ---------------- Globus
  const globe = new THREE.Scene(); globe.background = BLACK;
  const earth = new THREE.Group(); globe.add(earth);
  const RAD = 100;
  const toV = (lon, lat, r) => { const a = THREE.MathUtils.degToRad(lon), b = THREE.MathUtils.degToRad(lat);
    return new THREE.Vector3(r * Math.cos(b) * Math.sin(a), r * Math.sin(b), r * Math.cos(b) * Math.cos(a)); };
  earth.add(new THREE.Mesh(new THREE.SphereGeometry(RAD * 0.995, 48, 32), new THREE.MeshBasicMaterial({ color: 0x02040A })));
  const grid = [];
  for (let lat = -75; lat <= 75; lat += 15) for (let lon = -180; lon < 180; lon += 4) grid.push(toV(lon, lat, RAD), toV(lon + 4, lat, RAD));
  for (let lon = -180; lon < 180; lon += 15) for (let lat = -88; lat < 88; lat += 4) grid.push(toV(lon, lat, RAD), toV(lon, lat + 4, RAD));
  earth.add(new THREE.LineSegments(new THREE.BufferGeometry().setFromPoints(grid), new THREE.LineBasicMaterial({ color: 0x2A3A66 })));
  const CONT = __CONT__;
  const coast = [];
  for (const c of CONT) for (let i = 0; i < c.length; i++) { const a = c[i], b = c[(i + 1) % c.length];
    for (let k = 0; k < 6; k++) coast.push(toV(a[0] + (b[0] - a[0]) * k / 6, a[1] + (b[1] - a[1]) * k / 6, RAD * 1.002),
      toV(a[0] + (b[0] - a[0]) * (k + 1) / 6, a[1] + (b[1] - a[1]) * (k + 1) / 6, RAD * 1.002)); }
  const coastMat = new THREE.LineBasicMaterial({ color: 0xE8F0FF });
  earth.add(new THREE.LineSegments(new THREE.BufferGeometry().setFromPoints(coast), coastMat));
  const muc = new THREE.Mesh(new THREE.SphereGeometry(1.6, 12, 8), new THREE.MeshBasicMaterial({ color: 0xFF4D5E }));
  muc.position.copy(toV(11.6, 48.1, RAD * 1.01)); earth.add(muc);
  // Ozean-Welle: helle Front, die nach Osten über den Globus läuft
  const NWAVE = 3, waveGeo = new THREE.BufferGeometry(), wavePos = new Float32Array(NWAVE * 70 * 6);
  waveGeo.setAttribute("position", new THREE.BufferAttribute(wavePos, 3));
  const wave = new THREE.LineSegments(waveGeo, new THREE.LineBasicMaterial({ color: 0x7FC4FF, transparent: true, opacity: 0.95 }));
  wave.frustumCulled = false; earth.add(wave);
  const gstars = new THREE.Points(starGeo, new THREE.PointsMaterial({ color: 0xFFFFFF, size: 2, sizeAttenuation: false }));
  globe.add(gstars);

  const cam = new THREE.PerspectiveCamera(62, W / H, 0.1, 5000);
  const gcam = new THREE.PerspectiveCamera(40, W / H, 1, 5000);
  const look = new THREE.Vector3();

  function setWire(on) {
    for (const s of solids) { s.m.material = on ? blackMat : s.mat; s.e.visible = on; s.m.castShadow = !on; }
    city.background = on ? BLACK : SKY; city.fog.color.copy(on ? BLACK : SKY);
    city.fog.near = on ? 60 : 180; city.fog.far = on ? 520 : 900;
    stars.visible = on; wind.visible = on; renderer.shadowMap.enabled = !on; groundGrid.visible = on;
  }

  // Kamerapfad
  const P0 = new THREE.Vector3(-4, 26, 40), L0 = new THREE.Vector3(6, 30, -50);
  const P1 = new THREE.Vector3(-14, 1.7, 26), L1 = new THREE.Vector3(6, 14, -50);
  const V = 42;   // sichtbare Fluggeschwindigkeit (Meter pro Echtzeit-Sekunde)
  function flyX(s) { return s < 1.5 ? V * s * s / 3 : V * (s - 0.75); }   // sanft anfahren

  function render(t) {
    const stop = t >= K.stop, s = t - K.stop;
    // Rückkehr auf den Platz am Ende: alle Objekte an Ausgangsposition, liegen gebliebene Dinge fliegen nach Westen
    const back = t >= K.back;
    if (t >= K.globe && !back) {
      // ---------- Globus
      const g = t - K.globe;
      gcam.position.set(0, 60, 330 - 40 * ease(g / 3)); gcam.lookAt(0, 20, 0);
      const spin = t < K.restart ? 0 : (t - K.restart) * 0.9;
      earth.rotation.y = THREE.MathUtils.degToRad(-11.6) - spin; earth.rotation.x = THREE.MathUtils.degToRad(30);
      let p = 0;
      for (let k = 0; k < NWAVE; k++) {
        const lon0 = 11.6 + g * 22 + k * 3;
        for (let i = 0; i < 70; i++) {
          const la = -70 + i * 2, a = toV(lon0 + Math.sin(i * 0.7) * 2, la, RAD * 1.01), b = toV(lon0 + Math.sin((i + 1) * 0.7) * 2, la + 2, RAD * 1.01);
          wavePos.set([a.x, a.y, a.z, b.x, b.y, b.z], p); p += 6;
        }
      }
      waveGeo.attributes.position.needsUpdate = true;
      wave.material.opacity = t < K.restart ? 0.95 : Math.max(0, 0.95 - (t - K.restart) * 2);
      renderer.shadowMap.enabled = false;
      renderer.render(globe, gcam); return;
    }

    setWire(stop && !(t >= K.end + 10));
    // Ausgangslage
    for (const d of dyn) { d.g.position.copy(d.base || (d.base = d.g.position.clone())); d.g.rotation.set(0, d.ry ?? (d.ry = d.g.rotation.y), 0); }
    for (const r of streetRoofs) { r.roof.position.copy(r.base); r.roof.rotation.set(0, 0, 0); }
    for (const o of leftovers) { o.g.position.copy(o.base); o.g.rotation.set(0, 0, 0); }

    if (!stop) {
      // ---------- Vor dem Stopp: ruhiger Platz, Kamerafahrt auf Augenhöhe
      const k = ease(t / (K.stop - 1.5));
      cam.position.lerpVectors(P0, P1, k); look.lerpVectors(L0, L1, k); cam.fov = 62;
    } else if (!back) {
      // ---------- Stopp: du (die Kamera) und alles Lose fliegt mit ~310 m/s nach Osten (zeitlich gedehnt)
      const x = flyX(s);
      const turn = ease((s - 0.5) / 2.0);
      const up = t < K.space ? 0 : easeIn3((t - K.space) / 1.6);
      cam.position.set(P1.x + x, P1.y + 2.5 * ease(s / 3) + up * 1800, P1.z * (1 - ease((s - 0.2) / 1.8)) + Math.sin(s * 9) * 0.06);
      const yaw = -Math.PI / 2 * (1 - turn);       // erst Richtung Rathaus (Norden), dann nach Osten
      look.set(cam.position.x + Math.cos(yaw) * 50, cam.position.y + 6 - up * 60, cam.position.z + Math.sin(yaw) * 50);
      cam.fov = 62 + 10 * ease(s / 2);
      for (const d of dyn) {
        const v = 0.86 + d.s * 0.22, lift = d.kind === "p" ? 1.2 : 0.6;
        d.g.position.x = d.base.x + flyX(s) * v;
        d.g.position.y = Math.max(0, lift * s * (0.4 + d.s)) ;
        d.g.rotation.set(s * (0.6 + d.s) * 0.7, d.ry + s * 0.5, s * (d.s - 0.5) * 1.4);
      }
      const ts = t - K.roofs;
      for (const r of streetRoofs) {
        if (ts > 0 && Math.abs(cam.position.x - r.gx) < 160) {
          const f = clamp((ts) * (0.6 + r.s), 0, 6);
          r.roof.position.x = r.base.x + f * 9 * (0.6 + r.s);
          r.roof.position.y = r.base.y + f * f * 1.6;
          r.roof.rotation.set(f * 0.5 * (r.s - 0.5), f * 0.3, f * 0.4);
        }
      }
      // Windstreifen rund um die Kamera, schneller als du
      for (let i = 0; i < NW; i++) {
        const [ox, oy, oz, len, sp] = windBase[i];
        const px = cam.position.x - 120 + ((ox + s * 70 * sp) % 400);
        const py = cam.position.y - 6 + oy, pz = cam.position.z + oz;
        windPos.set([px, py, pz, px + len, py, pz], i * 6);
      }
      windGeo.attributes.position.needsUpdate = true;
    } else {
      // ---------- Zurück: Erde dreht wieder, Liegengebliebenes wird nach Westen gerissen
      const b = t - K.back, y = t - K.yank;
      cam.position.set(P1.x, P1.y + 1.5, P1.z + 6); look.set(P1.x + 6, 10, -50); cam.fov = 66;
      for (const d of dyn) d.g.visible = false;
      for (const o of leftovers) {
        if (y > 0) { const f = y * (0.8 + o.s);
          o.g.position.x = o.base.x - f * f * 18; o.g.position.y = f * 1.4; o.g.rotation.set(0, f * 0.6, f * 1.1 * (o.s + 0.3)); }
      }
      for (let i = 0; i < NW; i++) {
        const [ox, oy, oz, len, sp] = windBase[i];
        const px = cam.position.x + 160 - ((ox + b * 90 * sp) % 400);
        windPos.set([px, oy, cam.position.z - 70 + oz, px - len * 1.6, oy, cam.position.z - 70 + oz], i * 6);
      }
      windGeo.attributes.position.needsUpdate = true;
      wind.visible = y > -0.4;
    }
    if (!back) for (const d of dyn) d.g.visible = true;
    cam.updateProjectionMatrix(); cam.lookAt(look);
    renderer.render(city, cam);
  }

  const state = { t: 0 };
  const tl = gsap.timeline({ paused: true });
  tl.to(state, { t: DUR, duration: DUR, ease: "none", onUpdate: () => render(state.t) }, 0);
  window.__timelines["world"] = tl;
  render(0);
}).catch((e) => { console.error("world build failed", e); throw e; });
"""

CONTINENTS = [
    [(-10, 36), (-9, 43), (-2, 48), (2, 51), (8, 54), (12, 56), (20, 60), (30, 60), (40, 66), (60, 68), (80, 73), (100, 77), (140, 72),
     (170, 66), (160, 58), (140, 50), (130, 40), (122, 30), (110, 20), (105, 10), (100, 2), (95, 15), (80, 8), (72, 20), (60, 25),
     (50, 30), (35, 32), (28, 36), (20, 38), (12, 38), (5, 43), (-5, 36)],
    [(-17, 21), (-10, 30), (10, 37), (32, 31), (43, 12), (51, 11), (40, -10), (35, -25), (20, -35), (12, -18), (9, 0), (-8, 5), (-17, 14)],
    [(-165, 65), (-140, 70), (-100, 72), (-80, 70), (-65, 60), (-55, 50), (-70, 43), (-80, 30), (-97, 26), (-105, 20), (-90, 15),
     (-80, 8), (-95, 16), (-110, 24), (-118, 33), (-125, 48), (-140, 60)],
    [(-80, 8), (-60, 10), (-35, -6), (-40, -22), (-55, -35), (-68, -55), (-75, -40), (-71, -18), (-81, -5)],
    [(114, -22), (130, -12), (142, -11), (153, -28), (145, -38), (130, -32), (115, -34)],
]


def world_html():
    js = WORLD_JS.replace("__K__", json.dumps(K)).replace("__DUR__", str(TOTAL)).replace("__CONT__", json.dumps(CONTINENTS))
    return f"""<template>
  <style>
    #root {{ position:absolute; inset:0; background:#000; }}
    #w-canvas {{ position:absolute; left:0; top:0; width:{W}px; height:{H}px; }}
  </style>
  <div id="root" data-composition-id="world" data-width="{W}" data-height="{H}" data-duration="{fmt(TOTAL)}">
    <canvas id="w-canvas" width="{W}" height="{H}"></canvas>
  </div>
  <script>
{js}
  </script>
</template>
"""


# ------------------------------------------------------------------ Overlays: Titel, Countdown, Untertitel, Blitze, Endkarte

SERIF = "'EB Garamond', serif"
MONO_CAPS = "font-family:'Inter',sans-serif;font-weight:700;letter-spacing:0.22em;text-transform:uppercase"


def overlay_html():
    stop, rest, end = K["stop"], K["restart"], K["end"]
    title_off = B["platz"]["start"] - 0.2
    # Countdown: drei Phasen wie in der Referenz
    cd = f"""
    <div id="cd" style="position:absolute;left:64px;top:860px;color:#fff;text-shadow:0 2px 12px rgba(0,0,0,0.6)">
      <div style="position:relative;height:40px;font-size:28px;{MONO_CAPS}">
        <span id="cd-l1" style="position:absolute;left:0;white-space:nowrap">Erde stoppt in</span>
        <span id="cd-l2" style="position:absolute;left:0;white-space:nowrap;opacity:0">Erde dreht sich wieder in</span>
        <span id="cd-l3" style="position:absolute;left:0;white-space:nowrap;opacity:0">Erde</span></div>
      <div style="font-family:{SERIF};font-size:96px;line-height:1.0;font-variant-numeric:tabular-nums"><span id="cd-t">0:00.000</span></div>
      <div style="position:relative;height:40px;font-size:28px;{MONO_CAPS};color:#C9D3E6">
        <span id="cd-s1" style="position:absolute;left:0;white-space:nowrap">München dreht sich mit 1.117 km/h</span>
        <span id="cd-s2" style="position:absolute;left:0;white-space:nowrap;opacity:0">Zeit verlangsamt {str(SLOW).replace('.', ',')}×</span>
        <span id="cd-s3" style="position:absolute;left:0;white-space:nowrap;opacity:0">Alles wird zurückgerissen</span></div>
    </div>"""
    title = f"""
    <div id="ttl" style="position:absolute;left:60px;right:60px;top:330px;text-align:center;color:#fff;font-family:{SERIF};
      font-size:84px;line-height:1.08;text-shadow:0 3px 18px rgba(0,0,0,0.55)">
      <svg width="150" height="150" viewBox="-75 -75 150 150" style="display:block;margin:0 auto 24px">
        <circle r="46" fill="#1E3D7A" stroke="#BFD3FF" stroke-width="4"/>
        <path d="M -30 -20 Q -10 -34 8 -22 Q 20 -10 4 0 Q -14 10 -6 24 M 14 14 Q 30 8 34 -8" stroke="#8FB8FF" stroke-width="5" fill="none"/>
        <path id="ttl-arc" d="M -62 10 A 64 64 0 0 0 52 38" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round"/>
        <path d="M 44 30 L 56 40 L 40 46" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      Was wäre, wenn die <span style="color:#8FB8FF">Erde</span><br>5 Sekunden lang stoppt?</div>"""
    flashes = """
    <div id="fl1" style="position:absolute;inset:0;background:#fff;opacity:0"></div>
    <div id="dip" style="position:absolute;inset:0;background:#000;opacity:0"></div>"""
    card = f"""
    <div id="card" style="position:absolute;inset:0;background:#141414;opacity:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center">
      <div style="font-family:{SERIF};font-size:80px;line-height:1.1;color:#fff">Was wäre, wenn die <span style="color:#8FB8FF">Erde</span><br>5 Sekunden lang stoppt?</div>
      <div style="margin-top:44px;font-size:28px;{MONO_CAPS};color:#8A8F99;line-height:1.7">München dreht sich mit 1.117 km/h<br>in 5 Sekunden: 1,5 km nach Osten</div>
    </div>"""
    js = f"""
    tl.fromTo("#ttl", {{opacity:1}}, {{opacity:0, filter:"blur(8px)", duration:0.4, ease:"power2.in"}}, {title_off});
    tl.fromTo("#ttl-arc", {{rotation:0}}, {{rotation:-25, duration:0.8, yoyo:true, repeat:{int(title_off / 0.8)}, ease:"sine.inOut", svgOrigin:"0 0"}}, 0);
    (function(){{ const el=document.getElementById("cd-t"); const o={{t:0}};
      const f=(x)=>{{ x=Math.max(0,x); const s=Math.floor(x), ms=Math.floor((x-s)*1000); return "0:"+String(s).padStart(2,"0")+"."+String(ms).padStart(3,"0"); }};
      tl.fromTo(o,{{t:0}},{{t:{TOTAL},duration:{TOTAL},ease:"none",onUpdate:()=>{{
        const t=o.t;
        if (t < {stop}) el.textContent = f({stop} - t + 0.0);
        else if (t < {rest}) el.textContent = f(5 * ({rest} - t) / ({rest} - {stop}));
        else el.textContent = "dreht sich wieder";
        el.style.fontSize = t < {rest} ? "96px" : "64px";
      }}}},0); }})();
    tl.set(["#cd-l1","#cd-s1"], {{opacity:0}}, {stop});
    tl.set(["#cd-l2","#cd-s2"], {{opacity:1}}, {stop});
    tl.set(["#cd-l2","#cd-s2"], {{opacity:0}}, {rest});
    tl.set(["#cd-l3","#cd-s3"], {{opacity:1}}, {rest});
    tl.fromTo("#cd", {{opacity:0}}, {{opacity:1, duration:0.4}}, 0.3);
    tl.to("#cd", {{opacity:0, duration:0.3}}, {end - 0.3});
    tl.fromTo("#fl1", {{opacity:0}}, {{opacity:1, duration:0.08, ease:"power2.in"}}, {stop - 0.08});
    tl.to("#fl1", {{opacity:0, duration:0.7, ease:"power2.out"}}, {stop + 0.12});
    tl.fromTo("#dip", {{opacity:0}}, {{opacity:1, duration:0.35, ease:"power2.in"}}, {K['globe'] - 0.35});
    tl.to("#dip", {{opacity:0, duration:0.45, ease:"power2.out"}}, {K['globe']});
    tl.to("#fl1", {{opacity:1, duration:0.08, ease:"power2.in"}}, {rest - 0.08});
    tl.to("#fl1", {{opacity:0, duration:0.6, ease:"power2.out"}}, {rest + 0.1});
    tl.to("#dip", {{opacity:1, duration:0.3, ease:"power2.in"}}, {K['back'] - 0.3});
    tl.to("#dip", {{opacity:0, duration:0.35, ease:"power2.out"}}, {K['back']});
    tl.fromTo("#card", {{opacity:0}}, {{opacity:1, duration:0.6, ease:"power2.inOut"}}, {end});
"""
    return f"""<template>
  <style>#root {{ position:absolute; inset:0; }}</style>
  <div id="root" data-composition-id="overlay" data-width="{W}" data-height="{H}" data-layout-allow-overlap>
    {title}{cd}{flashes}{card}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{js}
    window.__timelines["overlay"] = tl;
  </script>
</template>
"""


def captions_html():
    lines = [l for b in T["beats"] if b["id"] != "hook" for l in b["lines"]]
    groups, js = [], []
    for i, l in enumerate(lines):
        st = l["start"] - 0.1
        nxt = lines[i + 1]["start"] - 0.1 if i + 1 < len(lines) else END_CARD
        en = min(nxt, l["end"] + 1.2, END_CARD)
        gid = f"sc{i}"
        groups.append(f'<div id="{gid}" class="clip line" data-start="{fmt(st)}" data-duration="{fmt(en - st)}" data-track-index="1">'
                      f'<span>{plain(l["show"])}</span></div>')
        js.append(f'    tl.fromTo("#{gid} span", {{opacity:0, filter:"blur(6px)"}}, {{opacity:1, filter:"blur(0px)", duration:0.25, ease:"power2.out"}}, {fmt(st)});')
        js.append(f'    tl.to("#{gid} span", {{opacity:0, duration:0.15, ease:"power2.in"}}, {fmt(en - 0.16)});')
    return f"""<template>
  <style>
    #root {{ position:absolute; inset:0; }}
    .line {{ position:absolute; left:70px; right:70px; top:1180px; text-align:center; }}
    .line span {{ display:inline-block; font-family:{SERIF}; font-style:italic; font-size:58px; line-height:1.15; color:#fff;
      text-shadow:0 2px 16px rgba(0,0,0,0.85), 0 0 3px rgba(0,0,0,0.9); }}
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


SFX = [
    (K["stop"] - 2.6, "riser.mp3", 0.0),   # Platzhalter, siehe unten (riser via media-start)
    (K["stop"] - 0.05, "impact-bass-1.mp3", 0.7),
    (K["stop"] + 0.05, "glitch-2.mp3", 0.25),
    (K["turn"] - 0.3, "whoosh-cinematic.mp3", 0.4),
    (K["roofs"] - 0.2, "whoosh.mp3", 0.4),
    (K["space"], "whoosh-cinematic.mp3", 0.35),
    (K["globe"] - 0.1, "sparkle.mp3", 0.35),
    (K["restart"] - 0.05, "impact-bass-2.mp3", 0.7),
    (K["yank"] - 0.1, "whoosh-short.mp3", 0.5),
    (K["end"], "whoosh.mp3", 0.3),
]
SFX = [s for s in SFX if s[2] > 0]


def write():
    comp = HERE / "compositions"
    comp.mkdir(exist_ok=True)
    (comp / "world.html").write_text(world_html())
    (comp / "overlay.html").write_text(overlay_html())
    (comp / "captions.html").write_text(captions_html())
    (HERE / "assets" / "sfx").mkdir(parents=True, exist_ok=True)
    audio = ['      <audio id="voice" class="clip" src="assets/voice.wav" data-start="0" data-track-index="10" data-volume="1"></audio>']
    for j, (t, f, vol) in enumerate(SFX):
        (HERE / "assets" / "sfx" / f).write_bytes((SFX_ROOT / f).read_bytes())
        d = min(audio_len(SFX_ROOT / f), TOTAL - t)
        audio.append(f'      <audio id="sfx{j}" class="clip" src="assets/sfx/{f}" data-start="{fmt(t)}" data-duration="{fmt(d)}" '
                     f'data-track-index="{11 + j}" data-volume="{vol}"></audio>')
    hosts = ""
    for z, (cid, kind) in enumerate((("world", "graphics"), ("overlay", "graphics"), ("captions", "captions"))):
        hosts += (f'      <div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" data-start="0" '
                  f'data-duration="{fmt(TOTAL)}" data-track-index="{z + 1}" data-track-kind="{kind}" data-width="{W}" data-height="{H}" '
                  f'style="z-index:{z + 1}"></div>\n')
    (HERE / "index.html").write_text(f"""<!doctype html>
<html lang="de" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <title>Was wäre, wenn die Erde 5 Sekunden lang stoppt?</title>
    <script src="assets/gsap.min.js"></script>
    <style>
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:#000; }}
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
    print("K", K, "| SLOW", SLOW, "| total", TOTAL)


if __name__ == "__main__":
    write()
