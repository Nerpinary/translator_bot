import torch
import tempfile
import os
from gtts import gTTS
import soundfile as sf
import numpy as np

class TTSService:
    def __init__(self):
        self.device = torch.device('cpu')
        torch.set_num_threads(4)
        local_file = 'models/silero_model.pt'
        
        if not os.path.exists(local_file):
            torch.hub.download_url_to_file(
                'https://models.silero.ai/models/tts/ru/v3_1_ru.pt',
                local_file
            )
        
        self.model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
        self.model.to(self.device)
    
    async def text_to_speech(self, text: str, is_russian: bool = True) -> str:
        """
        Преобразует текст в речь
        
        :param text: Текст для озвучивания
        :param is_russian: True для русского, False для тайского
        :return: Путь к аудио файлу
        """
        try:
            if not text:
                raise ValueError("Пустой текст для преобразования в речь")
                
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio:
                if is_russian:
                    sample_rate = 48000
                    speaker = 'xenia'
                    
                    audio = self.model.apply_tts(
                        text=text,
                        speaker=speaker,
                        sample_rate=sample_rate
                    )
                    
                    if audio is None or len(audio) == 0:
                        raise ValueError("Не удалось сгенерировать аудио")
                    
                    audio_np = audio.numpy()
                    sf.write(temp_audio.name, audio_np, sample_rate)
                    
                else:
                    tts = gTTS(text=text, lang='th', slow=False)
                    tts.save(temp_audio.name)
                
                return temp_audio.name
                
        except Exception as e:
            print(f"Error in TTS: {e}")
            raise 