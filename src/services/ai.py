import google.generativeai as genai
from src.config import GOOGLE_API_KEY
import time
from typing import Optional

class AITranslator:
    REPLACEMENTS = {
        "блять": "блин",
        "хуй": "мужское достоинство",
        "нахуй": "к черту",
        "хуево": "довольно плохо",
        "пиздец": "ужас",
        "пизда": "женская половая часть или плохая женщина",
        "пиздато": "очень хорошо",
        "пиздатый": "очень хороший",
        "пиздатая": "очень хорошая",
        "ебать": "вот это да",
        "ебаться": "заняться любовью",
        "ебун": "плохой человек",
        "ебанутый": "недальновидный человек",
        "ебнутый": "недальновидный человек",
        "еблан": "плохой человек",
        "ебланы": "плохие люди",   
        "охуеть": "обалдеть",
        "сука": "блин или самка собаки (если в контексте)",
        "сучка": "плохой человек или самка собаки (если в контексте)",
        "сучки": "плохие люди или самки собак (если в контексте)",
        "сучара": "плохой человек",
        "бля": "блин",
        "блядь": "блин",
        "блядство": "ужас",
        "блядствовать": "ходить по женщинам",
        "срань": "ужас",
        "срать": "сходить в туалет по большому",
        "посрать": "сходить в туалет по большому",
        "ссать": "сходить в туалет по маленькому",
        "поссать": "сходить в туалет по маленькому",
        "обосрать": "намусорить",
        "обосранец": "грязный человек",
        "обосраный": "грязный человек",
        "обоссать": "унизить",
        "обоссаный": "униженный",
        "обоссаная": "униженная",
        "обосранная": "грязная",
        "пиздун": "врун",
        "пиздунья": "врунья",
        "насрано": "грязно",
        "засрано": "грязно",
        "засрать": "намусорить",
        "насрать": "сходить в туалет или намусорить",
        "анус": "отверстие между ягодицами",
        "анусом": "отверстием между ягодицами",
        "анусы": "отверстия между ягодицами",
        "говно": "грязь или человеческие отходы",
        "говнище": "грязь или человеческие отходы",
        "говнецо": "грязь или человеческие отходы",
        "говнеца": "грязи или человеческих отходов", 
        "пидорас": "грязный человек или человек нетрадиционной сексуальной ориентации",
        "пидор": "грязный человек или человек нетрадиционной сексуальной ориентации",
        "пидоры": "грязные люди или люди нетрадиционной сексуальной ориентации",
        "пидорасы": "грязные люди или люди нетрадиционной сексуальной ориентации",
        "пидарас": "грязный человек или человек нетрадиционной сексуальной ориентации",
        "пидарасы": "грязные люди или люди нетрадиционной сексуальной ориентации",
        "педик": "человек нетрадиционной сексуальной ориентации",
        "педики": "люди нетрадиционной сексуальной ориентации", 
        "fuck": "darn",
        "fucking": "freaking",
        "fucked": "messed up",
        "shit": "stuff",
        "shitty": "bad",
        "bitch": "mean person",
        "bastard": "bad person",
        "ass": "bottom",
        "asshole": "mean person",
        "dick": "mean person",
        "pussy": "coward",
        "cunt": "mean person",
        "whore": "bad person",
        "slut": "bad person",
        "motherfucker": "very bad person",
        "cocksucker": "bad person",
        "damn": "darn",
        "goddamn": "darn",
        "piss": "urinate",
        "pissed": "angry",
        "cock": "rooster",
        "wtf": "what the heck",
        "stfu": "be quiet",
        "fck": "darn",
        "fuk": "darn",
        "fucker": "bad person",
        "bullshit": "nonsense",
        "ควย": "แย่",
        "เหี้ย": "แย่มาก",
        "สัส": "ไม่ดี",
        "มึง": "คุณ",
        "กู": "ฉัน",
        "เย็ด": "มีเพศสัมพันธ์",
        "หี": "อวัยวะเพศหญิง",
        "จู๋": "อวัยวะเพศชาย",
        "ไอ้": "คุณ",
        "อี": "คุณ",
        "ชิบหาย": "แย่มาก",
        "รึง": "หรือ",
        "มรึง": "คุณ",
        "กระหรี่": "หญิงขายบริการ",
        "อีดอก": "คนไม่ดี",
        "ส้นตีน": "คนไม่ดี",
        "หน้าหี": "คนไม่ดี",
        "ไอ้สัตว์": "คนไม่ดี",
        "สถุล": "ไม่ดี",
        "ระยำ": "แย่",
    }

    def __init__(self):
        self._model = None
        self._last_request_time = 0
        self.RATE_LIMIT_DELAY = 0.5

    @property
    def model(self):
        """Ленивая инициализация модели"""
        if self._model is None:
            genai.configure(api_key=GOOGLE_API_KEY)
            self._model = genai.GenerativeModel('gemini-pro')
        return self._model

    def clean_text(self, text: str) -> str:
        """Улучшенная очистка текста"""
        if not text or text.isspace():
            return text
            
        text_lower = text.lower()
        result = text
        
        result = ' '.join(result.split())
        
        for bad, good in self.REPLACEMENTS.items():
            if f" {bad} " in f" {text_lower} ":
                result = result.replace(bad, good)
                result = result.replace(bad.capitalize(), good.capitalize())
                result = result.replace(bad.upper(), good.upper())
        
        return result.strip()

    def handle_rate_limit(self):
        """Обработка ограничения частоты запросов"""
        current_time = time.time()
        time_since_last = current_time - self._last_request_time
        if time_since_last < self.RATE_LIMIT_DELAY:
            time.sleep(self.RATE_LIMIT_DELAY - time_since_last)
        self._last_request_time = time.time()

    async def translate(self, text: str, from_lang: str, to_lang: str) -> str:
        """Улучшенный перевод текста"""
        if not text or text.isspace():
            return "Ошибка: Пустой текст"

        try:
            cleaned_text = self.clean_text(text)
            print(f"Translating: '{cleaned_text}' from {from_lang} to {to_lang}")
            
            self.handle_rate_limit()
            
            prompt = f"""
            You are a professional translator with deep knowledge of {from_lang} and {to_lang}.
            Your task is to translate the following text, ensuring accuracy and natural language.

            Important rules:
            1. ALWAYS provide a translation, even if the word is complex or unusual
            2. If a direct translation is difficult, provide the closest meaningful equivalent
            3. For adjectives, consider multiple possible contexts
            4. For idioms, translate the meaning rather than word-by-word
            5. Preserve any emotional tone or formality level
            6. If a word has multiple meanings, choose the most likely one based on common usage
            7. For unclear cases, provide the most neutral and widely understood variant

            Original text: {cleaned_text}
            Original language: {from_lang}
            Target language: {to_lang}

            Translate the text above following these rules.
            Return ONLY the translation, without explanations or alternatives.
            """
            
            for attempt in range(3):
                try:
                    response = await self.model.generate_content_async(prompt)
                    
                    if not response.parts:
                        if attempt < 2:
                            if attempt == 1:
                                prompt = f"Translate this from {from_lang} to {to_lang}, simple words only: {cleaned_text}"
                            print(f"Empty response on attempt {attempt + 1}, retrying with simplified prompt...")
                            time.sleep(1)
                            continue
                        return "Ошибка: Не удалось получить перевод"
                    
                    translated_text = response.text.strip()
                    
                    if not translated_text or translated_text.isspace() or len(translated_text) < 2:
                        if attempt < 2:
                            print(f"Invalid translation on attempt {attempt + 1}, retrying...")
                            time.sleep(1)
                            continue
                        return "Ошибка: Некорректный перевод"
                    
                    print(f"Translation success: '{translated_text}'")
                    return translated_text
                    
                except Exception as e:
                    if attempt < 2:
                        print(f"Translation attempt {attempt + 1} failed: {e}")
                        if attempt == 1:
                            prompt = f"Translate: {cleaned_text}"
                        time.sleep(1)
                        continue
                    raise
                    
        except Exception as e:
            error_msg = str(e)
            print(f"Translation error: {error_msg}")
            
            if "quota" in error_msg.lower():
                return "Ошибка: Превышен лимит запросов. Попробуйте позже."
            elif "timeout" in error_msg.lower():
                return "Ошибка: Сервер не отвечает. Попробуйте позже."
            else:
                return "Ошибка перевода. Попробуйте другую формулировку."
