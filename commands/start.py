from telegram import Update 
from telegram.ext import ContextTypes

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Naksir VIP Bot!\n\n"
        "Use /help to see available commands.\n"
        "Use /analyze <fixture_id> to get an in-depth AI-powered match analysis."
    )
