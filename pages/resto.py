import dash
from dash import html, dcc, callback, Input, Output
import pandas as pd
import os

from interface.src.components import elo_time_series_plot, elo_time_series_dropdown, radar_plot_players, radar_plot_players_dropdown, radar_plot_positions_dropdown, radar_plot_positions, shots_plot, shots_plot_dropdown
from interface.src.components  import shots_plot_dropdown

dash.register_page(__name__)
# TODO importar isso de um arquivo de settings
ELO_DATA_DIR: str = "data/elo/"
BRASILEIRO_DATA_DIR: str = "data/brasileirao/"
SHOTS_DATA_DIR: str = "data/shots/"

df_dict: dict[str, pd.DataFrame] = {}
for filename in os.listdir(ELO_DATA_DIR):
    club_name: str = filename[: filename.index(".")]
    df_dict[club_name] = pd.read_csv(f"{ELO_DATA_DIR}/{filename}")

for filename in os.listdir(BRASILEIRO_DATA_DIR):
    club_name: str = filename[: filename.index(".")]
    df_dict[club_name] = pd.read_csv(f"{BRASILEIRO_DATA_DIR}/{filename}")

for filename in os.listdir(SHOTS_DATA_DIR):
    league_name: str = filename[: filename.index("_")]
    df_dict[f"{league_name}_shots"] = pd.read_csv(f"{SHOTS_DATA_DIR}/{filename}")

layout = html.Div([
   html.H1("Projeto de Visualização de Dados", style={"textAlign": "center"}),
            html.H2("Futebol", style={"textAlign": "center"}),
            html.Div(
                className="elo-time-series-plot",
                children=[
                    elo_time_series_dropdown.render(df_dict=df_dict),
                    elo_time_series_plot.render(df_dict=df_dict),
                ],
            ),
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
            html.Div(
                className="shots-plot",
                children=[
                    shots_plot.render(df_dict=df_dict),
                    shots_plot_dropdown.render(df_dict=df_dict),
                ],
            ),
])