from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

LANGUAGES = {
    'ru': '🇷🇺 Русский',
    'th': '🇹🇭 Тайский'
}

MAX_VOICE_SIZE = 20 * 1024 * 1024