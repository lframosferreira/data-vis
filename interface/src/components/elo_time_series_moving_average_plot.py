from dash import dcc
from dash import html


def render() -> html.Div:
    return html.Div(
        className="mb-5",
        children=[
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
        ]
    )
