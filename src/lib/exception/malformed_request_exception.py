from api_exception import ApiException

class MalformedRequestException(ApiException):
    status_code = 400
