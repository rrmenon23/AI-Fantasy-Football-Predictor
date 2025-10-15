from sqlalchemy import text
import pandas as pd
from .store.db import engine


FEATURE_COLS = [
    "r3_pass_yds","r3_pass_td","r3_interceptions","r3_rush_att","r3_rush_yds","r3_rush_td",
    "r3_targets","r3_receptions","r3_rec_yds","r3_rec_td"
]


RAW_COLS = [
    "pass_yds","pass_td","interceptions","rush_att","rush_yds","rush_td",
    "targets","receptions","rec_yds","rec_td"
]


def build_features(player_ids: list[int], season: int, week: int) -> pd.DataFrame:
    sql = text(
        """
        SELECT * FROM player_week
        WHERE player_id = ANY(:pids)
        AND (season < :season OR (season=:season AND week <= :week))
        ORDER BY player_id, season, week
        """
    )
    df = pd.read_sql(sql, engine, params={"pids":player_ids, "season":season, "week":week})
    frames = []
    for pid, sub in df.groupby("player_id"):
        sub = sub.sort_values(["season","week"]).copy()
        for col in RAW_COLS:
            sub[f"r3_{col}"] = sub[col].rolling(3, min_periods=1).mean()
        last = sub.iloc[-1:]
        frames.append(last)
    return pd.concat(frames, ignore_index=True)