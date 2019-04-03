from api_exception import ApiException

class PlayerNotFoundException(ApiException):
    status_code = 404
