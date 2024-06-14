import pandas as pd
import plotly.graph_objects as go
from dash import Input
from dash import Output
from dash import callback
from dash import dcc
from dash import html

from settings import TEAMS_BRASILEIRAO


def render_players_dropdown(df_dict: dict[str, pd.DataFrame]) -> html.Div:
    @callback(
        Output("players-dropdown", "options"),
        Input("teams-dropdown", "value"),
        prevent_initial_call=True,
    )
    def update_players_dropdown(team):
        if team == "Todos os times":
            return list(df_dict["players_standard_statsP90"]["Jogador"])
        return list(
            df_dict["players_standard_statsP90"][
                df_dict["players_standard_statsP90"]["Equipe"] == team
            ]["Jogador"]
        )

    return html.Div()


def render(df_dict: dict[str, pd.DataFrame]) -> html.Div:
    return html.Div(
        [
            html.Div(
                className="dropdowns-container",
                children=[
                    dcc.Dropdown(
                        id="teams-dropdown",
                        multi=False,
                        placeholder="Selecione um time:",
                        options=TEAMS_BRASILEIRAO,
                        value=[],
                        clearable=True,
                        style={"margin-bottom": "10px", "margin-top": "10px"},
                    ),
                    dcc.Dropdown(
                        id="players-dropdown",
                        multi=True,
                        placeholder="Selecione um jogador:",
                        options=render_players_dropdown(df_dict),
                        value=[],
                        clearable=True,
                    ),
                ],
            ),
            dcc.Graph(
                id="radar-plot",
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
