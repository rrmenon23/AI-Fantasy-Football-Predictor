import pandas as pd
from sqlalchemy import text
from ..store.db import engine
import lightgbm as lgb
import joblib
from pathlib import Path
POSITIONS = ["QB","RB","WR","TE"]

FEATURES = [
"pass_yds","pass_td","interceptions","rush_att","rush_yds","rush_td",
"targets","receptions","rec_yds","rec_td"
]
MODEL_DIR = Path(__file__).resolve().parent / "models"
MODEL_DIR.mkdir(exist_ok=True)
POSITIONS = ["QB","RB","WR","TE"]


def fetch_frame():
    q = """
    SELECT player_id, position, season, week, team, opp,
    pass_yds, pass_td, interceptions, rush_att, rush_yds, rush_td,
    targets, receptions, rec_yds, rec_td,
    ppr, half_ppr
    FROM player_week
    WHERE season >= 2019
    """
    return pd.read_sql(text(q), engine)




def add_rolls(df: pd.DataFrame, target_col: str) -> pd.DataFrame:
    df = df.sort_values(["player_id","season","week"]).copy()
    for col in FEATURES:
        df[f"r3_{col}"] = (
            df.groupby("player_id")[col]
            .rolling(3, min_periods=1).mean().reset_index(level=0, drop=True)
        )
    df["y"] = df.groupby("player_id")[target_col].shift(-1) # next-week points
    return df.dropna(subset=["y"])




def train_all(target_col: str = "ppr"):
    df = fetch_frame()
    df = add_rolls(df, target_col)
    for pos in POSITIONS:
        dpos = df[df.position==pos]
        if len(dpos) < 200:
            print(f"[train] skip {pos} — not enough rows")
            continue
        X = dpos[[c for c in dpos.columns if c.startswith("r3_")]].values
        y = dpos["y"].values
        dtrain = lgb.Dataset(X, label=y)
        params = dict(objective="regression", metric="mae", learning_rate=0.05, num_leaves=31)
        booster = lgb.train(params, dtrain, num_boost_round=600)
        joblib.dump(booster, MODEL_DIR / f"lgb_{pos}_{target_col}.joblib")
        print(f"[train] saved {pos} -> {MODEL_DIR / f'lgb_{pos}_{target_col}.joblib'}")


if __name__ == "__main__":
    # Train both targets
    train_all("ppr")
    train_all("half_ppr")