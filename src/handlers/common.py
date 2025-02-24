from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup

class TranslatorStates(StatesGroup):
    waiting_for_text_ru_th = State()
    waiting_for_text_th_ru = State()
    waiting_for_text_en_th = State()
    waiting_for_text_th_en = State()

async def update_keyboard(message: types.Message):
    """Обновляет клавиатуру"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("🇷🇺 Русский → 🇹🇭 Тайский"))
    keyboard.add(types.KeyboardButton("🇹🇭 Тайский → 🇷🇺 Русский"))
    keyboard.add(types.KeyboardButton("🇬🇧 Английский → 🇹🇭 Тайский"))
    keyboard.add(types.KeyboardButton("🇹🇭 Тайский → 🇬🇧 Английский"))
    
    await message.answer(
        "🔄 Клавиатура обновлена!\n"
        "Выберите направление перевода:",
        reply_markup=keyboard
    )

async def cmd_start(message: types.Message):
    """Обработчик команды /start"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("🇷🇺 Русский → 🇹🇭 Тайский"))
    keyboard.add(types.KeyboardButton("🇹🇭 Тайский → 🇷🇺 Русский"))
    keyboard.add(types.KeyboardButton("🇬🇧 Английский → 🇹🇭 Тайский"))
    keyboard.add(types.KeyboardButton("🇹🇭 Тайский → 🇬🇧 Английский"))
    
    await message.answer(
        "👋 Привет! Я бот-переводчик.\n\n"
        "🔄 Выберите направление перевода:",
        reply_markup=keyboard
    )

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=["start", "help"])
    dp.register_message_handler(update_keyboard, commands=["keyboard"])  # Новая команда