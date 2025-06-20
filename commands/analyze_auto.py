from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime, timedelta, timezone
import pytz

from services.api_football import get_raw_fixtures, get_fixture_details
from services.gpt_analyzer import generate_ai_analysis

def select_fixture(fixtures: list) -> dict:
    """Select a fixture within next 12h that has predictions."""
    now = datetime.now(tz=timezone.utc)
    upcoming = []

    for fx in fixtures:
        pred = fx.get("predictions")
        timestamp = fx.get("fixture", {}).get("timestamp")

        if pred and timestamp:
            start_time = datetime.fromtimestamp(timestamp, tz=timezone.utc)
            if now < start_time < now + timedelta(hours=12):
                upcoming.append((start_time, fx))

    if not upcoming:
        return None

    # Return soonest match
    upcoming.sort(key=lambda x: x[0])
    return upcoming[0][1]

# ✅ OVO JE IME KOJE KORISTI main.py
async def analyze_auto_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📅 Searching today's fixtures with predictions...")

    today = datetime.now(tz=pytz.timezone("Europe/Belgrade")).date().isoformat()
    fixtures_data = await get_raw_fixtures(today)
    fixtures = fixtures_data.get("response", [])

    if not fixtures:
        await update.message.reply_text("⚠️ No fixtures found for today.")
        return

    chosen = select_fixture(fixtures)
    if not chosen:
        await update.message.reply_text("⚠️ No suitable fixture found for analysis.")
        return

    fixture_id = chosen["fixture"]["id"]
    await update.message.reply_text(f"🎯 Selected Fixture ID: {fixture_id}\n🧠 Generating AI analysis...")

    details = await get_fixture_details(fixture_id)
    report = await generate_ai_analysis(details)

    await update.message.reply_text(report)
