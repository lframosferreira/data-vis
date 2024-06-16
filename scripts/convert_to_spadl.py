#!/usr/bin/env python

# In[8]:


import os

import pandas as pd
import socceraction.spadl as spd
from tqdm import tqdm

# # Carregando os dados da WyScout

def load_matches(path):
    matches = pd.read_json(path_or_buf=path)
    matches["label"] = matches["label"].str.decode("unicode-escape")

    def process_row(row):
        match = pd.DataFrame(row['teamsData']).T
        match['game_id'] = row['wyId']
        match['game_week'] = row['gameweek']
        match['game_label'] = row['label']
        match['game_date'] = pd.to_datetime(row['dateutc']).strftime("%d/%m/%Y")
        return match

    team_matches = pd.concat(matches.apply(process_row, axis=1).tolist()).reset_index(drop=True)

    new_path = path.replace(".json", ".csv")
    team_matches.to_csv(new_path)

    return team_matches


def load_players(path):
    players = pd.read_json(path_or_buf=path)
    players["player_name"] = players["firstName"] + " " + players["lastName"]
    players = players[["wyId", "player_name"]].rename(columns={"wyId": "player_id"})

    return players


# In[11]:


def load_events(path):
    events = pd.read_json(path_or_buf=path)
    # pré processamento em colunas da tabela de eventos para facilitar a conversão p/ SPADL
    events = events.rename(
        columns={
            "id": "event_id",
            "eventId": "type_id",
            "subEventId": "subtype_id",
            "teamId": "team_id",
            "playerId": "player_id",
            "matchId": "game_id",
        }
    )
    events["milliseconds"] = events["eventSec"] * 1000
    events["period_id"] = events["matchPeriod"].replace({"1H": 1, "2H": 2})

    return events


# In[12]:


def load_minutes_played_per_game(path):
    minutes = pd.read_json(path_or_buf=path)
    minutes = minutes.rename(
        columns={
            "playerId": "player_id",
            "matchId": "game_id",
            "teamId": "team_id",
            "minutesPlayed": "minutes_played",
        }
    )
    minutes = minutes.drop(["shortName", "teamName", "red_card"], axis=1)

    return minutes


# In[13]:


leagues = ["England", "Spain", "France", "Germany", "Italy"]
events = {}
matches = {}
minutes = {}
for league in tqdm(leagues, desc="Loading data from disc"):
    path = f"data/wyscout/matches/matches_{league}.json"
    matches[league] = load_matches(path)
    path = f"data/wyscout/events/events_{league}.json"
    events[league] = load_events(path)
    path = f"data/wyscout/minutes_played/minutes_played_per_game_{league}.json"
    minutes[league] = load_minutes_played_per_game(path)


# In[14]:


path = "data/wyscout/players/players.json"
players = load_players(path)
players["player_name"] = players["player_name"].str.decode("unicode-escape")


# # Conversão para o formato SPADL

# In[15]:


def spadl_transform(events, matches):
    spadl = []
    game_ids = events.game_id.unique().tolist()
    #for g in tqdm(game_ids, leave=False, desc="SPADL conversion"):
    for g in game_ids:
        match_events = events.loc[events.game_id == g]
        match_home_id = matches.loc[
            (matches.game_id == g) & (matches.side == "home"), "teamId"
        ].values[0]
        match_actions = spd.wyscout.convert_to_actions(
            events=match_events, home_team_id=match_home_id
        )
        match_actions = spd.play_left_to_right(
            actions=match_actions, home_team_id=match_home_id
        )
        match_actions = spd.add_names(match_actions)
        spadl.append(match_actions)
    spadl = pd.concat(spadl).reset_index(drop=True)

    return spadl


# In[16]:


if not os.path.exists("data/spadl_format"):
    os.makedirs("data/spadl_format")
players: pd.DataFrame = pd.read_json("data/wyscout/players/players.json")
players["player_name"] = players["shortName"].str.decode("unicode-escape")
players = players[["wyId", "player_name"]].rename(columns={"wyId": "player_id"})

teams: pd.DataFrame = pd.read_json("data/wyscout/teams/teams.json")
teams["officialName"] = teams["officialName"].str.decode("unicode-escape")
df_teams = teams[["wyId", "officialName"]]
df_teams = df_teams.rename(columns={
    "wyId": "team_id",
    "officialName": "team_official_name"
})

for league in tqdm(leagues, desc="All leagues SPADL conversion"):
    df_matches_league = matches[league]
    df_matches_league = df_matches_league[["game_id", "game_date", "game_label", "game_week"]]

    df_actions_league = spadl_transform(events=events[league], matches=matches[league])
    df_actions_league = df_actions_league.merge(players, on="player_id", how="left")
    df_actions_league = df_actions_league.merge(df_teams, on="team_id", how="left")
    #df_actions_league = df_actions_league.merge(df_matches_league, on="game_id", how="left")
    dest = f"data/spadl_format/{league}.csv"
    df_actions_league.to_csv(dest)
    df_matches_league.to_csv(dest.replace(".csv", "_matches.csv"))

