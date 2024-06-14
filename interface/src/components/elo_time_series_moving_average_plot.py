import pandas as pd
from dash import dcc
from dash import html

from settings import CLUBS_DICT


def render(df_dict: dict[str, pd.DataFrame]) -> html.Div:
    options: list[str] = [
        CLUBS_DICT[x] for x in filter(lambda x: x in CLUBS_DICT, df_dict.keys())
    ]
    return html.Div(
        [
            html.H4("Média móvel de variação de Elo ao longo dos anos"),
            dcc.Graph(id="elo-moving-average-evolution-chart"),
            html.P("Selecione um clube:"),
            dcc.Dropdown(
                id="ticker-moving-average",
                multi=True,
                placeholder="Arsenal, Chelsea",
                options=list(options),
                value=[],
                clearable=True,
            ),
        ]
    )
