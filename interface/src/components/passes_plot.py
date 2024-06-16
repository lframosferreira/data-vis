import base64
from io import BytesIO

import matplotlib.pyplot as plt
import pandas as pd
from dash import Input
from dash import Output
from dash import callback
from mplsoccer import VerticalPitch
from settings import LEAGUES
import matplotsoccer
import scipy

def render(df_dict: dict[str, pd.DataFrame]) -> None:
    @callback(
        Output("passes-plot", "src"),
        [Input("league-dropdown", "value"),
         Input("goal-dropdown", "value"),
        ]
    )
    def plot_passes(league: str, goal_event_id: int):
        fig, ax = plt.subplots(figsize=(10, 6)) 

        if league is None or goal_event_id is None:
            matplotsoccer.field(color="green", ax=ax)
        else:
            league_key = next(
                (key.capitalize() for key, value in LEAGUES.items() if value == league), None
            )
            spadl_df = df_dict[f"{league_key}_spadl"]

            goal_event_df = spadl_df[spadl_df['original_event_id'] == goal_event_id]

            player_id = goal_event_df.iloc[0]['player_id']
            game_id = goal_event_df.iloc[0]['game_id']

            player_actions_df = spadl_df[(spadl_df['player_id'] == player_id) & (spadl_df['game_id'] == game_id)]

            passes: pd.DataFrame = player_actions_df.loc[spadl_df["type_name"].isin(
                ['pass',
                'cross',
                'throw_in',
                'freekick_crossed',
                'freekick_short',
                'corner_crossed',
                'corner_short'])].copy()
            
            matplotsoccer.field("green",figsize=8, show=False)

            for i, thepass in passes.iterrows():
                x = thepass["start_x"]
                y = thepass["start_y"]
                
                plt.scatter(x, y, s=200, c="blue", alpha=.2)
                dx = thepass["end_x"] - x
                dy = thepass["end_y"] - y

                plt.arrow(x, y, dx, dy, width=.3, color="blue")

            #TODO imagem não está sendo gerada corretamente
            # fig.savefig("heatmap.png", format="png", bbox_inches='tight')
        
        img = BytesIO()
        fig.savefig(img, format="png", bbox_inches='tight')
        img.seek(0)

        img_base64 = base64.b64encode(img.read()).decode("utf-8")
        img.close()
        plt.close(fig)

        return f"data:image/png;base64,{img_base64}"