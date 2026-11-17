---
name: tiktok-community-serie
description: Baut deutsche TikTok-Serienfolgen im Format „Die Community entscheidet“ (Vorbild @kevin.und.karla) – 2D-Cartoon, Countdown-Ziel („Noch 30 Tage …“), HUD mit Folge/Tage/Stat-Balken/Kasse, Abstimmungsergebnis der letzten Folge, A/B-Cliffhanger für die Kommentare. Nutzen, wenn der Creator eine neue Folge, eine neue Serie, ein Serienthema, das Abstimmungsergebnis einer Folge oder Änderungen an dieser Serie will. Nicht für Einzelvideos im Erklär-/3D-Stil (dafür tiktok-sim-video).
---

# TikTok-Community-Serie („Ihr entscheidet“)

Interaktive Cartoon-Serie: Eine Figur hat ein Ziel mit Frist (Countdown), jede Folge = ein Tag,
am Ende stimmt die Community per Kommentar über A oder B ab, die nächste Folge zeigt das Ergebnis
und die Konsequenz. Vorbild: 9 Folgen von @kevin.und.karla (Glow-up bis zum Date) – **das Thema Glow-up
wird bewusst NICHT übernommen**, nur das Format.

Vor jeder Arbeit lesen:
1. `references/format-analyse.md` – was die Referenzen genau machen (Aufbau, HUD, Look, Sprechertext, Timing).
2. `references/themen.md` – Themen-Bank und die aktive Serie (Serienbibel).
3. `references/folge-vorlage.md` – Folgen-Bauplan, `script.json`-Beispiel, Checkliste.

Referenzvideos: `references/2026-11-serie/kevin-folge-NN.mp4` (+ `-uebersicht.jpg` Kontaktbögen, alle 2,5 s ein Bild).

## Feste Regeln

- **Sprache Deutsch**, Erzähler in 3. Person Präsens, locker, schnell, leicht fies-humorvoll, nie verletzend
  (keine Witze über Behinderung, Herkunft, Religion; Figur ist liebenswerter Loser, kein Opfer).
- **Format** 1080×1920, 30 fps, 60–90 s (Referenzen: 63–89 s, ~2,4 Wörter/s ≈ 150–200 Wörter).
- **Eigene Figuren, eigene Welt, eigener Seriename.** Nichts von Kevin/Karla kopieren (Namen, Figuren-Design,
  Zahnspange-Gags, Hausmeister Brömmel, Logo). Nur Struktur und Mechanik übernehmen.
- **Kein TikTok-Logo/Outro/Wasserzeichen** und kein „AI-generated“-Label einbauen – fügt TikTok selbst hinzu.
- **Abstimmungen ehrlich:** Ergebnis-Prozente in Folge N+1 kommen vom Creator (echte Kommentare zählen lassen).
  Nie Prozente erfinden. Fehlen sie, den Creator fragen; bis dahin Platzhalter `??%` im Skript.
- **Kontinuität ist Pflicht:** Jede Folge liest und schreibt `serien/<slug>/state.json` (Folge, Tage, Stats,
  Kasse, offene Abstimmung, Kanon-Fakten). Zahlen im HUD müssen mit der letzten Folge übereinstimmen.

## Dramaturgie jeder Folge (Kurzform – Details in folge-vorlage.md)

| Zeit | Beat | Inhalt |
|---|---|---|
| 0–4 s | **Hook/Recap** | „Noch 27 Tage bis …“ + Ziel-Karte (Polaroid/Kalender) + Figur im aktuellen Zustand |
| 4–12 s | **Ergebnis** | „Letzte Folge habt ihr entschieden“ – zwei Balken laufen hoch, Gewinner bekommt „GEWONNEN!“-Badge |
| 12–55 s | **Tag** | 3–5 Mini-Szenen (Ort wechselt alle 4–8 s): Entscheidung umsetzen → Panne/Gag → kleiner Erfolg (Stat/Kasse poppt hoch) |
| ~45–60 s | **Wendung** | Nachricht/Anruf/Fund, der ein Dilemma erzeugt (Chat-UI am Handy ist Standard) |
| letzte 10–15 s | **Cliffhanger-Abstimmung** | „Was soll X tun?“ + Karte A (blau) / B (orange) + Pill „Schreib A oder B in die Kommentare!“; Sprecher: „A … oder B … Dein Kommentar zählt.“ |

Gute Dilemmata haben einen **Preis auf beiden Seiten** (Geld vs. Stat, ehrlich vs. bequem, kurz- vs. langfristig)
und beide Optionen sind für die Folge danach erzählbar. Ab und zu eine „Moral“-Wahl (Fundgeld zurückgeben?).

## Arbeitsablauf

Ordner: Serie `serien/<serien-slug>/` (Bibel, `state.json`, Figuren-SVGs), Folge `videos/<nr>-<serien-slug>-f<NN>/`.

1. **State lesen**, Abstimmungsergebnis vom Creator holen, neue Werte (Tage −1, Stats) festlegen.
2. **Skript** `script.json` (gleiches Format wie die übrigen Projekte, siehe `tools/tts.py`):
   **jede `line` = 2–4 Wörter** (so erscheinen die Untertitel), Schlüsselwort mit `{y:…}` (gelb), selten `{r:…}`/`{g:…}`.
   Beat-IDs: `recap`, `ergebnis`, `szene1…n`, `wendung`, `abstimmung`.
