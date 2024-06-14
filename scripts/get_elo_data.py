import os

import requests

from settings import CLUB_ELO_API
from settings import CLUBS_DICT

if not os.path.exists("data/"):
    os.mkdir("data")

if not os.path.exists("data/elo/"):
    os.mkdir("data/elo")

for club in CLUBS_DICT:
    if os.path.exists(f"data/elo/{club}.csv"):
        continue
    url_data = requests.get(f"{CLUB_ELO_API}/{club}").content
    with open(f"data/elo/{club}.csv", "wb") as f:
        f.write(url_data)
