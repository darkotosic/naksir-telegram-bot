import os
import sys
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler

from commands.start import start_command as start
from commands.help import help_command
from commands.analyze import analyze_command as analyze
from commands.analyze_auto import analyze_auto_command as analyze_auto  # ✅ ISPRAVLJENO

from utils.logger import get_logger

if __name__ == "__main__":
    print("🐍 Python version:", sys.version)

load_dotenv()
logger = get_logger()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

if __name__ == "__main__":
    logger.info("🚀 Starting bot...")

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("analyze", analyze))            # /analyze <fixture_id>
    app.add_handler(CommandHandler("analyze_auto", analyze_auto))  # /analyze_auto

    app.run_polling()
