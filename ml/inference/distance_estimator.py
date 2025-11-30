import numpy as np

class DistanceEstimator:
    def __init__(self):
        # Known average heights for common objects (in meters)
        self.known_heights = {
            'person': 1.7,
            'phone': 0.15,
            'clock': 0.3,
            'chair': 0.9,
            'bottle': 0.25,
            'cup': 0.1,
            'laptop': 0.05,
            'book': 0.02,
            'television': 0.5,
            'keyboard': 0.02,
            'mouse': 0.02,
            'vehicle': 1.5,
            'pole': 3.0,
            'stairs': 0.15,
            'door': 2.0,
            'wall': 2.5,
            'obstacle': 1.0,
            'banana': 0.18,
            'apple': 0.07,
            'bowl': 0.1
        }
        
        self.focal_length = 500
    
    def estimate_distance(self, bbox, class_name, frame_shape):
        """Estimate distance using bounding box height and known object height"""
        known_height = self.known_heights.get(class_name, 1.0)  # Default height
        
        bbox_height = bbox[3] - bbox[1]
        
        if bbox_height > 0:
            distance = (known_height * self.focal_length) / bbox_height
            return max(0.1, distance)
        else:
            return 5.0  # Default distance