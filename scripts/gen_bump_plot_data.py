from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.genmod.generalized_linear_model import GLMResultsWrapper

rng = np.random.default_rng()

DATA_DIR = "../data"


df = pd.read_csv(f"{DATA_DIR}/leagues.csv")  # noqa: PD901


def get_poisson_model(model_df: pd.DataFrame) -> GLMResultsWrapper:
    goal_model_data = pd.concat(
        [
            model_df[["HT", "AT", "HS"]]
            .assign(home=1)
            .rename(columns={"HT": "team", "AT": "opponent", "HS": "goals"}),
            model_df[["AT", "HT", "AS"]]
            .assign(home=0)
            .rename(columns={"AT": "team", "HT": "opponent", "AS": "goals"}),
        ]
    )

    return smf.glm(
        formula="goals ~ home + team + opponent",
        data=goal_model_data,
        family=sm.families.Poisson(),
    ).fit()


def predict_match(home: str, away: str, model: GLMResultsWrapper) -> list:
    home_score_rate = model.predict(
        {"team": home, "opponent": away, "home": 1}
    ).tolist()[0]
    away_score_rate = model.predict(
        {"team": away, "opponent": home, "home": 0}
    ).tolist()[0]

    home_goals = rng.poisson(lam=home_score_rate)
    away_goals = rng.poisson(lam=away_score_rate)
    home_state = None
    if home_score_rate - away_score_rate > 1 / 2:
        home_state = "W"
    elif home_score_rate - away_score_rate < -1 / 2:
        home_state = "L"
    else:
        home_state = "D"

    return [home, away, home_goals, away_goals, home_state]


def get_table(df: pd.DataFrame, num_games: float) -> pd.DataFrame:
    teams = df["HT"].unique()
    data: list[list] = []
    for team in teams:
        team_df = df.query(f"HT == '{team}' or AT == '{team}'")
        if "Date" in team_df:
            team_df.sort_values(by=["Date"])

        # Ajusta dataframe para representar a porção mais recente dos jogos jogados pelo time
        team_df = team_df.head(num_games)

        won = len(
            team_df.query(
                f"(HT == '{team}' and WDL == 'W') or (AT == '{team}' and WDL == 'L')"
            )
        )
        drawn = len(
            team_df.query(
                f"(HT == '{team}' and WDL == 'D') or (AT == '{team}' and WDL == 'D')"
            )
        )
        lost = len(
            team_df.query(
                f"(HT == '{team}' and WDL == 'L') or (AT == '{team}' and WDL == 'W')"
            )
        )

        goals_for = sum(team_df.query(f"HT == '{team}'")["HS"]) + sum(
            team_df.query(f"AT == '{team}'")["AS"]
        )
        goals_against = sum(team_df.query(f"HT == '{team}'")["AS"]) + sum(
            team_df.query(f"AT == '{team}'")["HS"]
        )
        goal_difference = goals_for - goals_against

        points = 3 * won + drawn

        data.append(
            [
                team,
                num_games,
                won,
                drawn,
                lost,
                goals_for,
                goals_against,
                goal_difference,
                points,
            ]
        )

    table_df = pd.DataFrame(
        data,
        columns=["Team", "Matches", "Won", "Drawn", "Lost", "GF", "GA", "GD", "Points"],
    )
    sorted_df = table_df.sort_values(by=["Points", "Won", "GD", "GF"], ascending=False)
    sorted_df["Rank"] = range(1, len(sorted_df) + 1)
    return sorted_df.reset_index(drop=True)


def championship(league: str, season: str) -> pd.DataFrame:
    league_df = df.query(f"Lge == '{league}' and Sea == '{season}'")
    poisson_model = get_poisson_model(league_df)
    simulation_matches: list[list] = []
    teams = league_df["HT"].unique()
    for x in teams:
        for y in teams:
            if x != y:
                match = predict_match(x, y, poisson_model)
                simulation_matches.append(match)
    league_simulation_df = pd.DataFrame(
        simulation_matches, columns=["HT", "AT", "HS", "AS", "WDL"]
    )
    df_list: list[pd.DataFrame] = []
    num_rounds = 2 * (len(league_df["HT"].unique()) - 1)
    for i in range(num_rounds):
        nth_round_df = get_table(league_simulation_df, i + 1)
        df_list.append(nth_round_df)
    return pd.concat(df_list)


leagues = df["Lge"].unique()
for league in leagues:
    # Can't get latest "ARG1" because it exceeds poisson's lambda
    # Don't worry, we get an year prior to that (off-script)
    if league != "ARG1":
        continue
    league_df = df.query(f"Lge == '{league}'")
    season = league_df["Sea"].unique()[-2]
    file_path = f"{DATA_DIR}/hugo/{season}-{league}.csv"
    file = Path(file_path)
    # if not file.is_file():
    championship_df = championship(league, season)
    championship_df.to_csv(file_path, index=False)
