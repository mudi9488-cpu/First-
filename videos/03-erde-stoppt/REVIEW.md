# Review – „Was wäre, wenn die Erde 5 Sekunden lang stoppt?“

- 55,0 s, 1080×1920, 30 fps, ElevenLabs „Helmut“ (tools/align.py, 20/25 Pausen; Pausen mitten in Sätzen sind
  dramatische Pausen des Sprechers), −17 LUFS (gemessen, nicht gehört).
- Stil wie Referenz C: eine durchgehende Three.js-Welt (compositions/world.html) – Low-Poly-Marienplatz → weißer Blitz
  → Drahtgitter auf Schwarz mit Sternen → Flug durch das Tal nach Osten → Orbit/Globus → Rückkehr → Endkarte.
  Countdown mit Millisekunden, Serifen-Untertitel (EB Garamond kursiv).
- Blitz exakt auf dem „t“ von „stoppt“ (Zeilenende − 0,1 s, per Hüllkurve geprüft).
- Fakten: München ~48° N → 1.117 km/h = 310 m/s; Schall 343 m/s; 5 s × 310 m/s ≈ 1,55 km; stärkste Hurrikan-Böen
  ~345 km/h → ~3×. Ozeane: qualitativ.
- Render ohne GPU (SwiftShader): ca. 5 min für 55 s.
