from django.urls import path
from shofy_api import views


urlpatterns = [
    path("user/", views.UserApiView.as_view()),
    path("user/<int:user_id>", views.UserApiView.as_view()),
    # path("user/sign-up", views.UserCreate.as_view(), name='new-user')
]