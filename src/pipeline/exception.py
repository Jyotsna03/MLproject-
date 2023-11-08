from math import e
import sys
#sys.path.append('C:\\Users\\jyojy\\OneDrive\\Desktop\\MLproject\\src\\pipeline\\logger.py')
sys.path.append('C:\\Users\\jyojy\\OneDrive\\Desktop\\MLproject\\src\\pipeline\\logger.py')
#sys.path.append(r'C:\Users\jyojy\OneDrive\Desktop\MLproject\src\pipeline\logger.py')

import logging
import logger


def error_message_detail(error, error_detail: sys):
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error occurred in Python script name [{0}] line number [{1}] error message [{2}]".format(file_name, exc_tb.tb_lineno, str(error))
    return error_message

class CustomException(Exception):
    def __init__(self, error_message,error_detail:sys):
        #inherting the function 
        super().__init__(error_message) 
        self.error_message = error_message_detail(error_message, error_detail=error_detail)
    def __str__(self):
        return self.error_message   
    
if __name__ == "__main":
    try:
        # Your code that may raise an exception
        a = 10 / 0
    except Exception as e:
        # Log an error message
        logging.error("An exception occurred: %s", str(e))
        # Raise a custom exception
        raise CustomException("Custom exception message", e, type(e))
    
# import sys
# import logging

# def error_message_detail(error, error_detail: sys):
#     _, _, exc_tb = error_detail.exc_info()
#     file_name = exc_tb.tb_frame.f_code.co_filename
#     error_message = "Error occurred in Python script name [{0}] line number [{1}] error message [{2}]".format(file_name, exc_tb.tb_lineno, str(error))
#     return error_message

# class CustomException(Exception):
#     def __init__(self, error_message, error_detail: sys):
#         super().__init(error_message)
#         self.error_message = error_message_detail(error_message, error_detail=error_detail)
#     def __str__(self):
#         return self.error_message

# if __name__ == "__main":
#     try:
#         # Your code that may raise an exception
#         a = 10 / 0
#     except Exception as e:
#         # Log an error message
#         logging.error("An exception occurred: %s", str(e))
#         # Raise a custom exception
#         raise CustomException("Custom exception message", e)


 
 