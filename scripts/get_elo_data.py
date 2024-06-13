import os

import requests

if not os.path.exists("data/"):
    os.mkdir("data")

if not os.path.exists("data/elo/"):
    os.mkdir("data/elo")

CLUBS_DICT: dict[str, str] = {
    "barcelona": "Barcelona",
    "realmadrid": "Real Madrid",
    "girona": "Girona",
    "chelsea": "Chelsea",
    "arsenal": "Arsenal",
    "tottenham": "Tottenham Hotspur",
    "everton": "Everton",
    "liverpool": "Liverpool",
    "mancity": "Manchester City",
    "ajax": "AFC Ajax",
    "psv": "PSV Eindhoven",
    "manunited": "Manchester United",
    "rbleipzig": "RB Leipzig",
    "bayern": "Bayern Munich",
    "dortmund": "Borussia Dortmund",
    "newcastle": "Newcastle United",
    "westham": "West Ham United",
    "leverkusen": "Bayer Leverkusen",
    "wolfsburg": "VfL Wolfsburg",
    "juventus": "Juventus",
    "milan": "AC Milan",
    "inter": "Inter Milan",
    "lazio": "Lazio",
    "roma": "AS Roma",
    "atalanta": "Atalanta",
    "bologna": "Bologna",
    "napoli": "Napoli",
    "fiorentina": "Fiorentina",
    "benfica": "Benfica",
    "porto": "FC Porto",
    "braga": "SC Braga",
    "sporting": "Sporting CP",
    "valencia": "Valencia",
    "sevilla": "Sevilla",
    "vilarreal": "Villarreal",
    "lyon": "Olympique Lyonnais",
    "monaco": "AS Monaco",
    "parissg": "Paris Saint-Germain",
    "stuttgart": "VfB Stuttgart",
    "atletico": "Atlético Madrid",
}

CLUB_ELO_API: str = "http://api.clubelo.com"

for club in CLUBS_DICT.keys():
    if os.path.exists(f"data/elo/{club}.csv"):
        continue
    url_data = requests.get(f"{CLUB_ELO_API}/{club}").content
    with open(f"data/elo/{club}.csv", "wb") as f:
        f.write(url_data)
