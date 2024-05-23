import os

import requests

if not os.path.exists("data/"):
    os.mkdir("data")

if not os.path.exists("data/elo/"):
    os.mkdir("data/elo")

CLUBS_LIST: list[str] = [
    "barcelona",
    "realmadrid",
    "girona",
    "chelsea",
    "arsenal",
    "tottenham",
    "everton",
    "liverpool",
    "mancity",
    "ajax",
    "psv",
    "manunited",
    "rbleipzig",
    "bayern",
    "dortmund",
    "newcastle",
    "westham",
    "leverkusen",
    "wolfsburg",
    "juventus",
    "milan",
    "inter",
    "lazio",
    "roma",
    "atalanta",
    "bologna",
    "napoli",
    "fiorentina",
    "benfica",
    "porto",
    "braga",
    "sporting",
    "valencia",
    "sevilla",
    "vilarreal",
    "lyon",
    "monaco",
    "parissg",
    "stuttgart",
    "atletico",
]

CLUB_ELO_API: str = "http://api.clubelo.com"

for club in CLUBS_LIST:
    if os.path.exists(f"data/elo/{club}.csv"):
        continue
    url_data = requests.get(f"{CLUB_ELO_API}/{club}").content
    with open(f"data/elo/{club}.csv", "wb") as f:
        f.write(url_data)
