# Fantasy Insights AI
Start/Sit recommendations and projections for fantasy football with:

FastAPI backend (SportsDataIO ingestion, PPR/Half-PPR scoring, LightGBM models)

React + Vite frontend (name autocomplete, compare UI)

Postgres storage

Docker-friendly dev setup

Features

Toggle Full PPR / Half PPR

Positions: QB / RB / WR / TE (no K/DST)

Name-based search (autocomplete) – no Player IDs needed

Per-position LightGBM models with rolling features

Templated explanations endpoint (extendable to LLM later)

Ready to wire SportsDataIO Projections for ensembling

fantasy-insights-ai/
  backend/
    app/
      main.py
      config.py
      schemas.py
      scoring.py
      routers/ (predict, search, explain, admin)
      services/ (sportsdata, etl)
      store/ (db, models, migrations/0001_init.sql)
      ml/ (train.py, infer.py)
    Dockerfile
    requirements.txt
    .env.example
  frontend/
    src/ (App.tsx, components/, lib/api.ts, main.tsx, index.css)
    package.json
    vite.config.ts
    tailwind.config.js
    Dockerfile (optional)
    .env.example
  docker-compose.yml (optional, if you use it)
  README.md
