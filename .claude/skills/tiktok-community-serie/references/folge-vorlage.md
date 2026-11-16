# Folgen-Bauplan

## Szenen-Raster (Folge ≥ 2, Ziel 70–85 s)

| # | Beat-ID | Dauer | Bild | Sprecher (Muster) |
|---|---|---|---|---|
| 1 | `recap` | 4–6 s | Ziel-Karte (Kiosk-Polaroid + Kalenderblatt „NOCH 24 TAGE“) → Held im aktuellen Zustand, rote Kreise auf Problemen | „Noch 24 Tage, bis Herr Geier den Kiosk räumt. Und Kalle hat erst 410 Euro.“ |
| 2 | `ergebnis` | 6–8 s | Abstimmungs-Karten, Balken laufen hoch, GEWONNEN-Badge, Held-Reaktion groß unten | „Letzte Folge habt ihr entschieden: 64 Prozent wollten, dass Kalle … Also …“ |
| 3–6 | `szene1`…`szene4` | je 6–12 s | ein Ort pro Szene, Aufgabe → Panne → kleiner Erfolg, HUD-Wert ändert sich sichtbar | kurze Sätze, je Szene 1 Pointe |
| 7 | `wendung` | 6–10 s | Handy/Chat, Fund, Besuch von Geier – neues Problem | „Doch dann vibriert sein Handy …“ |
| 8 | `abstimmung` | 10–14 s | Titel + Karte A/B + Kommentar-Pill, Held abgedunkelt darunter | „Was soll Kalle tun? A: … oder B: … Dein Kommentar zählt.“ |
| – | Ende | 1,5 s | Standbild der Abstimmung (Loop-Puffer) | – |

Pilot (Folge 1): statt `ergebnis` → `praemisse` (Ziel, Frist, Bösewicht, Ist-Zustand).

## Regeln für das Skript

- Jede `line` = eine Untertitel-Gruppe mit **2–4 Wörtern**; genau ein `{y:…}` pro Gruppe ist der Normalfall.
- `{r:…}` für Verluste/Gefahr (Schulden, „geräumt“, „−40 €“), `{g:…}` für Gewinne („+120 Euro“).
- Zahlen, die anders gesprochen werden: `{"show": "{r:3.000 Euro}", "say": "dreitausend Euro"}`.
- Erster Satz = Ziel + Frist + Name. Letzter Satz = „Dein Kommentar zählt.“ (oder Variante „Ihr entscheidet.“).
- Die beiden Optionen im Sprechertext **genau so benennen wie auf den Karten**.
- Jede Szene braucht eine Lautmalerei oder ein sichtbares Pop (Zahl, Badge, Sprechblase).

## Beispiel: `script.json` Pilotfolge „Kiosk-Kalle – Folge 1“ (~165 Wörter ≈ 70 s)

