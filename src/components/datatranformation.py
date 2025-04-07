import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from src.logger import logging
from src.exception import CustomException
import pickle

class DataTransformation:
    def __init__(self):
        self.preprocessor_path = "artifacts/preprocessor.pkl"

    def get_data_transformer(self):
        """
        Creates a preprocessing pipeline to handle categorical and numerical features.
        :return: Preprocessing pipeline.
        """
        try:
            logging.info("Creating data transformation pipeline...")

            # Define columns
            categorical_cols = ["Company Name", "Processor"]
            numerical_cols = ["Mobile Weight", "RAM", "Front Camera", "Back Camera", 
                              "Battery Capacity", "Screen Size", "Launched Year"]

            # Define transformations
            categorical_transformer = OneHotEncoder(handle_unknown="ignore")
            numerical_transformer = StandardScaler()

            # Combine transformations
            preprocessor = ColumnTransformer([
                ("num_scaler", numerical_transformer, numerical_cols),
                ("cat_encoder", categorical_transformer, categorical_cols)
            ])

            return preprocessor

        except Exception as e:
            logging.error(f"Error in data transformation: {str(e)}")
            raise CustomException(e)

    def apply_transformation(self, train_path, test_path, val_path):
        """
        Reads datasets, applies transformations, and saves processed data.
        """
        try:
            logging.info("Applying data transformations...")

            # Load datasets
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            val_df = pd.read_csv(val_path)

            # Extract features and target variable
            target_column = "Launched Price (USA)"  # Change based on your prediction target

            X_train = train_df.drop(columns=[target_column])
            y_train = train_df[target_column]

            X_test = test_df.drop(columns=[target_column])
            y_test = test_df[target_column]

            X_val = val_df.drop(columns=[target_column])
            y_val = val_df[target_column]

            # Get transformer
            preprocessor = self.get_data_transformer()

            # Fit and transform data
            X_train_transformed = preprocessor.fit_transform(X_train)
            X_test_transformed = preprocessor.transform(X_test)
            X_val_transformed = preprocessor.transform(X_val)

            # Save the preprocessor model
            os.makedirs("artifacts", exist_ok=True)
            with open(self.preprocessor_path, "wb") as f:
                pickle.dump(preprocessor, f)

            logging.info("Data transformation completed successfully.")
            return X_train_transformed, y_train, X_test_transformed, y_test, X_val_transformed, y_val

        except Exception as e:
            logging.error(f"Error in data transformation: {str(e)}")
            raise CustomException(e)
