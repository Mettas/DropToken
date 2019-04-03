from api_exception import ApiException

class MovesNotFoundException(ApiException):
    status_code = 404
