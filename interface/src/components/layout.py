import pandas as pd
from dash import Dash, html

from . import elo_time_series_plot, elo_time_series_dropdown, radar_plot_players, radar_plot_players_dropdown, radar_plot_positions_dropdown, radar_plot_positions, shots_plot
from . import shots_plot_dropdown


def create_layout(app: Dash, df_dict: dict[str, pd.DataFrame]) -> html.Div:
    return html.Div(
        style={"display": "flex", "margin-right":"10%","margin-left": "10%","flex-direction":"column"},
        children=[
            html.H1("Projeto de Visualização de Dados", style={"textAlign": "center"}),
            html.H2("Futebol", style={"textAlign": "center"}),
            html.Div(
                className="elo-time-series-plot",
                children=[
                    elo_time_series_dropdown.render(app=app, df_dict=df_dict),
                    elo_time_series_plot.render(app=app, df_dict=df_dict),
                ],
            ),
            html.H2("RadarPlot", style={"textAlign": "center"}),
            html.H3("Comparação entre jogadores", style={"textAlign": "center"}),
            html.Div(
                className="radar-plot",
                children=[
                    radar_plot_players_dropdown.render(app=app, df_dict=df_dict),
                    radar_plot_players.render(app=app, df_dict=df_dict),
                ],
            ),
            html.H3("Comparação entre jogador e posição", style={"textAlign": "center"}),
            html.Div(
                className="radar-position-plot",
                children=[
                    radar_plot_positions_dropdown.render(app=app, df_dict=df_dict),
                    radar_plot_positions.render(app=app, df_dict=df_dict),
                ],
            ),
            html.Div(
                className="shots-plot",
                children=[
                    shots_plot.render(app=app, df_dict=df_dict),
                    shots_plot_dropdown.render(app=app, df_dict=df_dict),
                ],
            ),
        ]
    )