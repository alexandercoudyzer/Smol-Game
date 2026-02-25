"""
player_data.py - Centrale opslag voor alle spelerdata
=======================================================
Beheert: punten, stats per game, achievements, leaderboard,
         dagelijkse uitdagingen.

Puntensysteem:
  - Winst:        +10 punten basis
  - Win rate bonus: als win_rate > 60% → +5 bonus per win
  - Perfect score: +20 bonus (bv. quiz 5/5)
  - Achievement:  +15 per nieuw achievement
  - Dagelijkse uitdaging voltooid: +25 bonus
"""

import json
import os
import random
from datetime import date

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "player_data.json")

# ── ACHIEVEMENT DEFINITIES ──────────────────────────────────────
ACHIEVEMENTS = {
    # Algemeen
    "eerste_stap":      {"naam": "🐣 Eerste Stap",        "beschrijving": "Eerste game gespeeld",                  "punten": 15},
    "verslaafd":        {"naam": "🎮 Verslaafd",           "beschrijving": "50 games gespeeld",                     "punten": 15},
    "donut_master":     {"naam": "🍩 Donut Master",        "beschrijving": "100 games gespeeld",                    "punten": 15},
    # RPS
    "rps_winnaar":      {"naam": "✊ RPS Winnaar",          "beschrijving": "10 RPS rondes gewonnen",                "punten": 15},
    "rps_streak":       {"naam": "🔥 RPS Streak",          "beschrijving": "5 RPS rondes op rij gewonnen",          "punten": 15},
    "rps_legende":      {"naam": "👑 RPS Legende",          "beschrijving": "50 RPS rondes gewonnen",                "punten": 15},
    # Quiz
    "quiz_perfect":     {"naam": "🌟 Quiz Perfect",        "beschrijving": "Quiz met 5/5 gespeeld",                 "punten": 15},
    "quiz_meester":     {"naam": "🎓 Quiz Meester",        "beschrijving": "5x quiz perfect gespeeld",              "punten": 15},
    # Hangman
    "hangman_pro":      {"naam": "🪢 Hangman Pro",         "beschrijving": "Hangman gewonnen zonder fout",          "punten": 15},
    "hangman_winnaar":  {"naam": "🔤 Hangman Winnaar",     "beschrijving": "10 hangman gewonnen",                   "punten": 15},
    # Blackjack
    "blackjack_21":     {"naam": "🃏 Blackjack!",          "beschrijving": "Exact 21 gehaald",                      "punten": 15},
    "homer_verslaan":   {"naam": "🍺 Homer Verslagen",     "beschrijving": "10x blackjack gewonnen van Homer",      "punten": 15},
    # Trivia
    "trivia_held":      {"naam": "🏆 Trivia Held",         "beschrijving": "Trivia duel gewonnen",                  "punten": 15},
    "trivia_meester":   {"naam": "🧠 Trivia Meester",      "beschrijving": "5x trivia duel gewonnen",               "punten": 15},
    # Guess the number
    "lucky_guess":      {"naam": "🎯 Lucky Guess",         "beschrijving": "Getal geraden op eerste poging",        "punten": 15},
    "impossible":       {"naam": "💀 Impossible",          "beschrijving": "Impossible mode gewonnen",              "punten": 15},
    # Escape room
    "ontsnapt":         {"naam": "🚪 Ontsnapt!",           "beschrijving": "Escape room voltooid",                  "punten": 15},
    # Dagelijkse uitdaging
    "dagelijkse_held":  {"naam": "📅 Dagelijkse Held",     "beschrijving": "Eerste dagelijkse uitdaging voltooid",  "punten": 15},
    "week_streak":      {"naam": "🗓️ Week Streak",         "beschrijving": "7 dagen op rij dagelijkse uitdaging",   "punten": 15},
    # Springfield adventure
    "bart_pet":         {"naam": "🧢 Bart's Pet",          "beschrijving": "Bart zijn pet teruggevonden",           "punten": 15},
    "homer_bier":       {"naam": "🍺 Homer's Bier",        "beschrijving": "Homer zijn bier gevonden",              "punten": 15},
}

GAME_NAMEN = {
    "guess":      "Guess the Number",
    "adventure":  "Springfield Adventure",
    "quiz":       "Quiz",
    "rps":        "Steen Papier Schaar",
    "escape":     "Escape Room",
    "hangman":    "Hangman",
    "blackjack":  "Blackjack",
    "trivia":     "Trivia Duel",
}

# ── DATA LADEN / OPSLAAN ────────────────────────────────────────

def _laad():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}

