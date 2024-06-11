import pandas as pd
from dash import Dash, dcc, html
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
from dash import Dash, html, dash_table, dcc, callback, Output, Input

import os

teamsAndPositions: list[str] = [
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



def render(app: Dash, df_dict: dict[str, pd.DataFrame]) -> html.Div:
    return html.Div(
        [   
            html.Div(
                className="dropdowns-positions-container",
                children=[
                    dcc.Dropdown(
                        id="players-positions-dropdown",
                        multi=False,
                        placeholder="Selecione um jogador:",
                        options=list(df_dict["players_standard_statsP90"]["Jogador"]),
                        value=[],
                        clearable=True,
                        style={"margin-bottom": "10px", "margin-top": "10px"},
                    ),
                    dcc.Dropdown(
                        id="players-positions-mean-dropdown",
                        multi=True,
                        placeholder="Selecione uma posição ou time:",
                        options= teamsAndPositions,
                        value=[],
                        clearable=True,
                    ),
                ],
            ),
            dcc.Graph(
                id="radar-positions-plot",
                figure=go.Figure(data=go.Scatterpolar(
                    r=[0, 0, 0, 0, 0],
                    theta=["Non Penalty Expected Goals", "Progressive Carries", "Progressive Passes Received", "Goals Per 90 Minutes", "Expected Goals Per 90 Minutes"],
                    fill='toself',
                    name="Jogador"
                )),
            )
        ]
    )