from fastapi import APIRouter
from ..services.etl import Ingestor
from ..config import settings


router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/bootstrap")
def bootstrap():
    ing = Ingestor()
    ing.load_players_and_teams()
    return {"ok": True}


@router.post("/ingest/week/{week}")
def ingest_week(week: int):
    ing = Ingestor()
    n = ing.load_week(settings.season, week)
    return {"inserted": n}