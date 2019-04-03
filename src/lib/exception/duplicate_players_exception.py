from api_exception import ApiException

class DuplicatePlayersException(ApiException):
    status_code = 400
