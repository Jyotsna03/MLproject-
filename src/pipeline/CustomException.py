from src.pipeline.exception import error_message_detail


import sys


class CustomException(Exception):
    def __init__(self, error_message,error_detail:sys):
        #inherting the function 
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail=error_detail)
    def __str__(self):
        return self.error_message