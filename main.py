from os import environ
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, Defaults
from telegram.constants import ParseMode
from commands import start, help, play, kill, guess, about

# Load environment variables if needed
# from dotenv import load_dotenv
# load_dotenv()

TELEGRAM_BOT_TOKEN = environ.get("TELEGRAM_BOT_TOKEN", "7602939669:AAFTTrzXNVNbzVqECDFrZQXYakgw9W6_yhA")
PORT = environ.get("PORT", 8443)

config = Defaults(
    parse_mode=ParseMode.MARKDOWN_V2
)

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).defaults(config).build()

    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("play", play))
    app.add_handler(CommandHandler("kill", kill))
    app.add_handler(CommandHandler("guess", guess))
    app.add_handler(CommandHandler("about", about))

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TELEGRAM_BOT_TOKEN,
        webhook_url="https://pyal.herokuapp.com/" + TELEGRAM_BOT_TOKEN,
    )

if __name__ == "__main__":
    main()
