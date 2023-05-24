from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data["status_code"] = response.status_code

    """ if response is not None:
        if response.status_code == 401:
            response.data["datail"] = "인증되지 않은 사용자입니다."
            response.data["status_code"] = response.status_code
        elif response.status_code == 403:
            response.data["datail"] = "접근 권한이 없습니다."
            response.data["status_code"] = response.status_code
        elif response.status_code == 404:
            response.data["datail"] = "데이터를 가져올 수 없습니다."
            response.data["status_code"] = response.status_code
        elif response.status_code == 500:
            response.data["datail"] = "서버에러입니다. 관리자에게 문의 주세요."
            response.data["status_code"] = response.status_code """

    return response
