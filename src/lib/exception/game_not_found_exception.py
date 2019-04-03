from api_exception import ApiException

class GameNotFoundException(ApiException):
    status_code = 404
