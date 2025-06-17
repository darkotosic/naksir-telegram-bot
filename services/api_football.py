import os
import httpx
import asyncio
from dotenv import load_dotenv
from cachetools import TTLCache
from datetime import date

from utils.logger import get_logger  # ✅ Logger dodat

logger = get_logger()

load_dotenv()

API_KEY = os.getenv("API_FOOTBALL_KEY")
BASE_URL = "https://v3.football.api-sports.io"
HEADERS = {"x-apisports-key": API_KEY}

# Cache settings
cache_lock = asyncio.Lock()
cache = TTLCache(maxsize=1000, ttl=3600)

# General fetch
async def fetch(endpoint: str, params: dict = None):
    key = f"{endpoint}_{str(params)}"
    async with cache_lock:
        if key in cache:
            logger.info(f"Cache hit: {key}")
            return cache[key]

    try:
        logger.info(f"Fetching: {endpoint} {params}")
        async with httpx.AsyncClient() as client:
            res = await client.get(f"{BASE_URL}/{endpoint}", headers=HEADERS, params=params)
            data = res.json()
            async with cache_lock:
                cache[key] = data
            return data
    except Exception as e:
        logger.error(f"Fetch failed: {endpoint} {params} -> {e}")
        return {"error": str(e), "response": []}

# Core enrichments
async def get_fixture_details(fixture_id: int):
    logger.info(f"🔎 Getting details for fixture {fixture_id}")
    fixture_data = await fetch("fixtures", {"id": fixture_id})
    fixture = fixture_data.get("response", [])[0]

    home_id = fixture["teams"]["home"]["id"]
    away_id = fixture["teams"]["away"]["id"]
    league_id = fixture["league"]["id"]
    season = fixture["league"]["season"]

    logger.info(f"⚙️ Enriching fixture {fixture_id} with predictions, odds, stats, h2h")

    pred, odds, stats, h2h, th, ta = await asyncio.gather(
        fetch("predictions", {"fixture": fixture_id}),
        fetch("odds", {"fixture": fixture_id}),
        fetch("fixtures/statistics", {"fixture": fixture_id}),
        fetch("fixtures/headtohead", {"h2h": f"{home_id}-{away_id}"}),
        fetch("teams/statistics", {"team": home_id, "league": league_id, "season": season}),
        fetch("teams/statistics", {"team": away_id, "league": league_id, "season": season}),
    )

    return {
        "fixture": fixture,
        "predictions": pred.get("response", [])[0] if pred.get("response") else {},
        "odds": odds.get("response", [])[0] if odds.get("response") else {},
        "statistics": stats.get("response", []),
        "h2h": h2h.get("response", []),
        "team_home_stats": th.get("response", {}),
        "team_away_stats": ta.get("response", {}),
    }

# get_full_analysis_input za GPT analizu
async def get_full_analysis_input(fixture_id: int, home_id: int, away_id: int, league_id: int, season: int):
    try:
        f, p, o, s, h2h, th, ta = await asyncio.gather(
            fetch("fixtures", {"id": fixture_id}),
            fetch("predictions", {"fixture": fixture_id}),
            fetch("odds", {"fixture": fixture_id}),
            fetch("fixtures/statistics", {"fixture": fixture_id}),
            fetch("fixtures/headtohead", {"h2h": f"{home_id}-{away_id}"}),
            fetch("teams/statistics", {"team": home_id, "league": league_id, "season": season}),
            fetch("teams/statistics", {"team": away_id, "league": league_id, "season": season}),
        )

        return {
            "fixture": f.get("response", [])[0],
            "predictions": p.get("response", [])[0],
            "odds": o.get("response", [])[0],
            "statistics": s.get("response", []),
            "h2h": h2h.get("response", []),
            "team_home_stats": th.get("response", {}),
            "team_away_stats": ta.get("response", {}),
        }
    except Exception as e:
        return {"error": str(e)}

async def get_raw_fixtures(date: str):
    return await fetch("fixtures", {"date": date, "timezone": "Europe/Belgrade"})
