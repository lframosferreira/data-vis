import matplotlib.pyplot as plt
import pandas as pd
from dash import Input
from dash import Output
from dash import callback
from dash import dcc
from dash import html
from settings import LEAGUES

def render(df_dict: dict[str, pd.DataFrame], spadl_dict: dict[str, pd.DataFrame]) -> html.Div:
    @callback(
        [Output("goal-dropdown", "options"),
         Output("goal-dropdown", "disabled")],
        [Input("league-dropdown", "value"),
         Input("shots-players-dropdown", "value"),
         Input("shoot-range-slider", "value")]
    )
    def populate_goal_dropdown(league: str, player_name: str, shoot_prob_range: list[int]):
        if league is None or player_name is None or shoot_prob_range is None:
            return [], True

        min_prob = 0.01 if shoot_prob_range[0] == 0 else shoot_prob_range[0] / 100
        max_prob = shoot_prob_range[1] / 100

        league_key = next(
            (key for key, value in LEAGUES.items() if value == league), None
        )
        if league_key is None:
            return [], True

        shots = df_dict[f"{league_key}_shots"]
        filtered_goals = (
            shots[
                (shots["player_name"] == player_name)
                & (
                    (shots["xG"] > min_prob)
                    & (shots["xG"] < max_prob)
                    & (shots["result_name"] == "success")
                )
            ]
            .sort_values(by="xG")
        )

        goal_options = [
            {
                "label": f"Gol com {row['xG'] * 100:.2f}% de chance - {row['game_label']} | Rodada {row['game_week']} em {row['game_date']}",
                "value": row['original_event_id']}
            for row in filtered_goals.to_dict(orient="records")
        ]
        return goal_options, False

    return html.Div(
        children=[
            html.Hr(),
            html.H2("Sequência de ações até o gol", style={"textAlign": "center"}),
            html.P(
                """
                Você pode escolher até 5 ações antes do gol selecionado, mas é importante ressaltar que dependendo do gol
                escolhido, o número de ações que são da jogada do gol é menor. Nesse caso, você verá mais ações sem ser as que
                levaram ao gol.
                """,
                style={"textAlign": "justify", "margin": "20px"},
            ),
            dcc.Dropdown(
                id="goal-dropdown",
                multi=False,
                placeholder="Selecione o gol",
                options=[],
                clearable=True,
                searchable=False,
                style={"margin-bottom": "20px", "margin-top": "20px"},
            ),
            html.Div(
                id="shoot-slider-container",
                children=[
                    html.P(
                        "Selecione quantas ações antes do gol quer ver:",
                        style={"margin-right": "10px"},
                    ),
                    dcc.Slider(
                        id="goal-actions-slider",
                        min=0,
                        max=5,
                        step=1,
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
                    "height": "500px",
                },
                children=[
                    html.Iframe(
                        id="action-sequence-plot",
                        srcDoc=None,
                        style={
                            "display": "flex",
                            "width": "85%",
                            "height": "100%",
                            "borderWidth": "0px",
                        },
                    ),
                ],
            ),
        ]
    )