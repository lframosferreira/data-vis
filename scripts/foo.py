import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

df = pd.read_excel("TrainingSet_2023_02_08.xlsx")

WIN_RATIO = 0.5
LEAGUE = "GER1"
SEASON = "00-01"

df_sample = df.query(f"Lge == '{LEAGUE}' and Sea == '{SEASON}'")

goal_model_data = pd.concat(
    [
        df_sample[["HT", "AT", "HS"]]
        .assign(home=1)
        .rename(columns={"HT": "team", "AT": "opponent", "HS": "goals"}),
        df_sample[["AT", "HT", "AS"]]
        .assign(home=0)
        .rename(columns={"AT": "team", "HT": "opponent", "AS": "goals"}),
    ]
)

poisson_model = smf.glm(
    formula="goals ~ home + team + opponent",
    data=goal_model_data,
    family=sm.families.Poisson(),
).fit()


def predict_match(home_team: str, away_team: str) -> list:
    home_score_rate = poisson_model.predict(
        pd.DataFrame(
            data={"team": home_team, "opponent": away_team, "home": 1}, index=[1]
        )
    )
    away_score_rate = poisson_model.predict(
        pd.DataFrame(
            data={"team": away_team, "opponent": home_team, "home": 0}, index=[1]
        )
    )

    home_goals = np.random.poisson(home_score_rate)
    away_goals = np.random.poisson(away_score_rate)
    home_result = home_goals[0]
    away_result = away_goals[0]
    home_state = None
    if float(home_score_rate.iloc[0]) - float(away_score_rate.iloc[0]) > WIN_RATIO:
        home_state = "W"
    elif float(home_score_rate.iloc[0]) - float(away_score_rate.iloc[0]) < -WIN_RATIO:
        home_state = "L"
    else:
        home_state = "D"

    return [home_team, away_team, home_result, away_result, home_state]


def get_table(
    df: pd.DataFrame, league: str, season: str, num_games: float
) -> pd.DataFrame:
    df_league = df.query(f"Lge == '{league}' and Sea == '{season}'")
    teams = df_league["HT"].unique()
    data: list[list] = []
    for team in teams:
        df_team: pd.DataFrame = df_league.query(f"HT == '{team}' or AT == '{team}'")
        if "Date" in df_team:
            df_team.sort_values(by=["Date"])

        # Ajusta dataframe para representar a porção mais recente dos jogos jogados pelo time
        df_team = df_team.head(num_games)

        won = len(
            df_team.query(
                f"(HT == '{team}' and WDL == 'W') or (AT == '{team}' and WDL == 'L')"
            )
        )
        drawn = len(
            df_team.query(
                f"(HT == '{team}' and WDL == 'D') or (AT == '{team}' and WDL == 'D')"
            )
        )
        lost = len(
            df_team.query(
                f"(HT == '{team}' and WDL == 'L') or (AT == '{team}' and WDL == 'W')"
            )
        )

        points = 3 * won + drawn

        data.append([team, num_games, won, drawn, lost, points])

    df_table = pd.DataFrame(
        data,
        columns=["Team", "Matches", "Won", "Drawn", "Lost", "Points"],
    )
    return df_table.sort_values(by=["Points", "Won"], ascending=False)


def championship(league: str, season: str) -> pd.DataFrame:
    curr_df = df.query(f"Lge == '{league}' and Sea == '{season}'")
    num_rounds = 2 * (len(curr_df["HT"].unique()) - 1)
    df_list: list[pd.DataFrame] = []
    for i in range(num_rounds):
        n_df = get_table(df, league, season, i + 1)
        df_list.append(n_df)
    return pd.concat(df_list)


matches_df = championship(LEAGUE, SEASON)

# ma

matches_df.to_csv("sample.csv", index=False)


# https://stackoverflow.com/a/70569323
def bumpchart(
    df,
    show_rank_axis=True,
    rank_axis_distance=1.1,
    ax=None,
    scatter=False,
    holes=False,
    line_args={},
    scatter_args={},
    hole_args={},
):
    left_yaxis = plt.gca() if ax is None else ax

    # Creating the right axis.
    right_yaxis = left_yaxis.twinx()

    axes = [left_yaxis, right_yaxis]

    # Creating the far right axis if show_rank_axis is True
    if show_rank_axis:
        far_right_yaxis = left_yaxis.twinx()
        axes.append(far_right_yaxis)

    for col in df.columns:
        y = df[col]
        x = df.index.values
        # Plotting blank points on the right axis/axes
        # so that they line up with the left axis.
        for axis in axes[1:]:
            axis.plot(x, y, alpha=0)

        left_yaxis.plot(x, y, **line_args, solid_capstyle="round")

        # Adding scatter plots
        if scatter:
            left_yaxis.scatter(x, y, **scatter_args)

            # Adding see-through holes
            if holes:
                bg_color = left_yaxis.get_facecolor()
                left_yaxis.scatter(x, y, color=bg_color, **hole_args)

    # Number of lines
    lines = len(df.columns)

    y_ticks = [*range(1, lines + 1)]

    # Configuring the axes so that they line up well.
    for axis in axes:
        axis.invert_yaxis()
        axis.set_yticks(y_ticks)
        axis.set_ylim((lines + 0.5, 0.5))

    # Sorting the labels to match the ranks.
    left_labels = df.iloc[0].sort_values().index
    right_labels = df.iloc[-1].sort_values().index

    left_yaxis.set_yticklabels(left_labels)
    right_yaxis.set_yticklabels(right_labels)

    # Setting the position of the far right axis so that it doesn't overlap with the right axis
    if show_rank_axis:
        far_right_yaxis.spines["right"].set_position(("axes", rank_axis_distance))

    return axes


pivot_df = matches_df.pivot(index="Matches", columns="Team", values="Points").fillna(0)

my_cols = pivot_df.columns
pivot_df


# Function to get the reversed order
def reversed_order(row: list) -> list:
    sorted_row = sorted(row, reverse=True)
    return [sorted_row.index(x) + 1 for x in row]


# Apply the function to each row
series = pivot_df.apply(reversed_order, axis=1)

foobar = series.tolist()

foobar

new_df = pd.DataFrame(foobar, columns=my_cols)

new_df

df = series.to_frame(name="List")
df

df = df.explode("List")

df

data = {"A": [1, 2, 1, 3], "B": [2, 1, 3, 2], "C": [3, 3, 2, 1]}
df = pd.DataFrame(data, index=["step_1", "step_2", "step_3", "step_4"])

plt.figure(figsize=(10, 5))
bumpchart(
    new_df,
    show_rank_axis=True,
    scatter=True,
    holes=False,
    line_args={"linewidth": 5, "alpha": 0.5},
    scatter_args={"s": 100, "alpha": 0.8},
)  ## bump chart class with nice examples can be found on github
plt.show()
