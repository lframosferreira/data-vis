import pandas as pd
from dash import Dash, dcc, html


def render(app: Dash, df_dict: dict[str, pd.DataFrame]) -> html.Div:
    return html.Div(
        [
            html.H4("Evolução do Elo ao longo dos anos"),
            dcc.Graph(id="elo-evolution-chart"),
            html.P("Selecione um clube:"),
            dcc.Dropdown(
                id="ticker",
                multi=True,
                placeholder="Arsenal",
                options=list(df_dict.keys()),
                value=[],
                clearable=False,
            ),
        ]
    )
