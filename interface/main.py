import os

import pandas as pd
from dash import Dash
from src.components.layout import create_layout

ELO_DATA_DIR: str = "../data/elo/"
BRASILEIRO_DATA_DIR: str = "../data/brasileirao/"
SHOTS_DATA_DIR: str = "../data/shots/"


def main() -> None:
    app = Dash()
    app.title = "Visualização de Dados"

    df_dict: dict[str, pd.DataFrame] = {}
    for filename in os.listdir("../data/elo/"):
        club_name: str = filename[: filename.index(".")]
        df_dict[club_name] = pd.read_csv(f"{ELO_DATA_DIR}/{filename}")

    for filename in os.listdir("../data/brasileirao/"):
        club_name: str = filename[: filename.index(".")]
        df_dict[club_name] = pd.read_csv(f"{BRASILEIRO_DATA_DIR}/{filename}")

    for filename in os.listdir("../data/shots/"):
        league_name: str = filename[: filename.index("_")]
        df_dict[f"{league_name}_shots"] = pd.read_csv(f"{SHOTS_DATA_DIR}/{filename}")

    app.layout = create_layout(app=app, df_dict=df_dict)

    app.run(debug=True)


if __name__ == "__main__":
    main()
