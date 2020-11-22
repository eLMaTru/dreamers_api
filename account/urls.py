from django.urls import include, path
from account.router import router
from account.views import *

urlpatterns = [
    path('', include(router.urls)),
    path("users/exists/<str:email>", UserExists.as_view(), name="user-exists"),
    path("users/create/", CreateUser.as_view(), name="create-user"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("login/token/", LoginAPITokenView.as_view(), name="login-token"),
    path("whoami/", WhoAmIView.as_view(), name="whoami"),
]
