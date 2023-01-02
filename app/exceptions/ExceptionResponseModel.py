
from fastapi import HTTPException

class InvalidURLException(HTTPException):
    def __init__(self, status_code, detail, message: str):
        super().__init__(status_code, detail)
        self.message = message
