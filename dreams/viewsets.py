from rest_framework import viewsets, mixins

from dreams.models import Dream, Comment
from dreams.serializers import DreamSerializer, CommentSerializer


class DreamViewSet(viewsets.ModelViewSet):
    serializer_class = DreamSerializer
    queryset = Dream.objects.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
