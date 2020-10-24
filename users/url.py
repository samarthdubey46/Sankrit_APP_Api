from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    registration_view,
    ObtainAuthTokenView,
    account_properties_view,
    update_account_view,
    does_account_exist_view,
    ChangePasswordView,
    FriendsView,
    UserViewSet
)
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'users'
router = DefaultRouter()
router.register('delete',UserViewSet)
urlpatterns = [
    path('check_if_account_exists/', does_account_exist_view, name="check_if_account_exists"),
    path('change_password/', ChangePasswordView.as_view(), name="change_password"),
    path('properties', account_properties_view, name="properties"),
    path('properties/update', update_account_view, name="update"),
    path('login', ObtainAuthTokenView.as_view(), name="login"),
    path('register', registration_view, name="register"),
    path('list', FriendsView.as_view()),
    path('',include(router.urls))

]
