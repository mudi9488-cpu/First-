# Style-Guide: Blocky-3D-Storytime („In this town …“) – Nische seit Nov. 2026

Abgeleitet aus 3 Referenzen des Creators (alle 576×1024, 9:16, 30 fps, 129–182 s, Voiceover + leise Musik,
−17 bis −20 LUFS, ~65–70 Schnitte pro Video = **ein Schnitt alle 2–2,5 s**).

| Ref | Kanal-Stil | Thema / Hook | Welt |
|---|---|---|---|
| A | dunkel, Horror | „In this town, everyone has to be in their house before Halloween night begins …“ | Vorstadt-Häuser, Nacht, orangener Himmel, langes gelbes Wesen |
| B | knallbunt, Comedy | „In this town, touching the ground costs $10.“ | Pastell-Stadt, City Hall, Neon-Preisschilder |
| C | Neon, Drama | „In this town, everyone must choose between two pills on their 16th birthday.“ | Arm-Viertel vs. schwebende Luxus-Inseln, Bühne mit Gold-/Schwarz-Pille |

## Dramaturgie (alle drei gleich)

1. **Hook, Satz 1 (0–4 s):** „In dieser Stadt …“ + absurde Regel. Bild: Totale der Stadt/Straße aus der Luft, dann sofort Schnitt auf die Regel in Aktion.
2. **Regel erklären (4–20 s):** Wer, wann, was passiert bei Verstoß („Sobald die Uhr 18 Uhr schlägt …“, „Jeder Schritt: −10 $“, „Gold = reich, Schwarz = ?“). Jede Konsequenz bekommt ein eigenes Bild.
3. **Ich-Erzähler stellt sich vor:** „Mein Name ist Lucas, und morgen werde ich 16.“ – Nahaufnahme Gesicht, Zimmer/Bett.
4. **Eskalation:** Alltag unter der Regel → Persönliche Betroffenheit → Geheimnis/Gefahr (Wesen draußen, Regierung kassiert ab, Brief „NIMM NICHT GOLD. – RUBY“).
5. **Wendepunkt:** jemand bricht die Regel / Erzähler entdeckt den Trick (roter Knopf „GROUND TAX DEAKTIVIEREN“).
6. **Ende = Cliffhanger** (A: jemand steht vor der Tür; C: Countdown „00:02 – TRIFF DEINE WAHL“, Schnitt) → Teil 2. Kein Fazit.

Sprechtempo schnell und durchgehend (~2,8–3 Wörter/s), keine Pausen, ruhige Erzählerstimme, Präteritum + Ich-Perspektive.

## Visuelle Sprache

- **3D, Blockfiguren im „Klötzchen-Avatar“-Stil:** Würfelkopf, quaderförmiger Torso, Arme/Beine als Quader, Gesicht als
  aufgemalte 2D-Decals (große Augen, Brille, Augenbrauen, Mund wechselt je nach Emotion: Angst, Wut, Grinsen, Schock).
  Kleidung = farbige Texturen auf den Quadern (Trikot mit „8“, Hemd + Krawatte, Jacke). **Kein Roblox-Logo / keine Markennamen.**
- **Welt aus einfachen Low-Poly-Teilen:** Häuser, Türen mit Holzmaserung, Laminatboden, Möbel, Straßenlaternen, Bäume
  aus Kugel-Clustern, Polizeiauto, Hochhäuser im Hintergrund. Weiches Licht, Schatten, leichte Tiefenunschärfe.
- **Kamera:** fast jede Einstellung eine eigene Kamera – Totale von oben (Stadt), Nahaufnahme Gesicht (Reaktion),
  Detail (Tür, Uhr, Handy-Display, Knopf), Froschperspektive aufs Wesen. Langsame Dolly-/Push-ins, nie statisch.
  Harte Schnitte, gelegentlich Whip/Flash.
- **Lichtstimmung je Thema:** Horror = Nacht, orangener Himmel, Laternen, kühle Innenräume; Comedy = Mittag, blauer
  Himmel, Pastellfassaden; Drama = Lila/Gold-Neon, Spotlights, Konfetti bei Gewinn.
- **Text in der Welt (diegetisch) statt HUD:** Neon-Schilder „−$10“, Handy-Screens („NEUE STEUER: ATMEN – $1 PRO SEKUNDE“,
  „KONTOSTAND“), Countdown-Tafel „00:10“, Zettel in Handschrift, Schild „RESTRICTED“. Keine Datenkarten/Checklisten.

