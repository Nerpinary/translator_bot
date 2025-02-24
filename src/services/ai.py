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
            Your task is to translate text from {from_lang} to {to_lang}.
            If the text contains inappropriate content:
            1. First, make it appropriate while preserving the main meaning
            2. Then translate the appropriate version
            
            Return only the translation, without any additional comments or explanations.
            
            Text to translate: {text}
            """
            
            response = await self.model.generate_content_async(prompt)
            
            if not response.parts:
                prompt = f"""
                The text might contain inappropriate content.
                Please make it appropriate and translate from {from_lang} to {to_lang}.
                Preserve the main meaning where possible.
                Text: {text}
                """
                response = await self.model.generate_content_async(prompt)
            
            if response.parts and "text" in response.parts[0]:
                return response.text.strip()
            
            return f"Ошибка перевода. Попробуйте переформулировать сообщение. Текст: {text}"
            
        except Exception as e:
            print(f"Ошибка перевода: {str(e)}")
            return f"Ошибка перевода. Попробуйте другую формулировку. Текст: {text}"