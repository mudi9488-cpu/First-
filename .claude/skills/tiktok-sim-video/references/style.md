# Style-Guide: Erklär-/Simulationsvideos (TikTok)

Abgeleitet aus 3 Referenzvideos (alle 576×1024, 9:16, 30 fps, 77–112 s, mit Voiceover + Musik).

| Ref | Thema | Stil |
|---|---|---|
| A | „Rennen vs. Gehen – wer wird weniger nass?“ | 2D-Datensimulation, Live-Zähler |
| B | „Alle Frauen der Welt sind gestorben – bis auf eine“ (Greta) | 2D-Flat-Illustration, Story in Kapiteln |
| C | „What if electrons disappeared for 5 seconds?“ | 3D-Render, Wireframe, Countdown |

## Gemeinsamer Aufbau (Dramaturgie)

1. **Hook (0–3 s):** Frage oder Schock-Prämisse als großer Titel direkt im ersten Frame.
   - A: „RENNEN vs GEHEN – WER WIRD WENIGER NASS?“
   - B: „Du wachst eines Morgens auf …“
   - C: „What if electrons disappeared for 5 seconds?“
2. **Setup:** Regeln/Parameter werden eingeblendet (100 m, 5 km/h vs. 15 km/h; „Tag 1 · 07:12“; „Central Park, New York“).
3. **Eskalation in Stufen:** Kapitel/Phasen mit eigenem Label („Regel 1 · Handy“, „Regel 2 · Unsichtbar“; Zeitlupen-Countdown).
4. **Twist:** Erwartung wird gebrochen („Rennen ist besser?“ → „31 mL > 14 mL – Rennen schlechter?“ → Gleichstand → Geher wird doch nasser).
5. **Auflösung / Fazit:** Endstand-Karte, „Unterm Strich“-Vergleich, Prozentzahl.
6. **Cliffhanger bzw. Loop:** Letzter Satz endet offen („Drei leise Schläge.“) oder der Anfangstitel kommt zurück (C), damit das Video loopt.
7. *(Das TikTok-Logo mit Suchleiste am Ende und das Wasserzeichen in den Referenzen fügt TikTok beim Download selbst hinzu – nicht nachbauen.)*

## Visuelle Sprache

### Farben
- **Hintergrund:** sehr dunkles Navy/Blauschwarz (`#0E1621` – `#141B2D`), leichte Vignette, dezentes Raster/Sterne.
- **Akzentpaar für Vergleiche:** Koralle/Rot `#F2604F` vs. Türkis `#3CC6BE` (A).
- **Highlight/Wichtig:** Gold/Gelb `#F5B83D` (Titel „VON VORNE“, „REGEL 1“, Gleichstand-Badge).
- **Gefahr/Alarm:** Neon-Pink/Rot `#FF3B6B` (B: Eilmeldung, Standort gefunden, Puls).
- **Positiv/Ruhe:** Grün `#3DDC84` (Schild-Icon, ruhiger Puls).
- **Text neutral:** Weiß, Sekundärtext Grau `#8A94A6`.

### Typografie
- **Headlines:** fette, geometrische Sans (z. B. *Inter Black / Montserrat ExtraBold*), Versalien.
- **Untertitel (Captions):** Wort-für-Wort bzw. Phrase-für-Phrase synchron zum Voiceover, mittig unteres Drittel.
  - A: gemischte Schreibung, Schlüsselwort in Akzentfarbe („Der **Läufer** hat schon“).
  - B: Versalien, dicker schwarzer Rand/Schatten, bereits gesprochene Wörter weiß, kommende grau, Schlüsselwort farbig (gelb/pink/grün), leichter Glow.
  - C: Serif kursiv, klein und elegant („You can see the stars through your hands.“).
- **HUD-/Daten-Labels:** Monospace, gesperrt, klein (z. B. *JetBrains Mono / IBM Plex Mono*): „TAG 1 · 07:12“, „FRAUEN AUF DER ERDE“, „ELECTRONS RETURN IN“.

### HUD-Elemente (Markenzeichen aller drei Videos)
- **Oben-Mitte:** Kapitel-/Zeitlabel in abgerundetem Rahmen (Gold-Outline in B, große Stoppuhr `0:24` in A).
- **Zähler, die live hochlaufen:** Wasser in mL, Weltbevölkerung `3.038.956.585` → `1`, Countdown `0:04.779`.
- **Status-Pills:** „IM ZIEL“, „TROCKEN“, „PAUSE“, „NOCH NICHT IM ZIEL“, „33 m · 1/3“.
- **Checkliste links oben** (B): erledigte Regeln sammeln sich als kleine Mono-Tags („1. HANDY ✓“).
- **Info-Karten:** dunkle Karten mit dünnem farbigen Rand (Endstand, Personalausweis „NAME: GRETA · ALTER: 23“, Eilmeldung).
- **Vergleichsbalken** am Ende (A: „VON VORNE 25 = 25“, „VON OBEN 18 vs 6“).

### Illustration & Animation
- **Flat-Vektor**, keine Texturen, weiche Formen; Figuren minimalistisch (A: Strichmännchen mit Kreis-Kopf; B: einfache Cartoon-Figur mit großem Kopf).
- **Kamera:** sanfte Zooms auf das Wichtige (Ziel-Linie, Gesicht), Push-ins bei Spannung, Cut auf Schwarz für Dramatik.
- **Szenenwechsel alle 2–4 s** – nie ein statisches Bild länger als ~4 s.
- **Partikel:** Regen, Sterne, Glow um Highlights.
- **Pausen-Momente:** Bild friert ein („PAUSE“), Erklärung, dann weiter.
- C ist 3D (AI-generiert): realistische Szene → Wechsel in weißes Wireframe/Hologramm auf Schwarz, Licht-Explosion, Erde von außen.

## Ton
- Ruhiger, eindringlicher Erzähler (2. Person in B: „Du wachst auf …“), kurze Sätze.
- Hintergrundmusik: atmosphärisch/spannungsaufbauend, Sound-Effekte bei Ereignissen (Tick, Whoosh, Herzschlag, Klopfen).

## Technische Specs für die Produktion
- 1080×1920 (9:16), 30 fps, H.264 + AAC, 60–110 s.
- Safe-Zones: oben ~8 %, unten ~20 % und rechts ~15 % frei halten (TikTok-UI), Captions bei ~65–70 % Höhe.
