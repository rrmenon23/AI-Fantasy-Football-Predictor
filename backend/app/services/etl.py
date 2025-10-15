from datetime import datetime, timezone
from sqlalchemy import text
import pandas as pd
from .sportsdata import SDIO
from ..store.db import SessionLocal
from ..store import models


# Scoring helpers (PPR & Half-PPR)


def score_row_ppr(r: pd.Series) -> float:
    return (
    0.04 * r.get("PassingYards", 0)
    + 4 * r.get("PassingTouchdowns", 0)
    - 2 * r.get("PassingInterceptions", 0)
    + 0.1 * (r.get("RushingYards", 0) + r.get("ReceivingYards", 0))
    + 6 * (r.get("RushingTouchdowns", 0) + r.get("ReceivingTouchdowns", 0))
    - 2 * r.get("FumblesLost", 0)
    + 1 * r.get("Receptions", 0)
    )

def score_row_half_ppr(r: pd.Series) -> float:
    return score_row_ppr(r) - 0.5 * r.get("Receptions", 0)

class Ingestor:
    def __init__(self):
        self.sd = SDIO()
    
    def resolve_current_week(self, season: str) -> int:
        sched = self.sd.schedules(season)
        now = datetime.now(timezone.utc)
        weeks = []
        for g in sched:
            dt_raw = g.get("DateTimeUTC") or g.get("DateTime")
            try:
                dt = datetime.fromisoformat(dt_raw)
            except Exception:
                continue
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            wk = int(g.get("Week") or 0)
            if wk:
                weeks.append(wk)
        return max(weeks) if weeks else 1


    def load_players_and_teams(self):
        db = SessionLocal()
        try:
            teams = self.sd.teams_all()
            players = self.sd.players_all()
            for t in teams:
                db.execute(text(
                    "INSERT INTO teams(team_id, key, name, city) VALUES (:id,:key,:name,:city) "
                    "ON CONFLICT (team_id) DO UPDATE SET key=EXCLUDED.key, name=EXCLUDED.name, city=EXCLUDED.city"
                ), {"id": t.get("TeamID"), "key": t.get("Key"), "name": t.get("Name"), "city": t.get("City")})
            for p in players:
                db.execute(text(
                "INSERT INTO players(player_id, name, team, position, active) VALUES (:pid,:name,:team,:pos,:act) "
                "ON CONFLICT (player_id) DO UPDATE SET name=EXCLUDED.name, team=EXCLUDED.team, position=EXCLUDED.position, active=EXCLUDED.active"
                ), {"pid": p.get("PlayerID"), "name": p.get("Name"), "team": p.get("Team"), "pos": p.get("Position"), "act": p.get("Active", True)})
                db.commit()
        finally:
            db.close()

    def load_week(self, season: str, week: int) -> int:
        rows = self.sd.player_game_stats_by_week(season, week)
        df = pd.DataFrame(rows)
        if df.empty:
            return 0
        df["ppr"] = df.apply(score_row_ppr, axis=1)
        df["half_ppr"] = df.apply(score_row_half_ppr, axis=1)
        db = SessionLocal()
        try:
            db.execute(text("DELETE FROM player_week WHERE season=:s AND week=:w"), {"s": int(season[:4]), "w": week})
            for _, r in df.iterrows():
                db.execute(text(
                """
                INSERT INTO player_week(
                player_id, game_key, season, week, team, opp, position,
                pass_yds, pass_td, interceptions, rush_att, rush_yds, rush_td,
                targets, receptions, rec_yds, rec_td, fumbles_lost, ppr, half_ppr, created_at
                ) VALUES (
                :player_id, :game_key, :season, :week, :team, :opp, :position,
                :pass_yds, :pass_td, :interceptions, :rush_att, :rush_yds, :rush_td,
                :targets, :receptions, :rec_yds, :rec_td, :fumbles_lost, :ppr, :half_ppr, NOW()
                ) ON CONFLICT (player_id, season, week) DO UPDATE SET
                game_key=EXCLUDED.game_key, team=EXCLUDED.team, opp=EXCLUDED.opp, position=EXCLUDED.position,
                pass_yds=EXCLUDED.pass_yds, pass_td=EXCLUDED.pass_td, interceptions=EXCLUDED.interceptions,
                rush_att=EXCLUDED.rush_att, rush_yds=EXCLUDED.rush_yds, rush_td=EXCLUDED.rush_td,
                targets=EXCLUDED.targets, receptions=EXCLUDED.receptions, rec_yds=EXCLUDED.rec_yds, rec_td=EXCLUDED.rec_td,
                fumbles_lost=EXCLUDED.fumbles_lost, ppr=EXCLUDED.ppr, half_ppr=EXCLUDED.half_ppr
                """
                ), {
                "player_id": int(r.get("PlayerID")),
                "game_key": str(r.get("GameKey")),
                "season": int(r.get("Season", int(season[:4]))),
                "week": int(r.get("Week", week)),
                "team": r.get("Team"),
                "opp": r.get("Opponent"),
                "position": r.get("Position"),
                "pass_yds": float(r.get("PassingYards", 0) or 0),
                "pass_td": float(r.get("PassingTouchdowns", 0) or 0),
                "interceptions": float(r.get("PassingInterceptions", 0) or 0),
                "rush_att": float(r.get("RushingAttempts", 0) or 0),
                "rush_yds": float(r.get("RushingYards", 0) or 0),
                "rush_td": float(r.get("RushingTouchdowns", 0) or 0),
                "targets": float(r.get("ReceivingTargets", 0) or 0),
                "receptions": float(r.get("Receptions", 0) or 0),
                "rec_yds": float(r.get("ReceivingYards", 0) or 0),
                "rec_td": float(r.get("ReceivingTouchdowns", 0) or 0),
                "fumbles_lost": float(r.get("FumblesLost", 0) or 0),
                "ppr": float(r.get("ppr", 0) or 0),
                "half_ppr": float(r.get("half_ppr", 0) or 0),
                })
            db.commit()
            return len(df)
        finally:
            db.close()