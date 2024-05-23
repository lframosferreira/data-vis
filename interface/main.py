import os

import pandas as pd
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, exceptions, html
from src.components.layout import create_layout

ELO_DATA_DIR: str = "../data/elo/"


def main() -> None:
    app = Dash()
    app.title = "Visualização de Dados"

    df_dict: dict[str, pd.DataFrame] = {}
    for filename in os.listdir("../data/elo/"):
        club_name: str = filename[: filename.index(".")]
        df_dict[club_name] = pd.read_csv(f"{ELO_DATA_DIR}/{filename}")

    app.layout = create_layout(app=app, df_dict=df_dict)

    app.run(debug=True)


if __name__ == "__main__":
    main()
