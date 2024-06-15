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
        html.H2("Comparação entre jogador e posição", style={"textAlign": "center"}),
        html.P(
            "Essa visualização tem como objetivo facilitar a comparação entre as métricas de um jogador específico com uma posição ou time. A métrica usada é a média simples dos valores dos outros jogadores daquele time ou posição.",
            style={"textAlign": "start", "margin-bottom": "30px", "margin-top": "30px"},
        ),
        html.Div(
            className="radar-position-plot",
            children=[
                radar_plot_positions_dropdown.render(df_dict=df_dict),
                radar_plot_positions.render(df_dict=df_dict),
            ],
        ),
        html.H2("Comparação entre jogadores", style={"textAlign": "center"}),
        html.P(
            "Essa visualização tem como objetivo facilitar a comparação entre as métricas entre jogadores.",
            style={"textAlign": "start", "margin-bottom": "30px", "margin-top": "30px"},
        ),
        html.Div(
            className="radar-plot",
            children=[
                radar_plot_players_dropdown.render(df_dict=df_dict),
                radar_plot_players.render(df_dict=df_dict),
            ],
        ),
    ]
)
