from api_exception import ApiException

class NotYourTurnException(ApiException):
    status_code = 409
