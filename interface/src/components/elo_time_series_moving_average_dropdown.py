import pandas as pd
import plotly.graph_objects as go
from dash import Input
from dash import Output
from dash import callback
from dash import exceptions

from settings import REVERSED_CLUBS_DICT


def render(df_dict: dict[str, pd.DataFrame]) -> None:
    @callback(
        [
            Output(
                "elo-moving-average-evolution-chart", "figure", allow_duplicate=True
            ),
            Output("ticker-moving-average", "value"),
        ],
        Input("period-selector", "value"),
        prevent_initial_call=True,
    )
    def apply_moving_average(period):
        # clear plot and dropdown values
        fig = go.Figure()
        fig.update_layout(xaxis_title="Ano", yaxis_title="Elo")
        return fig, []

    @callback(
        Output("elo-moving-average-evolution-chart", "figure"),
        [Input("ticker-moving-average", "value"), Input("period-selector", "value")],
    )
    def display_time_series(ticker, period):
        if len(ticker) == 0:
            raise exceptions.PreventUpdate
        fig = go.Figure()
        for club in ticker:
            club_df = df_dict[REVERSED_CLUBS_DICT[club]]
            fig.add_trace(
                go.Scatter(
                    x=club_df["From"],
                    y=club_df["Elo"].rolling(period).mean(),
                    mode="lines",
                    name=club,
                )
            )
        fig.update_layout(xaxis_title="Ano", yaxis_title="Elo")
        return fig
