import os

import pandas as pd
from interface.src.components import moving_avarages
from interface.src.components import moving_avarages_dropdown
from settings import BRASILEIRO_DATA_DIR

import plotly.graph_objects as go



import dash
from dash import Input
from dash import Output
from dash import callback
from dash import dcc
from dash import html

dash.register_page(
    __name__,
    path="/gols-esperados",
    title="gols-esperados",
    name="Gols Esperados",
)

df_dict: dict[str, pd.DataFrame] = {}

for filename in os.listdir(BRASILEIRO_DATA_DIR):
    club_name: str = filename[: filename.index(".")]
    df_dict[club_name] = pd.read_csv(f"{BRASILEIRO_DATA_DIR}/{filename}")

df_dict["sportsref"].drop(columns=["Day", "Time", "Date", "Attendance", "Venue", "Referee", "Match Report", "Notes"], inplace=True)
df_dict["sportsref"].rename(columns={"xG": "xG_Home", "xG.1": "xG_Away"}, inplace=True)
df_dict["sportsref"]["xG_diff"] = df_dict["sportsref"]["xG_Home"] - df_dict["sportsref"]["xG_Away"]


layout = html.Div(
    [
        html.H2("Comparação da expectativa de gols entre um time e seus adversários no campeonato", style={"textAlign": "center"}),
        html.P("Essa visualização calcula a chance de um time fazer ou tomar um gol a partir de uma janela móvel com base nas rodadas do campeonato.", style={"textAlign": "start", "margin-bottom": "30px","margin-top": "30px"}),
        html.Div(
            className="radar-position-plot",
            children=[
                moving_avarages_dropdown.render(df_dict=df_dict),
                moving_avarages.render(df_dict=df_dict),
            ],
        ),
    ]
)
