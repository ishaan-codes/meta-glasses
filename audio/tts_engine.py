from gtts import gTTS
import os
import tempfile
from typing import Optional

class TTSEngine:
    def __init__(self, language: str = 'en', slow_speech: bool = False):
        self.language = language
        self.slow_speech = slow_speech
        self.temp_dir = tempfile.gettempdir()
        
    def text_to_speech(self, text: str, filename: Optional[str] = None) -> str:
        """
        Convert text to speech and save as MP3 file
        Returns path to the generated audio file
        """
        try:
            tts = gTTS(
                text=text,
                lang=self.language,
                slow=self.slow_speech
            )
            
            if filename is None:
                filename = f"alert_{hash(text) % 10000}.mp3"
            
            filepath = os.path.join(self.temp_dir, filename)
            
            tts.save(filepath)
            print(f"✅ Audio saved: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"❌ TTS Error: {e}")
            return ""
    
    def generate_obstacle_alert(self, object_type: str, distance: float) -> str:
        """Generate specific obstacle alert message"""
        if distance < 1.0:
            return f"Warning! {object_type} very close!"
        elif distance < 2.0:
            return f"{object_type} nearby, {distance:.1f} meters"
        else:
            return f"{object_type} ahead, {distance:.1f} meters"
    
    def generate_navigation_alert(self, direction: str, action: str) -> str:
        """Generate navigation instructions"""
        return f"{action}, {direction}"