"""
trivia.py - Trivia Duel vs Simpsons Personage
===============================================
Jij speelt tegen een Simpsons personage.
Elk personage heeft een eigen moeilijkheidsgraad
en grappige reacties.
"""

import random
import time

VRAGEN = [
    # (vraag, juist antwoord, verkeerde antwoorden, categorie)
    ("Wat is de naam van de kerncentrale in Springfield?",
     "Springfield Nuclear Power Plant",
     ["Springfield Coal Mine", "Springfield Gas Station", "Burns Industries"],
     "Springfield"),

    ("Hoeveel kinderen heeft de familie Simpson?",
     "3",
     ["2", "4", "5"],
     "Familie"),

    ("Wat is Bart's echte voornaam?",
     "Bartholomew",
     ["Barton", "Barry", "Brandon"],
     "Familie"),

    ("In welke staat ligt Springfield (officieel onbekend maar meest gesuggerd)?",
     "Het is bewust vaag gehouden",
     ["Ohio", "Oregon", "Illinois"],
     "Springfield"),

    ("Wat is de naam van Krusty de Clown zijn echte naam?",
     "Herschel Shmoikel Pinchas Yerucham Krustofsky",
     ["Harold Krusty", "Kevin Clown", "Bobbert Krustofski"],
     "Personages"),

    ("Wat zegt Homer altijd als hij iets doms doet?",
     "D'OH",
     ["DOH", "D'OH!", "DOOH"],
     "Citaten"),

    ("Wie is de eigenaar van de Kwik-E-Mart?",
     "Apu Nahasapeemapetilon",
     ["Sanjay", "Manjula", "Rajesh"],
     "Personages"),

    ("Wat is de naam van Bart zijn leraar?",
     "Edna Krabappel",
     ["Edna Flanders", "Patty Bouvier", "Elizabeth Hoover"],
     "School"),

    ("Hoe heet de kroeg van Homer?",
     "Moe's Tavern",
     ["Homer's Bar", "Springfield Pub", "Barney's Place"],
     "Springfield"),

    ("Wat is Lisa's favoriete muziekinstrument?",
     "Saxofoon",
     ["Fluit", "Trompet", "Klarinet"],
     "Familie"),

    ("Wie is Bart's beste vriend?",
     "Milhouse Van Houten",
     ["Nelson Muntz", "Martin Prince", "Database"],
     "School"),

    ("Wat is het adres van de Simpsons?",
     "742 Evergreen Terrace",
     ["742 Elm Street", "123 Evergreen Terrace", "742 Maple Avenue"],
     "Springfield"),

    ("Hoe heet de kat van de Simpsons?",
     "Snowball",
     ["Whiskers", "Mittens", "Felix"],
     "Familie"),

    ("Hoe heet de hond van de Simpsons?",
     "Santa's Little Helper",
     ["Fluffy", "Biscuit", "Lucky"],
     "Familie"),

    ("Wie zegt 'Haha!' als iemand iets doms doet?",
     "Nelson Muntz",
     ["Jimbo Jones", "Kearney Zzyzwicz", "Dolph Starbeam"],
     "School"),

    ("Wat is de naam van Homer zijn baas?",
     "Charles Montgomery Burns",
     ["Waylon Smithers", "Frank Grimes", "Lenny Leonard"],
     "Werk"),

    ("Wie is de assistent van meneer Burns?",
     "Waylon Smithers",
     ["Homer Simpson", "Lenny Leonard", "Carl Carlson"],
     "Werk"),

    ("Wat is Marge haar originele achternaam (meisjesnaam)?",
     "Bouvier",
     ["Van Houten", "Flanders", "Burns"],
     "Familie"),

    ("In welk jaar begon The Simpsons (de serie)?",
     "1989",
     ["1987", "1991", "1993"],
     "Serie"),

    ("Wie maakt The Simpsons?",
     "Matt Groening",
     ["Seth MacFarlane", "Mike Judge", "Trey Parker"],
     "Serie"),
]

