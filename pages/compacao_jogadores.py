import os

import dash
import pandas as pd
from dash import html

from interface.src.components import radar_plot_players
from interface.src.components import radar_plot_players_dropdown
from interface.src.components import radar_plot_positions
from interface.src.components import radar_plot_positions_dropdown
from settings import BRASILEIRO_DATA_DIR

dash.register_page(
    __name__,
    path="/comparacao-jogadores",
    title="Comparar jogadores",
    name="Comparar jogadores",
)

df_dict: dict[str, pd.DataFrame] = {}

for filename in os.listdir(BRASILEIRO_DATA_DIR):
    club_name: str = filename[: filename.index(".")]
    df_dict[club_name] = pd.read_csv(f"{BRASILEIRO_DATA_DIR}/{filename}")

layout = html.Div(
    [
        html.H2("RadarPlot", style={"textAlign": "center"}),
        html.H3("Comparação entre jogadores", style={"textAlign": "center"}),
        html.Div(
            className="radar-plot",
            children=[
                radar_plot_players_dropdown.render(df_dict=df_dict),
                radar_plot_players.render(df_dict=df_dict),
            ],
        ),
        html.H3("Comparação entre jogador e posição", style={"textAlign": "center"}),
        html.Div(
            className="radar-position-plot",
            children=[
                radar_plot_positions_dropdown.render(df_dict=df_dict),
                radar_plot_positions.render(df_dict=df_dict),
            ],
        ),
    ]
)
