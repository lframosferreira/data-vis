import os
from app import app

import pandas as pd
from dash import Dash
from interface.src.components.layout import create_layout

# TODO extrair isso aq pra um arquivo settings.py
ELO_DATA_DIR: str = "../data/elo/"
BRASILEIRO_DATA_DIR: str = "../data/brasileirao/"
SHOTS_DATA_DIR: str = "../data/shots/"


app.layout = create_layout()

def main() -> None:
    app.run(debug=True)


if __name__ == "__main__":
    main()
