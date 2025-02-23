from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
import os
import tempfile
from src.handlers.common import TranslatorStates
from src.services.ai import AITranslator
from src.services.tts import TTSService
from src.services.speech import SpeechService

# Инициализируем сервисы
translator = AITranslator()
tts_service = TTSService()
speech_service = SpeechService()  # Создаем один раз

async def process_voice_message(message: types.Message, state: FSMContext):
    """Обработка голосовых сообщений"""
    temp_voice_path = None
    wav_path = None
    status_message = None
    
    try:
        # Сообщаем о начале обработки
        status_message = await message.answer("🎧 Обрабатываю голосовое сообщение...")
        
        # Получаем информацию о текущем состоянии (режиме перевода)
        current_state = await state.get_state()
        is_ru_to_th = current_state == TranslatorStates.waiting_for_text_ru_th.state
        
        # Скачиваем голосовое сообщение
        voice_file = await message.voice.get_file()
        voice_path = voice_file.file_path
        
        # Создаем временные файлы
        temp_fd, temp_voice_path = tempfile.mkstemp(suffix='.ogg')
        os.close(temp_fd)
        
        # Скачиваем файл
        await message.bot.download_file(voice_path, temp_voice_path)
        
        # Конвертируем OGG в WAV
        wav_path = temp_voice_path + '.wav'
        os.system(f'ffmpeg -i "{temp_voice_path}" -ar 16000 -ac 1 "{wav_path}" -y')
        
        # Распознаем речь
        text = speech_service.recognize_speech(wav_path, is_russian=is_ru_to_th)
        
        if not text:
            await status_message.edit_text("❌ Не удалось распознать речь. Попробуйте еще раз.")
            return
        
        # Отправляем распознанный текст
        await message.answer(f"🎯 Распознанный текст:\n{text}")
        
        # Переводим
        await status_message.edit_text("🔄 Переводим...")
        translated = await translator.translate(
            text,
            "Russian" if is_ru_to_th else "Thai",
            "Thai" if is_ru_to_th else "Russian"
        )
        
        # Отправляем текстовый перевод
        await message.answer(
            f"{'🇹🇭' if is_ru_to_th else '🇷🇺'} {translated}"
        )
        
        # Генерируем и отправляем голосовое сообщение
        audio_path = await tts_service.text_to_speech(
            translated,
            is_russian=not is_ru_to_th
        )
        
        # Проверяем, что файл существует и не пустой
        if os.path.exists(audio_path) and os.path.getsize(audio_path) > 0:
            with open(audio_path, 'rb') as audio:
                await message.answer_voice(audio)
        else:
            await message.answer("❌ Не удалось сгенерировать голосовое сообщение")
        
        # Удаляем временный файл с аудио
        if os.path.exists(audio_path):
            os.unlink(audio_path)
        
    except Exception as e:
        print(f"Error processing voice message: {e}")
        if status_message:
            await status_message.edit_text("❌ Произошла ошибка при обработке голосового сообщения")
    
    finally:
        # Удаляем временные файлы
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
            TranslatorStates.waiting_for_text_th_ru
        ]
    )
