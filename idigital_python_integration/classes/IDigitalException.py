from src.utils.HttpStatus import HttpStatus
from datetime import datetime


class IDigitalException(Exception):
    def __init__(self, code: int, message: str):
        self.date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.name = HttpStatus.status[code]
        super().__init__(message)
        self.message = message
        self.code = code

    def __str__(self):
        return f"IDigitalException: [{self.date}: {self.code} - {self.name}]: {self.message}\n"
