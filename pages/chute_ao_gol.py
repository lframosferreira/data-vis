import os

import dash
import pandas as pd
from dash import html

from interface.src.components import shots_plot
from interface.src.components import shots_plot_dropdown
from interface.src.components import action_sequence_plot
from interface.src.components import action_sequence_dropdowns
from settings import SHOTS_DATA_DIR, SPALD_DATA_DIR

dash.register_page(
    __name__,
    path="/chute-ao-gol",
    title="Chute ao gol",
    name="Chute ao gol",
)
# TODO importar isso de um arquivo de settings

df_dict: dict[str, pd.DataFrame] = {}
spald_df_dict: dict[str, pd.DataFrame] = {}

for filename in os.listdir(SHOTS_DATA_DIR):
    league_name: str = filename[: filename.index("_")]
    df_dict[f"{league_name}_shots"] = pd.read_csv(f"{SHOTS_DATA_DIR}/{filename}")

for filename in os.listdir(SPALD_DATA_DIR):
    spadl_league: str = filename[: filename.index(".")]
    spald_df_dict[f"{spadl_league}_spadl"] = pd.read_csv(f"{SPALD_DATA_DIR}/{filename}")

layout = html.Div(
    [
        html.H2(
            "Visualização dos gols e suas probabilidades", style={"textAlign": "center"}
        ),
        html.P(
            """
            Utilizamos os dados das partidas das principais ligas europeias, mais especificamente os dados de chutes e de faltas ao gol, 
            para treinar um modelo de regressão logística para prever as chances de um chute ser gol. 
            De forma mais específica, as features utilizadas foram: distância até o gol, ângulo de chute, distância quadrática até o gol 
            e a parte do corpo que realizou a finalização ao gol. 
            """,
            style={"textAlign": "justify", "margin": "20px"},
        ),
        html.P(
            """
            Com essa métrica podemos analisar se os jogadores artilheiros mais 
            famosos realmente têm uma qualidade superior que os permite converter mais oportunidades de gols em posições desfavoráveis. 
            Além de ser possível observar de qual lado do campo um jogador se sobressai ao checar em qual deles ele realiza com sucesso 
            mais finalizações improváveis.
            """,
            style={"textAlign": "justify", "margin": "20px"},
        ),
        html.Div(
            className="shots-plot",
            children=[
                shots_plot.render(df_dict=df_dict),
                shots_plot_dropdown.render(df_dict=df_dict),
                action_sequence_plot.render(df_dict=spald_df_dict),
                action_sequence_dropdowns.render(df_dict=df_dict, spadl_dict=spald_df_dict),
            ],
        ),
    ]
)
