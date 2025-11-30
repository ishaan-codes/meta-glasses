import pygame
import time
import os
from typing import Optional

class AudioPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.is_playing = False
        
    def play_audio(self, audio_file: str) -> bool:
        """
        Play audio file using pygame
        Returns True if successful, False otherwise
        """
        try:
            if not os.path.exists(audio_file):
                print(f"Audio file not found: {audio_file}")
                return False
            
            # Stop any currently playing audio
            self.stop_audio()
            
            # Load and play the audio
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            self.is_playing = True
            
            # Wait for playback to complete
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
                
            self.is_playing = False
            return True
            
        except Exception as e:
            print(f"Audio playback error: {e}")
            return False
    
    def stop_audio(self):
        """Stop currently playing audio"""
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False
    
    def cleanup_file(self, audio_file: str):
        """Clean up temporary audio file"""
        try:
            if os.path.exists(audio_file):
                os.remove(audio_file)
                print(f"Cleaned up: {audio_file}")
        except Exception as e:
            print(f"Cleanup warning: {e}")