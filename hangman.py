"""
hangman.py - Simpsons Hangman
================================
Woorden en hints zijn allemaal Simpsons-gerelateerd.
"""

import random

WOORDEN = [
    ("springfield",    "De stad waar de Simpsons wonen"),
    ("donut",          "Homers favoriete eten 🍩"),
    ("kwikeemart",     "Apu zijn winkel"),
    ("saxophone",      "Lisa haar instrument 🎷"),
    ("skateboard",     "Bart zijn favoriete ding 🛹"),
    ("doh",            "Wat Homer zegt als er iets misgaat"),
    ("marge",          "De moeder van de familie Simpson"),
    ("maggie",         "De baby van de familie Simpson 🍼"),
    ("flanders",       "Ned ..., de buurman van Homer"),
    ("burns",          "De rijke eigenaar van de kerncentrale"),
    ("barney",         "Homers beste vriend bij Moe's"),
    ("skinner",        "De directeur van de school"),
    ("willie",         "De Schotse tuinman van de school"),
    ("itchy",          "Een van de twee tekenfilmmuizen"),
    ("scratchy",       "De kat in de tekenfilm van Bart"),
    ("krusty",         "De clown op tv 🤡"),
    ("sideshow",       "Krusty zijn assistent"),
    ("treehouse",      "Bart zijn geheime plek in de tuin"),
    ("monorail",       "Het mislukte project in Springfield"),
    ("shelbyville",    "De rivaalstad van Springfield"),
    ("nuclearplant",   "Waar Homer werkt"),
    ("apu",            "De eigenaar van de Kwik-E-Mart"),
    ("milhouse",       "Bart zijn beste vriend"),
    ("nelson",         "De pestkop op school, zegt 'Haha'"),
    ("otto",           "De schoolbuschauffeur"),
    ("lovejoy",        "De dominee van Springfield"),
    ("patty",          "Een van Marge haar zussen"),
    ("selma",          "De andere zus van Marge"),
    ("homer",          "De vader van de familie Simpson"),
    ("bart",           "De oudste zoon van de Simpsons"),
    ("lisa",           "De slimme dochter van de Simpsons"),
]

HANGMAN_FASES = [
    # 0 fouten
    """
  +---+
  |   |
      |
      |
      |
      |
=========""",
    # 1 fout
    """
  +---+
  |   |
  O   |
      |
      |
      |
=========""",
    # 2 fouten
    """
  +---+
  |   |
  O   |
  |   |
      |
      |
=========""",
    # 3 fouten
    """
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========""",
    # 4 fouten
    """
  +---+
  |   |
  O   |
 /|\\  |
      |
      |
=========""",
    # 5 fouten
    """
  +---+
  |   |
  O   |
 /|\\  |
 /    |
      |
=========""",
    # 6 fouten - dood
    """
  +---+
  |   |
  O   |
 /|\\  |
 / \\  |
      |
========="""
]

MAX_FOUTEN = 6


def speel_hangman(name: str, cheats: int = 0) -> dict:
    """
    Speel een ronde Hangman.
    Geeft dict terug: {"gewonnen": bool, "fouten": int, "woord": str}
    """
    woord_tuple = random.choice(WOORDEN)
    woord = woord_tuple[0].lower()
    hint = woord_tuple[1]

    geraden = set()
    fouten = 0
    foute_letters = []

    print("\n🪢 SIMPSONS HANGMAN")
    print("─" * 30)
    print(f"Hint: {hint}")
    if cheats == 1:
        print(f"\033[90m[Cheat] Het woord is: {woord}\033[0m")
    print(f"Het woord heeft {len(woord)} letters.\n")

    while fouten < MAX_FOUTEN:
        print(HANGMAN_FASES[fouten])
        print()

        # Toon het woord met underscores
        weergave = " ".join(l if l in geraden else "_" for l in woord)
        print(f"  Woord: {weergave}")
        print(f"  Foute letters: {', '.join(foute_letters) if foute_letters else '-'}")
        print(f"  Fouten: {fouten}/{MAX_FOUTEN}")
        print()

        # Check gewonnen
        if all(l in geraden for l in woord):
            print(f"\033[92mJuist! Het woord was: {woord.upper()} 🎉\033[0m")
            return {"gewonnen": True, "fouten": fouten, "woord": woord}

        # Input
        poging = input("Raad een letter (of typ het hele woord): ").lower().strip()

        if not poging:
            continue

        # Heel woord geraden
        if len(poging) > 1:
            if poging == woord:
                print(f"\033[92mJuist! Het woord was: {woord.upper()} 🎉\033[0m")
                return {"gewonnen": True, "fouten": fouten, "woord": woord}
            else:
                print(f"Fout! Dat is niet het woord. 😢")
                fouten += 1
                foute_letters.append(f"[{poging}]")
                continue

        if len(poging) != 1 or not poging.isalpha():
            print("Geef één letter op.")
            continue

        if poging in geraden or poging in foute_letters:
            print("Die letter heb je al geprobeerd.")
            continue

        if poging in woord:
            geraden.add(poging)
            print(f"\033[92m'{poging}' zit in het woord! ✅\033[0m")
        else:
            fouten += 1
            foute_letters.append(poging)
            print(f"\033[91m'{poging}' zit er niet in. ❌\033[0m")

    # Verloren
    print(HANGMAN_FASES[MAX_FOUTEN])
    print(f"\n\033[91mGame over! Het woord was: {woord.upper()}\033[0m")
    print("Homer: D'OH! 🍩")
    return {"gewonnen": False, "fouten": fouten, "woord": woord}
