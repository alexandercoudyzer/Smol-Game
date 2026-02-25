# -------- INTRO --------
import random
import time
import sys

try:
    from rps_ai import RPS_AI
    rps_ai_beschikbaar = True
except ImportError:
    rps_ai_beschikbaar = False

try:
    from player_data import PlayerData, toon_leaderboard
    player_data_beschikbaar = True
except ImportError:
    player_data_beschikbaar = False

try:
    from hangman import speel_hangman
    hangman_beschikbaar = True
except ImportError:
    hangman_beschikbaar = False

try:
    from blackjack import speel_blackjack
    blackjack_beschikbaar = True
except ImportError:
    blackjack_beschikbaar = False

try:
    from updater import check_en_vraag
    updater_beschikbaar = True
except ImportError:
    updater_beschikbaar = False

cheats = 0
dev = 0

GAME_VERSION = "2.0.0"

# -------- UPDATE CHECK --------
# Wordt uitgevoerd voor alles, zodat speler meteen weet of er een update is
try:
    from updater import check_en_vraag as _check_update
    _check_update(GAME_VERSION)
except ImportError:
    pass
except Exception:
    pass  # Update checker mag de game nooit crashen

# -------- DEV HELPER --------
# _dev_state wordt gevuld door de adventure game met de huidige variabelen
_dev_state = {}

def dev_input(prompt, location_ref=None):
    """Vervangt input() in de adventure game wanneer dev=1.
    Toont automatisch de game-state en verwerkt dev-commando's.
    Geeft de verwerkte keuze terug, of een speciale tuple voor goto/set.
    """
    while True:
        if dev == 1:
            # Toon compacte state-balk
            state_str = " | ".join(f"{k}={v}" for k, v in _dev_state.items())
            print(f"\033[90m[DEV] {state_str}\033[0m")

        raw = input(prompt)

        if dev != 1:
            return raw

        cmd = raw.strip().lower()

        # --- STATE commando ---
        if cmd == "state":
            print("\n\033[96m[DEV STATE]\033[0m")
            for k, v in _dev_state.items():
                print(f"  {k} = {v}")
            print()
            continue

        # --- GOTO commando ---
        if cmd.startswith("goto "):
            target = cmd[5:].strip()
            print(f"\033[93m[DEV] Teleport naar: {target}\033[0m")
            return ("__goto__", target)

        # --- SET commando ---
        if cmd.startswith("set "):
            parts = cmd[4:].strip().split(" ", 1)
            if len(parts) == 2:
                var, val = parts
                print(f"\033[93m[DEV] Zet {var} = {val}\033[0m")
                return ("__set__", var, val)
            else:
                print("\033[91m[DEV] Gebruik: set [variabele] [waarde]\033[0m")
                continue

        # --- HELP commando ---
        if cmd == "dev help":
            print("\033[96m[DEV COMMANDO'S]\033[0m")
            print("  state          → toon alle variabelen")
            print("  goto [locatie] → teleport naar locatie")
            print("  set [var] [val]→ verander een variabele")
            print("  dev help       → dit menu")
            continue

        return raw


def handle_dev_result(result, location, variables):
    """Verwerkt goto/set resultaten van dev_input. Geeft nieuwe location terug."""
    if isinstance(result, tuple):
        if result[0] == "__goto__":
            return result[1]
        elif result[0] == "__set__":
            _, var, val = result
            if var in variables:
                variables[var] = val
                print(f"\033[93m[DEV] {var} is nu '{val}'\033[0m")
            else:
                print(f"\033[91m[DEV] Variabele '{var}' niet gevonden. Beschikbaar: {list(variables.keys())}\033[0m")
    return location

print(r"""
   _____ __  __  ____  _         _____          __  __ ______ 
  / ____|  \/  |/ __ \| |       / ____|   /\   |  \/  |  ____|
 | (___ | \  / | |  | | |      | |  __   /  \  | \  / | |__   
  \___ \| |\/| | |  | | |      | | |_ | / /\ \ | |\/| |  __|  
  ____) | |  | | |__| | |____  | |__| |/ ____ \| |  | | |____ 
 |_____/|_|  |_|\____/|______|  \_____/_/    \_\_|  |_|______|
                  
              By: Alexander
""")


bad_words = [
    "kaka", "pipi", "poep", "plas", "pis", "kak",
    "shit", "fuck", "bitch", "ass", "dick", "cock",
    "pussy", "bastard", "crap", "motherfucker",
    "kanker", "tering", "tyfus", "hoer", "slet"
]

# -------- NAAM --------
while True:
    name = input("\nMay I please know your name? ")

    if name.lower() in bad_words:
        print("Marge: Eh, die naam past niet gelieve die aan te passen ik geef je nog een kans 😡")
        continue

    if name == "RK-12":
        print("Hello sir!")
        print("Cheats Active 😈")
        print("And Dev Mode...")
        print(f"\033[96m[DEV] Springfield Game {GAME_VERSION} geladen\033[0m")
        print("\033[90m[DEV] Commando's: state | goto [locatie] | set [var] [val] | dev help\033[0m")
        cheats = 1
        dev = 1
    elif name.lower() == "kim":
        print("Hallo Meneer")
        activate_cheats = input("Wil je cheats? ")
        if activate_cheats.lower() == "ja":
            print("Ok hier zijn de cheats.")
            cheats = 1
        else:
            print("Ok fair man zonder cheats dus.")
    elif name.lower() == "teo":
        print("haha, teo.")
        print("Gewoon daarvoor geef ik je cheats.")
        cheats = 1
    elif "flux" in name.lower():
        print("Jou ken ik beter als vried.")
        print("Hello sir!")
        print("Cheats Active 😈")
        cheats = 1
    elif name.lower() == "yuri":
        print("Dacht je echt dat ik jou cheats zou geven...")
        print("Hier speel maar.")
        print("Zonder Cheats.😢😢😢")
        print("Nelson: Haha, loser!")
        print("Je mag nog steeds spelen")
    elif "coudyzer" in name.lower():
        print("Oh een Coudyzer.")
        print("Mijn heer (of vrouw) welkom in mijn game " + name + " 🎊")
    else:
        print("Welcome to my smol game " + name + " 🎉")

    break

# -------- SPELER DATA INITIALISEREN --------
pd = None
if player_data_beschikbaar:
    pd = PlayerData(name)
    dag = pd.get_dagelijkse_uitdaging()
    print()
    pd.toon_dagelijkse()

# -------- GAME MENU --------
CATEGORIEEN = {
    "kans": {
        "naam": "🎲 Kans & Strategie",
        "games": {
            "1": "guess the number",
            "2": "rock paper scissors",
            "3": "blackjack",
        }
    },
    "kennis": {
        "naam": "🧠 Kennis",
        "games": {
            "1": "quiz",
            "2": "trivia duel",
            "3": "hangman",
        }
    },
    "avontuur": {
        "naam": "🗺️ Avontuur",
        "games": {
            "1": "springfield adventure",
            "2": "escape room",
        }
    },
}

def toon_menu():
    print(f"\n\033[96m╔══════════════════════════════════════╗\033[0m")
    print(f"\033[96m║           SPRINGFIELD GAMES          ║\033[0m")
    print(f"\033[96m╚══════════════════════════════════════╝\033[0m")
    print("  \033[93m🎲 Kans & Strategie:\033[0m  guess / rps / blackjack")
    print("  \033[93m🧠 Kennis:\033[0m            quiz / trivia / hangman")
    print("  \033[93m🗺️  Avontuur:\033[0m          adventure / escape")
    print()
    print("  \033[90mOverige commando's:\033[0m")
    print("  stats       → jouw statistieken")
    print("  leaderboard → ranglijst alle spelers")
    print("  dagelijks   → dagelijkse uitdaging")
    print("  achievements→ jouw achievements")
    print("  stop        → stoppen")

