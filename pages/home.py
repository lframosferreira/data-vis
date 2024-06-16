import dash
import dash_bootstrap_components as dbc
from dash import html

dash.register_page(
    __name__,
    path="/",
    title="Home",
    name="Página principal",
)

# Creating a list group of all pages in the app with clickable links
list_group = dbc.ListGroup(
    [
        dbc.ListGroupItem(dbc.NavLink(page["name"], href=page["relative_path"]))
        for page in dash.page_registry.values()
    ][1:],  # pular home page
)

# Defining the layout
layout = dbc.Container(
    [
        html.Div(
            [
                html.H1(
                    "Dashboard para análise de futebol", className="display-3 mb-3"
                ),
                html.P(
                    "Explore diferentes páginas para obter insights e análises detalhadas sobre futebol.",
                    className="lead",
                ),
                html.Hr(className="my-2"),
                html.P("Selecione uma das páginas abaixo para começar."),
                list_group,
            ],
            className="p-5 mb-4 bg-light rounded-3",
        ),
    ],
    style={"margin-top": "20px"},
)
