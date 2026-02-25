"""
updater.py - Update Checker voor Smol Game
============================================
Checkt GitHub repo voor nieuwe versies.
Repo: https://github.com/alexandercoudyzer/Smol-Game

Hoe het werkt:
1. Haalt version.json op van GitHub
2. Vergelijkt met lokale GAME_VERSION
3. Toont melding als er een update is
4. Speler kiest zelf of hij wil updaten
5. Download alle gewijzigde bestanden en vervangt ze

Setup op GitHub:
- Maak een repo aan: alexandercoudyzer/Smol-Game
- Zet alle .py bestanden erin
- Zet version.json erin (zie formaat hieronder)
- Bij nieuwe update: verhoog versie in version.json + push nieuwe bestanden

Formaat version.json:
{
  "version": "2.1.0",
  "changelog": "- Nieuwe game toegevoegd\\n- Bug fixes",
  "files": [
    "smol_game.py",
    "player_data.py",
    "hangman.py",
    "blackjack.py",
    "trivia.py",
    "rps_ai.py",
    "updater.py"
  ]
}
"""

import urllib.request
import urllib.error
import json
import os
import sys
import shutil
import time

# ── CONFIGURATIE ────────────────────────────────────────────────
GITHUB_USER   = "alexandercoudyzer"
GITHUB_REPO   = "Smol-Game"
GITHUB_BRANCH = "main"

# Raw content base URL
RAW_BASE = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/{GITHUB_BRANCH}"
VERSION_URL = f"{RAW_BASE}/version.json"

# Timeout voor requests (seconden)
TIMEOUT = 5


# ── HULPFUNCTIES ────────────────────────────────────────────────

def _versie_naar_tuple(versie_str: str) -> tuple:
    """Zet "2.1.0" om naar (2, 1, 0) voor vergelijking."""
    try:
        return tuple(int(x) for x in versie_str.strip().lstrip("v").split("."))
    except (ValueError, AttributeError):
        return (0, 0, 0)


def _haal_op(url: str) -> str | None:
    """Haalt tekst op van een URL. Geeft None bij fout."""
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "SmolGame-Updater/1.0"}
        )
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return resp.read().decode("utf-8")
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError):
        return None


def _download_bestand(url: str, pad: str) -> bool:
    """Download een bestand naar een lokaal pad. Geeft True bij succes."""
    inhoud = _haal_op(url)
    if inhoud is None:
        return False
    try:
        # Schrijf naar tijdelijk bestand eerst (veilig)
        tmp_pad = pad + ".tmp"
        with open(tmp_pad, "w", encoding="utf-8") as f:
            f.write(inhoud)
        # Vervang origineel
        shutil.move(tmp_pad, pad)
        return True
    except (IOError, OSError):
        if os.path.exists(tmp_pad):
            os.remove(tmp_pad)
        return False


def _laad_lokale_versie() -> str:
    """Laad de lokale versie uit version.json als die bestaat, anders uit smol_game.py."""
    lokaal_version_json = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "version.json"
    )
    if os.path.exists(lokaal_version_json):
        try:
            with open(lokaal_version_json, "r", encoding="utf-8") as f:
                data = json.loads(f.read())
                return data.get("version", "0.0.0")
        except (json.JSONDecodeError, IOError):
            pass
    return None  # Geen lokale version.json, gebruik wat smol_game doorgeeft


# ── PUBLIEKE API ────────────────────────────────────────────────

def check_update(huidige_versie: str, stil: bool = False) -> dict:
    """
    Checkt of er een update beschikbaar is.

    huidige_versie: de GAME_VERSION string uit smol_game.py
    stil: als True, geen output bij "geen update"

    Geeft dict terug:
    {
        "beschikbaar": bool,
        "huidige_versie": str,
        "nieuwe_versie": str,
        "changelog": str,
        "files": list,
        "fout": str of None
    }
    """
    resultaat = {
        "beschikbaar": False,
        "huidige_versie": huidige_versie,
        "nieuwe_versie": huidige_versie,
        "changelog": "",
        "files": [],
        "fout": None
    }

    if not stil:
        print("\033[90mUpdate checker: verbinding maken met GitHub...\033[0m", end="", flush=True)

    inhoud = _haal_op(VERSION_URL)

    if inhoud is None:
        resultaat["fout"] = "Geen verbinding met GitHub mogelijk."
        if not stil:
            print(f"\r\033[90mUpdate checker: geen verbinding, overgeslagen.    \033[0m")
        return resultaat

    try:
        data = json.loads(inhoud)
    except json.JSONDecodeError:
        resultaat["fout"] = "Ongeldige version.json op GitHub."
        if not stil:
            print(f"\r\033[90mUpdate checker: ongeldige data ontvangen.         \033[0m")
        return resultaat

    nieuwe_versie = data.get("version", "0.0.0")
    resultaat["nieuwe_versie"] = nieuwe_versie
    resultaat["changelog"] = data.get("changelog", "Geen changelog beschikbaar.")
    resultaat["files"] = data.get("files", [])

    huidig_tuple = _versie_naar_tuple(huidige_versie)
    nieuw_tuple  = _versie_naar_tuple(nieuwe_versie)

    if nieuw_tuple > huidig_tuple:
        resultaat["beschikbaar"] = True
        if not stil:
            print(f"\r\033[92m✨ Update beschikbaar: {huidige_versie} → {nieuwe_versie}        \033[0m")
    else:
        if not stil:
            print(f"\r\033[90mUpdate checker: je hebt de laatste versie ({huidige_versie}).  \033[0m")

    return resultaat


