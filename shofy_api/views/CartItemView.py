import json

from django.http import HttpRequest
from django.forms.models import model_to_dict
from rest_framework import permissions, status
from rest_framework.views import APIView

from shofy_api.extensions import *
from shofy_api.serializers import *
from shofy_api.models import *


class CartItemApiView(APIView):
    permission_classes = [permissions.AllowAny]

    def check_user_and_product_exists(self, user_id, product_id):
        """
        Check user and product exists or not
        :return: if user and product exists return user and product instance, otherwise return None and response
        """

        all_exists = False
        response = None
        product = None
        user = None

        try:
            user = User.objects.get(pk=user_id)
            all_exists = True
        except User.DoesNotExist:
            response = build_response(
                data=None,
                message=f"User with id {user_id} not found",
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            product = Product.objects.get(pk=product_id)
            all_exists = True
        except Product.DoesNotExist:
            # Product does not exist, abort
            response = build_response(
                data=None,
                message=f"Product with id {product_id} does not exist",
                status=status.HTTP_404_NOT_FOUND
            )

        if all_exists:
            return user, product

        return None, response

    def get_by_id(self, cart_item_id):
        """
        get cart item by id
        """

        try:
            cart_item = CartItem.objects.get(pk=cart_item_id)
            serializer = CartItemSerializer(cart_item)

            return build_response(
                data=serializer.data,
                message="Cart item found",
                status=status.HTTP_200_OK
            )
        except CartItem.DoesNotExist:
            return build_response(
                data=None,
                message="Cart item not found",
                status=status.HTTP_404_NOT_FOUND
            )

    def get(self, request, **kwargs):

        if "cart_item_id" in kwargs:
            # Accessing "/cart/{cart_item_id}"
            return self.get_by_id(kwargs["cart_item_id"])

        # Accessing "/cart"
        cart_items = CartItem.objects.all()
        serializer = CartItemSerializer(cart_items, many=True)

        if len(serializer.data) == 0:
            message = "No cart items"
        else:
            message = f"Cart item count: {len(serializer.data)}"

        return build_response(
            data=serializer.data,
            message=message,
            status=status.HTTP_200_OK
        )

    def post(self, request: HttpRequest):
        body = json.loads(request.body)

        r1, r2 = self.check_user_and_product_exists(body['user_id'], body['product_id'])

        if r1 is None:
            return r2

        user = r1
        product = r2

        # Check item exists or not, if exists sum quantity, otherwise create the item
        try:
            cart_item = CartItem.objects.get(user=user, product=product)
            cart_item.quantity += body['quantity']
            cart_item.save()

            return build_response(
                data=CartItemSerializer(cart_item).data,
                message="Cart item updated",
                status=status.HTTP_200_OK
            )
        except CartItem.DoesNotExist:
            # Create new cart item
            pass

        data = {
            "user": user,
            "product": product,
            "quantity": body["quantity"],
        }

        user.cart.create(**data)

        serializer = CartItemSerializer(data)

        return build_response(
            data=serializer.data,
            message="Cart item created",
            status=status.HTTP_201_CREATED
        )

    def put(self, request: HttpRequest, **kwargs):
        if "cart_item_id" in kwargs:
            body = json.loads(request.body)

            data = {
                "quantity": body["quantity"],
            }

            try:
                cart_item = CartItem.objects.get(pk=kwargs["cart_item_id"])
            except CartItem.DoesNotExist:
                return build_response(
                    data=None,
                    message="Cart item not found",
                    status=status.HTTP_404_NOT_FOUND
                )

            cart_item.__dict__.update(**data)
            cart_item.save()

            return build_response(
                data=CartItemSerializer(cart_item).data,
                message="Cart item updated",
                status=status.HTTP_200_OK
            )
        return build_response(
            data=None,
            message="Parameter \"cart_item_id\" does not exist",
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request: HttpRequest, **kwargs):
        if "cart_item_id" in kwargs:
            try:
                cart_item = CartItem.objects.get(pk=kwargs['cart_item_id'])
                serializer = CartItemSerializer(cart_item)

                cart_item.delete()

                return build_response(
                    data=serializer.data,
                    message="Cart item deleted",
                    status=status.HTTP_200_OK
                )
            except CartItem.DoesNotExist:
                return build_response(
                    data=None,
                    message="Cart item not found",
                    status=status.HTTP_404_NOT_FOUND
                )

        return build_response(
            data=None,
            message="Parameter \"cart_item_id\" does not exist",
            status=status.HTTP_400_BAD_REQUEST
        )
