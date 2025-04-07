import sys
from src.logger import logging

def error_message_details(error, error_detail):
    """
    Extracts error details, such as file name, line number, and the error message.

    This function is used to get detailed information about where the error occurred 
    in the code, including the file name and line number, along with the error message.

    Args:
        error (Exception): The exception object that contains the error message.
        error_detail (traceback, optional): The traceback object which contains detailed information 
                                  about where the exception occurred.

    Returns:
        str: A formatted string containing the file name, line number, and the error message.
    """
    if error_detail is None:
        return str(error)
        
    # Extracting the traceback information
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    error_message = str(error)
    
    return f"Error occurred in Python script: [{file_name}] line number: [{line_number}] error message: [{error_message}]"

class CustomException(Exception):
    """
    Custom exception class for handling errors in the application.

    This class extends the base Exception class and provides additional functionality
    for logging errors and providing detailed error messages.
    """
    def __init__(self, error_message, error_detail=None):
        """
        Initialize the custom exception with an error message and optional error details.

        Args:
            error_message (str): The error message to be displayed.
            error_detail (traceback, optional): The traceback object containing error details.
        """
        super().__init__(error_message)
        self.error_message = error_message
        if error_detail:
            self.error_message = error_message_details(error_message, error_detail)
        logging.error(self.error_message)

    def __str__(self):
        """
        Return the error message when the exception is converted to a string.

        Returns:
            str: The error message.
        """
        return self.error_message