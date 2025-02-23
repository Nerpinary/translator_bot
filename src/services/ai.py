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
        prompt = f"""
        Translate this text from {from_lang} to {to_lang}.
        Return only the translation, without any additional comments.
        Text: {text}
        """
        
        response = await self.model.generate_content_async(prompt)
        return response.text.strip()