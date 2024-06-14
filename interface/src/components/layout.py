import dash
from dash import dcc
from dash import html


# TODO deixar tudo no main
def create_layout() -> html.Div:
    return html.Div(
        style={
            "display": "flex",
            "margin-right": "10%",
            "margin-left": "10%",
            "flex-direction": "column",
        },
        children=[
            html.H1("Multi-page app with Dash Pages"),
            html.Div(
                [
                    html.Div(
                        dcc.Link(
                            f"{page['name']} - {page['path']}",
                            href=page["relative_path"],
                        )
                    )
                    for page in dash.page_registry.values()
                ]
            ),
            dash.page_container,
        ],
    )
