import streamlit as st
import numpy as np
import pandas as pd

from nba_api.live.nba.endpoints import boxscore, scoreboard
from nba_api.stats.endpoints import boxscoretraditionalv2

games = scoreboard.ScoreBoard()

game_score = games.get_dict()
scoreboard = game_score["scoreboard"]
game = scoreboard["games"]
game_date = scoreboard["gameDate"]


def ChangeIndexName(df, index_name):
    new_index = df.loc[:, index_name]
    df_change_index = df.set_axis(new_index)

    return df_change_index


def DropColumns(df, columns):
    df_drop_columns = df[columns]

    return df_drop_columns


gameid_list = []

for i in range(len(game)):
    game_id = game[i]["gameId"]
    gameid_list.append(game_id)

row2_1, row2_2, row2_3 = st.columns((3, 3, 2))


with row2_1:
    st.subheader(" ")

with row2_2:
    st.header(f"{game_date}")

with row2_3:
    st.subheader(" ")

for i in range(len(game)):
    awayTeam = game[i]["awayTeam"]["teamTricode"]
    homeTeam = game[i]["homeTeam"]["teamTricode"]

    awayTeamCity = game[i]["awayTeam"]["teamCity"]
    awayTeamname = game[i]["awayTeam"]["teamName"]

    awayTeam_full_name = awayTeamCity + (" ") + awayTeamname

    homeTeamCity = game[i]["homeTeam"]["teamCity"]
    homeTeamname = game[i]["homeTeam"]["teamName"]

    homeTeam_full_name = homeTeamCity + (" ") + homeTeamname

    awayTeam_score = game[i]["awayTeam"]["score"]
    homeTeam_score = game[i]["homeTeam"]["score"]

    awayTeam_win_count = game[i]["awayTeam"]["wins"]
    awayTeam_lose_count = game[i]["awayTeam"]["losses"]

    homeTeam_win_count = game[i]["homeTeam"]["wins"]
    homeTeam_lose_count = game[i]["homeTeam"]["losses"]

    away_Team_q1point = game[i]["awayTeam"]["periods"][0]["score"]
    away_Team_q2point = game[i]["awayTeam"]["periods"][1]["score"]
    away_Team_q3point = game[i]["awayTeam"]["periods"][2]["score"]
    away_Team_q4point = game[i]["awayTeam"]["periods"][3]["score"]

    home_Team_q1point = game[i]["homeTeam"]["periods"][0]["score"]
    home_Team_q2point = game[i]["homeTeam"]["periods"][1]["score"]
    home_Team_q3point = game[i]["homeTeam"]["periods"][2]["score"]
    home_Team_q4point = game[i]["homeTeam"]["periods"][3]["score"]

    leader_away_assist = game[i]["gameLeaders"]["awayLeaders"]["assists"]
    leader_away_rebounds = game[i]["gameLeaders"]["awayLeaders"]["rebounds"]
    leader_away_point = game[i]["gameLeaders"]["awayLeaders"]["points"]
    leader_away_player = game[i]["gameLeaders"]["awayLeaders"]["name"]

    leader_home_assist = game[i]["gameLeaders"]["homeLeaders"]["assists"]
    leader_home_rebounds = game[i]["gameLeaders"]["homeLeaders"]["rebounds"]
    leader_home_point = game[i]["gameLeaders"]["homeLeaders"]["points"]
    leader_home_player = game[i]["gameLeaders"]["homeLeaders"]["name"]

    boxscores = boxscore.BoxScore(game_id=gameid_list[i])
    boxscore_game = boxscores.game.get_dict()

    box_score_tradtional_v2 = boxscoretraditionalv2.BoxScoreTraditionalV2(
        game_id=gameid_list[i]
    )

    arena = boxscore_game["arena"]["arenaName"]
    arena_city = boxscore_game["arena"]["arenaCity"]
    arenaState = boxscore_game["arena"]["arenaState"]
    attendance = boxscore_game["attendance"]

    gameStatus = game[i]["gameStatusText"]

    df_box_score_tradtional = box_score_tradtional_v2.player_stats.get_data_frame()
    df_box_score_team = box_score_tradtional_v2.team_stats.get_data_frame()

    df_box_score_tradtional_index_change = ChangeIndexName(
        df_box_score_tradtional, "PLAYER_NAME"
    )
    df_box_score = DropColumns(
        df_box_score_tradtional_index_change,
        [
            "START_POSITION",
            "TEAM_ABBREVIATION",
            "COMMENT",
            "MIN",
            "FGM",
            "FGA",
            "FG_PCT",
            "FG3M",
            "FG3A",
            "FG3_PCT",
            "FTM",
            "FTA",
            "FT_PCT",
            "OREB",
            "DREB",
            "REB",
            "AST",
            "STL",
            "BLK",
            "TO",
            "PF",
            "PTS",
            "PLUS_MINUS",
        ],
    )

    df_box_score_fillna = df_box_score.fillna(0)

    df_box_score_dtype_change = df_box_score_fillna.astype(
        {
            "FGM": "int8",
            "FGA": "int8",
            "FGM": "int8",
            "FG3M": "int8",
            "FG3A": "int8",
            "FTM": "int8",
            "FTA": "int8",
            "OREB": "int8",
            "DREB": "int8",
            "REB": "int8",
            "AST": "int8",
            "STL": "int8",
            "BLK": "int8",
            "TO": "int8",
            "PF": "int8",
            "PTS": "int8",
            "PLUS_MINUS": "int8",
        }
    )

    df_away = df_box_score_dtype_change.query(" TEAM_ABBREVIATION== @awayTeam")
    df_home = df_box_score_dtype_change.query(" TEAM_ABBREVIATION== @homeTeam")

    df_away_new = df_away.drop(["TEAM_ABBREVIATION"], axis=1)
    df_home_new = df_home.drop(["TEAM_ABBREVIATION"], axis=1)

    if gameStatus == "Final" or gameStatus == "Final/OT":
        df_away_style = df_away_new.style.format(
            {"FG_PCT": "{:.3f}", "FG3_PCT": "{:.3f}", "FT_PCT": "{:.3f}"}
        )

        df_home_style = df_home_new.style.format(
            {"FG_PCT": "{:.3f}", "FG3_PCT": "{:.3f}", "FT_PCT": "{:.3f}"}
        )
    else:
        df_away_style = df_away_new
        df_home_style = df_home_new
    # df_away_style_loc = df_away_style.loc[
    #     df_away_style["MIN"] == 0,
    #     [
    #         "FGM",
    #         "FGA",
    #         "FG_PCT",
    #         "FG3M",
    #         "FG3A",
    #         "FG3_PCT",
    #         "FTM",
    #         "FTA",
    #         "FT_PCT",
    #         "OREB",
    #         "DREB",
    #         "REB",
    #         "AST",
    #         "STL",
    #         "BLK",
    #         "TO",
    #         "PF",
    #         "PTS",
    #         "PLUS_MINUS",
    #     ],
    # ] = "-"

    df_box_score_team_index_change = ChangeIndexName(
        df_box_score_team, "TEAM_ABBREVIATION"
    )
    df_box_score_team_fin = DropColumns(
        df_box_score_team_index_change,
        [
            "FGM",
            "FGA",
            "FG_PCT",
            "FG3M",
            "FG3A",
            "FG3_PCT",
            "FTM",
            "FTA",
            "FT_PCT",
            "OREB",
            "DREB",
            "REB",
            "AST",
            "STL",
            "BLK",
            "TO",
            "PF",
            "PTS",
            "PLUS_MINUS",
        ],
    )

    if gameStatus == "Final" or gameStatus == "Final/OT":
        df_box_score_team_style = df_box_score_team_fin.style.format(
            {
                "FG_PCT": "{:.3f}",
                "FG3_PCT": "{:.3f}",
                "FT_PCT": "{:.3f}",
                "PLUS_MINUS": "{:.0f}",
            }
        )
    else:
        df_box_score_team_style = df_box_score_team_fin

    # arena = boxscore_game["arena"]["arenaName"]
    # arena_city = boxscore_game["arena"]["arenaCity"]
    # arenaState = boxscore_game["arena"]["arenaState"]
    # attendance = boxscore_game["attendance"]

    # gameStatus = games[i]["gameStatusText"]

    score_table = pd.DataFrame(
        data={
            "1": [away_Team_q1point, home_Team_q1point],
            "2": [away_Team_q2point, home_Team_q2point],
            "3": [away_Team_q3point, home_Team_q3point],
            "4": [away_Team_q4point, home_Team_q4point],
            "TOTAL": [awayTeam_score, homeTeam_score],
        },
        index=[awayTeam_full_name, homeTeam_full_name],
    )
    stastics_away = boxscore_game["awayTeam"]["statistics"]
    stastics_home = boxscore_game["homeTeam"]["statistics"]
    index_away = boxscore_game["awayTeam"]["teamTricode"]
    index_home = boxscore_game["homeTeam"]["teamTricode"]

    df_statistics_away = pd.DataFrame(stastics_away, index=[index_away])
    df_statistics_home = pd.DataFrame(stastics_home, index=[index_home])

    df_statistics = pd.concat([df_statistics_away, df_statistics_home])

    df_statistics_new = df_statistics[
        [
            "biggestLead",
            "biggestLeadScore",
            "biggestScoringRun",
            "biggestScoringRunScore",
            "leadChanges",
            "benchPoints",
            "timeLeading",
            "timesTied",
            "pointsFastBreak",
            "fastBreakPointsAttempted",
            "fastBreakPointsMade",
            "fastBreakPointsPercentage",
            "pointsFromTurnovers",
            "pointsInThePaint",
            "pointsInThePaintAttempted",
            "pointsInThePaintMade",
            "pointsInThePaintPercentage",
            "pointsSecondChance",
            "secondChancePointsAttempted",
            "secondChancePointsMade",
            "secondChancePointsPercentage",
            "fieldGoalsEffectiveAdjusted",
            "trueShootingAttempts",
            "trueShootingPercentage",
            "reboundsPersonal",
            "reboundsTeam",
            "reboundsTeamDefensive",
            "reboundsTeamOffensive",
            "reboundsTotal",
            "assists",
            "turnovers",
            "turnoversTeam",
            "turnoversTotal",
            "assistsTurnoverRatio",
            "foulsOffensive",
            "foulsDrawn",
            "foulsPersonal",
            "foulsTeam",
            "foulsTechnical",
            "foulsTeamTechnical",
        ]
    ]

    row3_spacer1, row3_1, row3_2, row3_3, row3_spacer2 = st.columns(
        (1.5, 2, 1.5, 2, 0.5)
    )

    with row3_1:
        if awayTeam_score > homeTeam_score:
            st.subheader(
                f"{awayTeam}  {awayTeam_score} ◀︎ \n ({awayTeam_win_count}-{awayTeam_lose_count})"
            )

        else:
            st.subheader(
                f"{awayTeam}  {awayTeam_score} \n ({awayTeam_win_count}-{awayTeam_lose_count})"
            )

    with row3_2:
        st.text(f"{gameStatus}")

    with row3_3:
        if awayTeam_score < homeTeam_score:
            st.subheader(
                f" ▶︎ {homeTeam_score}  {homeTeam} \n ({homeTeam_win_count}-{homeTeam_lose_count})"
            )
        else:
            st.subheader(
                f" {homeTeam_score}  {homeTeam} \n ({homeTeam_win_count}-{homeTeam_lose_count})"
            )

    # row4_spacer1, row4_1, row4_2, row4_3, row4_spacer2 = st.columns(
    #     (0.5, 2, 1, 2, 0.5)
    # )

    st.table(score_table)

    st.text(
        f"{leader_away_player} ({awayTeam})  {leader_away_point} PTS  {leader_away_rebounds} REB  {leader_away_assist} AST     {leader_home_player} ({homeTeam})  {leader_home_point} PTS  {leader_home_rebounds} REB  {leader_home_assist} AST"
    )

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Game Information", "Team Stats", "Game Chart", "Box Score"]
    )

    with tab1:
        st.text(f"Arena : {arena}  {arena_city}  {arenaState}  ")
        st.text(f"Attendance :  {attendance}")

    with tab2:
        st.dataframe(df_box_score_team_style)

    with tab3:
        st.dataframe(df_statistics_new)

    with tab4:
        st.text(f"{awayTeam_full_name}")
        st.dataframe(df_away_style)

        st.text(f"{homeTeam_full_name}")
        st.dataframe(df_home_style)

    st.markdown("---")
