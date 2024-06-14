import pandas as pd
import plotly.graph_objects as go
from dash import Input
from dash import Output
from dash import callback
from dash import exceptions

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
    "Villarreal": "vilarreal",
    "Olympique Lyonnais": "lyon",
    "AS Monaco": "monaco",
    "Paris Saint-Germain": "parissg",
    "VfB Stuttgart": "stuttgart",
    "Atlético Madrid": "atletico",
}


def render(df_dict: dict[str, pd.DataFrame]) -> None:
    @callback(Output("elo-evolution-chart", "figure"), Input("ticker", "value"))
    def display_time_series(ticker):
        if len(ticker) == 0:
            raise exceptions.PreventUpdate
        fig = go.Figure()
        for club in ticker:
            df = df_dict[REVERSED_CLUBS_DICT[club]]
            fig.add_trace(
                go.Scatter(x=df["From"], y=df["Elo"], mode="lines", name=club)
            )
        fig.update_layout(xaxis_title="Ano", yaxis_title="Elo")
        return fig
