import os

import dash
import pandas as pd
from dash import html

from interface.src.components import shots_plot
from interface.src.components import shots_plot_dropdown
from settings import SHOTS_DATA_DIR

dash.register_page(
    __name__,
    path="/chute-ao-gol",
    title="Chute ao gol",
    name="Chute ao gol",
)
# TODO importar isso de um arquivo de settings

df_dict: dict[str, pd.DataFrame] = {}


for filename in os.listdir(SHOTS_DATA_DIR):
    league_name: str = filename[: filename.index("_")]
    df_dict[f"{league_name}_shots"] = pd.read_csv(f"{SHOTS_DATA_DIR}/{filename}")

layout = html.Div(
    [
        html.H2("Visualização dos gols e suas probabilidades", style={"textAlign": "center"}),
        html.Div(
            className="shots-plot",
            children=[
                shots_plot.render(df_dict=df_dict),
                shots_plot_dropdown.render(df_dict=df_dict),
            ],
        ),
    ]
)
