from rest_framework import routers

from dreams import viewsets

router = routers.DefaultRouter()
router.register("dreams", viewsets.DreamViewSet, basename='dreams')
router.register("comments", viewsets.CommentViewSet, basename="comments")
