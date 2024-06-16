import os

import dash
import pandas as pd
from dash import dcc
from dash import html

from interface.src.components import elo_time_series_dropdown
from interface.src.components import elo_time_series_moving_average_dropdown
from interface.src.components import elo_time_series_moving_average_plot
from interface.src.components import elo_time_series_plot
from settings import ELO_DATA_DIR

dash.register_page(
    __name__,
    path="/elo-ratings",
    title="Visualização de elos",
    name="Visualização de elos",
)

df_dict: dict[str, pd.DataFrame] = {}
for filename in os.listdir(ELO_DATA_DIR):
    club_name: str = filename[: filename.index(".")]
    df_dict[club_name] = pd.read_csv(f"{ELO_DATA_DIR}/{filename}")

markdown_content_elo: str = ""
with open("pages_content/elo_normal.md") as f:
    markdown_content_elo = f.read()

markdown_content_elo_moving_avg: str = ""
with open("pages_content/elo_media_movel.md") as f:
    markdown_content_elo_moving_avg = f.read()

layout = html.Div(
    [
        html.H2("Elo no futebol", style={"textAlign": "center"}),
        dcc.Markdown(children=markdown_content_elo, style={"textAlign": "justify"}),
        html.Div(
            className="elo-time-series-plot",
            children=[
                elo_time_series_dropdown.render(df_dict=df_dict),
                elo_time_series_plot.render(df_dict=df_dict),
            ],
        ),
        html.Br(),
        dcc.Markdown(
            children=markdown_content_elo_moving_avg, style={"textAlign": "justify"}
        ),
        html.Div(
            className="elo-time-series-moving-average-plot",
            children=[
                elo_time_series_moving_average_plot.render(),
                elo_time_series_moving_average_dropdown.render(df_dict=df_dict),
            ],
        ),
    ]
)
