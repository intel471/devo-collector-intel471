class BaseCollectorException(Exception):

    def __init__(self, code: int, cause: str) -> None:
        self.code: int = code
        self.cause: str = cause

    def __str__(self) -> str:
        return f'{self.__class__.__name__}[CODE:{self.code:04d}] {self.cause}'

class CredentialException(BaseCollectorException):
    pass

class InvalidIndicatorTypeException(BaseCollectorException):
    pass

class MaxLimitException(BaseCollectorException):
    pass

class NoAccessException(BaseCollectorException):
    pass

class UnauthorisedException(BaseCollectorException):
    pass

class MissingDurationException(BaseCollectorException):
    pass

class InvalidDurationException(BaseCollectorException):
    pass