3. **Stimme über das ElevenLabs-MCP** (`creative_generate_speech`, Modell `eleven_v4`, Stimme
   **„Timon – Energetic and Clear“, voice_id `0i5UT3fATBWphA0jBZug`** – feste Seriensstimme, nicht wechseln).
   Prompt = Sprechertext aller Beats (Zahlen ausgeschrieben, Absatz pro Beat), 2 Takes, den flüssigeren nehmen.
   **Immer mit Betonung (Wunsch des Creators, sonst klingt es monoton):** Emotions-Tags von eleven_v4 vor die Sätze setzen –
   `[dramatically]` Countdown/Cliffhanger, `[excited]` Ergebnis/Geld/Abstimmung, `[sad]`/`[sighs]` Pannen, `[mischievously]`
   Gags, `[surprised]` Überraschungen, `[shouting]` Schock-Zahlen, `[warmly]` Community-Momente; 1–2 Schlüsselwörter pro Beat
   in VERSALIEN, `…` für Spannungspausen. Tags nur im Prompt, nicht in script.json.
   Nach `align.py` die Silbenrate jeder Zeile prüfen (> 8 Silben/s = falsch zugeordnet) und solche Zeilen in
   `assets/timings.json` anhand der Pausen (`ffmpeg silencedetect`) von Hand korrigieren.
   MP3 per `curl` nach `assets/source/` laden → `python3 tools/align.py videos/<projekt> assets/source/take1.mp3`.
   **Musik:** `creative_generate_in_flow` (node_type `music`, Modell `eleven_music_v2_5`, 1 Take, „instrumental,
   playful quirky cartoon, pizzicato, ukulele, glockenspiel, 115 BPM, loopable“) → auf Videolänge kürzen,
   Fade-out, `loudnorm` −16 → `assets/music.mp3` (build.py mischt sie mit 0.16 unter die Stimme).
4. **Szenen** in `build.py` mit `tools/seriekit.py` (`scene`, `hud_html`, `captions_html`, `vote_cards`,
   `chat_phone`, `strahlen`, Helfer `pop_in/pop_out/shake/hop/breathe/punch/walk_in/lautmalerei`, `write_project`).
   Figuren: `serien/<slug>/figuren.py`, Orte: `serien/<slug>/orte.py`. **Vorlage: `videos/16-kiosk-kalle-f01/build.py`**
   (Folge kopieren, Szenenfunktionen anpassen). `scene()` präfixt alle IDs automatisch mit der Szenen-ID.
   Alle Zeiten über die Timings (`w(beat, zeile, wort)`), nie hart codieren.
   - Figuren als **wiederverwendbare Flat-SVG-Funktionen** in `serien/<slug>/figuren.py`
     (Posen: steht, jubelt, erschrocken, Nahaufnahme-Gesicht; Ausdrücke als austauschbare Mund/Augen-Gruppen).
     Einmal bauen, in jeder Folge wiederverwenden – Wiedererkennung ist das Kapital der Serie.
   - HUD als eigene Sub-Composition über die ganze Folge (Positionen/Farben in format-analyse.md).
   - Captions: `captions_html(timings, total, top=1380, upper=True, size=78)`.
   - Lautmalerei-Pops („ZACK!“, „PIEP!“, „RATSCH!“) als schräge gelbe Outline-Schrift mit Pop-in + SFX.
5. `python3 build.py` → HyperFrames `check --json` → Fehler beheben → `snapshot` an jedem Beat ansehen
   (HUD verdeckt nichts? Untertitel lesbar? Figur im Bild?).
6. `render -o renders/<slug>-f<NN>.mp4` (im Hintergrund), Lautheit −16…−14 LUFS.
7. **State aktualisieren** (neue Stats, offene Abstimmung A/B mit Text), committen, MP4 an Creator schicken,
   dazu: Caption-Vorschlag + 3–5 Hashtags + angepinnter Kommentar („A = … / B = … – was soll Kalle tun?“).

## Community einbinden

- Zuschauer, die in den Kommentaren mitmachen wollen, werden zu Figuren (Folge 2: **Maxim** aus den Kommentaren
  wird ehrenamtlicher Helfer). Nur Vornamen, nur wenn der Creator das will; am Anfang der Folge ankündigen
  („heute kriegt er Hilfe – von Maxim aus den Kommentaren!“) und in der Szene den echten Kommentar zitieren.
- Meistgelikte Kommentare als Kommentar-Karten einblenden (ohne Nutzernamen, außer der Creator wünscht es).

## Bekannte Grenzen

- HyperFrames-Plugin, Piper, Soundeffekte, GSAP-Vendor: siehe Abschnitt „Bekannte Grenzen“ in
  `.claude/skills/tiktok-sim-video/SKILL.md` (gleiche Umgebung, gleiche Workarounds).
- Keine Spracherkennung im Netz erreichbar → Untertitel der Referenzen wurden aus den Bildern gelesen.
- Musik: in der TikTok-App drunterlegen (leise, verspielter Trend-Sound).
