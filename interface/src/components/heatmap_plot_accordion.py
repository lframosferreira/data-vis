import matplotlib.pyplot as plt
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input
from dash import Output
from dash import callback
from dash import dcc
from dash import html
from settings import LEAGUES


def render(df_dict: dict[str, pd.DataFrame], spadl_dict: dict[str, pd.DataFrame]) -> html.Div:
    return html.Div(
        style={"margin-bottom": "50px"},
        children=[
            dbc.Accordion(
                [
                    dbc.AccordionItem(
                        [
                            html.Div(
                                style={
                                    "display": "flex",
                                    "justify-content": "center",
                                    "align-items": "center",
                                    "flex-direction": "column",
                                    "margin-top": "20px",
                                    "height": "500px",
                                },
                                children=html.Iframe(
                                    id="heatmap-plot",
                                    srcDoc=None,
                                    style={
                                        "display": "flex",
                                        "width": "100%",
                                        "height": "100%",
                                        "borderWidth": "0px",
                                    },
                                ),
                            )
                        ],
                        title="Heatmap de ações na partida",
                    ),
                ],
                start_collapsed=True,
            ),
        ]
    )
