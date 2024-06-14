# Constantes globais utilizadas entre os arquivos
SHOTS_DATA_DIR: str = "data/shots/"
BRASILEIRO_DATA_DIR: str = "data/brasileirao/"
ELO_DATA_DIR: str = "data/elo/"
RANK_DATA_DIR: str = "data/rank/"
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
    "lyon": "Olympique Lyonnais",
    "monaco": "AS Monaco",
    "parissg": "Paris Saint-Germain",
    "stuttgart": "VfB Stuttgart",
    "atletico": "Atlético Madrid",
}
CLUB_ELO_API: str = "http://api.clubelo.com"
REVERSED_CLUBS_DICT = {
    "Barcelona": "barcelona",
    "Real Madrid": "realmadrid",
    "Girona": "girona",
    "Chelsea": "chelsea",
    "Arsenal": "arsenal",
    "Tottenham Hotspur": "tottenham",
    "Everton": "everton",
    "Liverpool": "liverpool",
    "Manchester City": "mancity",
    "AFC Ajax": "ajax",
    "PSV Eindhoven": "psv",
    "Manchester United": "manunited",
    "RB Leipzig": "rbleipzig",
    "Bayern Munich": "bayern",
    "Borussia Dortmund": "dortmund",
    "Newcastle United": "newcastle",
    "West Ham United": "westham",
    "Bayer Leverkusen": "leverkusen",
    "VfL Wolfsburg": "wolfsburg",
    "Juventus": "juventus",
    "AC Milan": "milan",
    "Inter Milan": "inter",
    "Lazio": "lazio",
    "AS Roma": "roma",
    "Atalanta": "atalanta",
    "Bologna": "bologna",
    "Napoli": "napoli",
    "Fiorentina": "fiorentina",
    "Benfica": "benfica",
    "FC Porto": "porto",
    "SC Braga": "braga",
    "Sporting CP": "sporting",
    "Valencia": "valencia",
    "Sevilla": "sevilla",
    "Olympique Lyonnais": "lyon",
    "AS Monaco": "monaco",
    "Paris Saint-Germain": "parissg",
    "VfB Stuttgart": "stuttgart",
    "Atlético Madrid": "atletico",
}
TEAMS_BRASILEIRAO: list[str] = [
    "Todos os times",
    "América (MG)",
    "Ath Paranaense",
    "Atlético Mineiro",
    "Bahia",
    "Botafogo (RJ)",
    "Corinthians",
    "Coritiba",
    "Cruzeiro",
    "Cuiabá",
    "Flamengo",
    "Fluminense",
    "Fortaleza",
    "Goiás",
    "Grêmio",
    "Internacional",
    "Palmeiras",
    "Red Bull Bragantino",
    "Santos",
    "São Paulo",
    "Vasco da Gama",
]
TIMES_BRASILEIRAO_E_POSICOES: list[str] = [
    "América (MG)",
    "Ath Paranaense",
    "Atlético Mineiro",
    "Bahia",
    "Botafogo (RJ)",
    "Corinthians",
    "Coritiba",
    "Cruzeiro",
    "Cuiabá",
    "Flamengo",
    "Fluminense",
    "Fortaleza",
    "Goiás",
    "Grêmio",
    "Internacional",
    "Palmeiras",
    "Red Bull Bragantino",
    "Santos",
    "São Paulo",
    "Vasco da Gama",
    "G",
    "AT",
    "ZG",
    "LE",
    "LD",
    "CB",
    "LT",
    "MC",
    "ME",
    "MD",
    "GM",
    "PE",
    "PD",
    "MA",
]