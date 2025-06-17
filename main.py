import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler
from commands.start import start_command
from commands.help import help_command
from commands.analyze import analyze_command
from commands.analyze_auto import analyze_auto_command
from utils.logger import get_logger

load_dotenv()
logger = get_logger()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

if __name__ == "__main__":
    logger.info("🚀 Starting bot...")

    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("analyze", analyze_command))            # /analyze <fixture_id>
    app.add_handler(CommandHandler("analyze_auto", analyze_auto_command))  # /analyze_auto

    app.run_polling()
