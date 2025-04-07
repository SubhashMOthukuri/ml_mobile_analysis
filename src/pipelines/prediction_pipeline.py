"""
Prediction Pipeline for Mobile Price Prediction

This module handles the prediction of mobile prices using the trained model. It includes:
1. Loading the trained model and scaler
2. Processing input data
3. Converting processor names to clock speeds
4. Making predictions

The pipeline expects the following input features:
- Mobile Weight (g)
- RAM (GB)
- Front Camera (MP)
- Back Camera (MP)
- Processor (name or GHz value)
- Battery Capacity (mAh)
- Screen Size (inches)
- Launched Year
"""

import pickle
import numpy as np
import pandas as pd
import sys
from src.logger import logging
from src.exceptions import CustomException

def get_processor_speed(processor_name):
    """
    Convert processor name to its maximum clock speed in GHz.
    
    Args:
        processor_name (str): Name of the processor
    
    Returns:
        float: Clock speed in GHz
    """
    # Dictionary mapping processor names to their max clock speeds
    processor_speeds = {
        # Apple Processors
        'A17 Pro': 3.78,
        'A17 Bionic': 3.78,
        'A16 Bionic': 3.46,
        'A15 Bionic': 3.23,
        'A14 Bionic': 3.1,
        'A13 Bionic': 2.65,
        'A12 Bionic': 2.5,
        'A11 Bionic': 2.4,
        
        # Snapdragon Processors
        'Snapdragon 8 Gen 3': 3.3,
        'Snapdragon 8 Gen 2': 3.2,
        'Snapdragon 8+ Gen 1': 3.2,
        'Snapdragon 8 Gen 1': 3.0,
        'Snapdragon 7+ Gen 2': 2.91,
        'Snapdragon 7 Gen 1': 2.4,
        
        # MediaTek Processors
        'MediaTek Dimensity 9300': 3.25,
        'MediaTek Dimensity 9200': 3.05,
        'MediaTek Dimensity 9000': 3.05,
        'MediaTek Dimensity 8300': 3.35,
        'MediaTek Dimensity 8200': 3.1,
        
        # Exynos Processors
        'Exynos 2400': 3.2,
        'Exynos 2200': 2.8,
        'Exynos 1380': 2.4,
        
        # Google Processors
        'Google Tensor G3': 2.91,
        'Google Tensor G2': 2.85,
        'Google Tensor': 2.8
    }
    
    # Try to find the processor in the dictionary
    for key, value in processor_speeds.items():
        if key.lower() in processor_name.lower():
            return value
    
    # If processor not found, return a default value
    return 2.0  # Default to 2.0 GHz for unknown processors

class ModelPredictor:
    """
    Class for making predictions using the trained model.
    
    This class handles:
    1. Loading the trained model and scaler
    2. Processing input data
    3. Converting processor names to clock speeds
    4. Making predictions
    """
    
    def __init__(self, model_path="artifacts/best_model.pkl", scaler_path="artifacts/scaler.pkl"):
        """
        Initialize the predictor with model and scaler paths.
        
        Args:
            model_path (str): Path to the trained model file
            scaler_path (str): Path to the scaler file
        """
        self.model_path = model_path
        self.scaler_path = scaler_path
        try:
            self.model = self.load_model()
            self.scaler = self.load_scaler()
        except Exception as e:
            logging.error(f"Error loading model or scaler: {str(e)}")
            self.model = None
            self.scaler = None

    def load_model(self):
        """
        Load the saved model from artifacts.
        
        Returns:
            object: The trained model
        
        Raises:
            CustomException: If model file not found or error loading
        """
        try:
            with open(self.model_path, "rb") as f:
                model = pickle.load(f)
            logging.info("Model loaded successfully for predictions.")
            return model
        except FileNotFoundError:
            raise CustomException(f"Model file not found at {self.model_path}")
        except Exception as e:
            raise CustomException(f"Error loading model: {str(e)}")

    def load_scaler(self):
        """
        Load the saved scaler from artifacts.
        
        Returns:
            object: The trained scaler
        
        Raises:
            CustomException: If scaler file not found or error loading
        """
        try:
            with open(self.scaler_path, "rb") as f:
                scaler = pickle.load(f)
            logging.info("Scaler loaded successfully.")
            return scaler
        except FileNotFoundError:
            raise CustomException(f"Scaler file not found at {self.scaler_path}")
        except Exception as e:
            raise CustomException(f"Error loading scaler: {str(e)}")

    def make_prediction(self, input_data):
        """
        Predict output using the trained model.
        
        Args:
            input_data (list): List of values [Mobile Weight, RAM, Front Camera, Back Camera, 
                               Processor, Battery Capacity, Screen Size, Launched Year]
        
        Returns:
            float: Predicted price
        
        Raises:
            CustomException: If model/scaler not loaded or error in prediction
        """
        try:
            if self.model is None or self.scaler is None:
                raise CustomException("Model or scaler not loaded. Please ensure both files exist.")

            # Convert input to numpy array
            input_data = np.array(input_data)
            
            # Extract processor and convert to GHz
            processor = input_data[4]
            processor_speed = get_processor_speed(processor)
            
            # Replace processor with speed value
            input_data[4] = processor_speed
            
            # Reshape for prediction
            input_data = input_data.reshape(1, -1)

            # Scale the input data
            input_scaled = self.scaler.transform(input_data)

            # Make prediction
            prediction = self.model.predict(input_scaled)
            logging.info(f"Prediction made: {prediction}")
            return prediction
        except Exception as e:
            raise CustomException(f"Error in making prediction: {str(e)}")

if __name__ == "__main__":
    # Example usage
    predictor = ModelPredictor()

    # Example input: [Mobile Weight, RAM, Front Camera, Back Camera, Processor, Battery Capacity, Screen Size, Launched Year]
    sample_input = [180, 8, 16, 48, "A17 Bionic", 4500, 6.5, 2023]  # Example mobile data

    prediction_result = predictor.make_prediction(sample_input)
    print(f"Predicted Output: {prediction_result}")
