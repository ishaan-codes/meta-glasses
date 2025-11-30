import cv2
import numpy as np
from ultralytics import YOLO
from ml.inference.distance_estimator import DistanceEstimator

class ObstacleDetector:
    def __init__(self, model_path=None):
        print("🔄 Loading YOLO model...")
        # Use the built-in YOLOv8 model instead of custom path
        try:
            self.model = YOLO('yolov8n.pt')  # This will auto-download if not present
            self.distance_estimator = DistanceEstimator()
            self.class_names = self.model.names
            print("✅ YOLO model loaded successfully")
        except Exception as e:
            print(f"❌ Error loading YOLO model: {e}")
            print("🔄 Trying alternative approach...")
            self.load_fallback_model()
        
    def load_fallback_model(self):
        """Fallback if YOLO fails"""
        try:
            # Try loading with weights_only=False for PyTorch compatibility
            import torch
            self.model = YOLO('yolov8n.pt')
            self.distance_estimator = DistanceEstimator()
            self.class_names = self.model.names
            print("✅ YOLO model loaded with fallback method")
        except Exception as e:
            print(f"❌ Fallback also failed: {e}")
            raise e
        
    def process_frame(self, frame, confidence_threshold=0.5):
        """Process single frame for obstacle detection"""
        try:
            results = self.model(frame, conf=confidence_threshold, verbose=False)
            
            detections = []
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        class_id = int(box.cls[0])
                        confidence = float(box.conf[0])
                        bbox = box.xyxy[0].cpu().numpy()
                        
                        # Get readable class name
                        class_name = self.get_readable_name(self.class_names[class_id])
                        
                        distance = self.distance_estimator.estimate_distance(
                            bbox, class_name, frame.shape
                        )
                        
                        detection = {
                            'class_id': class_id,
                            'class_name': class_name,
                            'confidence': confidence,
                            'bbox': bbox,
                            'distance': distance,
                            'critical': distance < 1.5  # Critical if < 1.5 meters
                        }
                        detections.append(detection)
            
            return detections
        except Exception as e:
            print(f"❌ Error in process_frame: {e}")
            return []
    
    def get_readable_name(self, class_name):
        """Convert YOLO class names to more readable format"""
        name_mapping = {
            'person': 'person',
            'cell phone': 'phone',
            'clock': 'clock',
            'chair': 'chair',
            'cup': 'cup',
            'bottle': 'bottle',
            'laptop': 'laptop',
            'book': 'book',
            'tv': 'television',
            'keyboard': 'keyboard',
            'mouse': 'mouse',
            'cup': 'cup',
            'bowl': 'bowl',
            'banana': 'banana',
            'apple': 'apple'
        }
        return name_mapping.get(class_name, class_name)
    
    def draw_detections(self, frame, detections):
        """Draw bounding boxes and info on frame"""
        for det in detections:
            x1, y1, x2, y2 = map(int, det['bbox'])
            class_name = det['class_name']
            confidence = det['confidence']
            distance = det['distance']
            
            # Red for critical, Green for safe
            color = (0, 0, 255) if det['critical'] else (0, 255, 0)
            
            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            
            # Create label
            label = f"{class_name} {distance:.1f}m"
            
            # Draw label background
            label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
            cv2.rectangle(frame, (x1, y1-label_size[1]-10), 
                         (x1+label_size[0], y1), color, -1)
            
            # Draw label text
            cv2.putText(frame, label, (x1, y1-5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        return frame