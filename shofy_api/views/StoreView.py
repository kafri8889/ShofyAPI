import json

from django.http import HttpRequest
from django.forms.models import model_to_dict
from rest_framework import permissions, status
from rest_framework.views import APIView

from shofy_api.extensions import *
from shofy_api.serializers import *
from shofy_api.models import *


class StoreApiView(APIView):
    permission_classes = [permissions.AllowAny]

    def get_by_user_id(self, user_id):
        """
        get store by user id, if user not have store, return "store not found" 404
        """

        try:
            try:
                user = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                return build_response(
                    data=None,
                    message=f"User with id {user_id} not found",
                    status=status.HTTP_404_NOT_FOUND
                )

            return build_response(
                data=model_to_dict(user.store),
                message="Store found",
                status=status.HTTP_200_OK
            )
        except Store.DoesNotExist:
            return build_response(
                data=None,
                message="Store not found",
                status=status.HTTP_404_NOT_FOUND
            )

    def get_products(self, store_id):
        """
        Get all products with given store id
        """

        try:
            store = Store.objects.get(pk=store_id)
            serializer = ProductSerializer(store.products.all(), many=True)

            return build_response(
                data=serializer.data,
                message="Product found",
                status=status.HTTP_200_OK
            )
        except Store.DoesNotExist:
            return build_response(
                data=None,
                message="Store not found",
                status=status.HTTP_404_NOT_FOUND
            )

    def get(self, request: HttpRequest, **kwargs):
        if "store_id" in kwargs:
            if "/products" in request.path:
                # Accessing "/store/{store_id}/products"
                return self.get_products(kwargs["store_id"])

            # Accessing "/store/{store_id}"
            return self.get_by_user_id(kwargs["store_id"])

        # Accessing "/store"
        stores = Store.objects.all()
        serializer = StoreSerializer(stores, many=True)

        if len(serializer.data) == 0:
            message = "No stores"
        else:
            message = f"Store count: {len(serializer.data)}"

        return build_response(
            data=serializer.data,
            message=message,
            status=status.HTTP_200_OK
        )

    def post(self, request: HttpRequest):
        body = json.loads(request.body)
        data = {
            "name": body["name"],
            "location": body["location"],
            "user": body["user_id"]
        }

        try:
            user = User.objects.get(pk=body['user_id'])
        except User.DoesNotExist:
            return build_response(
                data=None,
                message=f"User with id {body['user_id']} not found",
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if store exists or not
        try:
            # if this code not throw an exception, means the store is already exists
            store = Store.objects.get(user=user)
            # return response
            return build_response(
                data=model_to_dict(store),
                message="Failed to create store, store already exists.",
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        except Store.DoesNotExist:
            # if store not found, create the store
            pass

        serializer = StoreSerializer(data=data)

        if serializer.is_valid():
            store = Store.objects.create(
                name=body["name"],
                location=body["location"],
                user=user
            )

            return build_response(
                data=model_to_dict(store),
                message="Store created",
                status=status.HTTP_201_CREATED
            )

        return build_response(
            data=merge_serializer_errors(serializer.errors),
            message="Failed to create store",
            status=status.HTTP_400_BAD_REQUEST
        )

    def put(self, request: HttpRequest, **kwargs):
        if "store_id" in kwargs:
            body = json.loads(request.body)
            data = {
                "user": kwargs["store_id"],
                "name": body["name"],
                "location": body["location"]
            }

            try:
                store = Store.objects.get(user=data["user"])
            except Store.DoesNotExist:
                return build_response(
                    data=None,
                    message="Store not found",
                    status=status.HTTP_404_NOT_FOUND
                )

            store.__dict__.update(**data)
            store.save()

            return build_response(
                data=data,
                message="Store updated",
                status=status.HTTP_200_OK
            )

        return build_response(
            data=None,
            message="Parameter \"store_id\" does not exist",
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request: HttpRequest, **kwargs):
        if "store_id" in kwargs:
            try:
                store = Store.objects.get(pk=kwargs["store_id"])
                serializer = StoreSerializer(data=model_to_dict(store))

                store.delete()

                if serializer.is_valid():
                    return build_response(
                        data=serializer.data,
                        message="Store deleted",
                        status=status.HTTP_200_OK
                    )

                return build_response(
                    data=merge_serializer_errors(serializer.errors),
                    message="Invalid store",
                    status=status.HTTP_400_BAD_REQUEST
                )
            except Store.DoesNotExist:
                return build_response(
                    data=None,
                    message="Store not found",
                    status=status.HTTP_404_NOT_FOUND
                )

        return build_response(
            data=None,
            message="Parameter \"store_id\" does not exist",
            status=status.HTTP_400_BAD_REQUEST
        )
