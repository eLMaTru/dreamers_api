from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from dreams.models import Dream, Comment, Reaction
from dreams.serializers import DreamSerializer, CommentSerializer, ReactionSerializer


class DreamViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = DreamSerializer
    queryset = Dream.objects.all()

    @action(detail=False, url_path="status")#@action(detail=False, url_path="averages/(?P<store_id>[^/.]+)")
    def get_dreams_enabled(self, request):
        estatus = request.query_params.get("status")
        dreams = Dream.object.filter(status=estatus)
        return Response(
            DreamSerializer(dreams, many=True).data, status=status.HTTP_200_OK
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


class ReactionViewSet(viewsets.ModelViewSet):
    serializer_class = ReactionSerializer
    queryset = Reaction.objects.all()
