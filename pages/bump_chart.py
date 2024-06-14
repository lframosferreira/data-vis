from pathlib import Path

import dash
import pandas as pd
from dash import html

from interface.src.components import bump_chart
from interface.src.components import bump_chart_dropdown
from settings import RANK_DATA_DIR

dash.register_page(
    __name__,
    path="/bump-chart",
    title="Simulação de Campeonato",
    name="Simulação de Campeonato",
)

df_dict: dict[str, pd.DataFrame] = {}
for path in Path(RANK_DATA_DIR).iterdir():
    filename = path.name
    club_name = filename[filename.rfind("-") + 1 : -4]
    df_dict[club_name] = pd.read_csv(path)

championships = list(df_dict.keys())

layout = html.Div(
    children=[
        bump_chart_dropdown.render(options=championships),
        bump_chart.render(df_dict),
    ]
)
