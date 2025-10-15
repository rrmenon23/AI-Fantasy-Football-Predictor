import requests
from typing import Any
from ..config import settings


BASE = "https://api.sportsdata.io/v3/nfl"


class SDIO:
    def _get(self, path: str) -> Any:
        url = f"{BASE}{path}?key={settings.sd_key}"
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        return r.json()


    def player_game_stats_by_week(self, season: str, week: int):
        return self._get(f"/stats/json/PlayerGameStatsByWeek/{season}/{week}")


    def schedules(self, season: str):
        return self._get(f"/scores/json/Schedules/{season}")


    def players_all(self):
        return self._get("/scores/json/Players")


    def teams_all(self):
        return self._get("/scores/json/Teams")


    def injuries(self, season: str):
        return self._get(f"/scores/json/Injuries/{season}")


    def depth_charts(self):
        return self._get("/scores/json/DepthCharts")


    def projections_by_week(self, season: str, week: int):
        url = f"{BASE}/projections/json/PlayerGameProjectionStatsByWeek/{season}/{week}?key={settings.sd_key}"
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        return r.json()