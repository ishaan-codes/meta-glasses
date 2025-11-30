from ultralytics import YOLO
import yaml
import torch

class MetaGlassesTrainer:
    def __init__(self, model_size='n'):
        """
        Initialize YOLO trainer for Meta Glasses
        model_size: n, s, m, l, x (nano to extra-large)
        """
        self.model_size = model_size
        self.model = YOLO(f'yolov8{model_size}.pt')
        
    def setup_data(self, data_yaml='../data/dataset.yaml'):
        """Verify and setup dataset"""
        with open(data_yaml, 'r') as f:
            self.data_config = yaml.safe_load(f)
        print(f"📊 Training on {self.data_config['nc']} classes: {self.data_config['names']}")
    
    def train_model(self, epochs=100, imgsz=640, batch=16):
        """Train the YOLO model"""
        print("🚀 Starting YOLO training for Meta Glasses...")
        
        results = self.model.train(
            data='../data/dataset.yaml',
            epochs=epochs,
            imgsz=imgsz,
            batch=batch,
            patience=10,           # Early stopping
            save=True,
            exist_ok=True,
            device='cuda' if torch.cuda.is_available() else 'cpu',
            name=f'meta_glasses_v8{self.model_size}'
        )
        
        return results
    
    def evaluate_model(self):
        """Evaluate trained model"""
        metrics = self.model.val()
        print(f"Model Evaluation Complete:")
        print(f"   - mAP50: {metrics.box.map50:.3f}")
        print(f"   - mAP50-95: {metrics.box.map:.3f}")
        print(f"   - Precision: {metrics.box.mp:.3f}")
        print(f"   - Recall: {metrics.box.mr:.3f}")
        return metrics

if __name__ == "__main__":
    # Initialize and train
    trainer = MetaGlassesTrainer(model_size='n')
    trainer.setup_data()
    
    # Train model
    results = trainer.train_model(epochs=50, batch=8)
    
    # Evaluate
    metrics = trainer.evaluate_model()
    
    print("🎉 Training Complete! Model ready for deployment.")