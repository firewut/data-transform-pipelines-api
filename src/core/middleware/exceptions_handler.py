from django.db.utils import IntegrityError
from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is None and exc:
        response = Response(
            str(exc),
            status=400,
            headers={}
        )

    # Now add the HTTP status code to the response.
    if isinstance(exc, IntegrityError):
        if 'duplicate key value' in str(exc):
            response.status_code = 409

    return response
