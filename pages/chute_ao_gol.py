import os

import dash
import pandas as pd
from dash import html

from interface.src.components import shots_plot
from interface.src.components import shots_plot_dropdown
from interface.src.components import action_sequence_plot
from interface.src.components import action_sequence_dropdowns
from interface.src.components import heatmap_plot_accordion
from interface.src.components import heatmap_plot
from interface.src.components import passes_plot
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

files_match = [f for f in os.listdir(SPALD_DATA_DIR) if "matches" in f]

for filename in os.listdir(SHOTS_DATA_DIR):
    league_name: str = filename[: filename.index("_")]
    csv = pd.read_csv(f"{SHOTS_DATA_DIR}/{filename}")

    league_name_match = league_name[0].upper() + league_name[1:]
    csv_matches = pd.read_csv(f"{SPALD_DATA_DIR}/{league_name_match}_matches.csv")
    merged_df = csv.merge(csv_matches, on="game_id", how="left")
    # drop columns that have "Unnamed" in the name
    merged_df = merged_df.loc[:, ~merged_df.columns.str.contains("^Unnamed")]
    df_dict[f"{league_name}_shots"] = merged_df


files = [f for f in os.listdir(SPALD_DATA_DIR) if "matches" not in f]
for filename in files:
    spadl_league: str = filename[: filename.index(".")]
    spadl_league_df = pd.read_csv(f"{SPALD_DATA_DIR}/{filename}")
    df_matches = pd.read_csv(f"{SPALD_DATA_DIR}/{spadl_league}_matches.csv")
    merged_df = spadl_league_df.merge(df_matches, on="game_id", how="left")
    # drop columns that have "Unnamed" in the name
    merged_df = merged_df.loc[:, ~merged_df.columns.str.contains("^Unnamed")]
    spald_df_dict[f"{spadl_league}_spadl"] = merged_df

keys = list(df_dict.keys())
# print(df_dict[keys[0]].columns)

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
                heatmap_plot.render(df_dict=spald_df_dict),
                heatmap_plot_accordion.render(df_dict=df_dict, spadl_dict=spald_df_dict),
                #passes_plot.render(df_dict=spald_df_dict),
            ],
        ),
    ]
)
