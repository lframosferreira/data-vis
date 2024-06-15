import pandas as pd
import plotly.graph_objects as go
from dash import dcc
from dash import html


def render(df_dict: dict[str, pd.DataFrame]) -> html.Div:
    return html.Div(
        [
            html.Div(
                className="dropdowns-moving-avarages-container",
                children=[
                    dcc.Dropdown(
                        id="teams-moving-avarages-dropdown",
                        multi=False,
                        placeholder="Selecione um time:",
                        options=df_dict["sportsref"]["Home"].unique(),
                        value=[],
                        clearable=True,
                        style={"margin-bottom": "10px", "margin-top": "10px"},
                    ),
                    dcc.RadioItems(
                        [
                            {"label": " Janela de 5", "value": 5},
                            {"label": " Janela de 10", "value": 10},
                            {"label": " Janela de 15", "value": 15},
                        ],
                        value=5,
                        id="teams-moving-avarages-window-radio",
                        style={
                            "margin-bottom": "10px",
                            "margin-top": "10px",
                        },
                    ),
                    html.P(
                        "As seŕies temporais com janela móvel maiores possuem grau de informação maior, já janelas menores possuem mais informação local",
                        style={"textAlign": "start", "margin-top": "5px"},
                    ),
                ],
            ),
            dcc.Graph(
                id="moving-avarages-plot",
                figure=go.Figure(data=go.Scatter()),
            ),
        ]
    )
