import cv2
from ml.inference.detect_obstacles import ObstacleDetector
from audio.alert_manager import AlertManager

class MetaGlassesSystem:
    def __init__(self, model_path='ml/training/weights/best.pt'):
        self.detector = ObstacleDetector(model_path)
        self.alert_manager = AlertManager()
        self.cap = cv2.VideoCapture(0)  # Webcam
        
    def run(self):
        print("🚀 Starting Meta Glasses System...")
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            detections = self.detector.process_frame(frame)
            
            critical_detections = [d for d in detections if d['critical']]
            for det in critical_detections:
                self.alert_manager.obstacle_detected(
                    det['class_name'], 
                    det['distance']
                )
            
            frame_with_detections = self.detector.draw_detections(frame, detections)
            
            cv2.imshow('Meta Glasses - Obstacle Detection', frame_with_detections)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    system = MetaGlassesSystem()
    system.run()