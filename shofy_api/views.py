import json

from django.http import HttpRequest
from django.forms.models import model_to_dict
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .extensions import *
from .serializers import *
from .models import *


class UserApiView(APIView):
    permission_classes = [permissions.AllowAny]

    def get_by_id(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            serializer = UserSerializer(data=model_to_dict(user))

            if serializer.is_valid():
                return build_response(
                    data=serializer.data,
                    message="User found",
                    status=status.HTTP_200_OK
                )

            return build_response(
                data=serializer.errors,
                message="Invalid user",
                status=status.HTTP_400_BAD_REQUEST
            )
        except User.DoesNotExist:
            return build_response(
                data=None,
                message="User not found",
                status=status.HTTP_404_NOT_FOUND
            )

    def get(self, request, **kwargs):

        if "user_id" in kwargs:
            return self.get_by_id(kwargs["user_id"])

        users = User.objects.all()
        serializer = UserSerializer(users, many=True)

        if len(serializer.data) == 0:
            message = "No users"
        else:
            message = f"User count: {len(serializer.data)}"

        return build_response(
            data=serializer.data,
            message=message,
            status=status.HTTP_200_OK
        )

    def post(self, request: HttpRequest):
        body = json.loads(request.body)
        data = {
            "name": body["name"],
            "username": body["username"],
            "email": body["email"]
        }

        serializer = UserSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return build_response(
                data=serializer.data,
                message="User created",
                status=status.HTTP_200_OK
            )

        return build_response(
            data=serializer.errors,
            message="Failed to create user",
            status=status.HTTP_400_BAD_REQUEST
        )

    def put(self, request: HttpRequest, **kwargs):
        if "user_id" in kwargs:
            body = json.loads(request.body)
            data = {
                "id": kwargs["user_id"],
                "name": body["name"],
                "username": body["username"],
                "email": body["email"]
            }

            user_response = self.get_by_id(kwargs["user_id"])

            if user_response.status_code == 200:
                serializer = UserSerializer(data=data, partial=True)

                if serializer.is_valid():
                    User.objects.filter(pk=kwargs["user_id"]).update(**data)

                    return build_response(
                        data=serializer.data,
                        message="User updated",
                        status=status.HTTP_200_OK
                    )

                return build_response(
                    data=serializer.errors,
                    message="Invalid user",
                    status=status.HTTP_400_BAD_REQUEST
                )

            return user_response

        return build_response(
            data=None,
            message="Parameter \"user_id\" does not exist",
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request: HttpRequest, **kwargs):
        if "user_id" in kwargs:
            try:
                user = User.objects.get(pk=kwargs["user_id"])
                serializer = UserSerializer(data=model_to_dict(user))

                user.delete()

                if serializer.is_valid():
                    return build_response(
                        data=serializer.data,
                        message="User deleted",
                        status=status.HTTP_200_OK
                    )

                return build_response(
                    data=serializer.errors,
                    message="Invalid user",
                    status=status.HTTP_400_BAD_REQUEST
                )
            except User.DoesNotExist:
                return build_response(
                    data=None,
                    message="User not found",
                    status=status.HTTP_404_NOT_FOUND
                )

        return build_response(
            data=None,
            message="Parameter \"user_id\" does not exist",
            status=status.HTTP_400_BAD_REQUEST
        )