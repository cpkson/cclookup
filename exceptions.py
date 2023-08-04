from dataclasses import dataclass


@dataclass
class InvalidIATACodeError(Exception):
    """
    Exception to raise when provided an invalid IATA code.

    Attributes:
        message (str): Message displayed when error is raised.
    """

    message: str

    def __str__(self) -> str:
        return self.message
    
@dataclass
class InvalidISOCodeError(Exception):
    """
    Exception to raise when provided an invalid ISO code.
    
    Attributes:
        message (str): Message displayed when error is raised.
    """
    
    message: str
    def __str__(self) -> str:
        return self.message