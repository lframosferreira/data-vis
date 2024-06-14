import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import VerticalPitch
from dash import Dash, html, Input, Output, exceptions, callback
from io import BytesIO
import base64
import matplotlib.colors as mcolors


LEAGUES: list[str, str] = {
    "england": "Premier League",
    "spain": "La Liga",
    "germany": "Bundesliga",
    "italy": "Serie A",
    "france": "Ligue 1",
}


def render(df_dict: dict[str, pd.DataFrame]) -> html.Div:
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
        Output("shots-plot", "srcDoc"),
        [Input("shots-players-dropdown", "value"), Input("league-dropdown", "value")],
    )
    def plot_shots(player_name: str, league: str):
        plt.style.use("ggplot")

        pitch = VerticalPitch(
            pitch_type="custom",
            pitch_color="#88d797",
            corner_arcs=True,
            half=True,
            goal_type="box",
            pitch_length=105,
            pitch_width=68,
        )

        fig, ax = pitch.draw()

        league_key = next(
            (key for key, value in LEAGUES.items() if value == league), None
        )
        if not (league_key is None):
            # raise exceptions.PreventUpdate
            shots = df_dict[f"{league_key}_shots"]
            filtered_shots = (
                shots[
                    (shots["player_name"] == player_name)
                    & ((shots["xG"] < 0.3) & (shots["result_name"] == "success"))
                ]
                .sort_values(by="xG")
                .head(5)
            )

            for idx, shot in filtered_shots.iterrows():
                pitch.scatter(
                    shot["start_x"],
                    shot["start_y"],
                    color="#276cb7",
                    s=100,
                    ax=ax,
                    label="Shooter",
                    zorder=1.2,
                )
                pitch.arrows(
                    shot["start_x"],
                    shot["start_y"],
                    shot["end_x"],
                    shot["end_y"],
                    label="shot",
                    color="#cb5a4c",
                    width=1,
                    headwidth=5,
                    headlength=5,
                    ax=ax,
                )

        img = BytesIO()
        fig.savefig(img, format="png")
        img.seek(0)

        img_base64 = base64.b64encode(img.read()).decode("utf-8")
        img.close()
        plt.close(fig)

        html_plot = f'<img src="data:image/png;base64,{img_base64}" alt="Shot Plot" style="border:none; margin:0; padding:0; display:block;">'

        return html_plot
