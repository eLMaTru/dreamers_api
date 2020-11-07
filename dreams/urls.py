from django.urls import include, path
from dreams.router import router

urlpatterns = [
    path('', include(router.urls)),
]