from telegram import Update
from telegram.ext import ContextTypes
from services.api_football import get_fixture_details
from services.gpt_analyzer import generate_ai_analysis

async def analyze_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗ Usage: /analyze <fixture_id>")
        return

    fixture_id = context.args[0]
    if not fixture_id.isdigit():
        await update.message.reply_text("❗ Invalid fixture ID. Please provide a numeric ID.")
        return

    await update.message.reply_text("🔍 Fetching match data...")

    try:
        details = await get_fixture_details(int(fixture_id))
        if not details:
            await update.message.reply_text("⚠️ Could not fetch fixture details.")
            return

        await update.message.reply_text("🧠 Generating AI analysis...")
        report = await generate_ai_analysis(details)

        await update.message.reply_text(report)
    except Exception as e:
        await update.message.reply_text(f"❌ Error during analysis: {str(e)}")
