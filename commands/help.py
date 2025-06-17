from telegram import Update
from telegram.ext import ContextTypes

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 *Available Commands:*\n\n"
        "/start - Welcome message\n"
        "/help - Show this help menu\n"
        "/analyze <fixture_id> - Get an in-depth AI-powered prediction and insights for a specific match\n\n"
        "_More features are coming soon!_",
        parse_mode="Markdown"
    )
