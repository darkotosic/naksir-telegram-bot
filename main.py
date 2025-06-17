import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler

from commands.start import start
from commands.help import help_command
from commands.analyze import analyze
from commands.analyze_auto import analyze_auto  # 🧠 NOVA komanda

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("analyze", analyze))        # /analyze <fixture_id>
app.add_handler(CommandHandler("analyze_auto", analyze_auto))  # 🔁 /analyze_auto

if __name__ == "__main__":
    print("🚀 Bot is running...")
    app.run_polling()
