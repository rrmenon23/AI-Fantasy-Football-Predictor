from fastapi import APIRouter
from sqlalchemy import text
from ..schemas import CompareReq, CompareResp
from ..ml.infer import load_model
from ..scoring import build_features, FEATURE_COLS
from ..store.db import engine


router = APIRouter(prefix="/predict", tags=["predict"])


@router.post("/compare", response_model=CompareResp)
def compare(req: CompareReq):
    feats = build_features(req.players, req.season, req.week)
    rows = []
    for _, r in feats.iterrows():
        pos = r["position"]
        model = load_model(pos, req.scoring)
        X = r[FEATURE_COLS].values.reshape(1, -1)
        yhat = float(model.predict(X)[0])
        rows.append({
        "player_id": int(r["player_id"]),
        "points": yhat,
        "name": "", # filled below
        "team": r["team"],
        "position": pos,
        })
    # fill names
    with engine.connect() as conn:
        q = conn.execute(text("SELECT player_id, name FROM players WHERE player_id = ANY(:ids)"),
            {"ids":[x["player_id"] for x in rows]})
        name_map = {pid:name for pid,name in q}
    for x in rows:
        x["name"] = name_map.get(x["player_id"], str(x["player_id"]))


    # recommendation
    best = max(rows, key=lambda x: x["points"]) if rows else None
    rec = f"Start {best['name']}" if best else "Insufficient data"
    conf = 0.65 # placeholder; wire quantile models later
    return {"predictions": rows, "recommendation": rec, "confidence": conf, "caveats": []}