```json
{
  "title": "Kiosk-Kalle – Folge 1",
  "voice": "thorsten-low",
  "length_scale": 0.95,
  "serie": "kiosk-kalle",
  "folge": 1,
  "hud": {"noch_tage": 30, "kunden_sterne": 1.2, "kasse_euro": 0},
  "abstimmung": {
    "titel": ["WAS SOLL", "KALLE TUN?"],
    "a": {"titel": "Konsole verkaufen", "unter": "neuer Kühlschrank", "icon": "konsole"},
    "b": {"titel": "Kredit bei Dennis", "unter": "500 € – mit Zinsen", "icon": "geldsack"}
  },
  "beats": [
    {"id": "praemisse", "label": "", "lines": [
      {"show": "{y:30 Tage.}", "say": "Dreißig Tage."},
      {"show": "So lange hat {y:Kalle} Zeit,"},
      {"show": "um den Kiosk"},
      {"show": "seiner {y:Oma} zu retten."},
      {"show": "Er hat ihn {y:geerbt} –"},
      {"show": "samt {r:3.000 Euro}", "say": "samt dreitausend Euro"},
      {"show": "{r:Mietschulden.}"},
      {"show": "Vermieter {y:Herr Geier}"},
      {"show": "gibt ihm 30 Tage.", "say": "gibt ihm dreißig Tage."},
      {"show": "Sonst wird {r:geräumt.}"}
    ]},
    {"id": "szene1", "label": "", "lines": [
      {"show": "Schau dir {y:Kalle} an."},
      {"show": "{y:Null Ahnung} vom Geschäft,"},
      {"show": "Kontostand: {r:0 Euro.}", "say": "Kontostand: null Euro."},
      {"show": "Erster Tag:"},
      {"show": "der Rollladen {y:klemmt.}"},
      {"show": "Um {y:elf Uhr}"},
      {"show": "ist er endlich offen."}
    ]},
    {"id": "szene2", "label": "", "lines": [
      {"show": "Stammkunde {y:Horst}"},
      {"show": "will Lotto spielen."},
      {"show": "Kalle findet"},
      {"show": "die {y:Scheine} nicht."},
      {"show": "Die {y:Schulkinder}"},
      {"show": "kaufen für {y:30 Cent}", "say": "kaufen für dreißig Cent"},
      {"show": "und zählen"},
      {"show": "{y:zehn Minuten} Kleingeld."}
    ]},
    {"id": "szene3", "label": "", "lines": [
      {"show": "Dann gibt"},
      {"show": "der {y:Kühlschrank} auf."},
      {"show": "Alle Getränke"},
      {"show": "werden {r:warm.}"},
      {"show": "Und gegenüber"},
      {"show": "eröffnet {y:Dennis}"},
      {"show": "seinen {r:Mega-Späti.}"}
    ]},
    {"id": "wendung", "label": "", "lines": [
      {"show": "Abends zählt Kalle"},
      {"show": "die Kasse:"},
      {"show": "{r:3 Euro 40.}", "say": "drei Euro vierzig."},
      {"show": "Dann {y:vibriert} sein Handy."},
      {"show": "{y:Herr Geier:}"},
      {"show": "„Noch {r:29 Tage.}", "say": "Noch neunundzwanzig Tage."},
      {"show": "Tick, tack.“"},
      {"show": "Kalle merkt:"},
      {"show": "Er braucht {y:einen Plan.}"},
      {"show": "Und {y:du} entscheidest ihn."}
    ]},
    {"id": "abstimmung", "label": "", "lines": [
      {"show": "Soll Kalle"},
      {"show": "seine {y:Konsole} verkaufen"},
      {"show": "für einen {y:neuen Kühlschrank}"},
      {"show": "oder bei {y:Dennis}"},
      {"show": "einen {r:Kredit} aufnehmen?"},
      {"show": "{y:A} oder {y:B}?"},
      {"show": "Dein Kommentar {y:zählt.}"}
    ]}
  ]
}
```

Bildfolge dazu: Kiosk außen mit schiefem Schild + Kalender „NOCH 30 TAGE“ → Geier mit Klemmbrett („TICK, TACK.“) →
Kalle-Nahaufnahme, rote Kreise (Ketchupfleck, Controller in der Hand) → Rollladen klemmt („RATTER… KLONK!“), Uhr 11:00 →
Horst an der Theke, Kalle wühlt („WO SIND DIE DINGER?!“) → Kinder mit Münzhaufen, Zeitraffer-Uhr → Kühlschrank
„BRZZZT… PFFF.“, Flaschen mit Schweißtropfen → Blick über die Straße: Dennis' Neon-Späti, Ringlicht, Menschenschlange →
Nacht, Kalle zählt Münzen (Kasse-HUD erscheint: „€ KASSE 3,40 / 3.000 €“ – neues HUD-Element!) → Handy: Chat
„Herr Geier 💀: Noch 29 Tage. Tick, tack.“ → Abstimmung.

## Nach dem Veröffentlichen (für den Creator)

- **Beschreibung:** „Folge 1 | Kalle hat 30 Tage, um Omas Kiosk zu retten. Ihr entscheidet, wie. 👇 A oder B?“
- **Angepinnter Kommentar:** „A = Konsole verkaufen 🎮 / B = Kredit bei Dennis 💰 – die Mehrheit gilt für Folge 2!“
- **Hashtags:** #serie #ihrentscheidet #kiosk #fyp #deutsch
- Kommentare 18–24 h nach Upload zählen, Prozente an Claude geben → kommen in `state.json` und in Folge N+1.

## Checkliste vor dem Render

- [ ] HUD-Werte = `state.json` (Folge, Tage, Sterne, Kasse) und Änderungen in dieser Folge plausibel
- [ ] Ergebnis-Prozente vom Creator (keine erfundenen Zahlen)
- [ ] Jede Szene hat einen Pop/Lautmalerei + SFX; Ortswechsel mit Whoosh
- [ ] Untertitel 2–4 Wörter, ein gelbes Wort, nichts verdeckt von HUD/Karten
- [ ] Abstimmungskarten-Text = gesprochener Text, Pill „Schreib A oder B in die Kommentare!“ sichtbar
- [ ] Keine Referenz-Figuren/-Namen/-Logos; kein TikTok-Logo
- [ ] `state.json` nach dem Render aktualisiert (neue Werte + `offene_abstimmung`)
