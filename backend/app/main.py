from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from sqlalchemy import text
from .store.db import engine
from .routers import predict, explain
from .routers import search as search_router
from .routers import admin as admin_router


app = FastAPI(title="Fantasy Insights AI")


# CORS for dev/UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Run bootstrap SQL migration once (idempotent)
MIGR = Path(__file__).resolve().parent / "store" / "migrations" / "0001_init.sql"
try:
    with engine.begin() as conn:
        conn.execute(text(MIGR.read_text()))
except Exception as e:
# avoid hard-failing if DB isn't ready yet under hot-reload; logs suffice
    print("[migrate] warning:", e)


# Routers
app.include_router(predict.router)
app.include_router(explain.router)
app.include_router(search_router.router)
app.include_router(admin_router.router)


@app.get("/")
def root():
    return {"ok": True, "service": "fantasy-insights-ai"}