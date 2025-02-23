from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from src.handlers.common import TranslatorStates
from src.services.ai import AITranslator
from gtts import gTTS
import os

translator = AITranslator()

async def process_language_selection(message: types.Message, state: FSMContext):
    """Обработка выбора языка перевода"""
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
    
    try:
        os.makedirs("temp", exist_ok=True)
        tts = gTTS(text=translated, lang='th')
        audio_path = f"temp/voice_{message.message_id}.mp3"
        tts.save(audio_path)
        
        await message.answer(f"🇹🇭 {translated}")
        await message.answer_voice(open(audio_path, 'rb'))
        
        os.remove(audio_path)
    except Exception as e:
        print(f"Ошибка создания аудио: {e}")
        await message.answer(f"🇹🇭 {translated}")

async def translate_th_to_ru(message: types.Message, state: FSMContext):
    """Перевод с тайского на русский"""
    if message.text in ["🇷🇺 Русский → 🇹🇭 Тайский", "🇹🇭 Тайский → 🇷🇺 Русский"]:
        await process_language_selection(message, state)
        return
        
    await message.answer("🔄 กำลังแปล...")
    translated = await translator.translate(message.text, "Thai", "Russian")
    
    try:
        os.makedirs("temp", exist_ok=True)
        tts = gTTS(text=translated, lang='ru')
        audio_path = f"temp/voice_{message.message_id}.mp3"
        tts.save(audio_path)
        
        await message.answer(f"🇷🇺 {translated}")
        await message.answer_voice(open(audio_path, 'rb'))
        
        os.remove(audio_path)
    except Exception as e:
        print(f"Ошибка создания аудио: {e}")
        await message.answer(f"🇷🇺 {translated}")

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(
        process_language_selection,
        lambda msg: msg.text in [
            "🇷🇺 Русский → 🇹🇭 Тайский",
            "🇹🇭 Тайский → 🇷🇺 Русский"
        ],
        state="*"
    )
    
    dp.register_message_handler(
        translate_ru_to_th,
        state=TranslatorStates.waiting_for_text_ru_th
    )
    dp.register_message_handler(
        translate_th_to_ru,
        state=TranslatorStates.waiting_for_text_th_ru
    )