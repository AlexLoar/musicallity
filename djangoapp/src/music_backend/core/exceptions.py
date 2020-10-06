from rest_framework.exceptions import APIException


class ISWCNotFound(APIException):
    status_code = 404
    default_detail = 'ISWC not found'
    default_code = 'not_found'
