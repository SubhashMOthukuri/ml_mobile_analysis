from flask import Flask, request, jsonify
from flask_cors import CORS
from src.pipelines.prediction_pipeline import ModelPredictor
import numpy as np
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize predictor with error handling
try:
    predictor = ModelPredictor()
    MODEL_LOADED = True
except Exception as e:
    print(f"Warning: Could not load model - {str(e)}")
    MODEL_LOADED = False

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Mobile Price Prediction API", "status": "Model loaded" if MODEL_LOADED else "Model not loaded"})

@app.route("/predict", methods=["POST"])
def predict():
    try:
        if not MODEL_LOADED:
            return jsonify({"error": "Model not loaded. Please ensure model file exists in artifacts/best_model.pkl"}), 503

        # Get JSON data from request
        data = request.get_json()

        # Ensure all required fields are provided
        required_features = [
            "Mobile Weight", "RAM", "Front Camera", "Back Camera", "Processor",
            "Battery Capacity", "Screen Size", "Launched Year"
        ]
        
        if not all(feature in data for feature in required_features):
            return jsonify({"error": "Missing required features in input data."}), 400

        # Extract features from request JSON
        input_data = [
            data["Mobile Weight"], data["RAM"], data["Front Camera"], data["Back Camera"],
            data["Processor"], data["Battery Capacity"], data["Screen Size"], data["Launched Year"]
        ]
        
        # Get prediction from model
        prediction = predictor.make_prediction(input_data)
        
        # Return prediction as JSON response
        return jsonify({"prediction": prediction.tolist()})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
