---
name: tiktok-sim-video
description: Erstellt ein deutsches TikTok-Video (9:16) im Stil „Was wäre, wenn …“ / Simulation / Erklär-Story mit HyperFrames – dunkles Navy, HUD-Labels, Live-Zähler, Karaoke-Untertitel, deutscher Sprecher. Nutzen, sobald der Creator ein neues Video, Thema oder eine Änderung an einem bestehenden Video in dieser Nische will.
---

# TikTok-Simulationsvideos (immer auf Deutsch)

Dieser Skill baut Videos, die aussehen wie die drei Referenzen des Creators
(„Rennen vs. Gehen“, „Alle Frauen gestorben – bis auf Greta“, „Elektronen verschwinden“).
Der komplette Look ist in `references/style.md` beschrieben – **vor jedem Video lesen.**

## Feste Regeln

- **Sprache: immer Deutsch** – Sprechertext, Untertitel, HUD-Labels, Dateinamen der Szenen-IDs dürfen Deutsch sein.
- **Alles in Code mit HyperFrames** (Plugin `hyperframes@hyperframes`). Vor dem Bauen den Skill
  `hyperframes:hyperframes` laden und dessen Vertrag einhalten. CLI immer über den Plugin-Launcher:
  `node ~/.claude/plugins/cache/hyperframes/hyperframes/<version>/skills/hyperframes/scripts/plugin-cli.mjs <befehl>`
  (fehlt das Plugin: `claude plugin marketplace add heygen-com/hyperframes && claude plugin install hyperframes@hyperframes`).
- Format 1080×1920, 30 fps. Länge nach Wunsch (Standard 30–60 s).
- Der Referenz-Look (dunkles Navy, HUD-Labels, Mono-Labels, Pills, Glow sparsam) ist **gewollt** – die
  „BANNED by default“-Liste von HyperFrames gilt hier für diese Elemente nicht, weil die Referenzen sie nutzen.
- **Kein** TikTok-Logo/Outro und kein Wasserzeichen einbauen – das fügt TikTok beim Download selbst hinzu.
- Safe-Zones: nichts Lesbares über y=168 px, Untertitel bei y≈1150, unter y≈1330 nur Deko.

## Dramaturgie (jedes Video)

1. **Hook in Frame 0**: Frage/Prämisse als großer Titel (Grau-Zeile + Gold-Zeile + Rot-Zeile) plus ein Bild-Objekt.
2. **Setup** mit Kapitel-Label oben („TAG 1 · 07:00“, „REGEL 1 · HANDY“, „0:24“).
3. **Eskalation in Stufen** – pro Stufe ein eigenes Bild-Objekt (Globus, Abfahrtstafel, Skyline, Regal …)
   und eine Datenkarte mit Live-Zähler; Checkliste oben links sammelt die Stufen („✕ STROM“).
4. **Twist** (Erwartung kippt, Farbe wechselt z. B. Rot → Grün).
5. **Auflösung / Cliffhanger / Loop**: letzter Frame führt zurück zum ersten (Loop) oder endet offen.

Neuer Beat alle 2–4 s, Szenenwechsel mit Whoosh, jede Zahl/Pill mit Pop/Impact.

## Arbeitsablauf

Projektordner: `videos/<nr>-<slug>/` (vorhandenes Video `videos/01-niemand-arbeitet/` ist die Vorlage).

1. **Skript** `script.json` schreiben: Beats mit `id`, `label` (Kapitel-Label) und `lines`.
   Jede Zeile = eine Untertitel-Gruppe (2–5 Wörter). Schlüsselwörter markieren:
   `{y:gold}` `{r:rot}` `{g:grün}` `{b:blau}` `{t:türkis}`. Zahlen, die anders gesprochen werden:
   `"show": "{y:3,6 Milliarden}", "say": "Drei Komma sechs Milliarden"`.
   Faustregel: ~2,6 Wörter pro Sekunde → 30 s ≈ 75 Wörter.
2. **Stimme**: `python3 tools/tts.py videos/<projekt>` → `assets/voice.wav` + `assets/timings.json`
   (Piper, Stimme „thorsten-low“, wird beim ersten Lauf von GitHub geladen; braucht `pip install piper-tts`).
   Länge über `length_scale` in `script.json` steuern (1.0 normal, 0.9 schneller).
   **Eigene Aufnahme / ElevenLabs (bevorzugt):** Datei nach `assets/source/` kopieren und
   `python3 tools/align.py videos/<projekt> videos/<projekt>/assets/source/<datei>.mp3` ausführen.
   Das Tool ordnet die Pausen der Aufnahme den Satzzeichen im Skript zu (ohne Spracherkennung) und schreibt
   `voice.wav` + `timings.json`; die Ausgabe Zeile für Zeile auf Plausibilität prüfen (Silbenrate ~4 /s).
   Dem Creator dafür den Sprechertext geben: eine Zeile pro Beat, kurze Pause zwischen den Sätzen.
   Danach `build.py` – alle Szenen, Zähler, Soundeffekte und Untertitel folgen automatisch dem Sprechtempo.
