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
            html.P("Selecione um valor para o comprimento da média móvel"),
            dcc.RadioItems(
                id="period-selector",
                options=[
                    {"label": "5", "value": 5},
                    {"label": "10", "value": 10},
                    {"label": "15", "value": 15},
                    {"label": "20", "value": 20},
                    {"label": "25", "value": 25},
                    {"label": "30", "value": 30},
                ],
                value=5,
                labelStyle={"display": "inline-block", "margin-right": "10px"},
                inputStyle={"margin-right": "5px"},
                style={"display": "inline-block", "text-align": "center"},
            ),
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