## Untertitel (wichtigstes Wiedererkennungsmerkmal)

- **Genau ein Wort**, exakt synchron, mittig, auf ca. **y ≈ 1300–1440 px** (bei 1080×1920; Referenz y≈690–730 von 1024).
- Kleinschreibung wie gesprochen, Zahlen als Ziffern („$10“, „16th“, „$10 million“).
- Variante A (Horror): Weiß, fett, runde Sans, weicher schwarzer Schatten, ~70 px.
- Variante B/C (bunt): **Neon-Gelb `#E8FF3A`**, extra fett (Cartoon-Font, z. B. *Lilita One / Luckiest Guy*),
  dicke schwarze Kontur + Schlagschatten, ~85 px; betonte Wörter größer („between“, „being“).
- Leichter Pop (Scale 0.85→1) bei jedem Wort, keine Karaoke-Farbe.

## Ton

Voiceover dominant, leise Hintergrundmusik (Horror: Spannungs-Drone; Comedy: lockerer Beat), Whoosh bei Schnitten,
Ka-ching/Kasse bei Geld, Herzschlag/Ticken bei Countdown. Musik kommt in der TikTok-App drunter.

## Umsetzung

**Vorlage: `videos/16-pirate-token/build.py`** (Pirate Token, Englisch, 2:25, 85 Einstellungen). Aufbau: eine Einstellung pro
Sprechzeile (`S`-Liste, harter Schnitt bei Zeilenstart), Sets weit auseinander in einer Szene (Stadt bei x=0, Halle x=200,
Zimmer x=−200, Token-Bühne z=400), `makeChar` (Klötzchen-Figur, Gesichts-Decals per Ausdruck), `pose` (walk/run/wave/up/
holdUp/reach/kick/…), Crowd-Modi, Canvas-Bildschirme (Billboard, Uhr, Handy, Countdown), Ein-Wort-Untertitel in Lilita One
(`tools/fonts/`). Nahaufnahmen: Kamera nie hinter einen aufgehenden Truhendeckel stellen.

### Ursprünglicher Plan

Three.js-Pipeline aus `videos/05-hochbeet/` wiederverwenden (prozedurale Canvas-Texturen, `SHOTS`-Kameraschnitte,
schwebende HTML-Labels). Neu dazu: Baukasten für Blockfiguren (Kopf/Torso/Arme/Beine, Gesichts-Decals per Canvas,
Posen + einfache Geh-/Wink-Animation), Gebäude-Kit (Haus, Laden, City Hall, Laterne, Baum, Auto) und Ein-Wort-Untertitel.

## Stimme + Musik über ElevenLabs (seit Video 17, `videos/17-red-light/`)

- Stimme: ElevenLabs-Stimme **„In This town“** (voice_id `zrH6TtgZnrCw5V6iLzqf`, Modell `eleven_v4`), ganzer Text in einem Durchgang
  (Absatz pro Beat), **immer nur eine Variante (`generations_count: 1`)** – Wunsch des Creators, spart Credits (~2.300 pro Video). Download braucht den Host `elevenlabsusercontent.com` (in der Umgebung „Mudi“ freigegeben).
- Wortgenaue Zeiten: Take als Asset-Knoten anlegen → `creative_transcribe_audio` (Scribe, 0 Credits) → `words.json` laden →
  `python3 tools/words_align.py <projekt> assets/source/voice-a.mp3 assets/source/words.json`.
- Schnitte: `SHOT_LINES` fasst kurze Zeilen zusammen, Ziel ~2 s pro Einstellung (Referenzen 2,0–2,7 s).
- Musik: `eleven_music_v2_5`, instrumental, 150 s; `build.py` legt sie auf −29 LUFS unter die Stimme (Referenzen: Musikteppich
  ca. −30 bis −34 dB), Fade-out am Ende.

## Zweite Referenz-Runde (Nov. 2026): 4 Videos, gleicher Kanal-Stil (hell, bunt, Neon-Gelb-Untertitel)

