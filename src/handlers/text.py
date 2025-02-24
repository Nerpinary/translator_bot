from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from src.handlers.common import TranslatorStates
from src.services.ai import AITranslator
from gtts import gTTS
import os
from aiogram.types import ContentType

translator = AITranslator()

async def process_language_selection(message: types.Message, state: FSMContext):
    """Обработка выбора языка перевода"""
    await state.finish()
    
    if message.text == "🇷🇺 Русский (Russian) → 🇹🇭 ไทย (Thai)":
        await TranslatorStates.waiting_for_text_ru_th.set()
        await message.answer("Отправьте текст для перевода на тайский язык:")
    elif message.text == "🇹🇭 ไทย (Thai) → 🇷🇺 Русский (Russian)":
        await TranslatorStates.waiting_for_text_th_ru.set()
        await message.answer("ส่งข้อความที่ต้องการแปลเป็นภาษารัสเซีย:")
    elif message.text == "🇬🇧 English → 🇹🇭 ไทย (Thai)":
        await TranslatorStates.waiting_for_text_en_th.set()
        await message.answer("Enter text to translate to Thai:")
    elif message.text == "🇹🇭 ไทย (Thai) → 🇬🇧 English":
        await TranslatorStates.waiting_for_text_th_en.set()
        await message.answer("ส่งข้อความที่ต้องการแปลเป็นภาษาอังกฤษ:")

async def translate_ru_to_th(message: types.Message, state: FSMContext):
    """Перевод с русского на тайский"""
    if message.text.startswith('/'):
        return
        
    if message.text in [
        "🇷🇺 Русский (Russian) → 🇹🇭 ไทย (Thai)",
        "🇹🇭 ไทย (Thai) → 🇷🇺 Русский (Russian)",
        "🇬🇧 English → 🇹🇭 ไทย (Thai)",
        "🇹🇭 ไทย (Thai) → 🇬🇧 English"
    ]:
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
    if message.text.startswith('/'):
        return
        
    if message.text in [
        "🇷🇺 Русский (Russian) → 🇹🇭 ไทย (Thai)",
        "🇹🇭 ไทย (Thai) → 🇷🇺 Русский (Russian)",
        "🇬🇧 English → 🇹🇭 ไทย (Thai)",
        "🇹🇭 ไทย (Thai) → 🇬🇧 English"
    ]:
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

async def translate_en_to_th(message: types.Message, state: FSMContext):
    """Перевод с английского на тайский"""
    if message.text.startswith('/'):
        return
        
    if message.text in [
        "🇷🇺 Русский (Russian) → 🇹🇭 ไทย (Thai)",
        "🇹🇭 ไทย (Thai) → 🇷🇺 Русский (Russian)",
        "🇬🇧 English → 🇹🇭 ไทย (Thai)",
        "🇹🇭 ไทย (Thai) → 🇬🇧 English"
    ]:
        await process_language_selection(message, state)
        return
        
    await message.answer("🔄 Translating...")
    translated = await translator.translate(message.text, "English", "Thai")
    
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

async def translate_th_to_en(message: types.Message, state: FSMContext):
    """Перевод с тайского на английский"""
    if message.text.startswith('/'):
        return
        
    if message.text in [
        "🇷🇺 Русский (Russian) → 🇹🇭 ไทย (Thai)",
        "🇹🇭 ไทย (Thai) → 🇷🇺 Русский (Russian)",
        "🇬🇧 English → 🇹🇭 ไทย (Thai)",
        "🇹🇭 ไทย (Thai) → 🇬🇧 English"
    ]:
        await process_language_selection(message, state)
        return
        
    await message.answer("🔄 กำลังแปล...")
    translated = await translator.translate(message.text, "Thai", "English")
    
    try:
        os.makedirs("temp", exist_ok=True)
        tts = gTTS(text=translated, lang='en')
        audio_path = f"temp/voice_{message.message_id}.mp3"
        tts.save(audio_path)
        
        await message.answer(f"🇬🇧 {translated}")
        await message.answer_voice(open(audio_path, 'rb'))
        
        os.remove(audio_path)
    except Exception as e:
        print(f"Ошибка создания аудио: {e}")
        await message.answer(f"🇬🇧 {translated}")

def register_handlers(dp: Dispatcher):
    """Регистрация обработчиков"""
    dp.register_message_handler(
        process_language_selection,
        lambda msg: msg.text in [
            "🇷🇺 Русский (Russian) → 🇹🇭 ไทย (Thai)",
            "🇹🇭 ไทย (Thai) → 🇷🇺 Русский (Russian)",
            "🇬🇧 English → 🇹🇭 ไทย (Thai)",
            "🇹🇭 ไทย (Thai) → 🇬🇧 English"
        ],
        state="*"
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
    dp.register_message_handler(
        translate_en_to_th,
        state=TranslatorStates.waiting_for_text_en_th
    )
    dp.register_message_handler(
        translate_th_to_en,
        state=TranslatorStates.waiting_for_text_th_en
    )
    
    # Обработчик голосовых сообщений
    dp.register_message_handler(
        handle_voice,
        content_types=[ContentType.VOICE, ContentType.AUDIO],
        state="*"
    )

async def handle_voice(message: types.Message, state: FSMContext):
    """Обработчик голосовых сообщений"""
    current_state = await state.get_state()
    
    if current_state == TranslatorStates.waiting_for_text_ru_th.state:
        await message.reply(
            "⚠️ Извините, но распознавание голосовых сообщений временно не поддерживается.\n"
            "Пожалуйста, отправьте ваше сообщение текстом."
        )
    elif current_state == TranslatorStates.waiting_for_text_th_ru.state:
        await message.reply(
            "⚠️ ขออภัย ขณะนี้ไม่รองรับการรับรู้ข้อความเสียง\n"
            "กรุณาส่งข้อความเป็นตัวอักษร"
        )
    elif current_state == TranslatorStates.waiting_for_text_en_th.state:
        await message.reply(
            "⚠️ Sorry, voice message recognition is temporarily unavailable.\n"
            "Please send your message as text."
        )
    elif current_state == TranslatorStates.waiting_for_text_th_en.state:
        await message.reply(
            "⚠️ ขออภัย ขณะนี้ไม่รองรับการรับรู้ข้อความเสียง\n"
            "กรุณาส่งข้อความเป็นตัวอักษร"
        )
    else:
        await message.reply(
            "⚠️ Извините, но распознавание голосовых сообщений временно не поддерживается.\n"
            "Пожалуйста, отправьте ваше сообщение текстом.\n\n"
            "⚠️ Sorry, voice message recognition is temporarily unavailable.\n"
            "Please send your message as text.\n\n"
            "⚠️ ขออภัย ขณะนี้ไม่รองรับการรับรู้ข้อความเสียง\n"
            "กรุณาส่งข้อความเป็นตัวอักษร"
        )