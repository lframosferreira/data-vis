import base64
from io import BytesIO

import matplotlib.pyplot as plt
import pandas as pd
from dash import Input
from dash import Output
from dash import callback
from mplsoccer import VerticalPitch

LEAGUES: dict[str, str] = {
    "england": "Premier League",
    "spain": "La Liga",
    "germany": "Bundesliga",
    "italy": "Serie A",
    "france": "Ligue 1",
}

COLORS = ["#0072B2", "#F0E442", "#4f4e4e", "#D55E00", "#CC79A7"]


def render(df_dict: dict[str, pd.DataFrame]) -> None:
    @callback(
        [
            Output("shots-players-dropdown", "disabled"),
            Output("shots-players-dropdown", "value"),
        ],
        Input("league-dropdown", "value"),
    )
    def enable_shots_dropdown(league: str):
        return (league is None), None

    @callback(
        [
            Output("shoot-range-slider", "disabled"),
            Output("shoot-range-slider", "value"),
        ],
        Input("shots-players-dropdown", "value"),
    )
    def toggle_slider_visibility(player_name):
        return player_name is None, [0, 30]

    @callback(
        Output("shots-plot", "src"),
        [
            Input("shots-players-dropdown", "value"),
            Input("league-dropdown", "value"),
            Input("shoot-range-slider", "value"),
        ],
    )
    def plot_shots(player_name: str, league: str, shoot_prob_range: list[int]):
        plt.style.use("ggplot")

        min_prob = 0.01 if shoot_prob_range[0] == 0 else shoot_prob_range[0] / 100
        max_prob = shoot_prob_range[1] / 100

        pitch = VerticalPitch(
            pitch_type="custom",
            pitch_color="#88d797",
            corner_arcs=True,
            half=True,
            goal_type="box",
            pitch_length=105,
            pitch_width=68,
        )

        fig, ax = pitch.draw(figsize=(9, 6))

        league_key = next(
            (key for key, value in LEAGUES.items() if value == league), None
        )
        if league_key is not None:
            shots = df_dict[f"{league_key}_shots"]
            filtered_shots = (
                shots[
                    (shots["player_name"] == player_name)
                    & (
                        (shots["xG"] > min_prob)
                        & (shots["xG"] < max_prob)
                        & (shots["result_name"] == "success")
                    )
                ]
                .sort_values(by="xG")
                .head(5)
                .reset_index(drop=True)
            )

            for idx, shot in filtered_shots.iterrows():
                xG = f"{shot['xG'] * 100:.2f}%"  # noqa: N806
                color = COLORS[idx]

                pitch.scatter(
                    shot["start_x"],
                    shot["start_y"],
                    color=color,
                    s=125,
                    ax=ax,
                    zorder=1.2,
                    label=xG,
                )
                pitch.arrows(
                    shot["start_x"],
                    shot["start_y"],
                    shot["end_x"],
                    shot["end_y"],
                    color="#cb5a4c",
                    width=1,
                    headwidth=5,
                    headlength=5,
                    ax=ax,
                )

        if player_name is not None and league is not None:
            ax.legend(
                title="Probabilidade de gol", labelspacing=1, bbox_to_anchor=(1.25, 0.7)
            )

        img = BytesIO()
        fig.savefig(img, format="png", bbox_inches="tight")
        img.seek(0)

        img_base64 = base64.b64encode(img.read()).decode("utf-8")
        img.close()
        plt.close(fig)

        return f"data:image/png;base64,{img_base64}"