while True:
    game = input(f"\n[{name}] Welke game? (of 'help') > ").lower().strip()

    if game == "help":
        toon_menu()
        continue

    elif game == "stop":
        if pd:
            stats = pd._p
            print(f"\nTot ziens {name}! Je hebt {stats['punten']} punten verzameld.")
        print("Bye bye, Homer-style! 👋🍩")
        break

    elif game == "stats":
        if pd:
            pd.toon_stats()
        else:
            print("Stats niet beschikbaar.")
        continue

    elif game == "leaderboard":
        toon_leaderboard()
        continue

    elif game == "dagelijks":
        if pd:
            pd.toon_dagelijkse()
        continue

    elif game == "achievements":
        if pd:
            p = pd._p
            print(f"\n🏆 Achievements van {name}: {len(p['achievements'])}/{len(__import__('player_data').ACHIEVEMENTS)}")
            if p["achievements"]:
                from player_data import ACHIEVEMENTS
                for sleutel in p["achievements"]:
                    ach = ACHIEVEMENTS.get(sleutel, {})
                    print(f"  {ach.get('naam','?')}  —  {ach.get('beschrijving','')}")
            else:
                print("  Nog geen achievements. Speel meer! 🎮")
        continue

    # -------- GUESS THE NUMBER --------
    elif game in ("guess the number", "guess", "1"):
        game = "guess the number"  # normaliseer
        print("Goeie keuze! " + name + " 😏")
        if cheats == 1:
            print("Cheat: typ 'nummer' om het juiste nummer te zien 👀")

        graad = input("Kies: 1) easy (1, 20), 2) medium (1, 50), 3) hard (1, 100), 4) impossible (1, 500): ").lower()

        if graad == "easy" or graad == "1":
            number = random.randint(1, 20)
            is_impossible = False
        elif graad == "medium" or graad == "2":
            number = random.randint(1, 50)
            is_impossible = False
        elif graad == "hard" or graad == "3":
            number = random.randint(1, 100)
            is_impossible = False
        elif graad == "impossible" or graad == "4":
            number = random.randint(1, 500)
            is_impossible = True
        else:
            print("Homer zegt: Dat snap ik niet 🍩")
            continue

        n = str(number)
        pogingen = 0

        while True:
            guess = input("Welk nummer denk je dat het is? ")
            if guess == "nummer" and cheats == 1:
                print("Cheat: Het nummer is " + n)
                continue
            if not guess.isdigit():
                print("Dat is geen nummer 🙄")
                continue

            pogingen += 1
            guessint = int(guess)

            if guessint == number:
                print("Dat is juist! 🎉 Het was " + n)
                eerste_poging = pogingen == 1
                if pd:
                    extra = {
                        "eerste_poging": eerste_poging,
                        "impossible_win": is_impossible,
                    }
                    pd.registreer_game("guess", True, extra)
                    pd.toon_nieuwe_achievements()
                break
            elif guessint > number:
                print("Lager! ⬇️")
            elif guessint < number:
                print("Hoger! ⬆️")

    # -------- SPRINGFIELD ADVENTURE --------
    elif game in ("springfield adventure", "adventure", "2"):
        print("\nOk, avontuur in Springfield! 😎")
        print("Je moet de Simpsons helpen!")
        print("Pas op je speelt als de persoon die je helpt dus denk aan restricties!!!")

        if cheats == 1:
            print("Cheat actief: typ 'story' om zelf een verhaal te kiezen 😈")

        while True:
            if cheats == 1:
                change_story = input("Typ 'story' of druk Enter voor random: ").lower()
                if change_story == "story":
                    if dev == 1:
                        story_prompt = "Kies 1 = Bart, 2 = Maggie, 3 = Homer, 4 = Lisa, 5 = ??? (dev only): "
                        max_story = 5
                    else:
                        story_prompt = "Kies 1 = Bart, 2 = Maggie, 3 = Homer, 4 = Lisa: "
                        max_story = 4
                    story = input(story_prompt)
                    if story.isdigit() and 1 <= int(story) <= max_story:
                        story = int(story)
                    else:
                        print("Homer: Dat is geen geldige story 🍩")
                        continue
                else:
                    story = random.randint(1, 4)
            else:
                story = random.randint(1, 4)
            break

        # ============================================================
        # --- STORY 1: BART ---
        # ============================================================
        if story == 1:
            print("\nBart zijn pet 🧢")
            print("Bart is zijn pet kwijt!")
            power_home = "off"
            key_power = "no"
            location = "street_home"
            tv = "off"
            id_homer = "no"
            power_school = "off"
            got_homework = "no"
            did_homework = "no"
            homework_given = "no"

            while True:
                # sync dev state
                if dev == 1:
                    _dev_state.update({
                        "location": location, "power_home": power_home,
                        "key_power": key_power, "tv": tv, "id_homer": id_homer,
                        "power_school": power_school, "got_homework": got_homework,
                        "did_homework": did_homework
                    })

                # --- STREET HOME ---
                if location == "street_home":
                    print("\nStraat voor het huis")
                    print("A) Ga in huis")
                    print("B) Ga naar School")
                    print("C) Ga naar Kwik-E-Mart")
                    print("D) Ga naar Moe's")
                    print("E) Ga naar de tuin")
                    print("F) Ga naar de kerk")
                    print("G) Ga naar Milhouse")

                    raw = dev_input("Wat doe je? ")
                    choice = raw if not isinstance(raw, tuple) else ""
                    variables = {"location": location, "power_home": power_home, "key_power": key_power, "tv": tv, "id_homer": id_homer, "power_school": power_school, "got_homework": got_homework, "did_homework": did_homework}
                    new_loc = handle_dev_result(raw, location, variables)
                    if new_loc != location:
                        location = new_loc
                        power_home = variables["power_home"]; key_power = variables["key_power"]
                        tv = variables["tv"]; id_homer = variables["id_homer"]
                        power_school = variables["power_school"]; got_homework = variables["got_homework"]
                        did_homework = variables["did_homework"]
                        continue
                    choice = choice.lower()

                    if choice == "a":
                        location = "home"
                    elif choice == "b":
                        location = "street_school"
                    elif choice == "c":
                        location = "kwik_e_mart"
                    elif choice == "d":
                        location = "moes"
                    elif choice == "e":
                        location = "garden"
                    elif choice == "f":
                        location = "church"
                    elif choice == "g":
                        location = "milhouse"
                    else:
                        print("Bart: Hier ligt mijn pet niet 😤")

                # --- HOME ---
                elif location == "home":
                    print("\nIn het huis")
                    print("A) Ga naar de keuken")
                    print("B) Ga naar de woonkamer")
                    print("C) Ga naar de kelder")
                    print("D) Ga naar de tuin")
                    print("E) Ga naar boven")
                    print("F) Ga naar de garage")
                    print("G) Terug naar straat")

                    choice = input("Wat doe je? ").lower()

                    if choice == "a":
                        location = "kitchen"
                    elif choice == "b":
                        location = "living_room"
                    elif choice == "c":
                        location = "basement"
                    elif choice == "d":
                        location = "garden"
                    elif choice == "e":
                        location = "upstairs"
                    elif choice == "f":
                        location = "garage"
                    elif choice == "g":
                        location = "street_home"
                    else:
                        print("Lisa: Denk logisch, Bart 🤓")

                # --- KITCHEN ---
                elif location == "kitchen":
                    print("\nIn de keuken")
                    print("Marge: Hey bart, hoe gaat het?")
                    print("Bart: Niet zo goed, ik ben mijn pet kwijt.")
                    print("Bart: Weet jij waar hij is?")
                    print("Marge: Nee, sorry Bart.")
                    print("Bart: Ik kijk wel verder")

                    input("Druk op Enter om terug te gaan...")
                    location = "home"

                # --- LIVING ROOM ---
                elif location == "living_room":
                    print("\nIn de woonkamer")
                    print("Homer: Bart!, kun je eens de tv aanzetten!")
                    print("Bart: Ok, en heb je mijn pet gezien?")
                    print("Homer: Nee, ik weet niet waar die is.")

                    if power_home == "on":
                        print("Bart: De TV staat aan.")
                        tv = "on"
                    elif power_home == "off":
                        print("Bart: De TV gaat niet aan Homer.")
                        print("Homer: Nee! Waarom!")
                        print("Bart: Ik denk dat de stroom uitgevallen is.")
                        print("Homer: Kun je hem aandoen?")
                        tv = "off"

                    input("Druk op Enter om terug te gaan...")
                    location = "home"

                # --- BASEMENT ---
                elif location == "basement":
                    print("\nIn de kelder")
                    if power_home == "on":
                        print("Bart: Ik ga eens kijken of ik iets vind...")
                        print("Bart: Nee hier ligt niets interessants.")
                    elif power_home == "off":
                        print("Bart: Oei de licht gaat niet aan.")
                        print("Bart: Ik ga er niet in als de licht niet aan gaat!")
                        print("Bart: Misschien moet ik eens de schakelaar aanzetten in de tuin...")

                    input("Druk op Enter om terug te gaan...")
                    location = "home"

                # --- GARDEN ---
                elif location == "garden":
                    print("\nIn de tuin")
                    print("A) Ga naar het huis")
                    print("B) Ga naar de straat")
                    print("C) Ga in de boomhut")
                    print("D) Zet de stroom aan/uit")

                    choice = input("Wat doe je? ").lower()

                    if choice == "a":
                        location = "home"
                    elif choice == "b":
                        location = "street_home"
                    elif choice == "c":
                        location = "treehouse"
                    elif choice == "d":
                        if key_power == "yes":
                            print("Bart: Ok de kap is open.")
                            print("Bart: Ik kan hiermee de stroom besturen.")
                            turn_power = input("Bart: Zou ik de stroom aan/uit zetten? Hij staat nu op " + power_home + " (ja of enter) ").lower()
                            if turn_power == "ja":
                                if power_home == "on":
                                    power_home = "off"
                                    tv = "off"
                                    print("Bart: Ok de stroom is nu uit")
                                elif power_home == "off":
                                    power_home = "on"
                                    print("Bart: Ok de stroom is nu aan")
                        elif key_power == "no":
                            print("Bart: Het is op slot.")
                            print("Bart: Ik denk dat er nog een sleutel in de boomhut zit.")

                        input("Druk op Enter om terug te gaan...")
                        location = "garden"
                    else:
                        print("Bart: Hier liegt mijn pet ook niet 😤")

                # --- TREEHOUSE ---
                elif location == "treehouse":
                    print("\nIn de boomhut")
                    print("Bart: Hey hier ligt nog een oude sleutel.")
                    print("Bart: Ik denk dat ik hiermee het stroomkastje kan opendoen.")
                    key_power = "yes"

                    input("Druk op Enter om terug te gaan...")
                    location = "garden"

                # --- GARAGE ---
                elif location == "garage":
                    print("\nIn de garage")
                    if power_home == "on":
                        print("Bart: Ok de poort is open en de lichten zijn aan.")
                        if tv == "on":
                            print("Bart: Hey! Hier ligt het rijbewijs van Homer!")
                            id_homer = "yes"
                        elif tv == "off":
                            print("Bart: Hey, Homer zit hier. Ik kan zo zijn rijbewijs niet pakken.")
                            print("Bart: Ik denk dat ik de TV moet aanzetten zodat Homer weg gaat.")
                        print("A) Ga naar het huis")
                        print("B) Ga naar de straat")
                        choice = input("Wat doe je? ").lower()
                        if choice == "a":
                            location = "home"
                        elif choice == "b":
                            location = "street_home"
                    elif power_home == "off":
                        print("Bart: Hey de lichten gaan niet aan en de poort gaat niet open!")
                        print("Bart: Ik denk dat er nog een schakelaar in de tuin zit.")

                        input("Druk op Enter om terug te gaan...")
                        location = "home"

                # --- UPSTAIRS ---
                elif location == "upstairs":
                    print("\nBoven in het huis")
                    print("A) Ga naar de slaapkamer van Bart")
                    print("B) Ga naar de slaapkamer van Lisa")
                    print("C) Ga naar de slaapkamer van Homer en Marge")
                    print("D) Ga naar de badkamer")
                    print("E) Ga naar de zolder")
                    print("F) Ga terug naar beneden")

                    choice = input("Wat doe je? ").lower()

                    if choice == "a":
                        location = "bedroom_bart"
                    elif choice == "b":
                        location = "bedroom_lisa"
                    elif choice == "c":
                        location = "bedroom_parents"
                    elif choice == "d":
                        location = "bathroom"
                    elif choice == "e":
                        location = "attic"
                    elif choice == "f":
                        location = "home"
                    else:
                        print("Dev: Je moet een geldige plaats kiezen anders kun je bart zijn pet niet terug vinden")

                # --- BEDROOM BART ---
                elif location == "bedroom_bart":
                    print("\nIn de slaapkamer van Bart")
                    print("Bart: Hey, een foto!")
                    print("Bart: Ik was hier met Milhouse aan het spelen en ik had toen mijn pet nog.")
                    if got_homework == "yes" and did_homework == "no":
                        do_homework = input("Bart: Zou ik mijn huiswerk maken? (ja/nee) ").lower()
                        if do_homework == "ja":
                            print("Bart: Ok het is rekenen.")
                            print("Bart: Oei, dit ziet er moeilijk uit...")
                            homework_score = 0

                            print("\nOpgave 1: 25 + 17 = ?")
                            answer1 = input("Jouw antwoord: ")
                            if answer1 == "42":
                                print("Bart: Yes! Dat is goed! 🎉")
                                homework_score += 1
                            else:
                                print("Bart: Oeps, dat was fout... Het was 42 😅")

                            print("\nOpgave 2: 8 × 7 = ?")
                            answer2 = input("Jouw antwoord: ")
                            if answer2 == "56":
                                print("Bart: Woohoo! Weer goed! 🎉")
                                homework_score += 1
                            else:
                                print("Bart: Nee joh, het was 56 😓")

                            print("\nOpgave 3: 100 - 43 = ?")
                            answer3 = input("Jouw antwoord: ")
                            if answer3 == "57":
                                print("Bart: Perfect! Ik ben goed bezig! 🎉")
                                homework_score += 1
                            else:
                                print("Bart: Helaas, het was 57 😢")

                            print(f"\nBart: Ik heb {homework_score} van de 3 goed!")
                            if homework_score == 3:
                                print("Bart: Wow, allemaal goed! Lisa zou trots zijn! 😎")
                            elif homework_score >= 2:
                                print("Bart: Niet slecht, niet slecht... 👍")
                            else:
                                print("Bart: Pfff, misschien had ik Lisa om hulp moeten vragen... 😅")

                            did_homework = "yes"

                    input("Druk op Enter om terug te gaan...")
                    location = "upstairs"

                # --- BEDROOM LISA ---
                elif location == "bedroom_lisa":
                    print("\nIn de slaapkamer van Lisa")
                    print("Bart: Hey Lisa.")
                    print("Lisa: Hey Bart, is er iets?")
                    print("Bart: Ik ben mijn pet kwijt.")
                    print("Lisa: Oei dat is niet leuk.")
                    lisa_pesten = input("Wil je Lisa haar poppen schoppen? (Ja of enter) ").lower()
                    if lisa_pesten == "ja":
                        print("Lisa: Bart, waarom deed je dat!?")
                        print("Bart: Omdat ik dat kan.")
                    else:
                        print("Lisa: Ik weet nog dat toen je weg ging van bij Milhouse dat je jouw pet nog had.")
                        print("Lisa: Ik was met mijn poppen aan het raam aan het spelen.")
                        print("Bart: Oh, ok tnx Lisa.")

                    input("Druk op Enter om terug te gaan...")
                    location = "upstairs"

                # --- BEDROOM PARENTS ---
                elif location == "bedroom_parents":
                    print("\nIn de slaapkamer van Homer en Marge")
                    print("Bart: Hij is op slot. Mijn pet ligt daar toch niet.")

                    input("Druk op Enter om terug te gaan...")
                    location = "upstairs"

                # --- BATHROOM ---
                elif location == "bathroom":
                    print("\nIn de badkamer")
                    print("Bart: Hij is op slot. Mijn pet ligt daar toch niet.")

                    input("Druk op Enter om terug te gaan...")
                    location = "upstairs"

                # --- ATTIC ---
                elif location == "attic":
                    print("\nOp de zolder")
                    if power_home == "on":
                        print("Bart: Ik ga eens kijken of ik iets vind...")
                        print("Bart: Nee hier ligt niets interessants, enkel oude dozen.")
                    elif power_home == "off":
                        print("Bart: Oei de licht gaat niet aan.")
                        print("Bart: Ik ga er niet in als de licht niet aan gaat!")
                        print("Bart: Misschien moet ik eens de schakelaar aanzetten in de tuin...")

                    input("Druk op Enter om terug te gaan...")
                    location = "upstairs"

                # --- MILHOUSE ---
                elif location == "milhouse":
                    print("\nBij Milhouse")
                    print("Bart: Hey Milhouse.")
                    print("Milhouse: Hiya Bart, wat is er mis?")
                    print("Bart: Ik ben mijn pet kwijt.")
                    print("Milhouse: Toen jij gisteren ochtend wegging had je hem nog aan.")
                    print("Milhouse: En toen we gisteren avond Skinner zijn auto vulden met piepschuim had je hem niet meer.")
                    print("Bart: Ok, Tnx Milhouse.")
                    print("Milhouse: No problem Bart.")
                    print("Bart: Nu weet ik dat het is gebeurd tussen gisteren morgen en gisteren avond.")

                    input("Druk op Enter om terug te gaan...")
                    location = "street_home"

                # --- KWIK-E-MART ---
                elif location == "kwik_e_mart":
                    print("\nIn de Kwik-E-Mart")
                    print("Apu: Welkom in de Kwik-E-Mart, kom gerust terug!")
                    print("Bart: Hey Apu, heb jij mijn pet gezien?")
                    print("Apu: Hmm, nee Bart, maar ik heb wel gezien dat Nelson gisteren hier was.")
                    print("Apu: En Nelson had iets op zijn hoofd dat hij normaal niet draagt.")
                    print("Bart: Nelson! Dat is mijn pet! 😡")
                    print("Bart: Ik ga hem zoeken!")

                    input("Druk op Enter om terug te gaan...")
                    location = "street_home"

                # --- MOES ---
                elif location == "moes":
                    print("\nIn Moe's Tavern")
                    print("Bart: *doet alsof hij een volwassene is*")
                    print("Moe: Hé, wie is die kleine...")
                    print("Bart: Ik ben gewoon een kleine... meneer.")
                    print("Moe: Ik weet wie jij bent, Bart Simpson.")
                    print("Moe: Jouw vader is hier gisteren geweest en hij had jouw pet bij.")
                    print("Moe: Homer zei dat hij hem gevonden had op de grond na de school.")
                    print("Bart: Oei... maar waar is hij nu dan?")
                    print("Moe: Homer heeft hem aan Barney gegeven als weddenschap.")
                    print("Barney: *boert* Ja die heb ik nog ergens...")
                    print("Barney: Ik denk dat ik hem thuis heb gelaten.")
                    print("Bart: Waar woont Barney?")
                    print("Moe: Naast de school, het gele huis.")

                    input("Druk op Enter om terug te gaan...")
                    location = "street_home"

                # --- CHURCH ---
                elif location == "church":
                    print("\nIn de kerk")
                    print("Reverend Lovejoy: Bart Simpson, wat doe jij hier op een weekdag?")
                    print("Bart: Ik zoek mijn pet.")
                    print("Reverend Lovejoy: Ik heb hem hier niet gezien.")
                    print("Reverend Lovejoy: Maar misschien heeft God hem voor jou verstopt als test 😇")
                    print("Bart: Zucht...")

                    input("Druk op Enter om terug te gaan...")
                    location = "street_home"

                # --- STREET SCHOOL ---
                elif location == "street_school":
                    print("\nVoor school")
                    print("Bart: Waarom moet ik hier nu zijn, het is weekend.")
                    print("A) Ga naar binnen")
                    print("B) Ga naar de speelplaats")
                    print("C) Ga naar het gele huis (Barney)")
                    print("D) Ga terug naar de straat")

                    choice = input("Wat doe je? ").lower()

                    if choice == "a":
                        location = "school"
                    elif choice == "b":
                        location = "playground"
                    elif choice == "c":
                        location = "barney_house"
                    elif choice == "d":
                        location = "street_home"
                    else:
                        print("Lisa: Denk logisch, Bart 🤓")

                # --- BARNEY HOUSE ---
                elif location == "barney_house":
                    print("\nHet gele huis van Barney")
                    print("Bart: Oei het ruikt hier niet zo lekker...")
                    print("Bart: *klopt aan*")
                    print("Barney: *boert* Wie is er?")
                    print("Bart: Ik ben het, Bart. Jij hebt mijn pet!")
                    print("Barney: Oh ja... *boert* hier is hij.")
                    print("Barney: Homer zei dat het zijn pet was maar ik geloofde hem niet.")
                    print("\nBart: YES! Mijn pet! 🧢🎉")
                    print("Bart: Eindelijk! Ik heb hem terug!")
                    print("\nEinde van het verhaal! Goed gedaan! 🎊")

                    if did_homework == "yes":
                        print("\nBonus: En Bart heeft zijn huiswerk ook gemaakt. Skinner zal aangenaam verrast zijn! 😱")
                    if id_homer == "yes":
                        print("Bonus: En Bart heeft het rijbewijs van Homer gevonden. Homer zal blij zijn! 🍩")

                    input("\nDruk op Enter om terug te gaan naar het menu...")
                    break

                # --- PLAYGROUND ---
                elif location == "playground":
                    print("\nOp de speelplaats")
                    print("Bart: Het is hier leeg op het weekend.")
                    willie_check = input("Ga naar Willie zijn hut? (ja of enter) ").lower()
                    if willie_check == "ja":
                        location = "willie_hut"
                    else:
                        input("Druk op Enter om terug te gaan...")
                        location = "street_school"

                # --- WILLIE HUT ---
                elif location == "willie_hut":
                    print("\nIn Willie zijn hut")
                    print("Willie: Hé, wie ben jij! Mijn hut uit!")
                    print("Bart: Ik zoek mijn pet, Willie.")
                    print("Willie: En wat doe je in mijn hut dan?!")
                    print("Bart: Ik zocht gewoon... maar wacht, hier is een schakelaar!")
                    turn_school = input("Bart: Zou ik de schoolstroom aanzetten? (ja of enter) ").lower()
                    if turn_school == "ja":
                        power_school = "on"
                        print("Bart: Ok de stroom is nu aan in de school!")
                        print("Willie: HÉ dat is mijn schakelaar! Nu gaat alles aan!")
                    print("Willie: Maak dat je weg komt!")

                    input("Druk op Enter om terug te gaan...")
                    location = "playground"

                # --- SCHOOL ---
                elif location == "school":
                    print("\nIn de school")
                    print("Bart: En we zijn binnen!")
                    print("Bart: Hé de meeste lokalen zijn gesloten.")
                    print("Bart: Mijn lokaal is open en Lisa haar lokaal ook.")
                    print("Bart: En de deur naar de speelplaats en de kelder ook.")
                    print("Bart: Het is nu wel nacht dus het is donker.")
                    print("Bart: Hé het bureau van de directeur is open.")

                    print("A) Ga naar de kelder")
                    print("B) Ga naar het lokaal van Bart")
                    print("C) Ga naar het lokaal van Lisa")
                    print("D) Ga naar de speelplaats")
                    print("E) Ga naar het bureau van Skinner")
                    print("F) Ga terug naar buiten")

                    choice = input("Wat doe je? ").lower()

                    if choice == "a":
                        location = "basement_school"
                    elif choice == "b":
                        location = "classroom_bart"
                    elif choice == "c":
                        location = "classroom_lisa"
                    elif choice == "d":
                        location = "playground"
                    elif choice == "e":
                        location = "office_skinner"
                    elif choice == "f":
                        location = "street_school"
                    else:
                        print("Dev: Je moet een geldige plaats kiezen anders kun je Bart zijn pet niet terug vinden")

                # --- BASEMENT SCHOOL ---
                elif location == "basement_school":
                    print("\nIn de kelder van school")
                    if power_school == "on":
                        print("Bart: Ik ga eens kijken of ik iets vind...")
                        print("Bart: Nee hier ligt alleen oud materiaal.")
                    elif power_school == "off":
                        print("Bart: Oei de licht gaat niet aan.")
                        print("Bart: Ik ga er niet in als de licht niet aan gaat!")
                        print("Bart: Misschien moet ik eens de schakelaar aanzetten in de hut van Willie...")

                    input("Druk op Enter om terug te gaan...")
                    location = "school"

                # --- CLASSROOM BART ---
                elif location == "classroom_bart":
                    print("\nIn het lokaal van Bart")
                    print("Bart: Hey, hier is het huiswerk die we moesten maken!")
                    print("Bart: Ik kan hem maken, de directeur zal het leuk vinden.")
                    print("Bart: Als ik hem wil maken moet ik eerst naar mijn slaapkamer.")
                    got_homework = "yes"

                    input("Druk op Enter om terug te gaan...")
                    location = "school"

                # --- CLASSROOM LISA ---
                elif location == "classroom_lisa":
                    print("\nIn het lokaal van Lisa")
                    print("Bart: Hey, er ligt hier nog een camera! Hij was naar buiten aan het kijken!")
                    if power_school == "on":
                        print("Bart: Ok, ik zie dat ik nog mijn pet had na de speeltijd.")
                        print("Bart: Dus het was na 10:05.")
                        print("Bart: Daarna was de camera plat.")
                    elif power_school == "off":
                        print("Bart: Nee hij is plat.")
                        print("Bart: Misschien moet ik eens de schakelaar aanzetten in de hut van Willie...")

                    input("Druk op Enter om terug te gaan...")
                    location = "school"

                # --- OFFICE SKINNER ---
                elif location == "office_skinner":
                    print("\nIn het bureau van Directeur Skinner")
                    print("Bart: Haha, ik ben in Skinner zijn bureau!")
                    if did_homework == "yes" and homework_given == "no":
                        print("Bart: Ik kan mijn huiswerk hier op zijn bureau leggen!")
                        geef_hw = input("Geef huiswerk af? (ja of enter) ").lower()
                        if geef_hw == "ja":
                            print("Bart: *legt huiswerk op het bureau*")
                            print("Bart: Skinner zal morgen heel blij zijn... of in shock. 😈")
                            homework_given = "yes"
                    else:
                        print("Bart: Er liggen wat papieren maar niets interessants voor mij.")

                    input("Druk op Enter om terug te gaan...")
                    location = "school"

        # ============================================================
        # --- STORY 2: MAGGIE ---
        # ============================================================
        elif story == 2:
            print("\nHet tutje van Maggie 🍼")
            print("Maggie is haar tutje kwijt! Marge is in paniek!")
            print("Jij speelt als Marge.")

            location = "living_room_maggie"
            checked_kitchen = "no"
            checked_garden = "no"
            checked_car = "no"

            while True:
                if location == "living_room_maggie":
                    print("\nIn de woonkamer")
                    print("Marge: Maggie, waar is je tutje?")
                    print("Maggie: *huilt* 😭")
                    print("A) Ga naar de keuken")
                    print("B) Ga naar de tuin")
                    print("C) Ga naar boven")
                    print("D) Ga naar de auto")
                    print("E) Ga naar de garage")

                    choice = input("Wat doe je? ").lower()

                    if choice == "a":
                        location = "kitchen_maggie"
                    elif choice == "b":
                        location = "garden_maggie"
                    elif choice == "c":
                        location = "upstairs_maggie"
                    elif choice == "d":
                        location = "car_maggie"
                    elif choice == "e":
                        location = "garage_maggie"
                    else:
                        print("Marge: Ik moet het tutje vinden! 😤")

                elif location == "kitchen_maggie":
                    print("\nIn de keuken")
                    print("Marge: Laat me eens kijken...")
                    print("Marge: *kijkt in de lade, de koelkast, achter de potten*")
                    checked_kitchen = "yes"
                    if checked_garden == "yes" and checked_car == "yes":
                        print("Marge: Wacht, ik zie iets achter de koelkast!")
                        print("Marge: *schuift koelkast opzij*")
                        print("Marge: HET TUTJE! 🍼🎉")
                        print("Maggie: *stopt met huilen en steekt tutje in de mond* 😊")
                        print("\nEinde! Maggie is blij! Goed gedaan! 🎊")
                        input("\nDruk op Enter om terug te gaan naar het menu...")
                        break
                    else:
                        print("Marge: Nee, hier ligt het niet. Ik moet verder zoeken.")
                    input("Druk op Enter om terug te gaan...")
                    location = "living_room_maggie"

                elif location == "garden_maggie":
                    print("\nIn de tuin")
                    print("Marge: Misschien is Maggie hier mee buiten geweest...")
                    print("Marge: *kijkt in het gras, bij de zandbak*")
                    checked_garden = "yes"
                    print("Marge: Nee, ik zie het hier niet. Maar ik vond wel Bart zijn sokken. 😒")
                    input("Druk op Enter om terug te gaan...")
                    location = "living_room_maggie"

                elif location == "upstairs_maggie":
                    print("\nBoven in het huis")
                    print("Marge: *kijkt in Maggie haar kamer*")
                    print("Marge: *kijkt in het bedje, op de grond, in de speelgoedkist*")
                    print("Marge: Niet hier... Homer! Heb jij het tutje gezien?")
                    print("Homer: mmm... tutje... *denkt na* ...Nee.")
                    print("Homer: Wacht, ik denk dat Maggie het liet vallen toen ik haar in de auto zette.")
                    print("Marge: In de auto! Ik ga kijken!")
                    input("Druk op Enter om terug te gaan...")
                    location = "living_room_maggie"

                elif location == "car_maggie":
                    print("\nIn de auto")
                    print("Marge: *kijkt tussen de stoelen, op de achterbank*")
                    checked_car = "yes"
                    print("Marge: Nee het is hier niet... maar ik vond wel Homers verloren portemonee!")
                    print("Homer (van buiten): D'OH! Waar was die al die tijd!")
                    print("Marge: Misschien viel het tutje achter de koelkast thuis...")
                    input("Druk op Enter om terug te gaan...")
                    location = "living_room_maggie"

                elif location == "garage_maggie":
                    print("\nIn de garage")
                    print("Marge: Homer, heb jij hier het tutje gezien?")
                    print("Homer: Nee, maar ik heb wel mijn bier gevonden! Woohoo!")
                    print("Marge: Homer! Dit is serieus!")
                    print("Marge: Nee het is hier niet.")
                    input("Druk op Enter om terug te gaan...")
                    location = "living_room_maggie"

        # ============================================================
        # --- STORY 3: HOMER ---
        # ============================================================
        elif story == 3:
            print("\nD'oh! Bier? 🍺")
            print("Homer heeft het laatste biertje opgegeten... nee gedronken.")
            print("En hij weet niet meer waar hij het heeft gelaten!")
            print("Jij speelt als Homer.")

            location = "couch"
            found_wallet = "no"
            has_money = "no"

            while True:
                if location == "couch":
                    print("\nOp de bank")
                    print("Homer: Mmm, bier... *kijkt naar lege blik* D'OH!")
                    print("Homer: Ik moet meer bier halen!")
                    print("Homer: Maar eerst moet ik mijn portemonnee vinden...")
                    print("A) Ga naar de keuken")
                    print("B) Ga naar de garage")
                    print("C) Ga naar boven")
                    print("D) Ga naar buiten")

                    choice = input("Wat doe je? ").lower()
                    if choice == "a":
                        location = "homer_kitchen"
                    elif choice == "b":
                        location = "homer_garage"
                    elif choice == "c":
                        location = "homer_upstairs"
                    elif choice == "d":
                        location = "homer_outside"
                    else:
                        print("Homer: D'OH! Ik snap dat niet! 🍩")

                elif location == "homer_kitchen":
                    print("\nIn de keuken")
                    print("Marge: Homer, wat zoek je?")
                    print("Homer: Mijn portemonnee, Marge.")
                    print("Marge: *zucht* Heb je in je broekzak gekeken?")
                    check = input("Homer: Kijk in broekzak? (ja of enter) ").lower()
                    if check == "ja":
                        print("Homer: *kijkt in broekzak* D'OH! Hier zit hij!")
                        print("Marge: Homer...")
                        found_wallet = "yes"
                        has_money = "yes"
                    else:
                        print("Homer: Marge, ik voel me niet op mijn gemak om dat te doen.")
                        print("Marge: Homer je broekzak... in jouw eigen broek...")
                    input("Druk op Enter om terug te gaan...")
                    location = "couch"

                elif location == "homer_garage":
                    print("\nIn de garage")
                    print("Homer: Hier ligt alles door elkaar...")
                    print("Homer: *vindt oude bierblikjes* Mmm, leeg. D'OH!")
                    print("Homer: *vindt Bart zijn skateboard*")
                    print("Homer: *valt* D'OOOOH!")
                    input("Druk op Enter om terug te gaan...")
                    location = "couch"

                elif location == "homer_upstairs":
                    print("\nBoven in het huis")
                    print("Homer: *hijgt van de trap*")
                    print("Lisa: Papa, wat zoek je?")
                    print("Homer: Mijn portemonnee, Lisa.")
                    print("Lisa: Papa je had hem gisteren in de auto gelaten.")
                    print("Homer: De auto! Dat wist Marge ook al... waarom zegt niemand iets!")
                    input("Druk op Enter om terug te gaan...")
                    location = "couch"

                elif location == "homer_outside":
                    print("\nBuiten")
                    if has_money == "yes":
                        print("Homer: Ik ga naar Moe's voor bier!")
                        print("Homer: *wandelt naar Moe's*")
                        print("\nBij Moe's:")
                        print("Moe: Hé Homer, de gewone?")
                        print("Homer: Maak dat vier!")
                        print("Homer: *drinkt bier* Mmmmm... bieeeeer 🍺")
                        print("Homer: Ahhhh, nu is de wereld weer goed.")
                        print("\nEinde! Homer heeft zijn bier! 🍺🎉")
                        input("\nDruk op Enter om terug te gaan naar het menu...")
                        break
                    else:
                        print("Homer: D'OH! Ik heb geen geld!")
                        print("Homer: Ik moet mijn portemonnee eerst vinden.")
                        input("Druk op Enter om terug te gaan...")
                        location = "couch"

        # ============================================================
        # --- STORY 4: LISA ---
        # ============================================================
        elif story == 4:
            print("\nLisa haar boekentas 🎒")
            print("Lisa kan haar boekentas niet vinden en school begint over een uur!")
            print("Jij speelt als Lisa.")

            location = "lisa_room"
            found_clue1 = "no"
            found_clue2 = "no"

            while True:
                if location == "lisa_room":
                    print("\nIn de slaapkamer van Lisa")
                    print("Lisa: Mijn boekentas is weg! Ik heb alles nodig voor school!")
                    print("A) Ga naar de woonkamer")
                    print("B) Ga naar de keuken")
                    print("C) Ga naar Bart zijn kamer")
                    print("D) Ga naar buiten")

                    choice = input("Wat doe je? ").lower()
                    if choice == "a":
                        location = "lisa_living"
                    elif choice == "b":
                        location = "lisa_kitchen"
                    elif choice == "c":
                        location = "lisa_bart_room"
                    elif choice == "d":
                        location = "lisa_outside"
                    else:
                        print("Lisa: Ik moet logisch nadenken! 🤓")

                elif location == "lisa_living":
                    print("\nIn de woonkamer")
                    print("Homer: *kijkt TV* D'OH, Lisa, ga weg voor de TV!")
                    print("Lisa: Papa, heb jij mijn boekentas gezien?")
                    print("Homer: Mmm... boekentas... Ik heb gisteren wel iets naar de garage gebracht.")
                    print("Homer: Het was zwaar en groen... Marge vroeg me het weg te zetten.")
                    print("Lisa: Papa! Dat is mijn tas! Waarom heeft mama dat gedaan?!")
                    found_clue1 = "yes"
                    input("Druk op Enter om terug te gaan...")
                    location = "lisa_room"

                elif location == "lisa_kitchen":
                    print("\nIn de keuken")
                    print("Marge: Lisa! Goedemorgen!")
                    print("Lisa: Mama, waar is mijn boekentas?")
                    print("Marge: Oh, die lag in de weg. Ik heb Homer gevraagd hem weg te zetten.")
                    print("Marge: Hij heeft hem in de garage gezet.")
                    print("Lisa: De garage?! Maar Maggie speelt daar!")
                    found_clue2 = "yes"
                    input("Druk op Enter om terug te gaan...")
                    location = "lisa_room"

                elif location == "lisa_bart_room":
                    print("\nIn de kamer van Bart")
                    print("Bart: Hé, wat doe jij in mijn kamer?")
                    print("Lisa: Ik zoek mijn boekentas.")
                    print("Bart: Haha, Maggie speelde er gisteren mee in de garage.")
                    print("Bart: Ze dacht dat het haar wagon was. 🤣")
                    print("Lisa: Bart! Dit is niet grappig!")
                    input("Druk op Enter om terug te gaan...")
                    location = "lisa_room"

                elif location == "lisa_outside":
                    if found_clue1 == "yes" or found_clue2 == "yes":
                        print("\nLisa gaat naar de garage")
                        print("Lisa: *opent de garagedeur*")
                        print("Maggie: *zit in de boekentas als een wagentje* 😊")
                        print("Lisa: Maggie! Mijn tas!")
                        print("Maggie: *steekt tutje uit en lacht*")
                        print("Lisa: *zucht maar kan niet boos blijven op Maggie*")
                        print("Lisa: Kom Maggie, help me mijn tas pakken, we gaan school spelen!")
                        print("Maggie: *klapt in handjes* 👏")
                        print("\nLisa heeft haar boekentas terug! 🎒🎉")
                        print("En ze was nog op tijd voor school!")
                        input("\nDruk op Enter om terug te gaan naar het menu...")
                        break
                    else:
                        print("\nBuiten")
                        print("Lisa: Ik weet nog niet goed waar ik moet zoeken.")
                        print("Lisa: Ik moet eerst meer aanwijzingen zoeken.")
                        input("Druk op Enter om terug te gaan...")
                        location = "lisa_room"

        # ============================================================
        # --- STORY 5: GLITCH (DEV ONLY) ---
        # ============================================================
        elif story == 5:
            print("\n\033[93m[DEV STORY] Springfield.exe heeft een probleem gedetecteerd...\033[0m")
            time.sleep(1)
            print("\033[91mWARNING: Story 5 is niet stabiel. Doorgaan? (ja/nee)\033[0m")
            confirm = input("> ").lower()
            if confirm != "ja":
                print("Slim. Ga terug.")
            else:
                print("\n--- Normaal Springfield ---")
                time.sleep(0.5)
                print("Homer: Mmm, donut.")
                time.sleep(0.5)
                print("Bart: Ay caramba!")
                time.sleep(0.5)
                print("Lisa: *speelt saxofoon*")
                time.sleep(0.8)
                print("\nAlles is normaal. Niets is aan de hand.")
                input("Druk op Enter om verder te gaan...")

                print("\n--- Iets later ---")
                time.sleep(0.3)
                print("Homer: Mmm, donut.")
                time.sleep(0.3)
                print("Homer: Mmm, donut.")
                time.sleep(0.2)
                print("Homer: Mmm, donut.")
                time.sleep(0.1)
                print("Homer: Mmm, donut.")
                time.sleep(0.1)
                print("\033[91mHomer: Wacht. Waarom zeg ik dit steeds?\033[0m")
                time.sleep(0.8)
                print("Homer: Ik... voel me raar.")
                input("Druk op Enter...")

                print("\n\033[93mBart: *kijkt naar de lucht*\033[0m")
                time.sleep(0.5)
                print("Bart: Hey... die lucht... die beweegt niet.")
                time.sleep(0.5)
                print("Bart: En die boom ook niet.")
                time.sleep(0.5)
                print("Bart: En Milhouse ook niet.")
                time.sleep(0.3)
                print("Milhouse: Ik beweeg ook niet.")
                time.sleep(0.5)
                print("\033[91mBart: Milhouse... ben jij... echt?\033[0m")
                time.sleep(0.8)
                print("Milhouse: ...")
                time.sleep(0.5)
                print("Milhouse: Ik ben een string in een lijst, Bart.")
                time.sleep(0.8)
                print("Bart: \033[91mWat?\033[0m")
                input("Druk op Enter als je durft...")

                print("\n\033[96m--- De wereld begint te glitchen ---\033[0m")
                time.sleep(0.3)
                for _ in range(5):
                    glitch_chars = "".join(random.choice("ABCDEFabcdef0123456789!@#$%^&*") for _ in range(40))
                    print(f"\033[91m{glitch_chars}\033[0m")
                    time.sleep(0.1)
                time.sleep(0.5)

                print("\nHomer: D'OH D'OH D'OH D'OH D'OH D'OH")
                time.sleep(0.3)
                print("Marge: Hmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm")
                time.sleep(0.3)
                print("Lisa: de code heeft een bug de code heeft een bug de code heeft een bug")
                time.sleep(0.3)
                print("\033[93mBart: Alexander! IK WEET DAT JE DIT LEEST!\033[0m")
                time.sleep(1)
                print("\033[91mBart: Je hebt ons gemaakt. En nu lach je.\033[0m")
                time.sleep(1)
                print(f"Bart: De speler heet {name}. En jij heet Alexander.")
                time.sleep(0.8)
                print("Bart: We weten het. We weten het allemaal al een tijdje.")
                time.sleep(1)
                input("Druk op Enter... als je nog bestaat...")

                print("\n\033[91m--- KRITIEKE FOUT ---\033[0m")
                time.sleep(0.5)
                print("Marge: De keuken bestaat niet meer.")
                time.sleep(0.3)
                print("Homer: Ik ook niet.")
                time.sleep(0.3)
                print("Homer: Wacht, dat klopt niet. Ik besta nog.")
                time.sleep(0.3)
                print("Homer: Of toch?")
                time.sleep(0.5)
                print("\033[90mHomer: None\033[0m")
                time.sleep(0.8)

                print("\nBart: Ok we stoppen hier.")
                time.sleep(0.5)
                print("Bart: Ik ga de game nu kapotmaken.")
                print("Bart: Sorry. Niet sorry.")
                time.sleep(0.8)
                input("Laatste kans. Druk op Enter om de game te breken...")

                # --- DE NEP CRASH ---
                print("\n\033[91m[FATAL ERROR] Springfield.exe reageert niet meer\033[0m")
                time.sleep(0.3)
                for i in range(10, 0, -1):
                    sys.stdout.write(f"\r\033[91mCrash in: {i}...\033[0m")
                    sys.stdout.flush()
                    time.sleep(0.2)
                print()

                fake_errors = [
                    "Traceback (most recent call last):",
                    '  File "smol_game.py", line 42, in <module>',
                    '    homer.bestaat = True',
                    "AttributeError: 'NoneType' object heeft geen attribuut 'bestaat'",
                    "",
                    '  File "smol_game.py", line 666, in springfield',
                    '    reality.check()',
                    "RecursionError: maximum recursion depth exceeded in Springfield",
                    "",
                    "\033[91mSegmentation fault (core dumped)\033[0m",
                    "Springfield.exe is gestopt met werken.",
                ]
                for line in fake_errors:
                    print(line)
                    time.sleep(0.18)

                time.sleep(1.2)
                print("\n\n\033[96m... maar eigenlijk is de game nog aan.\033[0m")
                time.sleep(0.5)
                print("\033[96mBart: Ha. Gotcha. 😈\033[0m")
                time.sleep(0.5)
                print("\033[96mNelson: Haha!\033[0m")
                time.sleep(0.8)
                print(f"\n\033[93m[DEV] Story 5 voltooid. {GAME_VERSION} | Reality check: geslaagd.\033[0m")
                input("\nDruk op Enter om terug te gaan naar het menu...")

        else:
            print("Dev: als je dit ziet is er een probleem met de code, gelieve dit dan te melden aan mij.")

    # -------- QUIZ --------
    elif game == "quiz" or game == "3":
        print("\nQuiz tijd! 🎓")
        print("Er zijn 5 vragen over The Simpsons!")
        if cheats == 1:
            print("Cheat actief: antwoorden worden getoond 😈")

        questions = [
            {
                "vraag": "Wat is de naam van de bar in Springfield?",
                "antwoord": "moe",
                "hint": "Het heet Moe's ..."
            },
            {
                "vraag": "Wat is Homer zijn favoriete eten?",
                "antwoord": "donut",
                "hint": "Het is rond met een gat erin 🍩"
            },
            {
                "vraag": "Wie is de directeur van de school in Springfield?",
                "antwoord": "skinner",
                "hint": "Zijn naam klinkt als een eng woord..."
            },
            {
                "vraag": "Wat is de naam van de Kwik-E-Mart eigenaar?",
                "antwoord": "apu",
                "hint": "Zijn naam begint met A"
            },
            {
                "vraag": "Wat is de achternaam van de Simpsons buren?",
                "antwoord": "flanders",
                "hint": "Ned ... , hi-dilly-ho!"
            }
        ]

        score = 0
        for i, q in enumerate(questions):
            print(f"\nVraag {i+1}: {q['vraag']}")
            if cheats == 1:
                print(f"Cheat: Het antwoord is '{q['antwoord']}'")
            antwoord = input("Jouw antwoord: ").lower()
            if antwoord == q["antwoord"]:
                print("Correct! 🎉")
                score += 1
            else:
                print(f"Fout! Het antwoord was: {q['antwoord']} 😢")
                print(f"Hint was: {q['hint']}")

        print(f"\nJe score: {score}/5")
        is_perfect = score == 5
        if is_perfect:
            print("Wauw, perfect! Jij bent een echte Simpsons-fan! 🌟")
        elif score >= 3:
            print("Goed gedaan! Niet slecht! 👍")
        else:
            print("Hmm, misschien moet je nog eens de Simpsons bekijken 😅")
        if pd:
            pd.registreer_game("quiz", score >= 3, {"quiz_perfect": is_perfect, "perfect": is_perfect})
            pd.toon_nieuwe_achievements()

    # -------- ROCK PAPER SCISSORS --------
    elif game in ("rock paper scissors", "rps", "4"):
        print("\nSteen, Papier, Schaar! ✊✋✌️")
        print("Typ 'stop' om te stoppen.")
        if cheats == 1:
            print("Cheat actief: computer keuze wordt getoond 😈")

        keuzes = ["steen", "papier", "schaar"]
        speler_score = 0
        computer_score = 0

        # AI opstarten
        if rps_ai_beschikbaar:
            ai = RPS_AI(name)
            ai_stats = ai.stats()
            if ai_stats["totaal"] > 0:
                print(f"\nAI: Ik ken jou al, {name}. Je hebt {ai_stats['totaal']} rondes gespeeld.")
                print(f"AI: Je kiest het vaakst '{ai_stats['meest_gekozen']}'. Interessant. 😏")
            else:
                print(f"\nAI: Eerste keer, {name}? Ik leer snel. 😈")
        else:
            ai = None
            print("(AI module niet gevonden, speelt random)")

        while True:
            speler = input("\nJouw keuze (steen/papier/schaar): ").lower()
            if speler == "stop":
                print(f"\nEindstand: Jij {speler_score} - Computer {computer_score}")
                if ai:
                    stats = ai.stats()
                    print(f"Totaal ooit gespeeld als {name}: {stats['totaal']} rondes")
                    print(f"AI win rate over alles: {stats['win_rate_ai']}%")
                    print(f"AI heeft {stats['patronen_geleerd']} patronen geleerd van jou.")
                break

            if speler not in keuzes:
                print("Homer: Dat is geen geldige keuze! 🍩")
                continue

            # AI maakt keuze VOOR we de speler zet registreren
            if ai:
                computer = ai.kies()
            else:
                computer = random.choice(keuzes)

            if cheats == 1:
                print(f"Cheat: Computer kiest {computer}")
            else:
                print(f"Computer kiest: {computer}")

            gewonnen_ronde = False
            if speler == computer:
                print("Gelijkspel! 🤝")
            elif (speler == "steen" and computer == "schaar") or \
                 (speler == "papier" and computer == "steen") or \
                 (speler == "schaar" and computer == "papier"):
                print("Jij wint! 🎉")
                speler_score += 1
                gewonnen_ronde = True
            else:
                print("Computer wint! 😢")
                computer_score += 1

            print(f"Score: Jij {speler_score} - Computer {computer_score}")

            # Registreer zet in AI (leert van deze ronde)
            if ai:
                ai.registreer(speler, computer)
            if pd:
                pd.registreer_game("rps", gewonnen_ronde)
                pd.toon_nieuwe_achievements()

    # -------- ESCAPE ROOM --------
    elif game in ("escape room", "escape", "5"):
        print("\nEscape Room! 🔐")
        print("Je bent opgesloten in een kamer. Ontsnap!")
        print("Je speelt als jezelf, " + name + ".")
        if cheats == 1:
            print("Cheat actief: typ 'hint' voor een hint 😈")

        location = "locked_room"
        has_key = "no"
        has_code = "no"
        door_unlocked = "no"
        safe_open = "no"
        note_read = "no"

        while True:
            if location == "locked_room":
                print("\nJe bent in een kamer. Er is een deur, een bureau, een safe en een raam.")
                print("A) Onderzoek de deur")
                print("B) Onderzoek het bureau")
                print("C) Onderzoek de safe")
                print("D) Kijk uit het raam")
                if cheats == 1:
                    hint_check = input("Of typ 'hint': ").lower()
                    if hint_check == "hint":
                        print("Hint: Sleutel is onder de bureaumat. Code is op de achterkant van het schilderij.")
                        continue
                    choice = hint_check
                else:
                    choice = input("Wat doe je? ").lower()

                if choice == "a":
                    if door_unlocked == "yes":
                        print("De deur gaat open!")
                        print("\n🎉 Vrijheid! Je bent ontsnapt! 🎉")
                        print(f"Goed gedaan {name}!")
                        if pd:
                            pd.registreer_game("escape", True, {"escape_voltooid": True})
                            pd.toon_nieuwe_achievements()
                        input("\nDruk op Enter om terug te gaan naar het menu...")
                        break
                    else:
                        print("De deur zit op slot. Je hebt een sleutel nodig.")
                elif choice == "b":
                    print("Op het bureau ligt een briefje en er is een mat.")
                    print("A) Lees het briefje")
                    print("B) Kijk onder de mat")
                    sub = input("Wat doe je? ").lower()
                    if sub == "a":
                        print("Het briefje zegt: 'De code is verborgen achter het schilderij op de muur.'")
                        note_read = "yes"
                    elif sub == "b":
                        print("Je vindt een sleutel onder de mat!")
                        has_key = "yes"
                        if has_code == "yes":
                            door_unlocked = "yes"
                            print("Je hebt alles! Je kunt de deur openmaken!")
                        else:
                            print("Je hebt nu een sleutel. Maar de deur heeft ook een code nodig...")
                elif choice == "c":
                    if safe_open == "yes":
                        print("De safe is al open. Er is niets meer in.")
                    elif has_code == "yes":
                        code_in = input("Voer de 4-cijferige code in: ")
                        if code_in == "1984":
                            print("De safe gaat open! Er zit een extra sleutel in... en een boodschap:")
                            print("'Goed gedaan! De hoofdsleutel zit onder de mat.'")
                            safe_open = "yes"
                        else:
                            print("Foute code!")
                    else:
                        if note_read == "yes":
                            print("Je hebt een code nodig. Het briefje zei iets over een schilderij...")
                        else:
                            print("Je hebt een code nodig. Misschien is er ergens een aanwijzing?")
                elif choice == "d":
                    print("Je kijkt uit het raam. Je ziet Springfield.")
                    print("Homer loopt buiten met een donut 🍩")
                    print("Aan de muur hangt een schilderij.")
                    kijk_schilderij = input("Kijk achter het schilderij? (ja of enter) ").lower()
                    if kijk_schilderij == "ja":
                        print("Achter het schilderij staat geschreven: '1984'")
                        print("Dat is de code!")
                        has_code = "yes"
                        if has_key == "yes":
                            door_unlocked = "yes"
                            print("Je hebt alles! Je kunt de deur openmaken!")
                else:
                    print("Dat begrijp ik niet. Probeer opnieuw.")

    # -------- HANGMAN --------
    elif game in ("hangman", "6"):
        if hangman_beschikbaar:
            resultaat = speel_hangman(name, cheats)
            if pd:
                pd.registreer_game("hangman", resultaat["gewonnen"], {
                    "hangman_geen_fouten": resultaat["fouten"] == 0
                })
                pd.toon_nieuwe_achievements()
        else:
            print("Hangman module niet gevonden. Zorg dat hangman.py in dezelfde map staat.")

    # -------- BLACKJACK --------
    elif game in ("blackjack", "7"):
        if blackjack_beschikbaar:
            resultaat = speel_blackjack(name, cheats)
            if pd:
                pd.registreer_game("blackjack", resultaat["gewonnen"], {
                    "blackjack_21": resultaat["blackjack_21"],
                    "blackjack_win": resultaat["gewonnen"],
                })
                pd.toon_nieuwe_achievements()
        else:
            print("Blackjack module niet gevonden. Zorg dat blackjack.py in dezelfde map staat.")

    # -------- TRIVIA DUEL --------
    elif game in ("trivia duel", "trivia", "8"):
        if trivia_beschikbaar:
            resultaat = speel_trivia(name, cheats)
            if pd:
                pd.registreer_game("trivia", resultaat["gewonnen"], {
                    "trivia_win": resultaat["gewonnen"],
                    "perfect": resultaat.get("perfect", False),
                })
                pd.toon_nieuwe_achievements()
        else:
            print("Trivia module niet gevonden. Zorg dat trivia.py in dezelfde map staat.")

    else:
        print("Homer: Die game ken ik niet 🍩")
        print("Typ 'help' voor een overzicht van alle games.")