| Ref | Hook | Länge | Schnitt alle | Ende |
|---|---|---|---|---|
| D | „In this town, the higher you live, the richer you are“ (Holzhütte am Boden ↔ Milliardäre auf Wolkenkratzern, Leiter, Aufzug „FLOOR 200“, Scanner) | 2:04 | 2,2 s | – |
| E | „In this town, every living thing is the opposite size“ (Babys 50 ft groß, Ameisen so groß wie Elefanten, Opas so klein wie eine Kaffeetasse) | 2:15 | 1,4 s | Pointe: „Mom is having twins … we're gonna need a bigger house.“ |
| F | „In this town, you get paid for being embarrassed“ ($500 → $5,000 → $100,000) | 2:26 | 1,9 s | Mama zeigt Babyfotos im Stadion → Konto explodiert auf $100 Mio. |
| G | „In this town, everyone is a ninja – except me“ | 2:25 | 2,3 s | Held ohne Kräfte zerstört die Maschine → Moral: „real ninjas don't need magic“ |

Gemessen: −14 bis −18,5 LUFS, Musikteppich ca. −35 dB (leiser als Runde 1), Erzählstimme F0 ≈ 205–213 Hz (dieselbe junge Stimme
in allen vier → passt zu „In This town“), ca. 400–470 Wörter ≈ 3,2 Wörter/s.

**Dramaturgie Runde 2 (anders als Runde 1!): komplette Geschichte mit Auflösung + Pointe statt Cliffhanger**
1. Hook-Regel + **3 Beispiele mit steigender Zahl/Größe** („$500 … $5,000 … $100,000“, „ants the size of elephants“).
2. Weltbau-Montage (5–8 absurde Details, je 1 Bild): Ausnahmen, Alltag, Haustiere, Schule.
3. „My name is X, I'm 16, and I have one huge problem“ → der Held ist die **Ausnahme** (keine Kräfte, $0, wohnt ganz unten).
4. 2–3 gescheiterte Versuche (Komik), Zähler bleibt bei „$0“.
5. Großes Ereignis (Wettbewerb im Stadion vor 100.000 Leuten / Angriff auf das Dorf / Baby läuft Amok).
6. Wendung: die Schwäche wird zur Stärke (der Held ohne Kräfte ist als Einziger nicht betroffen; das Peinlichste macht ihn reich).
7. Triumph: Konfetti, Geldregen, Zähler explodiert, Menge jubelt; letzte Zeile = Pointe oder Moral, die den Anfang aufgreift.

**Visuell neu:** extreme Perspektiven (Froschperspektive Wolkenkratzer, Vogelperspektive), Maßstabs-Gags (Riesen-Baby, Mini-Opa),
große Menschenmengen (Stadion), Farbumschwung bei Gefahr (Ninja-Dorf: alles rot getönt, danach wieder pastell),
Effekte (Konfetti, Geldscheine, Funken, Kirschblüten, Explosion/Rauch), Kostüm-Requisiten (Hühnerkostüm, Badeente, Pylonen-Hut),
Zähler/Bildschirme in der Welt („$0“ → „$100,000,000“, „FLOOR 200“, „SCANNING…“, „GRAND PRIZE $10,000,000“).
Pro Beat ein neuer Ort (Straße, Schulflur mit Spinden, Stadion, Dorf, Wohnzimmer).

## Hintergrundmusik ab Video 21 (Wunsch des Creators: immer diese)

- Quelle: `tools/music/bg-source.mp3` (vom Creator, ohne Effekte). Vorbereitet mit
  `python3 tools/music_prep.py tools/music/bg-source.mp3 tools/music/bg-music.wav` → Stille vorne (3,7 s) weg,
  Pfeif-Stellen 6 dB leiser.
- Pro Projekt nach `assets/source/music-base.wav` kopieren; `build.py` loopt sie (`-stream_loop -1`) von vorne, falls kürzer
  als das Video, und legt sie auf −23 LUFS. Alte `music-ref.mp3` (mit eingebackenen Effekten) nicht mehr verwenden.

## Soundeffekte ab Video 22 (Feedback des Creators zu Video 21)

- **Whoosh/Rauschen bei Schnitten weglassen** – höchstens ganz selten und sehr leise (Volume ≤ 0.08). Video 21 hatte 25 Whooshes, das nervt.
- Alle übrigen Effekte deutlich leiser als bisher: etwa halbe Lautstärke (Sparkle/Chime/Pop/Klick ≤ 0.12, Bass-Impacts ≤ 0.2, Riser ≤ 0.12).
- Lieber wenige gezielte Effekte an Story-Höhepunkten (Schock, Brüllen, Fußstapfen) als ein Effekt pro Schnitt.
