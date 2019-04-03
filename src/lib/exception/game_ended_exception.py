from api_exception import ApiException

class GameEndedException(ApiException):
    status_code = 410
