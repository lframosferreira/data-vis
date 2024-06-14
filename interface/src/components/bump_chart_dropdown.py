from dash import html
from dash.dcc import Dropdown
from dash.dcc import Graph


def render(options: list[str]) -> Dropdown:
    return html.Div(
        [
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
        ]
    )
