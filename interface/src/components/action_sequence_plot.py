import base64
from io import BytesIO

import matplotlib.pyplot as plt
import matplotsoccer
import pandas as pd
from dash import Input
from dash import Output
from dash import callback
from dash import html

from settings import LEAGUES


def render(df_dict: dict[str, pd.DataFrame]) -> html.Div:
    @callback(
        Output("action-sequence-plot", "src"),
        [
            Input("goal-actions-slider", "value"),
            Input("league-dropdown", "value"),
            Input("goal-dropdown", "value"),
        ],
    )
    def plot_actions_sequence(num_of_actions: int, league: str, goal_event_id: int):
        fig, ax = plt.subplots()

        if league is None or goal_event_id is None:
            matplotsoccer.field(color="green", ax=ax)
        else:
            league_key = next(
                (key.capitalize() for key, value in LEAGUES.items() if value == league),
                None,
            )
            spadl_df = df_dict[f"{league_key}_spadl"]

            num_of_actions = 0 if num_of_actions is None else num_of_actions
            index = spadl_df.index[
                spadl_df["original_event_id"] == goal_event_id
            ].tolist()[0]

            actions_df: pd.DataFrame = spadl_df[
                index - num_of_actions : index + 1
            ].copy()

            matplotsoccer.actions(
                color="green",
                location=actions_df[["start_x", "start_y", "end_x", "end_y"]],
                action_type=actions_df["type_name"],
                result=actions_df["result_name"] == "success",
                label=actions_df[["time_seconds", "type_name", "player_name"]],
                labeltitle=["time", "actiontype", "player"],
                zoom=False,
                ax=ax,
            )

        img = BytesIO()
        fig.savefig(img, format="png", bbox_inches="tight")
        img.seek(0)

        img_base64 = base64.b64encode(img.read()).decode("utf-8")
        img.close()
        plt.close(fig)

        return f"data:image/png;base64,{img_base64}"

