from fastapi import HTTPException

class AppException(HTTPException):
    def __init__(self, status_code: int, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(status_code=status_code, detail=message)

class NotFoundException(AppException):
    def __init__(self, message="Resource not found"):
        super().__init__(404, "NOT_FOUND", message)

class UnauthorizedException(AppException):
    def __init__(self, message="Unauthorized"):
        super().__init__(401, "UNAUTHORIZED", message)

class BadRequestException(AppException):
    def __init__(self, message="Bad request"):
        super().__init__(400, "BAD_REQUEST", message)
