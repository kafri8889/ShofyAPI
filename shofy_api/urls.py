from django.urls import path
from shofy_api.views import (
    UserView,
    StoreView,
    ProductView,
    CartItemView
)

urlpatterns = [
    path("user/", UserView.UserApiView.as_view()),
    path("user/<int:user_id>", UserView.UserApiView.as_view()),
    path("user/<int:user_id>/cart", UserView.UserApiView.as_view()),

    path("store/", StoreView.StoreApiView.as_view()),
    path("store/<int:store_id>", StoreView.StoreApiView.as_view()),
    path("store/<int:store_id>/products", StoreView.StoreApiView.as_view()),

    path("product/", ProductView.ProductApiView.as_view()),
    path("product/<int:product_id>", ProductView.ProductApiView.as_view()),

    path("cart/", CartItemView.CartItemApiView.as_view()),
    path("cart/<int:cart_item_id>", CartItemView.CartItemApiView.as_view()),
]
