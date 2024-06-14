import pandas as pd
from dash import Dash, dcc, html

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


def render(df_dict: dict[str, pd.DataFrame]) -> html.Div:
    options: list[str] = list(
        map(lambda x: CLUBS_DICT[x], filter(lambda x: x in CLUBS_DICT, df_dict.keys()))
    )
    return html.Div(
        [
            html.H4("Evolução do Elo ao longo dos anos"),
            dcc.Graph(id="elo-evolution-chart"),
            html.P("Selecione um clube:"),
            dcc.Dropdown(
                id="ticker",
                multi=True,
                placeholder="Arsenal",
                options=list(options),
                value=[],
                clearable=False,
            ),
        ]
    )
