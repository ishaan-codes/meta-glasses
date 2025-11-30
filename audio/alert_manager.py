from audio.tts_engine import TTSEngine
from audio.audio_player import AudioPlayer
import threading
import time
from enum import Enum

class AlertPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class AlertManager:
    def __init__(self):
        self.tts_engine = TTSEngine()
        self.audio_player = AudioPlayer()
        self.alert_queue = []
        self.is_processing = False
        
    def add_alert(self, message: str, priority: AlertPriority = AlertPriority.MEDIUM):
        """Add alert to queue with priority"""
        self.alert_queue.append({
            'message': message,
            'priority': priority,
            'timestamp': time.time()
        })
        # Sort by priority (highest first)
        self.alert_queue.sort(key=lambda x: x['priority'], reverse=True)
        
        # Process alerts if not already processing
        if not self.is_processing:
            self._process_alerts()
    
    def _process_alerts(self):
        """Process alerts in a separate thread"""
        def process():
            self.is_processing = True
            while self.alert_queue:
                alert = self.alert_queue.pop(0)
                self._speak_alert(alert['message'])
                time.sleep(0.5)  # Small gap between alerts
            self.is_processing = False
        
        thread = threading.Thread(target=process)
        thread.daemon = True
        thread.start()
    
    def _speak_alert(self, message: str):
        """Convert text to speech and play it"""
        print(f"🔊 Speaking: {message}")
        
        # Generate audio file
        audio_file = self.tts_engine.text_to_speech(message)
        
        if audio_file:
            # Play audio
            success = self.audio_player.play_audio(audio_file)
            
            # Clean up temporary file
            if success:
                self.audio_player.cleanup_file(audio_file)
    
    def emergency_stop(self):
        """Stop all audio immediately"""
        self.alert_queue.clear()
        self.audio_player.stop_audio()
    
    # Predefined alert methods
    def obstacle_detected(self, object_type: str, distance: float):
        """Alert for obstacle detection"""
        message = self.tts_engine.generate_obstacle_alert(object_type, distance)
        
        # Determine priority based on distance
        if distance < 1.0:
            priority = AlertPriority.CRITICAL
        elif distance < 2.0:
            priority = AlertPriority.HIGH
        else:
            priority = AlertPriority.MEDIUM
            
        self.add_alert(message, priority)
    
    def navigation_instruction(self, direction: str, action: str = "turn"):
        """Alert for navigation instructions"""
        message = self.tts_engine.generate_navigation_alert(direction, action)
        self.add_alert(message, AlertPriority.LOW)
    
    def sos_alert(self):
        """Emergency SOS alert"""
        self.add_alert("Emergency! Help needed! Sending location to contacts.", AlertPriority.CRITICAL)