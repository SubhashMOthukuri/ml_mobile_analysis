# Mobile Price Prediction System

A machine learning-based system that predicts mobile phone prices based on various specifications like processor speed, RAM, camera, etc.

## Project Structure

```
mobile_analysis/
├── artifacts/                 # Saved model and scaler files
├── frontend/                  # Frontend application
│   ├── static/               # Static files (CSS, JS)
│   │   ├── styles.css
│   │   └── app.js
│   ├── templates/            # HTML templates
│   │   └── index.html
│   └── server.py             # Frontend server
├── notebook/                  # Jupyter notebooks and datasets
│   └── Mobiles Dataset (2025).csv
├── src/                      # Source code
│   ├── pipelines/           # Training and prediction pipelines
│   │   ├── training_pipeline.py
│   │   └── prediction_pipeline.py
│   ├── logger.py            # Logging configuration
│   ├── exceptions.py        # Custom exceptions
│   └── application.py       # Backend API server
└── README.md                # Project documentation
```

## Features

- Predicts mobile phone prices based on specifications
- Handles various processor types and converts them to clock speeds
- Clean and modern web interface
- RESTful API backend
- Machine learning model using Random Forest Regressor

## Prerequisites

- Python 3.8 or higher
- Required Python packages:
  ```
  flask
  flask-cors
  pandas
  numpy
  scikit-learn
  ```

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd mobile_analysis
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Train the model:

   ```bash
   python src/pipelines/training_pipeline.py
   ```

   This will:

   - Clean and preprocess the dataset
   - Convert processor names to clock speeds
   - Train the Random Forest model
   - Save the model and scaler to the artifacts directory

2. Start the backend server:

   ```bash
   $env:PYTHONPATH = "."; python src/application.py
   ```

   The backend API will run on http://localhost:5000

3. Start the frontend server:

   ```bash
   cd frontend
   python server.py
   ```

   The frontend will be available at http://localhost:3000

4. Use the web interface:
   - Open http://localhost:3000 in your browser
   - Fill in the mobile specifications:
     - Mobile Weight (g)
     - RAM (GB)
     - Front Camera (MP)
     - Back Camera (MP)
     - Processor (e.g., "A17 Bionic", "Snapdragon 8 Gen 2")
     - Battery Capacity (mAh)
     - Screen Size (inches)
     - Launched Year
   - Click "Predict Price" to get the estimated price

## Data Processing

The system processes the following features:

- Mobile Weight: Cleaned by removing 'g' unit
- RAM: Cleaned by removing 'GB' unit
- Front Camera: Cleaned by removing 'MP' unit
- Back Camera: Cleaned by removing 'MP' unit
- Processor: Converted to clock speed in GHz
- Battery Capacity: Cleaned by removing 'mAh' unit
- Screen Size: Cleaned by removing 'inches' unit
- Launched Year: Used as is

## Model Details

- Algorithm: Random Forest Regressor
- Features: 8 numerical features
- Target: Mobile phone price in INR
- Preprocessing: StandardScaler for feature scaling

## API Endpoints

- POST /predict
  - Input: JSON with mobile specifications
  - Output: Predicted price in INR

## Error Handling

The system includes comprehensive error handling for:

- Missing or invalid input data
- Model loading failures
- Data preprocessing errors
- API request validation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
