from django.urls import include, path
from account.router import router

urlpatterns = [
    path('', include(router.urls)),
]
