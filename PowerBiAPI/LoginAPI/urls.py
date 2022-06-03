from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from .views import UserViewSet, LoginApi
from rest_framework import routers

router = routers.DefaultRouter()
router.register('users', UserViewSet)

authUrls = [
    path("login", LoginApi.as_view(), name="login"),
    # path("logout", UserAuthApi.LogoutApi.as_view(), name="logout"),
    # path("verify", UserAuthApi.AuthenticateCredentials.as_view(), name="verify")
]


urlpatterns = [
    path('', include(router.urls)),
    path('authorise/', include(authUrls), name='authorise'),
    ]