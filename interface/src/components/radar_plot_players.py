import pandas as pd
from dash import Dash, dcc, html
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
from dash import Dash, html, dash_table, dcc, callback, Output, Input

import os

teams: list[str] = [
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

def renderPlayersDropdown(app: Dash, df_dict: dict[str, pd.DataFrame]) -> html.Div:
    @app.callback(Output("players-dropdown", "options"), Input("teams-dropdown", "value"),prevent_initial_call=True)
    def update_players_dropdown(team):
        if team == "Todos os times":
            return list(df_dict["players_standard_statsP90"]["Jogador"])
        return list(df_dict["players_standard_statsP90"][df_dict["players_standard_statsP90"]["Equipe"] == team]["Jogador"])
    return []

def render(app: Dash, df_dict: dict[str, pd.DataFrame]) -> html.Div:
    return html.Div(
        [   
            html.Div(
                className="dropdowns-container",
                children=[
                    dcc.Dropdown(
                        id="teams-dropdown",
                        multi=False,
                        placeholder="Selecione um time:",
                        options=teams,
                        value=[],
                        clearable=True,
                        style={"margin-bottom": "10px", "margin-top": "10px"},
                    ),
                    dcc.Dropdown(
                        id="players-dropdown",
                        multi=True,
                        placeholder="Selecione um jogador:",
                        options= renderPlayersDropdown(app, df_dict),
                        value=[],
                        clearable=True,
                    ),
                ],
            ),
            dcc.Graph(
                id="radar-plot",
                figure=go.Figure(data=go.Scatterpolar(
                    r=[0, 0, 0, 0, 0],
                    theta=["Non Penalty Expected Goals", "Progressive Carries", "Progressive Passes Received", "Goals Per 90 Minutes", "Expected Goals Per 90 Minutes"],
                    fill='toself',
                    name="Jogador"
                )),
            )
        ]
    )