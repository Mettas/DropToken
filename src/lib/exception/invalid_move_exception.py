from api_exception import ApiException

class InvalidMoveException(ApiException):
    status_code = 400
