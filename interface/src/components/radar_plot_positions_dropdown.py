from dash import Dash, html, dash_table, dcc, Output, Input
import pandas as pd
import plotly.express as px

import pandas as pd
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, exceptions, html, callback

import numpy as np

teamns: list[str] = [
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


def make_radar_plot(df_dict: dict[str, pd.DataFrame], player, fig) -> go.Figure:
    df: pd.DataFrame = df_dict["players_standard_statsP90"]
    jogadorSeries: pd.Series = df[
        (df["Jogador"] == f"{player}")
    ]  # & (df["Equipe"] == "Atlético Mineiro")]
    names = ["npxG", "PrgC", "PrgR", "Gols", "xG"]

    descriptive_names: np.array = np.array(
        [
            "Non Penalty Expected Goals",
            "Progressive Carries",
            "Progressive Passes Received",
            "Goals Per 90 Minutes",
            "Expected Goals Per 90 Minutes",
        ]
    )

    values: np.array = jogadorSeries[names].to_numpy()[0]

    fig.add_trace(
        go.Scatterpolar(
            r=values, theta=descriptive_names, fill="toself", name=f"{player}"
        )
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True),
        ),
        showlegend=True,
    )

    return fig


def make_mean_radar_plot(df_dict, ticker, fig) -> go.Figure:
    df: pd.DataFrame = df_dict["players_standard_statsP90"]
    jogadorSeries: pd.Series
    descriptive_names: np.array = np.array(
        [
            "Non Penalty Expected Goals",
            "Progressive Carries",
            "Progressive Passes Received",
            "Goals Per 90 Minutes",
            "Expected Goals Per 90 Minutes",
        ]
    )
    names = ["npxG", "PrgC", "PrgR", "Gols", "xG"]

    for selected in ticker:
        if selected in teamns:
            jogadorSeries: pd.Series = df[(df["Equipe"] == f"{selected}")]
            values: np.array = jogadorSeries[names].mean().to_numpy()
            fig.add_trace(
                go.Scatterpolar(
                    r=values, theta=descriptive_names, fill="toself", name=f"{selected}"
                )
            )
        else:
            jogadorSeries: pd.Series = df[(df["Pos."] == f"{selected}")]
            values: np.array = jogadorSeries[names].mean().to_numpy()
            fig.add_trace(
                go.Scatterpolar(
                    r=values, theta=descriptive_names, fill="toself", name=f"{selected}"
                )
            )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True),
        ),
        showlegend=True,
    )

    return fig


def render(df_dict: dict[str, pd.DataFrame]) -> None:
    @callback(
        Output("radar-positions-plot", "figure"),
        [
            Input("players-positions-dropdown", "value"),
            Input("players-positions-mean-dropdown", "value"),
        ],
        prevent_initial_call=True,
    )
    def display_radar_plot(ticker, ticker2):
        if ticker and len(ticker) == 0:
            raise exceptions.PreventUpdate
        fig = go.Figure()
        if ticker:
            fig = make_radar_plot(df_dict, ticker, fig)

        if ticker2 and len(ticker2) == 0:
            raise exceptions.PreventUpdate
        if ticker2:
            fig = make_mean_radar_plot(df_dict, ticker2, fig)
        return fig
