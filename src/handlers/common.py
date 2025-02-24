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
    keyboard.add(types.KeyboardButton("🇷🇺 Русский (Russian) → 🇹🇭 ไทย (Thai)"))
    keyboard.add(types.KeyboardButton("🇹🇭 ไทย (Thai) → 🇷🇺 Русский (Russian)"))
    keyboard.add(types.KeyboardButton("🇬🇧 English → 🇹🇭 ไทย (Thai)"))
    keyboard.add(types.KeyboardButton("🇹🇭 ไทย (Thai) → 🇬🇧 English"))
    
    await message.answer(
        "🔄 Клавиатура обновлена! | Keyboard updated! | แป้นพิมพ์อัปเดตแล้ว!\n\n"
        "Выберите направление перевода | Choose translation direction | เลือกทิศทางการแปล:",
        reply_markup=keyboard
    )

async def cmd_start(message: types.Message):
    """Обработчик команды /start"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("🇷🇺 Русский (Russian) → 🇹🇭 ไทย (Thai)"))
    keyboard.add(types.KeyboardButton("🇹🇭 ไทย (Thai) → 🇷🇺 Русский (Russian)"))
    keyboard.add(types.KeyboardButton("🇬🇧 English → 🇹🇭 ไทย (Thai)"))
    keyboard.add(types.KeyboardButton("🇹🇭 ไทย (Thai) → 🇬🇧 English"))
    
    welcome_message = (
        "👋 Привет! Я бот-переводчик.\n"
        "🔄 Выберите направление перевода:\n"
        "\n"
        "👋 Hello! I'm a translator bot.\n"
        "🔄 Choose translation direction:\n"
        "\n"
        "👋 สวัสดี! ฉันคือบอทแปลภาษา\n"
        "🔄 เลือกทิศทางการแปล:"
    )
    
    await message.answer(welcome_message, reply_markup=keyboard)

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=["start", "help"])
    dp.register_message_handler(update_keyboard, commands=["keyboard"])