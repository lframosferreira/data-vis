import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import Input
from dash import Output
from dash import callback
from dash import exceptions

from settings import TEAMS_BRASILEIRAO


def make_moving_avarages_plot(df_dict: dict[str, pd.DataFrame], team,window, fig) -> go.Figure:
    
    df: pd.DataFrame = df_dict["sportsref"]
    
    xG_pro_global_moving_average: np.array = np.zeros(38)
    xG_against_global_moving_average: np.array = np.zeros(38)
    xG_diff_global_moving_average: np.array = np.zeros(38)
    
    window_size: int = window
    
    x = np.arange(0, 37, 1)
    
    team_df: pd.DataFrame = df[(df["Home"] == team) | (df["Away"] == team)]
    team_df["xG_pro"] = np.where(team_df["Home"] == team, team_df["xG_Home"], team_df["xG_Away"])
    team_df["xG_against"] = np.where(team_df["Home"] == team, team_df["xG_Away"], team_df["xG_Home"])
    
    xG_pro_moving_average: np.array = team_df["xG_pro"].rolling(window=window_size, min_periods=1).mean().to_numpy()
    xG_against_moving_average: np.array = team_df["xG_against"].rolling(window=window_size, min_periods=1).mean().to_numpy()
    xG_diff_moving_average: np.array = team_df["xG_diff"].rolling(window=window_size, min_periods=1).mean().to_numpy()
    fig.add_trace(
        go.Scatter(x=x, y=xG_pro_moving_average, name="xG Pro " + team)
    )
    
    fig.add_trace(
        go.Scatter(x=x, y=xG_against_moving_average, name="xG Against " + team)
    )
    
    fig.add_trace(
        go.Scatter(x=x, y=xG_diff_moving_average, name="xG Diff " + team)
    )
        
        
    return fig


def render(df_dict: dict[str, pd.DataFrame]) -> None:
    @callback(
        Output("moving-avarages-plot", "figure"),
        [
            Input("teams-moving-avarages-dropdown", "value"),
            Input("teams-moving-avarages-window-radio", "value"),
        ],
        prevent_initial_call=True,
    )
    def moving_avarages_plot(ticker,ticker2):
        fig = go.Figure()
        if ticker:
            fig = make_moving_avarages_plot(df_dict, ticker,ticker2, fig)
            
        return fig