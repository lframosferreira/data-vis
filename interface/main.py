import io

import numpy as np
import pandas as pd
import plotly.express as px
import requests
from dash import Dash, Input, Output, dcc, html, exceptions
import plotly.graph_objects as go

CLUB_ELO_API: str = "http://api.clubelo.com"
CLUB: str = "arsenal"


def main() -> None:
    app = Dash()
    app.title = "Quem tem medo pula fora"

    # url_data = requests.get(f"{CLUB_ELO_API}/{CLUB}").content
    # df = pd.read_csv(io.StringIO(url_data.decode("utf-8")))
    df_dict = {}
    df_dict[CLUB] = pd.read_csv("saida.csv")

    app.layout = html.Div(
        [
            html.H4("Evolução do Elo"),
            dcc.Graph(id="elo-evolution-chart"),
            html.P("Select stock:"),
            dcc.Dropdown(
                id="ticker",
                multi=True,
                placeholder="Selecione um clube",
                options=list(df_dict.keys()),
                value=[],
                clearable=False,
            ),
        ]
    )

    @app.callback(Output("elo-evolution-chart", "figure"), Input("ticker", "value"))
    def display_time_series(ticker):
        if len(ticker) == 0:
            raise exceptions.PreventUpdate
        fig = go.Figure()
        for club in ticker:
            df = df_dict[club]
            fig.add_trace(
                go.Scatter(x=df["From"], y=df["Elo"], mode="lines", name=club)
            )
            max_y = df["Elo"].max()
            fig.add_annotation(x=df["From"].iloc[-1], y=max_y, text=club)
        fig.update_layout(title="vasco", xaxis_title="Ano", yaxis_title="Elo")
        return fig

    app.run(debug=True)


if __name__ == "__main__":
    main()
