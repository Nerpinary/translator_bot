from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from src.handlers.common import TranslatorStates
from src.services.ai import AITranslator

translator = AITranslator()

async def process_language_selection(message: types.Message, state: FSMContext):
    """Обработка выбора языка перевода"""
    # Сначала сбрасываем текущее состояние
    await state.finish()
    
    if message.text == "🇷🇺 Русский → 🇹🇭 Тайский":
        await TranslatorStates.waiting_for_text_ru_th.set()
        await message.answer("Отправьте текст для перевода на тайский язык:")
    elif message.text == "🇹🇭 Тайский → 🇷🇺 Русский":
        await TranslatorStates.waiting_for_text_th_ru.set()
        await message.answer("ส่งข้อความที่ต้องการแปลเป็นภาษารัสเซีย:")

async def translate_ru_to_th(message: types.Message, state: FSMContext):
    """Перевод с русского на тайский"""
    if message.text in ["🇷🇺 Русский → 🇹🇭 Тайский", "🇹🇭 Тайский → 🇷🇺 Русский"]:
        await process_language_selection(message, state)
        return
        
    await message.answer("🔄 Переводим...")
    translated = await translator.translate(message.text, "Russian", "Thai")
    await message.answer(f"🇹🇭 {translated}")

async def translate_th_to_ru(message: types.Message, state: FSMContext):
    """Перевод с тайского на русский"""
    if message.text in ["🇷🇺 Русский → 🇹🇭 Тайский", "🇹🇭 Тайский → 🇷🇺 Русский"]:
        await process_language_selection(message, state)
        return
        
    await message.answer("🔄 กำลังแปล...")
    translated = await translator.translate(message.text, "Thai", "Russian")
    await message.answer(f"🇷🇺 {translated}")

def register_handlers(dp: Dispatcher):
    # Обработчики выбора языка
    dp.register_message_handler(
        process_language_selection,
        lambda msg: msg.text in [
            "🇷🇺 Русский → 🇹🇭 Тайский",
            "🇹🇭 Тайский → 🇷🇺 Русский"
        ],
        state="*"  # Обрабатываем в любом состоянии
    )
    
    # Обработчики текста для перевода
    dp.register_message_handler(
        translate_ru_to_th,
        state=TranslatorStates.waiting_for_text_ru_th
    )
    dp.register_message_handler(
        translate_th_to_ru,
        state=TranslatorStates.waiting_for_text_th_ru
    )