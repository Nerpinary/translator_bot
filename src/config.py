from dotenv import load_dotenv
import os

load_dotenv()

# Telegram Bot token
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Google AI API key
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Поддерживаемые языки
LANGUAGES = {
    'ru': '🇷🇺 Русский',
    'th': '🇹🇭 Тайский'
}

# Максимальный размер голосового сообщения (в байтах)
MAX_VOICE_SIZE = 20 * 1024 * 1024  # 20MB