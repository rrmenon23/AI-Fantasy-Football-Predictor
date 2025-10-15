from pydantic import BaseModel
from typing import List, Literal


Scoring = Literal["ppr","half_ppr"]


class CompareReq(BaseModel):
    players: List[int] # PlayerIDs
    season: int
    week: int
    scoring: Scoring = "ppr"


class CompareRespItem(BaseModel):
    player_id: int
    name: str
    team: str
    position: str
    points: float
    reasons: list[str] = []


class CompareResp(BaseModel):
    predictions: List[CompareRespItem]
    recommendation: str
    confidence: float
    caveats: list[str] = []