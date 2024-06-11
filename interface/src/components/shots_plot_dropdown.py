import pandas as pd
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, exceptions, html

LEAGUES: list[str, str] = {
    "england": "Premier League",
    "spain": "La Liga",
    "germany": "Bundesliga",
    "italy": "Serie A",
    "france": "Ligue 1",
}

def render(app: Dash, df_dict: dict[str, pd.DataFrame]) -> None:
    @app.callback(Output("shots-players-dropdown", "options"), Input("league-dropdown", "value"))
    def populate_shots_dropdown(league: str):
        if league is None:
            raise exceptions.PreventUpdate
        
        league_key = next((key for key, value in LEAGUES.items() if value == league), None)
        if league_key is None:
            raise exceptions.PreventUpdate
        
        shots = df_dict[f"{league_key}_shots"]
        filtered_shots = shots[(shots["xG"] < 0.3) & (shots["result_name"] == "success")]

        player_names = filtered_shots['player_name'].unique()
        player_options = [{"label": name, "value": name} for name in player_names]
        return player_options

    return html.Div(
        children=[   
            html.Hr(style={"margin-top": "50px", "margin-bottom": "50px"}),
            html.H2("Gols com menos de 30% de chance feitos pelo jogador", style={"textAlign": "center", "margin-bottom": "50px"}),
            dcc.Dropdown(
                id="league-dropdown",
                multi=False,
                placeholder="Selecione a liga",
                options=list(LEAGUES.values()),
                clearable=True,
                searchable=False,
                style={"margin-bottom": "10px", "margin-top": "10px"},
            ),
            dcc.Dropdown(
                id="shots-players-dropdown",
                multi=False,
                placeholder="Selecione um jogador",
                options=[],
                clearable=True,
                disabled=False,
                style={"margin-bottom": "10px"},
            ),
            html.Div(
                style={"display": "flex", "justify-content": "center", "align-items": "center", "flex-direction": "column"},
                children=[html.Iframe(
                    id="shots-plot",
                    srcDoc=None, 
                    style={"width": "700px", "height": "500px", "display": "flex", "borderWidth": "0px"},),
                ],
            ),
        ]
    )