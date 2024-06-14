import pandas as pd
from dash import dcc
from dash import html

from settings import CLUBS_DICT

RANGE_SLIDER_MARKS: dict[int, str] = {
    0: "1950",
    5: "1960",
    10: "1970",
    15: "1980",
    20: "1990",
    25: "2000",
    30: "2010",
    35: "2020",
    40: "40%",
    45: "45%",
    50: "50%",
}


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
                clearable=False,
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
