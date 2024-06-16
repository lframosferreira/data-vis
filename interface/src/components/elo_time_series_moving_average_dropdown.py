import pandas as pd
import plotly.graph_objects as go
from dash import Input
from dash import Output
from dash import callback

from settings import REVERSED_CLUBS_DICT


def render(df_dict: dict[str, pd.DataFrame]) -> None:
    @callback(
        Output("elo-moving-average-evolution-chart", "figure"),
        [Input("ticker", "value"), Input("period-selector", "value")],
    )
    def display_time_series(ticker, period):
        fig = go.Figure()
        fig.update_layout(xaxis_title="Ano", yaxis_title="Média móvel do valor de Elo")
        if len(ticker) == 0:
            return fig
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
        return fig
