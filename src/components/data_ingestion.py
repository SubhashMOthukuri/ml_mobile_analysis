import os
import pandas as pd
from sklearn.model_selection import train_test_split
from src.logger import logging
from src.exception import CustomException

class DataIngestion:
    def __init__(self, data_path: str = "data/mobile_prices.csv"):
        """
        Initializes the data ingestion component.
        :param data_path: Path to the dataset (CSV file).
        """
        self.data_path = data_path
        self.train_path = "artifacts/train.csv"
        self.test_path = "artifacts/test.csv"
        self.val_path = "artifacts/val.csv"

    def initiate_data_ingestion(self):
        """
        Reads data, handles missing values, and splits it into train, validation, and test sets.
        :return: Paths of the train, validation, and test datasets.
        """
        logging.info("Starting data ingestion process...")

        try:
            # Load data
            df = pd.read_csv(self.data_path)
            logging.info(f"Dataset loaded successfully with shape {df.shape}")

            # Handle missing values (if any)
            df.dropna(inplace=True)
            logging.info(f"Dataset after removing missing values: {df.shape}")

            # Train-Test-Validation Split (70-20-10)
            train, temp = train_test_split(df, test_size=0.3, random_state=42)
            test, val = train_test_split(temp, test_size=0.33, random_state=42)

            # Ensure artifacts directory exists
            os.makedirs("artifacts", exist_ok=True)

            # Save datasets
            train.to_csv(self.train_path, index=False)
            test.to_csv(self.test_path, index=False)
            val.to_csv(self.val_path, index=False)

            logging.info("Data ingestion completed successfully.")
            return self.train_path, self.test_path, self.val_path

        except Exception as e:
            logging.error(f"Error in data ingestion: {str(e)}")
            raise CustomException(e)

