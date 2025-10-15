# Fantasy Insights AI
Start/Sit recommendations and projections for fantasy football with:
FastAPI backend (SportsDataIO ingestion, PPR/Half-PPR scoring, LightGBM models)
React + Vite frontend (name autocomplete, compare UI)
Postgres storage
Docker-friendly dev setup

Features:
Toggle Full PPR / Half PPR
Positions: QB / RB / WR / TE (no K/DST)
Name-based search (autocomplete) – no Player IDs needed
Per-position LightGBM models with rolling features
Templated explanations endpoint (extendable to LLM later)
Ready to wire SportsDataIO Projections for ensembling
