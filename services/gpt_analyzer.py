import os
import openai
import asyncio
from dotenv import load_dotenv
from services.api_football import get_full_analysis_input
from utils.logger import get_logger  # ✅ Dodaj logger

logger = get_logger()

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def format_prediction_percentages(pred: dict) -> str:
    p = pred.get("predictions", {})
    return f"""
Predictions:
BTTS Yes: {p.get("btts", {}).get("yes", {}).get("percentage", "N/A")}%
BTTS No: {p.get("btts", {}).get("no", {}).get("percentage", "N/A")}%
HT Over 0.5 Goals: {p.get("goals", {}).get("ht_over_0_5", {}).get("percentage", "N/A")}%
Over 1.5 Goals: {p.get("goals", {}).get("over_1_5", {}).get("percentage", "N/A")}%
Over 2.5 Goals: {p.get("goals", {}).get("over_2_5", {}).get("percentage", "N/A")}%
Under 2.5 Goals: {p.get("goals", {}).get("under_2_5", {}).get("percentage", "N/A")}%
Home Win: {p.get("winner", {}).get("home", {}).get("percentage", "N/A")}%
Draw: {p.get("winner", {}).get("draw", {}).get("percentage", "N/A")}%
Away Win: {p.get("winner", {}).get("away", {}).get("percentage", "N/A")}%
""".strip()


async def analyze_fixture(fixture_id: int, home_id: int, away_id: int, league_id: int, season: int) -> str:
    logger.info(f"🎯 Analyzing fixture {fixture_id} between team {home_id} and {away_id}")
    
    data = await get_full_analysis_input(fixture_id, home_id, away_id, league_id, season)

    if "error" in data:
        logger.error(f"❌ Failed to fetch full analysis input: {data['error']}")
        return f"❌ Failed to fetch match data: {data['error']}"

    fixture = data["fixture"]
    predictions = data["predictions"]
    h2h = data["h2h"]
    team_home = data["team_home_stats"]
    team_away = data["team_away_stats"]

    home_name = fixture["teams"]["home"]["name"]
    away_name = fixture["teams"]["away"]["name"]
    date = fixture["fixture"]["date"]
    league = fixture["league"]["name"]
    advice = predictions.get("predictions", {}).get("advice", "No advice available")

    home_form = team_home.get("form", "N/A")
    away_form = team_away.get("form", "N/A")

    logger.info(f"🧠 Creating GPT prompt for match: {home_name} vs {away_name}")

    prompt = f"""
You are a professional football analyst.
Analyze the following match using the form, head-to-head, predictions and team stats.

Match: {home_name} vs {away_name}
Date: {date}
League: {league}
Bookie Advice: {advice}

Team Form:
- {home_name}: {home_form}
- {away_name}: {away_form}

H2H: {len(h2h)} recent matches available.

Generate a concise but smart analysis of the likely match outcome. Be neutral, do not mention "as an AI", and do not explain the data source.
"""

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.7
        )

        analysis = completion["choices"][0]["message"]["content"].strip()
        prediction_block = format_prediction_percentages(predictions)

        logger.info(f"✅ GPT analysis complete for fixture {fixture_id}")
        return f"{analysis}\n\n{prediction_block}"

    except Exception as e:
        logger.error(f"❌ GPT API failed: {e}")
        return f"❌ GPT analysis failed: {str(e)}"

from utils.logger import get_logger
logger = get_logger()

async def generate_ai_analysis(data: dict) -> str:
    try:
        fixture = data["fixture"]
        fixture_id = fixture["fixture"]["id"]
        home_id = fixture["teams"]["home"]["id"]
        away_id = fixture["teams"]["away"]["id"]
        league_id = fixture["league"]["id"]
        season = fixture["league"]["season"]

        logger.info(f"Generating GPT analysis for fixture {fixture_id}")
        return await analyze_fixture(fixture_id, home_id, away_id, league_id, season)

    except Exception as e:
        logger.error(f"generate_ai_analysis failed: {str(e)}")
        return f"❌ Analysis failed: {str(e)}"
