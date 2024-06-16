from dash import Input
from dash import Output
from dash import callback
from dash import html
from dash.dcc import Dropdown
from dash.dcc import Graph
from dash.dcc import Markdown
from dash.dcc import RangeSlider
from pandas import DataFrame

from settings import PAGES_CONTENT_DIR

markdown_content = ""
with open(f"{PAGES_CONTENT_DIR}/rank.md") as f:
    markdown_content = f.read()


def render(options: list[str], df_dict: dict[str, DataFrame]) -> html.Div:
    @callback(
        Output("rank-range-slider", "max"),
        Input("rank-league-dropdown", "value"),
    )
    def plot_slider(league: str):
        rank_df = df_dict[league] if league is not None else df_dict["BRA1"]
        return len(rank_df)

    options.sort()
    return html.Div(
        [
            html.H2("Simulando Campeonatos", style={"textAlign": "center"}),
            Markdown(markdown_content, style={"textAlign": "justify"}, mathjax=True),
            Dropdown(
                id="rank-league-dropdown",
                multi=False,
                placeholder="Selecione a liga",
                options=options,
                clearable=True,
                searchable=True,
                style={"margin-bottom": "10px", "margin-top": "10px"},
            ),
            Graph(id="bump-chart"),
            RangeSlider(
                id="rank-range-slider",
                min=1,
                max=38,
                value=[1, 38],
                step=1,
                marks=None,
                disabled=False,
            ),
        ]
    )
