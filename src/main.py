from aiogram import executor
from src.bot import dp
from src.handlers import common, text, voice
from src.services.speech import SpeechService

def register_handlers():
    """Регистрация всех обработчиков"""
    common.register_handlers(dp)
    text.register_handlers(dp)
    voice.register_handlers(dp)

def main():
    """Точка входа в приложение"""
    print("Инициализация моделей распознавания речи...")
    
    speech_service = SpeechService()
    
    register_handlers()
    
    print("Запуск бота...")
    executor.start_polling(dp, skip_updates=True)

if __name__ == '__main__':
    main()