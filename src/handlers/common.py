from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup

class TranslatorStates(StatesGroup):
    waiting_for_text_ru_th = State()  # Ожидание текста для перевода RU -> TH
    waiting_for_text_th_ru = State()  # Ожидание текста для перевода TH -> RU

async def cmd_start(message: types.Message):
    """
    Обработчик команды /start
    """
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        types.KeyboardButton("🇷🇺 Русский → 🇹🇭 Тайский"),
        types.KeyboardButton("🇹🇭 Тайский → 🇷🇺 Русский")
    )
    
    await message.answer(
        "👋 Привет! Я бот-переводчик с русского на тайский и наоборот.\n\n"
        "🔄 Выберите направление перевода:",
        reply_markup=keyboard
    )

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=["start", "help"])