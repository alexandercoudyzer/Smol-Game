"""
blackjack.py - Blackjack tegen Homer
=======================================
Klassiek Blackjack maar Homer speelt slecht
en zegt grappige dingen tussendoor.
"""

import random
import time

KAARTEN = ['2','3','4','5','6','7','8','9','10','B','D','K','A']
WAARDEN = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
    '7': 7, '8': 8, '9': 9, '10': 10,
    'B': 10, 'D': 10, 'K': 10, 'A': 11
}
NAMEN = {
    'B': 'Boer', 'D': 'Dame', 'K': 'Koning', 'A': 'Aas'
}

HOMER_OPMERKINGEN_KAART = [
    "Homer: Mmm, kaarten... 🃏",
    "Homer: Is dit goed? Ik weet het niet.",
    "Homer: *pakt stiekem een donut*",
    "Homer: Marge zei dat ik niet te veel moest gokken...",
    "Homer: Wacht, hoeveel is een Boer ook alweer?",
    "Homer: D'OH! Nee wacht, het is ok.",
]

HOMER_BUST = [
    "Homer: D'OH! Ik heb te veel! 😤",
    "Homer: Neeeeee! D'OOOOH!",
    "Homer: Marge gaat dit niet leuk vinden.",
    "Homer: *slaat zichzelf op het hoofd* D'OH!",
]

HOMER_WINT = [
    "Homer: WOOHOO! In je gezicht! 😎",
    "Homer: Haha! Homer Simpson wint weer!",
    "Homer: Ik ga dit vieren met een donut! 🍩",
    "Homer: Ja! Dit gaat in mijn superklapper-geheugen!",
]

HOMER_VERLIEST = [
    "Homer: D'OH! Alweer verloren...",
    "Homer: Ik ga naar Moe's om dit te vergeten. 🍺",
    "Homer: Bart heeft me dit zeker geleerd.",
    "Homer: *zucht* Homer Simpson verliest van iedereen.",
]


def _kaart_naam(k: str) -> str:
    return NAMEN.get(k, k)

def _hand_waarde(hand: list) -> int:
    waarde = sum(WAARDEN[k] for k in hand)
    azen = hand.count('A')
    while waarde > 21 and azen:
        waarde -= 10
        azen -= 1
    return waarde

def _toon_hand(hand: list, naam: str, verberg_tweede: bool = False):
    if verberg_tweede and len(hand) > 1:
        kaarten_str = f"{_kaart_naam(hand[0])}  [verborgen]"
        waarde_str = f"{WAARDEN[hand[0]]} + ?"
    else:
        kaarten_str = "  ".join(_kaart_naam(k) for k in hand)
        waarde_str = str(_hand_waarde(hand))
    print(f"  {naam}: {kaarten_str}  (waarde: {waarde_str})")

def _nieuw_deck() -> list:
    deck = KAARTEN * 4
    random.shuffle(deck)
    return deck


def speel_blackjack(name: str, cheats: int = 0) -> dict:
    """
    Speel een ronde Blackjack tegen Homer.
    Geeft dict terug: {"gewonnen": bool, "blackjack_21": bool, "resultaat": str}
    """
    deck = _nieuw_deck()

    # Uitdelen
    speler_hand = [deck.pop(), deck.pop()]
    homer_hand  = [deck.pop(), deck.pop()]

    print("\n🃏 BLACKJACK TEGEN HOMER")
    print("─" * 35)
    print("Homer: Oh, we spelen kaarten? Ik ben er klaar voor! 🍩\n")
    time.sleep(0.5)

    if cheats == 1:
        print(f"\033[90m[Cheat] Homer's hand: {homer_hand} = {_hand_waarde(homer_hand)}\033[0m")

    # Toon handen
    _toon_hand(speler_hand, name)
    _toon_hand(homer_hand, "Homer", verberg_tweede=True)
    print()

    speler_waarde = _hand_waarde(speler_hand)

    # Controleer direct blackjack
    if speler_waarde == 21:
        print(f"\033[93m✨ BLACKJACK! Je hebt direct 21!\033[0m")
        homer_waarde = _hand_waarde(homer_hand)
        print(f"\nHomer legt zijn kaarten neer:")
        _toon_hand(homer_hand, "Homer")
        if homer_waarde == 21:
            print("Homer: Wacht, ik ook! Gelijkspel! 😱")
            return {"gewonnen": False, "blackjack_21": True, "resultaat": "gelijkspel"}
        else:
            print(random.choice(HOMER_VERLIEST))
            return {"gewonnen": True, "blackjack_21": True, "resultaat": "blackjack"}

    # Speler beurt
    while True:
        speler_waarde = _hand_waarde(speler_hand)
        print(f"Jouw waarde: {speler_waarde}")

        if speler_waarde > 21:
            print(f"\n\033[91mBust! Je hebt {speler_waarde}. Te veel! 😢\033[0m")
            print(random.choice(HOMER_WINT))
            return {"gewonnen": False, "blackjack_21": False, "resultaat": "bust"}

        keuze = input("Wat doe je? (h = hit, s = stay): ").lower().strip()

        if keuze == "h":
            nieuwe_kaart = deck.pop()
            speler_hand.append(nieuwe_kaart)
            print(f"\nJe trekt: {_kaart_naam(nieuwe_kaart)}")
            _toon_hand(speler_hand, name)
            print()
        elif keuze == "s":
            print(f"\nJe blijft staan op {speler_waarde}.")
            break
        else:
            print("Typ 'h' voor hit of 's' voor stay.")

    speler_waarde = _hand_waarde(speler_hand)

    # Homer zijn beurt
    print("\nHomer legt zijn kaarten neer:")
    _toon_hand(homer_hand, "Homer")
    time.sleep(0.8)

    # Homer strategie: hij trekt als hij onder 17 zit
    # maar hij maakt ook af en toe stomme fouten (entertainment)
    while _hand_waarde(homer_hand) < 17:
        time.sleep(0.5)
        print(random.choice(HOMER_OPMERKINGEN_KAART))
        nieuwe_kaart = deck.pop()
        homer_hand.append(nieuwe_kaart)
        print(f"Homer trekt: {_kaart_naam(nieuwe_kaart)}")
        _toon_hand(homer_hand, "Homer")
        print()

    homer_waarde = _hand_waarde(homer_hand)

    # Uitkomst
    print(f"\n{'─'*35}")
    print(f"Jouw eindwaarde: {speler_waarde}")
    print(f"Homer eindwaarde: {homer_waarde}")
    print()

    blackjack_21 = (speler_waarde == 21)

    if homer_waarde > 21:
        print(random.choice(HOMER_BUST))
        print(f"\033[92mJij wint! Homer heeft bust! 🎉\033[0m")
        return {"gewonnen": True, "blackjack_21": blackjack_21, "resultaat": "homer_bust"}
    elif speler_waarde > homer_waarde:
        print(random.choice(HOMER_VERLIEST))
        print(f"\033[92mJij wint! 🎉\033[0m")
        return {"gewonnen": True, "blackjack_21": blackjack_21, "resultaat": "winst"}
    elif speler_waarde == homer_waarde:
        print("Homer: Gelijkspel... D'OH! 🤝")
        return {"gewonnen": False, "blackjack_21": blackjack_21, "resultaat": "gelijkspel"}
    else:
        print(random.choice(HOMER_WINT))
        print(f"\033[91mHomer wint! 😢\033[0m")
        return {"gewonnen": False, "blackjack_21": blackjack_21, "resultaat": "verlies"}
