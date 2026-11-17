# Serienbibel: Kiosk-Kalle – 30 Tage bis zur Räumung

**Logline:** Zocker Kalle erbt Omas Pleite-Kiosk. 30 Tage, 3.000 € Mietschulden, ein gieriger Vermieter –
und die Community entscheidet jeden Tag, wie er den Laden rettet.

## Ziel & Spielregeln

- Frist: 30 Tage (Folge 1 = „Noch 30 Tage“, Folge N = „Noch 31−N Tage“).
- Ziel: 3.000 € in der KASSE bis Tag 0. Schafft er es nicht → Räumung (offenes Ende, Community kann retten).
- Stat **KUNDEN ★** (0,0–5,0): steigt durch guten Service/Angebot, fällt durch Pannen. Mehr Sterne = mehr Tagesumsatz.
- Kassenlogik grob plausibel halten: Tagesumsatz am Anfang 20–60 €, später bis ~250 €. Investitionen
  (Kaffeemaschine, Schild, Kühlschrank) kosten sichtbar Geld und zahlen sich später aus.
- Jede Folge: höchstens eine große Zahlenänderung pro Stat + ein Kassen-Effekt, damit der HUD lesbar bleibt.
- Neues HUD-Element = Ereignis (z. B. ab Folge 5 „🧾 SCHULDEN BEI DENNIS“, wenn Kalle sich Geld leiht).

## Figuren

| Figur | Rolle | Look (Flat-SVG) | Running Gag |
|---|---|---|---|
| **Kalle** (24) | Held, Underdog | großer Kopf, wuschelige orange-rote Haare, Gaming-Cap rückwärts, grüner Hoodie mit Ketchupfleck, Jogginghose, weiße Sneaker | Kommentiert alles wie ein Gamer („Quest angenommen“, „Lag!“), denkt bei Problemen an Speedrun-Taktiken |
| **Oma Erika** | ✝ Gründerin, nur als gerahmtes Foto an der Wand + Notizzettel | Dutt, Brille, Strickjacke | Ihr Foto „schaut“ je nach Situation streng/stolz (Augen ändern sich) |
| **Herr Geier** | Vermieter, Bösewicht | lang, dünn, Glatze, Hakennase, Nadelstreifen, Klemmbrett | Taucht unangekündigt auf („Tick, tack, Herr Kalle.“), hakt Tage auf dem Klemmbrett ab |
| **Dennis „Späti-King“** | Rivale gegenüber | Sonnenbrille, Goldkette, Ringlicht vor dem Laden, filmt alles für TikTok | Kopiert jede gute Idee von Kalle am nächsten Tag |
| **Horst** (71) | Stammkunde | Schiebermütze, Schnauzer, Rollator mit Wimpel | Kauft jeden Tag Lotto + Zeitung + „ein Kurzer“ (Kalle gibt ihm Kaffee), erzählt „Früher bei Erika …“ |
| **Jule** (23) | Paketbotin, Sympathieträgerin | Pferdeschwanz, gelbe Uniform-Jacke, Sackkarre | Bringt täglich Pakete für die Packstation, gibt Kalle ehrliche Tipps; leises Love-Interest, nie Hauptthema |
| **Max** (ab F2) | ehrenamtlicher Helfer | blonde Locken, blauer Pulli, rote Schürze „KIOSK“ (`figuren.max_helfer`) | Übereifrig, will alles „wie im Fernsehen“ machen; steht für die Community, die mithelfen will |
| **Die Bauarbeiter** (ab F2) | Stammkunden mittags | gelber Helm, orange Warnweste (`figuren.bauarbeiter`) | Kaufen nur, wenn es eiskalt ist |
| **Die Schulkids** | Kunden | 3 Kinder, Schulranzen | Kaufen nur 10-Cent-Süßigkeiten, zählen ewig Kleingeld |

## Orte (wiederverwendbare Hintergründe)

1. **Kiosk außen** – Eckhaus, verblasstes Schild „KIOSK ERIKA“ (ein Buchstabe hängt schief), Rollladen, Zeitungsständer,
   gegenüber Dennis' Neon-Späti.
2. **Kiosk innen** – Theke, Süßigkeiten-Glasbehälter, Zigarettenregal (nur von hinten/als Farbblöcke), Kühlschrank
   (brummt, Tür klemmt), Kasse mit Kurbel, Omas Foto.
3. **Kalles Zimmer über dem Kiosk** – Matratze, Gaming-Setup, Pizzakartons (Nacht-/Abstimmungsszenen).
4. **Großmarkt** – hohe Regale, Paletten, Einkaufswagen (Einkauf/Investitionen).
5. **Straße/Bushaltestelle** – Laufwege, Begegnungen.
6. **Messenger-UI** – Chat mit Jule oder Gruppenchat „Kiosk-Kunden“, Kontakt „Herr Geier“ mit Totenkopf-Emoji.

## Farbwelt (eigene Hausfarbe statt Lila)

- Nacht/Abstimmung: Petrol-Dunkel #12333A → #0B2228, Strahlen #1C4A52.
- HUD-Pill „FOLGE N“: Orange #FF7A2F; Countdown-Text Gelb #FFD23F mit Schlüssel-Icon 🔑.
- KUNDEN-Balken: Gold #FFC233 mit Stern-Icon; KASSE-Leiste mit Fortschrittsfüllung Grün #3DDC84 Richtung 3.000 €.
- Karten A/B: Blau #3B6FF0 / Pink #FF4F8B (Unterschied zu Kevin: Pink statt Orange).
- Tag-Szenen: Himmel #9ED8F5, Kiosk-Fassade #F4E3B5, Markise rot-weiß gestreift.

## Staffelbogen (grobe Planung, Community darf abweichen)

| Folgen | Phase | Mögliche Ereignisse |
|---|---|---|
| 1 | Pilot | Erbe, Geier-Ultimatum, erster Tag: 3 € Umsatz, Kühlschrank kaputt → 1. Abstimmung |
| 2–7 | Lernen | Lieferant betrügt ihn, Horst wird Stammgast, Dennis eröffnet „Mega-Späti“, erstes Schild |
| 8–14 | Aufschwung | Virale Idee (z. B. Omas Rezept-Kakao), Kunden-Sterne steigen, erster 200-€-Tag |
| 15 | Mittel-Twist | Geier verdoppelt angeblich die Schulden / Einbruch / Gesundheitsamt |
| 16–25 | Kampf | Mitarbeiter einstellen? Kredit bei Dennis? Kiosk-Fest? |
| 26–30 | Finale | Countdown in Stunden, Spendenaktion der Stammkunden, letzte Abstimmung entscheidet das Ende |
