import pandas as pd
from dash import Dash, Input, Output, callback, dash_table, html

from . import elo_time_series_plot, elo_time_series_dropdown


def create_layout(app: Dash, df_dict: dict[str, pd.DataFrame]) -> html.Div:
    return html.Div(
        children=[
            html.H1("Projeto de Visualização de Dados", style={"textAlign": "center"}),
            html.H2("Futebol", style={"textAlign": "center"}),
            html.Div(
                className="elo-time-series-plot",
                children=[
                    elo_time_series_plot.render(app=app, df_dict=df_dict),
                    elo_time_series_dropdown.render(app=app, df_dict=df_dict),
                ],
            ),
        ]
    )