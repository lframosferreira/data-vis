import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import Input
from dash import Output
from dash import callback
from dash import exceptions

from settings import TEAMS_BRASILEIRAO


def make_radar_plot(df_dict: dict[str, pd.DataFrame], player, fig) -> go.Figure:
    df: pd.DataFrame = df_dict["players_standard_statsP90"]
    df = df.drop(df[df['npxG'] == 0 or df['PrgC'] == 0 or df['PrgR'] == 0].index)
    
    jogador_series: pd.Series = df[
        (df["Jogador"] == f"{player}")
    ]
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
    )

    return fig


def make_mean_radar_plot(df_dict, ticker, fig) -> go.Figure:
    df: pd.DataFrame = df_dict["players_standard_statsP90"]
    df = df.drop(df[df['npxG'] == 0 or df['PrgC'] == 0 or df['PrgR'] == 0].index)
    
    jogador_series: pd.Series
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
        if selected in TEAMS_BRASILEIRAO:
            jogador_series: pd.Series = df[(df["Equipe"] == f"{selected}")]
            values: np.array = jogador_series[names].mean().to_numpy()
            fig.add_trace(
                go.Scatterpolar(
                    r=values, theta=descriptive_names, fill="toself", name=f"{selected}"
                )
            )
        else:
            jogador_series: pd.Series = df[(df["Pos."] == f"{selected}")]
            values: np.array = jogador_series[names].mean().to_numpy()
            fig.add_trace(
                go.Scatterpolar(
                    r=values, theta=descriptive_names, fill="toself", name=f"{selected}"
                )
            )

    fig.update_layout(
        polar={
            "radialaxis": {"visible": True},
        },
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
