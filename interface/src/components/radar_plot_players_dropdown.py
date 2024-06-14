import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import Input
from dash import Output
from dash import callback
from dash import exceptions

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


def render(df_dict: dict[str, pd.DataFrame]) -> None:
    @callback(Output("radar-plot", "figure"), Input("players-dropdown", "value"))
    def display_time_series(ticker):
        if len(ticker) == 0:
            raise exceptions.PreventUpdate
        fig = go.Figure()
        for jogador in ticker:
            fig = make_radar_plot(df_dict, jogador, fig)
        return fig
