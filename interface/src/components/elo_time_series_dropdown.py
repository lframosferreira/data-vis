import pandas as pd
import plotly.graph_objects as go
from dash import Dash, Input, Output, exceptions


def render(app: Dash, df_dict: dict[str, pd.DataFrame]) -> None:
    @app.callback(Output("elo-evolution-chart", "figure"), Input("ticker", "value"))
    def display_time_series(ticker):
        if len(ticker) == 0:
            raise exceptions.PreventUpdate
        fig = go.Figure()
        for club in ticker:
            df = df_dict[club]
            fig.add_trace(
                go.Scatter(
                    x=df["From"],
                    y=df["Elo"],
                    mode="lines",
                    name=CLUBS_DICT[club],
                )
            )
        fig.update_layout(xaxis_title="Ano", yaxis_title="Elo")
        return fig
