import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import Input
from dash import Output
from dash import callback
from dash import exceptions


def make_radar_plot(df_dict: dict[str, pd.DataFrame], player, fig) -> go.Figure:
    df: pd.DataFrame = df_dict["players_standard_statsP90"]
    jogador_series: pd.Series = df[(df["Jogador"] == f"{player}")]
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

    values: np.array = jogador_series[names].to_numpy()[0]

    fig.add_trace(
        go.Scatterpolar(
            r=values, theta=descriptive_names, fill="toself", name=f"{player}"
        )
    )

    fig.update_layout(
        polar={
            "radialaxis": {"visible": True},
        },
        showlegend=True,
        template="seaborn",
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