def toon_update_melding(update_info: dict) -> bool:
    """
    Toont de update melding en vraagt of de speler wil updaten.
    Geeft True terug als de speler wil updaten.
    """
    if not update_info["beschikbaar"]:
        return False

    print(f"""
\033[93m╔══════════════════════════════════════════════╗
║           🆕 UPDATE BESCHIKBAAR!             ║
╚══════════════════════════════════════════════╝\033[0m
  Huidige versie : \033[91m{update_info['huidige_versie']}\033[0m
  Nieuwe versie  : \033[92m{update_info['nieuwe_versie']}\033[0m

  Wat is er nieuw:
""")
    for regel in update_info["changelog"].split("\\n"):
        print(f"    {regel}")

    print(f"""
  Te updaten bestanden: {len(update_info['files'])}
    {', '.join(update_info['files'])}
""")

    while True:
        keuze = input("  Wil je nu updaten? (ja/nee): ").lower().strip()
        if keuze in ("ja", "j", "yes", "y"):
            return True
        elif keuze in ("nee", "n", "no"):
            print("  Ok, je speelt verder met de huidige versie.")
            return False
        else:
            print("  Typ 'ja' of 'nee'.")


def voer_update_uit(update_info: dict) -> bool:
    """
    Download en installeer alle bestanden uit de update.
    Geeft True terug als alle bestanden succesvol gedownload zijn.
    """
    if not update_info["beschikbaar"] or not update_info["files"]:
        return False

    game_dir = os.path.dirname(os.path.abspath(__file__))
    bestanden = update_info["files"]
    geslaagd = []
    mislukt = []

    print(f"\n\033[96mUpdate downloaden...\033[0m")

    for bestand in bestanden:
        url = f"{RAW_BASE}/{bestand}"
        pad = os.path.join(game_dir, bestand)
        sys.stdout.write(f"  Downloaden: {bestand}... ")
        sys.stdout.flush()

        if _download_bestand(url, pad):
            print("\033[92m✅\033[0m")
            geslaagd.append(bestand)
        else:
            print("\033[91m❌\033[0m")
            mislukt.append(bestand)

        time.sleep(0.1)  # kleine pauze zodat GitHub niet rate-limit

    # Sla nieuwe versie op in lokale version.json
    lokaal_version_json = os.path.join(game_dir, "version.json")
    try:
        lokale_data = {
            "version": update_info["nieuwe_versie"],
            "changelog": update_info["changelog"],
            "files": update_info["files"]
        }
        with open(lokaal_version_json, "w", encoding="utf-8") as f:
            json.dump(lokale_data, f, indent=2, ensure_ascii=False)
    except IOError:
        pass

    print()
    if mislukt:
        print(f"\033[91m  {len(mislukt)} bestand(en) konden niet gedownload worden:\033[0m")
        for b in mislukt:
            print(f"    - {b}")
        print(f"  {len(geslaagd)}/{len(bestanden)} bestanden succesvol geüpdatet.")
        return False
    else:
        print(f"\033[92m  ✅ Update voltooid! {len(geslaagd)}/{len(bestanden)} bestanden geüpdatet.\033[0m")
        print(f"\033[93m  ⚠️  Herstart de game om de nieuwe versie te laden.\033[0m")
        return True


def check_en_vraag(huidige_versie: str) -> bool:
    """
    Alles in één: check, toon melding, vraag en installeer eventueel.
    Dit is de enige functie die je in smol_game.py hoeft aan te roepen.

    Geeft True terug als een update geïnstalleerd is (game moet herstarten).
    """
    update_info = check_update(huidige_versie)

    if update_info["fout"]:
        return False

    if not update_info["beschikbaar"]:
        return False

    wil_updaten = toon_update_melding(update_info)

    if not wil_updaten:
        return False

    succes = voer_update_uit(update_info)

    if succes:
        print("\n\033[93mDe game wordt afgesloten. Start smol_game.py opnieuw op.\033[0m")
        input("Druk op Enter om af te sluiten...")
        sys.exit(0)

    return False
