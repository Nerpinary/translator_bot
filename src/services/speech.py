from vosk import Model, KaldiRecognizer
import whisper
import json
import os
import wave
import re
from typing import Optional

class SpeechService:
    _model_ru: Optional[Model] = None
    _whisper_model = None
    
    QUESTION_WORDS_RU = {
        'что', 'где', 'когда', 'почему', 'зачем', 'как', 'какой', 'какая', 'какое', 
        'какие', 'кто', 'чей', 'чья', 'чье', 'чьи', 'сколько', 'куда', 'откуда'
    }
    
    QUESTION_PATTERNS_RU = [
        r'\bты\b.*\?$',
        r'\bвы\b.*\?$',
        r'\bон\b.*\?$',
        r'\bона\b.*\?$',
        r'\bоно\b.*\?$',
        r'\bони\b.*\?$',
        r'.*\bли\b.*',
        r'.*\bправда\b.*',
        r'.*\bда\b\?*$',
        r'.*\bверно\b.*',
        r'.*\bтак\b\?*$'
    ]
    
    @classmethod
    def get_model_ru(cls) -> Model:
        """Получает или инициализирует русскую модель"""
        if cls._model_ru is None:
            print("Загрузка русской модели Vosk...")
            if not os.path.exists("models/vosk-model-ru"):
                raise Exception("Пожалуйста, скачайте русскую модель")
            cls._model_ru = Model("models/vosk-model-ru")
            print("Русская модель Vosk загружена!")
        return cls._model_ru
    
    @classmethod
    def get_whisper_model(cls):
        """Получает или инициализирует модель Whisper"""
        if cls._whisper_model is None:
            print("Загрузка модели Whisper...")
            cls._whisper_model = whisper.load_model("base")
            print("Модель Whisper загружена!")
        return cls._whisper_model
    
    def __init__(self):
        self.get_model_ru()
        self.get_whisper_model()
    
    def is_question(self, text: str) -> bool:
        """Определяет, является ли предложение вопросом"""
        text = text.lower().strip()
        
        words = text.split()
        first_word = words[0] if words else ''
        
        if first_word in self.QUESTION_WORDS_RU:
            return True
        
        if any(word in self.QUESTION_WORDS_RU for word in words[1:]):
            return True
        
        intonation_patterns = [
            r'^[а-я\s]+\?$',
            r'.*\bли\b.*',
            r'^а\b.*',
            r'.*\bправда\b.*',
            r'.*\bда\b\s*$',
            r'.*\bтак\b\s*$',
            r'.*\bверно\b\s*$',
            r'.*\bразве\b.*',
            r'.*\bнеужели\b.*',
            r'\bты\b.*',
            r'\bвы\b.*',
            r'\bон\b.*',
            r'\bона\b.*',
            r'\bоно\b.*',
            r'\bони\b.*'
        ]
        
        for pattern in intonation_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        
        return False
    
    def add_punctuation(self, text: str, is_russian: bool = True) -> str:
        """Добавляет знаки препинания на основе анализа текста"""
        if not text:
            return text
            
        text = text.strip()
        
        if is_russian:
            if self.is_question(text):
                return text + "?"
            
            exclamation_patterns = [
                r'\b(привет|здравствуй|ура|здорово|круто|класс|супер|вау|ого|ничего себе|спасибо|благодарю|поздравляю)\b',
                r'!\s*$'
            ]
            
            for pattern in exclamation_patterns:
                if re.search(pattern, text.lower()):
                    return text + "!"
            
            return text + "."
        else:
            thai_question_particles = ['ไหม', 'หรือ', 'เหรอ', 'มั้ย', 'ใช่ไหม']
            
            for particle in thai_question_particles:
                if particle in text:
                    return text + "?"
            
            return text + "."
    
    def recognize_speech(self, audio_path: str, is_russian: bool = True) -> str:
        """Распознает речь из WAV файла и добавляет знаки препинания"""
        if is_russian:
            wf = wave.open(audio_path, "rb")
            rec = KaldiRecognizer(self.get_model_ru(), wf.getframerate())
            rec.SetWords(True)
            
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                rec.AcceptWaveform(data)
            
            result = json.loads(rec.FinalResult())
            text = result.get('text', '')
            
            return self.add_punctuation(text, is_russian=True)
        else:
            result = self.get_whisper_model().transcribe(
                audio_path,
                language='th',
                task='transcribe'
            )
            text = result.get('text', '').strip()
            
            return self.add_punctuation(text, is_russian=False)