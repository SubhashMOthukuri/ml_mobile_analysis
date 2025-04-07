"""
Training Pipeline for Mobile Price Prediction

This module handles the training of the mobile price prediction model. It includes:
1. Data loading and preprocessing
2. Feature engineering (converting processor names to clock speeds)
3. Model training
4. Saving the trained model and scaler

The pipeline processes the following features:
- Mobile Weight (g)
- RAM (GB)
- Front Camera (MP)
- Back Camera (MP)
- Processor (converted to GHz)
- Battery Capacity (mAh)
- Screen Size (inches)
- Launched Year
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
import pickle
import os
import re
from src.logger import logging

def clean_numeric_column(series, unit=''):
    """
    Clean numeric columns by removing units and converting to float.
    
    Args:
        series (pd.Series): The column to clean
        unit (str): The unit to remove (e.g., 'g', 'GB', 'MP')
    
    Returns:
        pd.Series: Cleaned numeric series
    """
    if unit:
        # Handle cases where the unit might be separated by a space
        series = series.str.replace(f' {unit}', unit).str.replace(unit, '')
    # Remove commas from numbers
    series = series.str.replace(',', '')
    return pd.to_numeric(series, errors='coerce')

def clean_price(price_series):
    """
    Clean price by removing currency symbols and converting to numeric.
    
    Args:
        price_series (pd.Series): Price column with currency symbols
    
    Returns:
        pd.Series: Cleaned numeric price series
    """
    # Remove currency symbols, commas, and spaces
    cleaned = price_series.str.replace(r'[₹,\s]', '', regex=True)
    # Remove 'INR' prefix
    cleaned = cleaned.str.replace('INR', '', regex=False)
    return pd.to_numeric(cleaned, errors='coerce')

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

def train_and_save_model():
    """
    Main function to train and save the mobile price prediction model.
    
    Steps:
    1. Load and preprocess the dataset
    2. Convert processor names to clock speeds
    3. Clean and scale features
    4. Train Random Forest model
    5. Save model and scaler
    
    Returns:
        tuple: (model, scaler) The trained model and scaler
    """
    try:
        # Create artifacts directory if it doesn't exist
        os.makedirs("artifacts", exist_ok=True)

        # Load the dataset with different encodings
        data_path = "notebook/Mobiles Dataset (2025).csv"
        try:
            df = pd.read_csv(data_path, encoding='utf-8')
        except UnicodeDecodeError:
            try:
                df = pd.read_csv(data_path, encoding='latin1')
            except UnicodeDecodeError:
                df = pd.read_csv(data_path, encoding='cp1252')
        
        print("Initial shape:", df.shape)
        
        # Clean numeric data
        df["Mobile Weight"] = clean_numeric_column(df["Mobile Weight"], 'g')
        df["RAM"] = clean_numeric_column(df["RAM"], 'GB')
        df["Front Camera"] = clean_numeric_column(df["Front Camera"], 'MP')
        df["Back Camera"] = clean_numeric_column(df["Back Camera"], 'MP')
        df["Battery Capacity"] = clean_numeric_column(df["Battery Capacity"], 'mAh')
        df["Screen Size"] = clean_numeric_column(df["Screen Size"], 'inches')
        
        # Convert processor names to GHz values
        df["Processor_Speed"] = df["Processor"].apply(get_processor_speed)
        
        print("After cleaning features:", df.shape)
        print("Missing values after cleaning features:", 
              df[["Mobile Weight", "RAM", "Front Camera", "Back Camera", 
                  "Processor_Speed", "Battery Capacity", "Screen Size"]].isnull().sum())
        
        # Clean price
        df["Launched Price (India)"] = clean_price(df["Launched Price (India)"])
        print("After cleaning price:", df.shape)
        print("Sample of prices:", df["Launched Price (India)"].head())
        
        # Select features and target
        features = [
            "Mobile Weight", "RAM", "Front Camera", "Back Camera",
            "Processor_Speed", "Battery Capacity", "Screen Size", "Launched Year"
        ]
        
        # Remove rows with missing values
        df = df.dropna(subset=features + ["Launched Price (India)"])
        print("After removing missing values:", df.shape)
        
        X = df[features]
        y = df["Launched Price (India)"]  # Using India price as target

        # Scale the features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Train the model
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_scaled, y)

        # Save the model and scaler
        model_path = "artifacts/best_model.pkl"
        scaler_path = "artifacts/scaler.pkl"
        
        with open(model_path, "wb") as f:
            pickle.dump(model, f)
            
        with open(scaler_path, "wb") as f:
            pickle.dump(scaler, f)

        logging.info(f"Model and scaler trained and saved to artifacts directory")
        return model, scaler

    except Exception as e:
        logging.error(f"Error in training pipeline: {str(e)}")
        raise

if __name__ == "__main__":
    train_and_save_model()
