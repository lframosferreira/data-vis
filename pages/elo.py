import os

import dash
import pandas as pd
from dash import html

from interface.src.components import elo_time_series_dropdown
from interface.src.components import elo_time_series_plot

dash.register_page(
    __name__,
    path="/elo-ratings",
    title="Visualizaçao de elos",
    name="Visualizaçao de elos",
)
# TODO importar isso de um arquivo de settings
ELO_DATA_DIR: str = "data/elo/"


df_dict: dict[str, pd.DataFrame] = {}
for filename in os.listdir(ELO_DATA_DIR):
    club_name: str = filename[: filename.index(".")]
    df_dict[club_name] = pd.read_csv(f"{ELO_DATA_DIR}/{filename}")


layout = html.Div(
    [
        html.H2("Futebol", style={"textAlign": "center"}),
        html.Div(
            className="elo-time-series-plot",
            children=[
                elo_time_series_dropdown.render(df_dict=df_dict),
                elo_time_series_plot.render(df_dict=df_dict),
            ],
        ),
    ]
)
