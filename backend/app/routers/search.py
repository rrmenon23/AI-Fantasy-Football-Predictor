from fastapi import APIRouter, Query
from sqlalchemy import text
from ..store.db import engine


router = APIRouter(prefix="/search", tags=["search"])


@router.get('/players')
def search_players(q: str = Query(..., min_length=1)):
    sql = text(
        """
        SELECT player_id, name, team, position
        FROM players
        WHERE name ILIKE :q
        ORDER BY name
        LIMIT 25
        """
    )
    with engine.connect() as con:
        rows = [dict(r) for r in con.execute(sql, {"q": f"%{q}%"}).mappings().all()]
    return {"results": rows}