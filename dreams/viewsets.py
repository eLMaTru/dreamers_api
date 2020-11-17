from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny

from dreams.models import Dream, Comment
from dreams.serializers import DreamSerializer, CommentSerializer


class DreamViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = DreamSerializer
    queryset = Dream.objects.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
