import numpy as np
import pandas as pd
import pyautogui
import time
import threading
import joblib
import logging
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split

"""
if the algorithm detects an anomaly
a prompt will appear to confirm the presence of the user
also a notification will be send to the server. 
"""


class MLMouseJigglerDetector:
    def __init__(self, 
                 model_path='mouse_jiggler_model.joblib',
                 log_file='ml_mouse_jiggler_detection.log',
                 contamination=0.1,  # expected proportion of anomalies
                 detection_window=60,  # seconds to monitor
                 feature_window=5):  # seconds between feature captures
        """
        Machine Learning-based Mouse Jiggler Detection
        
        :param model_path: Path to save/load trained model
        :param log_file: Path to log detection results
        :param contamination: Expected proportion of anomalous instances
        :param detection_window: Total time to monitor for anomalies
        :param feature_window: Time between feature collection points
        """
        # Logging setup
        logging.basicConfig(
            filename=log_file, 
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s: %(message)s'
        )
        self.logger = logging.getLogger()
        
        # Model and detection parameters
        self.model_path = model_path
        self.contamination = contamination
        self.detection_window = detection_window
        self.feature_window = feature_window
        
        # ML components
        self.scaler = StandardScaler()
        self.model = None
        
        # Detection tracking
        self.is_detecting = False
        self.detection_thread = None
    
    def extract_mouse_features(self, duration=5):
        """
        Extract features from mouse movements
        
        :param duration: Time to collect mouse movement data
        :return: DataFrame of mouse movement features
        """
        features = {
            'total_distance': [],
            'avg_speed': [],
            'max_speed': [],
            'num_direction_changes': [],
            'movement_variance': []
        }
        
        # Collect initial position
        last_pos = pyautogui.position()
        start_time = time.time()
        total_distance = 0
        speeds = []
        positions = [last_pos]
        
        while time.time() - start_time < duration:
            time.sleep(0.1)  # Small delay between measurements
            current_pos = pyautogui.position()
            
            # Calculate distance and speed
            dx = current_pos[0] - last_pos[0]
            dy = current_pos[1] - last_pos[1]
            distance = np.sqrt(dx**2 + dy**2)
            
            total_distance += distance
            speed = distance / 0.1  # Distance per second
            speeds.append(speed)
            positions.append(current_pos)
            
            last_pos = current_pos
        
        # Calculate features
        features['total_distance'] = total_distance
        features['avg_speed'] = np.mean(speeds) if speeds else 0
        features['max_speed'] = max(speeds) if speeds else 0
        
        # Direction changes
        direction_changes = 0
        for i in range(2, len(positions)):
            angle1 = np.arctan2(
                positions[i-1][1] - positions[i-2][1],
                positions[i-1][0] - positions[i-2][0]
            )
            angle2 = np.arctan2(
                positions[i][1] - positions[i-1][1],
                positions[i][0] - positions[i-1][0]
            )
            if abs(angle1 - angle2) > np.pi/4:  # Significant direction change
                direction_changes += 1
        
        features['num_direction_changes'] = direction_changes
        features['movement_variance'] = np.var(speeds) if speeds else 0
        
        return pd.DataFrame([features])
    
    def train_model(self, num_samples=1000, normal_duration=5, anomaly_duration=5):
        """
        Train an Isolation Forest model for mouse movement anomaly detection
        
        :param num_samples: Number of training samples
        :param normal_duration: Duration to collect normal mouse movement data
        :param anomaly_duration: Duration to simulate anomalous movements
        """
        # Collect normal mouse movement data
        normal_data = []
        for _ in range(num_samples // 2):
            features = self.extract_mouse_features(normal_duration)
            normal_data.append(features.values[0])
        
        # Simulate anomalous mouse movements (mouse jiggler-like)
        anomaly_data = []
        for _ in range(num_samples // 2):
            # Simulate consistent small movements characteristic of mouse jigglers
            features = pd.DataFrame([{
                'total_distance': np.random.uniform(10, 50),
                'avg_speed': np.random.uniform(10, 100),
                'max_speed': np.random.uniform(50, 200),
                'num_direction_changes': np.random.randint(1, 10),
                'movement_variance': np.random.uniform(0, 50)
            }])
            anomaly_data.append(features.values[0])
        
        # Combine and prepare data
        X = np.array(normal_data + anomaly_data)
        y = np.array([0] * (num_samples // 2) + [1] * (num_samples // 2))
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42
        )
        
        # Train Isolation Forest
        self.model = IsolationForest(
            contamination=self.contamination, 
            random_state=42
        )
        self.model.fit(X_train)
        
        # Evaluate model
        train_predictions = self.model.predict(X_train)
        test_predictions = self.model.predict(X_test)
        
        train_accuracy = np.mean(train_predictions == -1) * 100
        test_accuracy = np.mean(test_predictions == -1) * 100
        
        self.logger.info(f"Model Training Results:")
        self.logger.info(f"Training Anomaly Detection Rate: {train_accuracy:.2f}%")
        self.logger.info(f"Testing Anomaly Detection Rate: {test_accuracy:.2f}%")
        
        # Save model
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler
        }, self.model_path)
        
        print(f"Model trained and saved to {self.model_path}")
    
    def load_model(self):
        """
        Load pre-trained model
        """
        try:
            saved_data = joblib.load(self.model_path)
            self.model = saved_data['model']
            self.scaler = saved_data['scaler']
            print(f"Model loaded from {self.model_path}")
        except FileNotFoundError:
            print("No pre-trained model found. Please train a model first.")
            self.model = None
    
    def detect_mouse_jiggler(self):
        """
        Detect potential mouse jiggler using trained model
        """
        if not self.model:
            self.logger.error("No model loaded. Train a model first.")
            return
        
        start_time = time.time()
        anomaly_detected = False
        anomaly_count = 0
        
        while time.time() - start_time < self.detection_window and self.is_detecting:
            # Extract mouse movement features
            features = self.extract_mouse_features(self.feature_window)
            
            # Scale features
            features_scaled = self.scaler.transform(features)
            
            # Predict anomaly
            prediction = self.model.predict(features_scaled)
            
            if prediction[0] == -1:  # Anomaly detected
                anomaly_count += 1
                log_message = (
                    f"POTENTIAL MOUSE JIGGLER DETECTED! "
                    f"Anomaly Features: {features.to_dict('records')[0]}"
                )
                print(log_message)
                self.logger.warning(log_message)
                anomaly_detected = True
            
            time.sleep(self.feature_window)
        
        if anomaly_detected:
            self.logger.info(f"Total Anomalies Detected: {anomaly_count}")
        
        return anomaly_detected
    
    def start_detection(self):
        """
        Start mouse jiggler detection in a separate thread
        """
        if not self.is_detecting:
            # Ensure model is loaded
            if not self.model:
                try:
                    self.load_model()
                except Exception:
                    print("No model found. Training new model...")
                    self.train_model()
            
            self.is_detecting = True
            self.detection_thread = threading.Thread(target=self.detect_mouse_jiggler)
            self.detection_thread.start()
            print(f"ML Mouse Jiggler Detection started for {self.detection_window} seconds")
    
    def stop_detection(self):
        """
        Stop mouse jiggler detection
        """
        self.is_detecting = False
        if self.detection_thread:
            self.detection_thread.join()
        print("ML Mouse Jiggler Detection stopped")

def main():
    # Create detector
    detector = MLMouseJigglerDetector(
        detection_window=120,  # monitor for 2 minutes
        contamination=0.1,  # 10% of instances expected to be anomalies
        feature_window=5  # check every 5 seconds
    )
    
    # Optional: Train a new model or use existing
    # Uncomment to retrain
    # detector.train_model(num_samples=2000)
    
    try:
        # Start detection
        detector.start_detection()
        
        # Wait for detection to complete
        detector.detection_thread.join()
    except KeyboardInterrupt:
        print("\nDetection interrupted by user")
    finally:
        detector.stop_detection()

if __name__ == "__main__":
    main()

"""
Dependencies:
pip install numpy pandas scikit-learn pyautogui joblib

Key ML Anomaly Detection Strategies:
1. Feature Extraction:
   - Total mouse movement distance
   - Average mouse speed
   - Maximum mouse speed
   - Number of direction changes
   - Movement variance

2. Anomaly Detection Approach:
   - Uses Isolation Forest algorithm
   - Unsupervised learning technique
   - Identifies anomalies based on feature distribution
   - Handles high-dimensional datasets efficiently

Limitations:
- Requires training on representative mouse movement data
- Performance depends on quality of training data
- May have false positives/negatives
- Computational overhead for real-time detection
"""