import pandas as pd
from dash import Input
from dash import Output
from dash import callback
from dash import dcc
from dash import html

LEAGUES: dict[str, str] = {
    "england": "Premier League",
    "spain": "La Liga",
    "germany": "Bundesliga",
    "italy": "Serie A",
    "france": "Ligue 1",
}

PROBABILITY_THRESHOLD = 0.3

RANGE_SLIDER_MARKS = {
    0: '0%',
    5: '5%',
    10: '10%',
    15: '15%',
    20: '20%',
    25: '25%',
    30: '30%',
    35: '35%',
    40: '40%',
    45: '45%',
    50: '50%',
}

def render(df_dict: dict[str, pd.DataFrame]) -> None:
    @callback(
            Output("shots-players-dropdown", "options"),
        Input("league-dropdown", "value"),
    )
    def populate_shots_dropdown(league: str):
        if league is None:
            return []

        league_key = next(
            (key for key, value in LEAGUES.items() if value == league), None
        )
        if league_key is None:
            return []

        shots = df_dict[f"{league_key}_shots"]
        filtered_shots = shots[
            (shots["xG"] < PROBABILITY_THRESHOLD) & (shots["result_name"] == "success")
        ]

        player_names = filtered_shots["player_name"].unique()
        player_options = [{"label": name, "value": name} for name in player_names]
        return player_options

    return html.Div(
        children=[
            html.Hr(style={"margin-top": "30px", "margin-bottom": "30px"}),
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
                style={ "margin-bottom": "10px"},
            ),
            html.Div(
                id="shoot-slider-container",
                children=[
                    html.P(
                        "Selecione a faixa de probabilidade de gol:",
                        style={"margin-right": "10px"},
                    ),
                    dcc.RangeSlider(
                        id='shoot-range-slider',
                        min=0,
                        max=50,
                        value=[0, 30],
                        step=5,
                        marks=RANGE_SLIDER_MARKS,
                        disabled=False,
                    ),
                ],
                style={"margin-top": "15px"},
            ),
            html.Div(
                style={
                    "display": "flex",
                    "justify-content": "center",
                    "align-items": "center",
                    "flex-direction": "column",
                    "margin-top": "20px",
                },
                children=[
                    html.Iframe(
                        id="shots-plot",
                        srcDoc=None,
                        style={
                            "width": "950px",
                            "height": "600px",
                            "display": "flex",
                            "borderWidth": "0px",
                        },
                    ),
                ],
            ),
        ]
    )
