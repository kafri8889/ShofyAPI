from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnDict


def build_response(data, message, status):
    response = {
        "message": message,
        "status": status,
        "data": data
    }

    return Response(
        data=response,
        status=status
    )


def merge_serializer_errors(errors: ReturnDict):
    new_errors = []
    for error in errors:
        for sub_error in errors[error]:
            new_errors.append(f"{error}: {sub_error}")

    return new_errors
