import google.generativeai as genai
from src.config import GOOGLE_API_KEY

class AITranslator:
    # Словарь замен (можно расширять)
    REPLACEMENTS = {
        "блять": "блин",
        "хуй": "мужское достоинство",
        "нахуй": "к черту",
        "хуево": "довольно плдохо",
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
        "бля": "блин",
        "блядь": "блин",
        "блядство": "ужас",
        "блядствовать": "ходить по женщинам",
        "срань": "ужас",
        "срать": " в туалет",
        "посрать": "сходить в туалет",
        "пиздун": "врун",
        "пиздунья": "врунья",
        "насрано": "грязно",
        "засрано": "грязно",
        "засрать": "намусорить",
        "насрать": "сходить в туалет или намусорить",
    }

    def __init__(self):
        genai.configure(api_key=GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')

    def clean_text(self, text: str) -> str:
        """Заменяет нецензурные слова на приемлемые аналоги"""
        text_lower = text.lower()
        result = text
        
        for bad, good in self.REPLACEMENTS.items():
            if f" {bad} " in f" {text_lower} ":
                result = result.replace(bad, good)
                result = result.replace(bad.capitalize(), good.capitalize())
                result = result.replace(bad.upper(), good.upper())
        
        return result

    async def translate(self, text: str, from_lang: str, to_lang: str) -> str:
        """Переводит текст используя Google Gemini"""
        try:
            # Сначала очищаем текст
            cleaned_text = self.clean_text(text)
            
            prompt = f"""
            Translate this text from {from_lang} to {to_lang}.
            Return only the translation, without any additional comments.
            Text: {cleaned_text}
            """
            
            response = await self.model.generate_content_async(prompt)
            
            if not response.parts or "text" not in response.parts[0]:
                return f"Ошибка перевода. Попробуйте переформулировать сообщение."
            
            return response.text.strip()
            
        except Exception as e:
            print(f"Ошибка перевода: {str(e)}")
            return f"Ошибка перевода. Попробуйте другую формулировку."