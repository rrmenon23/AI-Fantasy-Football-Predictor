from fastapi import APIRouter
from sqlalchemy import text
from ..schemas import CompareReq
from ..store.db import engine


router = APIRouter(prefix="/explain", tags=["explain"])


@router.post("/startsit")
def startsit(req: CompareReq):
# Example templated explanation using last-game usage
    with engine.connect() as con:
        rows = con.execute(text(
            """
            SELECT pw.player_id, p.name, pw.receptions, pw.targets, pw.rush_att, pw.rec_yds
            FROM player_week pw
            JOIN players p ON p.player_id=pw.player_id
            WHERE season=:s AND week=:w AND pw.player_id = ANY(:ids)
            """
            ), {"s":req.season, "w":req.week-1, "ids":req.players}).mappings().all()
    bullets = [
        f"{r['name']}: {r['receptions']} rec on {r['targets']} targets; {r['rush_att']} rush, {r['rec_yds']} rec yds"
        for r in rows
    ]
    return {"bullets": bullets}