from rest_framework.response import Response


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