def _sla_op(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except IOError as e:
        print(f"[DATA] Kon niet opslaan: {e}")

def _leeg_profiel():
    return {
        "punten": 0,
        "games_gespeeld": 0,
        "achievements": [],
        "dagelijkse": {
            "laatste_datum": "",
            "streak": 0,
            "voltooid_vandaag": False,
            "uitdaging_type": "",
            "uitdaging_doel": 0,
            "uitdaging_voortgang": 0,
        },
        "stats": {game: {"gespeeld": 0, "gewonnen": 0, "verloren": 0} for game in GAME_NAMEN},
        "rps_streak": 0,
        "quiz_perfect_count": 0,
        "hangman_geen_fouten": 0,
        "blackjack_21_count": 0,
        "blackjack_wins": 0,
        "trivia_wins": 0,
        "guess_eerste_poging": 0,
        "guess_impossible_wins": 0,
        "escape_voltooid": False,
    }

# ── PUBLIEKE API ────────────────────────────────────────────────

class PlayerData:
    def __init__(self, speler_naam: str):
        self.speler = speler_naam.lower().strip()
        self._data = _laad()
        if self.speler not in self._data:
            self._data[self.speler] = _leeg_profiel()
        self._p = self._data[self.speler]
        self._nieuwe_achievements = []

    # ── PUNTEN ──

    def geef_punten(self, amount: int, reden: str = ""):
        self._p["punten"] += amount
        if reden:
            print(f"  \033[93m+{amount} punten\033[0m — {reden}")
        _sla_op(self._data)

    # ── GAME REGISTREREN ──

    def registreer_game(self, game_id: str, gewonnen: bool, extra: dict = None):
        """
        Registreer een gespeelde game.
        game_id: "guess", "adventure", "quiz", "rps", "escape", "hangman", "blackjack", "trivia"
        extra: dict met optionele info, bv. {"perfect": True, "fouten": 0, "blackjack_21": True}
        """
        if extra is None:
            extra = {}

        p = self._p
        p["games_gespeeld"] += 1

        if game_id in p["stats"]:
            p["stats"][game_id]["gespeeld"] += 1
            if gewonnen:
                p["stats"][game_id]["gewonnen"] += 1
            else:
                p["stats"][game_id]["verloren"] += 1

        # Basispunten
        if gewonnen:
            punten = 10
            win_rate = self._win_rate(game_id)
            if win_rate > 60:
                punten += 5
            self.geef_punten(punten, f"Gewonnen ({GAME_NAMEN.get(game_id, game_id)})")

        # Extra punten / achievement triggers
        if extra.get("perfect"):
            self.geef_punten(20, "Perfect score!")
        if extra.get("eerste_poging"):
            p["guess_eerste_poging"] += 1
        if extra.get("impossible_win"):
            p["guess_impossible_wins"] += 1
        if extra.get("quiz_perfect"):
            p["quiz_perfect_count"] += 1
        if extra.get("hangman_geen_fouten") and gewonnen:
            p["hangman_geen_fouten"] += 1
        if extra.get("blackjack_21"):
            p["blackjack_21_count"] += 1
        if extra.get("blackjack_win") and gewonnen:
            p["blackjack_wins"] += 1
        if extra.get("trivia_win") and gewonnen:
            p["trivia_wins"] += 1
        if game_id == "rps":
            if gewonnen:
                p["rps_streak"] = p.get("rps_streak", 0) + 1
            else:
                p["rps_streak"] = 0
        if extra.get("escape_voltooid"):
            p["escape_voltooid"] = True
        if extra.get("adventure_bart"):
            self._check_achievement("bart_pet")
        if extra.get("adventure_homer"):
            self._check_achievement("homer_bier")

        # Dagelijkse uitdaging voortgang
        self._update_dagelijkse(game_id, gewonnen)

        # Check alle achievements
        self._check_alle_achievements()

        _sla_op(self._data)
        return self._nieuwe_achievements

    # ── ACHIEVEMENTS ──

    def _check_achievement(self, sleutel: str):
        p = self._p
        if sleutel not in p["achievements"] and sleutel in ACHIEVEMENTS:
            p["achievements"].append(sleutel)
            ach = ACHIEVEMENTS[sleutel]
            self._nieuwe_achievements.append(ach)
            self.geef_punten(ach["punten"], f"Achievement: {ach['naam']}")

    def _check_alle_achievements(self):
        p = self._p
        gs = p["games_gespeeld"]
        rps_w = p["stats"]["rps"]["gewonnen"]

        if gs >= 1:                             self._check_achievement("eerste_stap")
        if gs >= 50:                            self._check_achievement("verslaafd")
        if gs >= 100:                           self._check_achievement("donut_master")
        if rps_w >= 10:                         self._check_achievement("rps_winnaar")
        if p.get("rps_streak", 0) >= 5:         self._check_achievement("rps_streak")
        if rps_w >= 50:                         self._check_achievement("rps_legende")
        if p.get("quiz_perfect_count", 0) >= 1: self._check_achievement("quiz_perfect")
        if p.get("quiz_perfect_count", 0) >= 5: self._check_achievement("quiz_meester")
        if p.get("hangman_geen_fouten", 0) >= 1:self._check_achievement("hangman_pro")
        if p["stats"]["hangman"]["gewonnen"] >= 10: self._check_achievement("hangman_winnaar")
        if p.get("blackjack_21_count", 0) >= 1: self._check_achievement("blackjack_21")
        if p.get("blackjack_wins", 0) >= 10:    self._check_achievement("homer_verslaan")
        if p.get("trivia_wins", 0) >= 1:        self._check_achievement("trivia_held")
        if p.get("trivia_wins", 0) >= 5:        self._check_achievement("trivia_meester")
        if p.get("guess_eerste_poging", 0) >= 1:self._check_achievement("lucky_guess")
        if p.get("guess_impossible_wins", 0) >= 1: self._check_achievement("impossible")
        if p.get("escape_voltooid"):            self._check_achievement("ontsnapt")
        streak = p["dagelijkse"].get("streak", 0)
        if streak >= 1:                         self._check_achievement("dagelijkse_held")
        if streak >= 7:                         self._check_achievement("week_streak")

    def toon_nieuwe_achievements(self):
        if self._nieuwe_achievements:
            print("\n\033[93m╔══════════════════════════════╗\033[0m")
            print("\033[93m║    🏆 ACHIEVEMENT UNLOCKED!  ║\033[0m")
            print("\033[93m╚══════════════════════════════╝\033[0m")
            for ach in self._nieuwe_achievements:
                print(f"  {ach['naam']}")
                print(f"  \033[90m{ach['beschrijving']}\033[0m")
                print(f"  \033[93m+{ach['punten']} punten\033[0m\n")
            self._nieuwe_achievements = []

    # ── DAGELIJKSE UITDAGING ──

    UITDAGINGEN = [
        # (type, game_id, doel, beschrijving, afwisselend: 0=game, 1=quiz)
        {"type": "game",  "game": "rps",       "doel": 3,  "tekst": "Win 3x Steen Papier Schaar"},
        {"type": "game",  "game": "hangman",    "doel": 2,  "tekst": "Win 2x Hangman"},
        {"type": "game",  "game": "blackjack",  "doel": 2,  "tekst": "Win 2x Blackjack van Homer"},
        {"type": "quiz",  "game": "quiz",       "doel": 1,  "tekst": "Haal een perfecte quiz score"},
        {"type": "game",  "game": "trivia",     "doel": 1,  "tekst": "Win een Trivia Duel"},
        {"type": "quiz",  "game": "quiz",       "doel": 2,  "tekst": "Speel 2x de quiz"},
        {"type": "game",  "game": "rps",        "doel": 5,  "tekst": "Win 5x Steen Papier Schaar"},
        {"type": "game",  "game": "guess",      "doel": 1,  "tekst": "Raad een getal op de eerste poging"},
    ]

    def get_dagelijkse_uitdaging(self) -> dict:
        """Geeft de uitdaging van vandaag terug, genereert een nieuwe als nodig."""
        dag = self._p["dagelijkse"]
        vandaag = str(date.today())

        if dag["laatste_datum"] != vandaag:
            # Nieuwe dag: nieuwe uitdaging
            # Afwisselend: even dag = game, oneven dag = quiz
            dag_nr = date.today().toordinal()
            uitdaging = self.UITDAGINGEN[dag_nr % len(self.UITDAGINGEN)]
            dag["laatste_datum"] = vandaag
            dag["voltooid_vandaag"] = False
            dag["uitdaging_type"] = uitdaging["type"]
            dag["uitdaging_game"] = uitdaging["game"]
            dag["uitdaging_doel"] = uitdaging["doel"]
            dag["uitdaging_tekst"] = uitdaging["tekst"]
            dag["uitdaging_voortgang"] = 0
            _sla_op(self._data)

        return dag

    def _update_dagelijkse(self, game_id: str, gewonnen: bool):
        dag = self._p["dagelijkse"]
        vandaag = str(date.today())
        if dag.get("voltooid_vandaag") or dag.get("laatste_datum") != vandaag:
            return

        game_match = dag.get("uitdaging_game") == game_id
        type_ = dag.get("uitdaging_type", "")

        telt = False
        if type_ == "game" and game_match and gewonnen:
            telt = True
        elif type_ == "quiz" and game_match:
            telt = True  # quiz: telt ook als niet perfect, tenzij doel "perfect" is

        if telt:
            dag["uitdaging_voortgang"] = dag.get("uitdaging_voortgang", 0) + 1
            if dag["uitdaging_voortgang"] >= dag.get("uitdaging_doel", 1):
                dag["voltooid_vandaag"] = True
                dag["streak"] = dag.get("streak", 0) + 1
                self.geef_punten(25, "Dagelijkse uitdaging voltooid! 📅")
                print("\n\033[96m🎉 DAGELIJKSE UITDAGING VOLTOOID!\033[0m")
            _sla_op(self._data)

    # ── STATS & DISPLAY ──

    def _win_rate(self, game_id: str) -> float:
        s = self._p["stats"].get(game_id, {})
        g = s.get("gespeeld", 0)
        w = s.get("gewonnen", 0)
        return round(w / g * 100, 1) if g > 0 else 0.0

    def toon_stats(self):
        p = self._p
        print(f"\n\033[96m╔══════════════════════════════════════╗\033[0m")
        print(f"\033[96m║  📊 STATS VAN {self.speler.upper():<22}║\033[0m")
        print(f"\033[96m╚══════════════════════════════════════╝\033[0m")
        print(f"  Totaal punten:    \033[93m{p['punten']}\033[0m")
        print(f"  Games gespeeld:   {p['games_gespeeld']}")
        print(f"  Achievements:     {len(p['achievements'])}/{len(ACHIEVEMENTS)}")
        print()
        print("  \033[90mPer game:\033[0m")
        for gid, gnaam in GAME_NAMEN.items():
            s = p["stats"].get(gid, {})
            gs = s.get("gespeeld", 0)
            if gs == 0:
                continue
            gw = s.get("gewonnen", 0)
            wr = round(gw / gs * 100) if gs > 0 else 0
            print(f"    {gnaam:<22} {gs:>3}x gespeeld  {wr:>3}% gewonnen")
        print()
        if p["achievements"]:
            print("  \033[90mAchievements:\033[0m")
            for sleutel in p["achievements"]:
                ach = ACHIEVEMENTS.get(sleutel, {})
                print(f"    {ach.get('naam','?')}")

    def toon_dagelijkse(self):
        dag = self.get_dagelijkse_uitdaging()
        print(f"\n\033[96m📅 DAGELIJKSE UITDAGING\033[0m")
        print(f"  {dag.get('uitdaging_tekst','?')}")
        voortgang = dag.get("uitdaging_voortgang", 0)
        doel = dag.get("uitdaging_doel", 1)
        if dag.get("voltooid_vandaag"):
            print(f"  \033[92m✅ Voltooid! Streak: {dag.get('streak',0)} dagen\033[0m")
        else:
            print(f"  Voortgang: {voortgang}/{doel}")
            print(f"  Streak: {dag.get('streak',0)} dagen")

# ── LEADERBOARD ─────────────────────────────────────────────────

def toon_leaderboard(max_spelers: int = 10):
    data = _laad()
    if not data:
        print("Nog geen spelers.")
        return

    spelers = []
    for naam, profiel in data.items():
        punten = profiel.get("punten", 0)
        games = profiel.get("games_gespeeld", 0)
        ach = len(profiel.get("achievements", []))
        # Totaalscore: punten + bonus voor games en achievements
        score = punten + (games // 5) + (ach * 5)
        spelers.append((naam, score, punten, games, ach))

    spelers.sort(key=lambda x: x[1], reverse=True)

    print(f"\n\033[93m╔══════════════════════════════════════════════╗\033[0m")
    print(f"\033[93m║              🏆 LEADERBOARD                 ║\033[0m")
    print(f"\033[93m╚══════════════════════════════════════════════╝\033[0m")
    print(f"  {'#':<3} {'Naam':<15} {'Score':>6} {'Punten':>7} {'Games':>6} {'Ach.':>5}")
    print(f"  {'─'*50}")

    medals = ["🥇", "🥈", "🥉"]
    for i, (naam, score, punten, games, ach) in enumerate(spelers[:max_spelers]):
        medal = medals[i] if i < 3 else f" {i+1}."
        print(f"  {medal:<3} {naam:<15} {score:>6} {punten:>7} {games:>6} {ach:>5}")
    print()
