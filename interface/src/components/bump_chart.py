import plotly.graph_objs as go
from dash import Input
from dash import Output
from dash import callback
from pandas import DataFrame
from plotly.graph_objects import Scatter


def render(df_dict: dict[str, DataFrame]):
    @callback(
        Output("bump-chart", "figure"),
        [
            Input("rank-league-dropdown", "value"),
            Input("rank-range-slider", "value"),
        ],
    )
    def plot_bump_chart(league: str, slider: list[int]):
        rank_df = df_dict[league] if league is not None else df_dict["BRA1"]
        # we must handle the case when switching to a shorter dataframe
        low = slider[0] if slider[0] < len(rank_df) else len(rank_df)
        up = slider[1] if slider[1] < len(rank_df) else len(rank_df)
        rank_df = rank_df[rank_df.index >= low - 1]
        rank_df = rank_df[rank_df.index < up]
        rank_df = rank_df.T
        rank_df.columns = [str(x) for x in range(low, up + 1)]

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
        br_league: str = "BRA1"
        layout = go.Layout(
            title=f"Ranking Simulado dos Times no Campeonato {league if league is not None else br_league}",
            title_x=0.5,
            template="seaborn",
            xaxis={"title": "Rodada", "tickangle": 0},
            yaxis={
                "title": "Classificação",
                "autorange": "reversed",
            },
            margin={"l": 0, "r": 0, "t": 30, "b": 0},
        )

        return go.Figure(data=traces, layout=layout)
