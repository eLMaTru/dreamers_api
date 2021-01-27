from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated

from dreams.models import Dream, Comment, Reaction
from dreams.serializers import DreamSerializer, CommentSerializer, ReactionSerializer


class DreamViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = DreamSerializer
    queryset = Dream.objects.all()

    @action(detail=False, url_path="status")
    def get_dreams_enabled(self, request):
        status = request.query_params.get('status')
        print()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


class ReactionViewSet(viewsets.ModelViewSet):
    serializer_class = ReactionSerializer
    queryset = Reaction.objects.all()
