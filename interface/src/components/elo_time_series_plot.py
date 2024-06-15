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
            html.H4("Evolução do Elo ao longo dos anos"),
            dcc.Graph(id="elo-evolution-chart"),
            html.P("Selecione um clube:"),
            dcc.Dropdown(
                id="ticker",
                multi=True,
                placeholder="Arsenal, Chelsea",
                options=list(options),
                value=[],
                clearable=True,
            ),
            html.Div(
                id="elo-slider-container",
                children=[
                    html.P(
                        "Selecione a faixa de anos desejada:",
                        style={"margin-right": "10px"},
                    ),
                    dcc.RangeSlider(
                        id="year-slider",
                        min=1955,
                        max=2024,
                        step=1,
                        value=[1955, 2024],
                        marks={year: str(year) for year in range(1955, 2025, 5)},
                    ),
                ],
                style={"margin-top": "15px"},
            ),
        ]
    )
