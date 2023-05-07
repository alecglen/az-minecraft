class _BaseHttpException(Exception):
    "Abstract base class for custom exception types with a message"
    code = 500
    
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
        

class ValidationError(_BaseHttpException):
    "Raise to indicate a mistake in client input"
    code = 400


class DataConflict(_BaseHttpException):
    "Raise to indicate a data conflict making the request invalid"
    code = 409
    
    
class DBConnectionFailure(_BaseHttpException):
    "Raise to indicate a failed connection to a required backend resource"
    code = 502
