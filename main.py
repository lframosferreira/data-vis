from dash import dcc
from dash import html
from dash import page_container
from dash import page_registry

from app import app

app.layout = html.Div(
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
                for page in page_registry.values()
            ]
        ),
        page_container,
    ],
)


def main() -> None:
    app.run(debug=True)


if __name__ == "__main__":
    main()
