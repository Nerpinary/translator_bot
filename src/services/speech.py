from gtts import gTTS
import os
import tempfile

class SpeechService:
    """Сервис для работы с преобразованием текста в речь"""
    
    @staticmethod
    def get_lang_code(language: str) -> str:
        """Преобразует название языка в код для gTTS"""
        lang_map = {
            "Thai": "th",
            "Russian": "ru",
            "English": "en"
        }
        return lang_map.get(language, "en")
    
    @staticmethod
    def text_to_speech(text: str, language: str) -> str:
        """
        Преобразует текст в голосовое сообщение
        
        Args:
            text: Текст для озвучки
            language: Язык ('Thai', 'Russian', 'English')
            
        Returns:
            str: Путь к аудио файлу или None в случае ошибки
        """
        try:
            os.makedirs("temp", exist_ok=True)
            
            lang_code = SpeechService.get_lang_code(language)
            
            audio_path = f"temp/tts_{hash(text)}_{lang_code}.mp3"
            
            tts = gTTS(text=text, lang=lang_code)
            tts.save(audio_path)
            
            return audio_path
            
        except Exception as e:
            print(f"Ошибка создания аудио: {e}")
            return None