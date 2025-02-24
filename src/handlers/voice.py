from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
import os
import tempfile
from src.handlers.common import TranslatorStates
from src.services.ai import AITranslator
from src.services.tts import TTSService
from src.services.speech import SpeechService

translator = AITranslator()
tts_service = TTSService()
speech_service = SpeechService()

async def process_voice_message(message: types.Message, state: FSMContext):
    """Обработка голосовых сообщений"""
    temp_voice_path = None
    wav_path = None
    status_message = None
    
    try:
        status_message = await message.answer("🎧 Обрабатываю голосовое сообщение...")
        
        current_state = await state.get_state()
        
        if current_state == TranslatorStates.waiting_for_text_ru_th.state:
            from_lang, to_lang = "Russian", "Thai"
            is_russian = True
        elif current_state == TranslatorStates.waiting_for_text_th_ru.state:
            from_lang, to_lang = "Thai", "Russian"
            is_russian = False
        elif current_state == TranslatorStates.waiting_for_text_en_th.state:
            from_lang, to_lang = "English", "Thai"
            is_russian = False
        elif current_state == TranslatorStates.waiting_for_text_th_en.state:
            from_lang, to_lang = "Thai", "English"
            is_russian = False
        else:
            await status_message.edit_text("❌ Неверное состояние перевода")
            return
        
        voice_file = await message.voice.get_file()
        voice_path = voice_file.file_path
        
        temp_fd, temp_voice_path = tempfile.mkstemp(suffix='.ogg')
        os.close(temp_fd)
        await message.bot.download_file(voice_path, temp_voice_path)
        
        wav_path = temp_voice_path + '.wav'
        os.system(f'ffmpeg -i "{temp_voice_path}" -ar 16000 -ac 1 "{wav_path}" -y')
        
        text = speech_service.recognize_speech(wav_path, is_russian=is_russian)
        
        if not text:
            await status_message.edit_text("❌ Не удалось распознать речь. Попробуйте еще раз.")
            return
        
        await message.answer(f"🎯 Распознанный текст:\n{text}")
        
        await status_message.edit_text("🔄 Переводим...")
        translated = await translator.translate(text, from_lang, to_lang)
        
        flag = {
            "Thai": "🇹🇭",
            "Russian": "🇷🇺",
            "English": "🇬🇧"
        }.get(to_lang, "")
        
        await message.answer(f"{flag} {translated}")
        
        audio_path = await tts_service.text_to_speech(
            translated,
            lang='th' if to_lang == "Thai" else ('ru' if to_lang == "Russian" else 'en')
        )
        
        if os.path.exists(audio_path) and os.path.getsize(audio_path) > 0:
            with open(audio_path, 'rb') as audio:
                await message.answer_voice(audio)
        else:
            await message.answer("❌ Не удалось сгенерировать голосовое сообщение")
        
        if os.path.exists(audio_path):
            os.unlink(audio_path)
        
    except Exception as e:
        print(f"Error processing voice message: {e}")
        if status_message:
            await status_message.edit_text("❌ Произошла ошибка при обработке голосового сообщения")
    
    finally:
        if temp_voice_path and os.path.exists(temp_voice_path):
            os.unlink(temp_voice_path)
        if wav_path and os.path.exists(wav_path):
            os.unlink(wav_path)

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(
        process_voice_message,
        content_types=[types.ContentType.VOICE],
        state=[
            TranslatorStates.waiting_for_text_ru_th,
            TranslatorStates.waiting_for_text_th_ru,
            TranslatorStates.waiting_for_text_en_th,
            TranslatorStates.waiting_for_text_th_en
        ]
    )
