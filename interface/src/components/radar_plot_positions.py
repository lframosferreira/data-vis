import pandas as pd
import plotly.graph_objects as go
from dash import dcc
from dash import html

from settings import TIMES_BRASILEIRAO_E_POSICOES


def render(df_dict: dict[str, pd.DataFrame]) -> html.Div:
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
                        options=TIMES_BRASILEIRAO_E_POSICOES,
                        value=[],
                        clearable=True,
                    ),
                ],
            ),
            dcc.Graph(
                id="radar-positions-plot",
                figure=go.Figure(
                    data=go.Scatterpolar(
                        r=[0, 0, 0, 0, 0],
                        theta=[
                            "Non Penalty Expected Goals",
                            "Progressive Carries",
                            "Progressive Passes Received",
                            "Goals Per 90 Minutes",
                            "Expected Goals Per 90 Minutes",
                        ],
                        fill="toself",
                        name="Jogador",
                    )
                ),
            ),
        ]
    )
