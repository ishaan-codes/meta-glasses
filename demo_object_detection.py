import cv2
import time
import sys
import os

# Add the ml directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'ml/inference'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'audio'))

from ml.inference.detect_obstacles import ObstacleDetector
from audio.alert_manager import AlertManager

class MetaGlassesDemo:
    def __init__(self):
        print("🔄 Initializing Smart Meta Glasses...")
        self.detector = ObstacleDetector()
        self.alert_manager = AlertManager()
        
        # Initialize camera
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("❌ Error: Could not open camera")
            return
        
        # Set camera resolution
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        print("✅ Camera initialized successfully")
        time.sleep(2)  # Allow camera to warm up
        
    def run_demo(self):
        print("\n🚀 Starting Smart Meta Glasses Demo")
        print("🔊 Audio alerts: ENABLED")
        print("📷 Camera: ACTIVE") 
        print("🎯 Object Detection: RUNNING")
        print("Press 'Q' to quit the demo")
        print("-" * 50)
        
        # Welcome message
        self.alert_manager.add_alert("Smart Meta Glasses system activated. Starting object detection.")
        time.sleep(3)
        
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    print("❌ Failed to capture video frame")
                    break
                
                # Process frame for object detection
                detections = self.detector.process_frame(frame)
                
                # Generate alerts for detected objects
                for det in detections:
                    if det['distance'] < 5.0:  # Alert for objects within 5 meters
                        self.alert_manager.obstacle_detected(
                            det['class_name'], 
                            det['distance']
                        )
                
                # Draw detections on frame
                frame_with_detections = self.detector.draw_detections(frame, detections)
                
                # Add info overlay
                cv2.putText(frame_with_detections, "Smart Meta Glasses - Live Demo", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                cv2.putText(frame_with_detections, "Objects Detected: {}".format(len(detections)), 
                           (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                cv2.putText(frame_with_detections, "Press 'Q' to Exit", 
                           (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                
                # Display frame
                cv2.imshow('Smart Meta Glasses - Object Detection Demo', frame_with_detections)
                
                # Exit on 'q' press
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.alert_manager.add_alert("System shutting down. Thank you.")
                    time.sleep(2)
                    break
                    
        except Exception as e:
            print(f"❌ Error during demo: {e}")
        finally:
            # Cleanup
            self.cap.release()
            cv2.destroyAllWindows()
            print("✅ Demo completed successfully")

if __name__ == "__main__":
    print("=" * 60)
    print("        SMART META GLASSES - DEMONSTRATION")
    print("        AI-Powered Assistive Technology")
    print("=" * 60)
    
    demo = MetaGlassesDemo()
    demo.run_demo()