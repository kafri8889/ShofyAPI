import json

from django.http import HttpRequest
from django.forms.models import model_to_dict
from rest_framework import permissions, status
from rest_framework.views import APIView

from shofy_api.extensions import *
from shofy_api.serializers import *
from shofy_api.models import *


class ProductApiView(APIView):
    permission_classes = [permissions.AllowAny]

    def get_by_id(self, product_id):
        """
        get product by id
        """

        try:
            product = Product.objects.get(pk=product_id)

            return build_response(
                data=model_to_dict(product),
                message="Product found",
                status=status.HTTP_200_OK
            )
        except Product.DoesNotExist:
            return build_response(
                data=None,
                message="Product not found",
                status=status.HTTP_404_NOT_FOUND
            )

    def get(self, request, **kwargs):

        if "product_id" in kwargs:
            return self.get_by_id(kwargs["product_id"])

        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)

        if len(serializer.data) == 0:
            message = "No products"
        else:
            message = f"Product count: {len(serializer.data)}"

        return build_response(
            data=serializer.data,
            message=message,
            status=status.HTTP_200_OK
        )

    def post(self, request: HttpRequest):
        body = json.loads(request.body)

        try:
            store = Store.objects.get(pk=body['store_id']).products
        except Store.DoesNotExist:
            return build_response(
                data=None,
                message=f"Store with id {body['store_id']} not found",
                status=status.HTTP_404_NOT_FOUND
            )

        data = {
            "name": body["name"],
            "description": body["description"],
            "price": body["price"],
            "quantity": body["quantity"],
            "store": body["store_id"],
        }

        serializer = ProductSerializer(data=data)

        if serializer.is_valid():
            product = serializer.save()
            store.add(product)

            return build_response(
                data=model_to_dict(product),
                message="Product created",
                status=status.HTTP_201_CREATED
            )

        return build_response(
            data=merge_serializer_errors(serializer.errors),
            message="Failed to create product",
            status=status.HTTP_400_BAD_REQUEST
        )

    def put(self, request: HttpRequest, **kwargs):
        if "product_id" in kwargs:
            body = json.loads(request.body)
            data = {
                "name": body["name"],
                "description": body["description"],
                "price": body["price"],
                "quantity": body["quantity"]
            }

            try:
                product = Product.objects.get(pk=kwargs["product_id"])
            except Product.DoesNotExist:
                return build_response(
                    data=None,
                    message="Product not found",
                    status=status.HTTP_404_NOT_FOUND
                )

            product.__dict__.update(**data)
            product.save()

            return build_response(
                data=data,
                message="Product updated",
                status=status.HTTP_200_OK
            )

        return build_response(
            data=None,
            message="Parameter \"product_id\" does not exist",
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request: HttpRequest, **kwargs):
        if "product_id" in kwargs:
            try:
                product = Product.objects.get(pk=kwargs["product_id"])
                serializer = ProductSerializer(data=model_to_dict(product))

                product.delete()

                if serializer.is_valid():
                    return build_response(
                        data=serializer.data,
                        message="Product deleted",
                        status=status.HTTP_200_OK
                    )

                return build_response(
                    data=merge_serializer_errors(serializer.errors),
                    message="Invalid product",
                    status=status.HTTP_400_BAD_REQUEST
                )
            except Product.DoesNotExist:
                return build_response(
                    data=None,
                    message="Product not found",
                    status=status.HTTP_404_NOT_FOUND
                )

        return build_response(
            data=None,
            message="Parameter \"product_id\" does not exist",
            status=status.HTTP_400_BAD_REQUEST
        )
