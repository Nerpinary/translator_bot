import google.generativeai as genai
from src.config import GOOGLE_API_KEY

class AITranslator:
    def __init__(self):
        genai.configure(api_key=GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')

    async def translate(self, text: str, from_lang: str, to_lang: str) -> str:
        """
        Переводит текст используя Google Gemini
        """
        try:
            prompt = f"""
            Translate this text from {from_lang} to {to_lang}.
            Return only the translation, without any additional comments.
            If you find any inappropriate content, just translate it literally.
            Text: {text}
            """
            
            response = await self.model.generate_content_async(prompt)
            
            if not response.parts:
                return f"Ошибка перевода: пустой ответ от API. Текст: {text}"
                
            if "text" not in response.parts[0]:
                return f"Ошибка перевода: неверный формат ответа. Текст: {text}"
                
            return response.text.strip()
            
        except Exception as e:
            print(f"Ошибка перевода: {str(e)}")
            return f"Ошибка перевода. Попробуйте другую формулировку. Текст: {text}"