PERSONAGES = {
    "bart": {
        "naam": "Bart Simpson 🛹",
        "moeilijkheid": 0.4,  # kans dat hij het goed heeft
        "goed": [
            "Bart: Eet mijn shorts! Ik wist het! 😎",
            "Bart: Ay caramba! Dat wist ik!",
            "Bart: Cowabunga! Punt voor mij!",
        ],
        "fout": [
            "Bart: D'oh... bedoel ik... Ay caramba!",
            "Bart: Pfff wie weet dat nou.",
            "Bart: Die vraag was stom.",
            "Bart: *krast op zijn skateboard en negeert het*",
        ],
        "intro": "Bart: Ok ok, jij denkt dat je slimmer bent dan ik? Bewijs het! 😏"
    },
    "homer": {
        "naam": "Homer Simpson 🍩",
        "moeilijkheid": 0.25,
        "goed": [
            "Homer: WOOHOO! Ik wist het! Doe ik altijd! 😎",
            "Homer: In je gezicht! Ik ben een genie!",
            "Homer: Mmm... punt. Lekker.",
        ],
        "fout": [
            "Homer: D'OH!",
            "Homer: *bijt in een donut en negeert de vraag*",
            "Homer: Is het een donut? Nee? Dan weet ik het niet.",
            "Homer: Marge! Wat is het antwoord?!",
        ],
        "intro": "Homer: Trivia? Ik hou van trivia! Mmm... trivia... 🍩"
    },
    "lisa": {
        "naam": "Lisa Simpson 🎷",
        "moeilijkheid": 0.85,
        "goed": [
            "Lisa: Uiteraard. Dat staat in hoofdstuk 3. 🤓",
            "Lisa: Correct! Ik heb dit gisteren nog bestudeerd.",
            "Lisa: *speelt triomfantel saxofoon* 🎷",
        ],
        "fout": [
            "Lisa: Dat... kan niet kloppen. Of toch?",
            "Lisa: Hmm, mijn geheugen liet me in de steek.",
            "Lisa: *mompelt* Dat was een strikvraag.",
        ],
        "intro": "Lisa: Een intellectueel duel? Met plezier. Maar wees voorbereid. 🤓"
    },
    "nelson": {
        "naam": "Nelson Muntz 😤",
        "moeilijkheid": 0.35,
        "goed": [
            "Nelson: Haha! Geweten! In je gezicht!",
            "Nelson: *port je in de arm* Ha!",
            "Nelson: Dat wist ik. Doe ik altijd.",
        ],
        "fout": [
            "Nelson: Haha! ...wacht. D'oh.",
            "Nelson: Dat telt niet. De vraag was vals.",
            "Nelson: *kijkt weg* Ik ga je nu niet pesten om dit te vergeten.",
        ],
        "intro": "Nelson: Trivia? Haha! Ik ga je verslaan en dan uitlachen. 😤"
    },
}


def speel_trivia(name: str, cheats: int = 0) -> dict:
    """
    Trivia duel. Geeft {"gewonnen": bool, "score_speler": int, "score_personage": int}
    """
    # Kies personage
    print("\n🏆 TRIVIA DUEL")
    print("─" * 35)
    print("Tegen wie wil je spelen?")
    for i, (pid, pdata) in enumerate(PERSONAGES.items(), 1):
        diff = "⭐" * int(pdata["moeilijkheid"] * 5)
        print(f"  {i}) {pdata['naam']}  {diff}")

    keuze = input("\nJouw keuze (1-4): ").strip()
    personage_lijst = list(PERSONAGES.items())
    if keuze.isdigit() and 1 <= int(keuze) <= len(personage_lijst):
        pid, personage = personage_lijst[int(keuze) - 1]
    else:
        pid, personage = random.choice(personage_lijst)
        print(f"Ongeldige keuze, random gekozen: {personage['naam']}")

    print(f"\n{personage['intro']}")
    time.sleep(1)

    # Selecteer vragen (5 willekeurige)
    geselecteerd = random.sample(VRAGEN, min(5, len(VRAGEN)))
    score_speler = 0
    score_personage = 0
    rondes = len(geselecteerd)

    for i, (vraag, juist, fout_antwoorden, categorie) in enumerate(geselecteerd, 1):
        print(f"\n\033[96mRonde {i}/{rondes} — {categorie}\033[0m")
        print(f"Vraag: {vraag}\n")

        # Maak antwoordopties (1 goed + 3 fout, geshuffeld)
        opties = fout_antwoorden[:3] + [juist]
        random.shuffle(opties)
        juist_index = opties.index(juist)

        for j, optie in enumerate(opties, 1):
            print(f"  {j}) {optie}")

        if cheats == 1:
            print(f"\033[90m[Cheat] Juist antwoord: {juist_index + 1}) {juist}\033[0m")

        antwoord = input("\nJouw antwoord (1-4): ").strip()

        speler_goed = False
        if antwoord.isdigit() and 1 <= int(antwoord) <= len(opties):
            if opties[int(antwoord) - 1] == juist:
                print(f"\033[92m✅ Juist!\033[0m")
                score_speler += 1
                speler_goed = True
            else:
                print(f"\033[91m❌ Fout! Het juiste antwoord was: {juist}\033[0m")
        else:
            print(f"\033[91m❌ Ongeldig. Het juiste antwoord was: {juist}\033[0m")

        # Personage antwoord (op basis van moeilijkheid)
        time.sleep(0.5)
        personage_goed = random.random() < personage["moeilijkheid"]
        if personage_goed:
            print(random.choice(personage["goed"]))
            score_personage += 1
        else:
            print(random.choice(personage["fout"]))

        print(f"\033[90mStand: {name} {score_speler} — {personage['naam']} {score_personage}\033[0m")
        time.sleep(0.5)

    # Eindresultaat
    print(f"\n{'─'*35}")
    print(f"EINDSTAND: {name}: {score_speler}  |  {personage['naam']}: {score_personage}")

    gewonnen = score_speler > score_personage
    if gewonnen:
        print(f"\n\033[92m🏆 Jij wint het trivia duel! Goed gedaan {name}!\033[0m")
    elif score_speler == score_personage:
        print(f"\n🤝 Gelijkspel! Goed gespeeld!")
    else:
        print(f"\n\033[91m😢 {personage['naam']} wint het trivia duel!\033[0m")

    return {
        "gewonnen": gewonnen,
        "score_speler": score_speler,
        "score_personage": score_personage,
        "perfect": score_speler == rondes
    }
