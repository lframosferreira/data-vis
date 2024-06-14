import pandas as pd
import plotly.graph_objs as go
from dash import Input
from dash import Output
from dash import callback
from dash.html import Div
from plotly.graph_objects import Scatter


def render(df_dict: dict[str, pd.DataFrame]) -> Div:
    @callback(Output("bump-chart", "figure"), Input("rank-league-dropdown", "value"))
    def plot_bump_chart(league: str):
        rank_df = df_dict[league] if league is not None else df_dict["BRA1"]
        rank_df = rank_df.T
        rank_df.columns = [str(x + 1) for x in range(len(rank_df.columns))]

        traces: list[Scatter] = []

        for team, row in rank_df.iterrows():
            trace = Scatter(
                x=rank_df.columns,
                y=row.values,
                mode="lines+markers",
                name=team,
                text=team,
                hoverinfo="text",
                line={"shape": "spline"},
            )
            traces.append(trace)

        layout = go.Layout(
            title="Ranking Simulado dos Times no Campeonato",
            title_x=0.5,
            xaxis={"title": "Rodada"},
            yaxis={"title": "Classificação", "autorange": "reversed"},
        )

        return go.Figure(data=traces, layout=layout)
