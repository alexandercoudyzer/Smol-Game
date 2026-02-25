# Smol Game — GitHub Setup & Update Gids

## 📁 Bestanden in de repo zetten

Zet deze bestanden allemaal in je GitHub repo `alexandercoudyzer/Smol-Game`:

```
smol_game.py
player_data.py
hangman.py
blackjack.py
trivia.py
rps_ai.py
updater.py
version.json
```

---

## 🚀 Eerste keer instellen

1. Ga naar https://github.com/new
2. Naam: `Smol-Game`
3. Zet op **Public** (anders kan de updater het niet downloaden)
4. Klik "Create repository"
5. Upload alle bestanden via de website of via Git

---

## 📦 Een update uitbrengen (elke keer)

### Stap 1 — Pas `version.json` aan

Verhoog het versienummer en schrijf wat er nieuw is:

```json
{
  "version": "2.1.0",
  "changelog": "- Nieuwe game toegevoegd\n- Bug fix in hangman\n- Meer trivia vragen",
  "files": [
    "smol_game.py",
    "player_data.py",
    "hangman.py",
    "blackjack.py",
    "trivia.py",
    "rps_ai.py",
    "updater.py",
    "version.json"
  ]
}
```

> **Tip:** je hoeft niet alle bestanden in `files` te zetten.
> Zet er alleen die in die je echt veranderd hebt.
> De rest wordt niet gedownload en blijft zoals het is.

### Stap 2 — Pas `GAME_VERSION` aan in `smol_game.py`

```python
GAME_VERSION = "2.1.0"   # ← zelfde als in version.json
```

### Stap 3 — Push naar GitHub

Zet de gewijzigde bestanden op GitHub (via de website of Git).

### Klaar!

Zodra spelers de game starten, zien ze automatisch:

```
✨ Update beschikbaar: 2.0.0 → 2.1.0

  Wat is er nieuw:
    - Nieuwe game toegevoegd
    - Bug fix in hangman
    - Meer trivia vragen

  Wil je nu updaten? (ja/nee):
```

Als ze "ja" kiezen, worden de bestanden automatisch gedownload
en krijgen ze de melding om de game te herstarten.

---

## ⚙️ Versienummering

Gebruik het formaat `MAJOR.MINOR.PATCH`:

| Type         | Wanneer                              | Voorbeeld         |
|--------------|--------------------------------------|-------------------|
| MAJOR (x.0.0)| Grote herstructurering van de game   | 1.0.0 → 2.0.0     |
| MINOR (x.x.0)| Nieuwe game of grote feature         | 2.0.0 → 2.1.0     |
| PATCH (x.x.x)| Bug fix of kleine aanpassing         | 2.1.0 → 2.1.1     |

---

## ❗ Belangrijke regels

- De repo moet **Public** zijn
- Branch moet **main** heten (of pas `GITHUB_BRANCH` aan in `updater.py`)
- `version.json` moet altijd in de root van de repo staan
- De updater vervangt bestanden direct — maak eerst een backup
  als je belangrijke lokale aanpassingen hebt

---

## 🔧 Updater aanpassen

In `updater.py` bovenaan:

```python
GITHUB_USER   = "alexandercoudyzer"   # jouw GitHub naam
GITHUB_REPO   = "Smol-Game"           # naam van de repo
GITHUB_BRANCH = "main"                # branch naam
TIMEOUT       = 5                     # seconden voor timeout
```
