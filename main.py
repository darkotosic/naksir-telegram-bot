import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler

from commands.start import start_command
from commands.help import help_command
from commands.analyze import analyze_command as analyze
from commands.analyze_auto import analyze_auto_command as analyze_auto

from utils.logger import get_logger

load_dotenv()
logger = get_logger()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("start", start_command))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("analyze", analyze))
app.add_handler(CommandHandler("analyze_auto", analyze_auto))

if __name__ == "__main__":
    logger.info("🚀 Bot is starting...")
    print("🚀 Bot is running...")
    app.run_polling()
