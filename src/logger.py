import logging
import os
from datetime import datetime

# Define log file name with timestamp
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Corrected `os.getcw()` to `os.getcwd()`
logs_path = os.path.join(os.getcwd(), "logs")  # Get the current working directory and create a 'logs' directory path
os.makedirs(logs_path, exist_ok=True)  # Create the 'logs' directory if it doesn't exist

LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)  # Define the full log file path with timestamped log file name

# Configure logging settings
logging.basicConfig(
    filename=LOG_FILE_PATH,  # Log messages will be saved in the specified log file
    level=logging.INFO,  # Set the logging level to INFO
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",  # Log format with timestamp, line number, logger name, log level, and message
)