3. **Szenen** in `build.py` schreiben (Vorlage kopieren). Baukasten `tools/simkit.py`:
   `scene_html`, `hud_card` (Datenkarte mit Zähler/Balken), `js_count` (Live-Zähler),
   `write_project` (erzeugt index.html, HUD-Label + Checkliste, Karaoke-Untertitel, Audio-Spuren).
   Alle Zeiten über `w(beat, zeile, wort)` aus den Timings – nie hart codieren.
   Bild-Objekte als Flat-SVG (keine Verläufe auf großen Flächen, keine Texturen), Figuren minimalistisch.
4. `python3 build.py`, dann `check --json` → alle Fehler beheben.
5. `snapshot --at <zeiten>` an jedem Beat ansehen (Überlappungen Karte/Objekt/Checkliste, Lesbarkeit).
6. `render -o renders/<slug>.mp4`, Lautheit prüfen (`ffmpeg … ebur128`, Ziel −16 bis −14 LUFS).
7. Committen und dem Creator das MP4 schicken.

## Aktuelle Nische (seit Okt. 2026): hilfreiche 3D-Bauanleitungen / Aufklärung

Die „Was wäre, wenn“-Videos liefen schlecht – der Creator will jetzt **Themen, die Menschen weiterhelfen oder aufklären**,
im Stil der Garten-Querschnitt-Referenz („Glückwunsch, du hast … gebaut“). Vorlage: `videos/05-hochbeet/`.

- **Look:** realistisch wirkende Three.js-Welt (sonniger Garten, Haus, Baum, Wolken, weiche Schatten,
  ACES-Tonemapping); alle Oberflächen als prozedurale Canvas-Texturen (Rasen, Holz, Rinde, Laub, Kompost, Erde).
  **Boden im Querschnitt**: Schnittkante zur Kamera mit Erdschichten und Steinen – das Markenzeichen.
- **Ablauf:** Schritt für Schritt bauen – jedes Teil fällt/wächst einzeln ins Bild, harte Kameraschnitte zwischen
  den Schritten (`SHOTS` mit Start, Position von→nach, Ziel, FOV). Kameras weit genug weg (Hochformat: ~4–6 m bei
  einem 2-m-Objekt), damit Objekt, Garten und Querschnitt gleichzeitig zu sehen sind.
- **Untertitel:** **ein Wort pro Untertitel**, groß, fett, schwarze Kontur, mittig im unteren Drittel (y≈1290);
  `{y:}`-Wörter gelb, `{r:}` rot, `{g:}` grün.
- **Schwebende 3D-Beschriftungen** (`LABELS`): HTML, jeden Frame auf 3D-Punkte projiziert („ÄSTE · 30 CM“,
  „WÜHLMAUS“, „NIE UNTEN! ✕“), Pop-in. Schicht-Beschriftungen direkt auf die Schicht im Querschnitt setzen.
- **Dramaturgie:** Hook mit häufigem Fehler („Die meisten … Großer Fehler.“) → richtiger Aufbau Schritt für Schritt
  mit Zahlen → Tipps → „Glückwunsch, du hast … gebaut“.
- **Fakten:** nur gesichertes Wissen, Zahlen als gängige Richtwerte formulieren.
- Render ohne GPU ist langsam (~10–15 min für 60 s): mit `run_in_background` rendern.

## Bekannte Grenzen der Umgebung

- Die Microsoft/Edge-Stimmen und Hugging-Face-Modelle sind im Netzwerk gesperrt → Piper „thorsten-low“
  (Qualität „low“) nur als Platzhalter. Standard: der Creator liefert eine ElevenLabs-Datei
  (bisher genutzt: Stimme „Helmut – Distinctive and Authentic“), die mit `tools/align.py` eingebaut wird.
- Keine Musik-Quelle ohne HeyGen-Login → Video wird mit Stimme + Soundeffekten geliefert; Musik/Trend-Sound
  in der TikTok-App drunterlegen (leise, ~10–15 %).
- GSAP liegt lokal in `tools/vendor/` (CDN gesperrt); `write_project` kopiert es nach `assets/`.
- Soundeffekte: gebündelte HyperFrames-SFX (`skills/media-use/audio/assets/sfx/`).
