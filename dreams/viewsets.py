from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from dreams.models import Dream, Comment, Reaction
from dreams.serializers import (
    CommentSerializer,
    ReactionSerializer,
    DreamPostSerializer,
    DreamGetSerializer,
)


class DreamViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = DreamPostSerializer
    queryset = Dream.objects.all().order_by("-created_at")
    # filter_backends = (DjangoFilterBackend,)
    filterset_fields = ["status", "is_public", "user_account"]

    @action(
        filterset_fields=["status"], detail=False, url_path="status"
    )  # @action(detail=False, url_path="averages/(?P<store_id>[^/.]+)")
    def get_dreams_enabled(self, request):
        estatus = request.query_params.get("status")
        is_public = bool(request.query_params.get("isPublic"))
        dreams = Dream.objects.filter(
            status=estatus,
            is_public=is_public,
        ).order_by("-created_at")
        return Response(
            DreamGetSerializer(dreams, many=True).data, status=status.HTTP_200_OK
        )

    @action(detail=True, url_path="status", methods=['put'])
    def update_status(self, request, pk):
        estatus = request.query_params.get("status")

        dream = Dream.objects.get(pk=pk)
        dream.status = status
        dream.save()
        return Response(status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


class ReactionViewSet(viewsets.ModelViewSet):
    serializer_class = ReactionSerializer
    queryset = Reaction.objects.all()

    @action(detail=False, url_path="sets", methods=["post"])
    def set_reaction_for_dream(self, request):

        like_sum = False
        dislike_sum = False
        like_subtract = False
        dislike_subtract = False
        is_like = request.data.get("isLike")
        user_name = request.data.get("userName")
        user_id = request.data.get("userId")
        dream_id = request.data.get("dreamId")

        dream = Dream.objects.get(pk=dream_id)

        re, created = Reaction.objects.get_or_create(
            dream_id=dream_id, user_account_id=user_id
        )
        if created:
            re.username = user_name
            if is_like:
                re.like = True
                like_sum = True
                dream.like_len += 1
            else:
                re.dislike = True
                dislike_sum = True
                dream.dislike_len += 1
        else:
            if is_like:
                if re.like and not re.dislike:
                    re.like = not re.like
                    like_subtract = True
                    dream.like_len = 0 if dream.like_len == 0 else dream.like_len - 1

                else:
                    if not re.like and not re.dislike:
                        re.like = not re.like
                        like_sum = True
                        dream.like_len += 1

                if not re.like and re.dislike:
                    re.like = not re.like
                    re.dislike = not re.dislike
                    like_sum = True
                    dislike_subtract = True
                    dream.like_len += 1
                    dream.dislike_len = (
                        0 if dream.dislike_len == 0 else dream.dislike_len - 1
                    )

            else:
                if re.dislike and not re.like:
                    re.dislike = not re.dislike
                    dislike_subtract = True
                    dream.dislike_len = (
                        0 if dream.dislike_len == 0 else dream.dislike_len - 1
                    )
                else:

                    if not re.dislike and not re.like:
                        re.dislike = not re.dislike
                        dislike_sum = True
                        dream.dislike_len += 1

                if not re.dislike and re.like:
                    re.dislike = not re.dislike
                    re.like = not re.like
                    dislike_sum = True
                    like_subtract = True
                    dream.like_len = 0 if dream.like_len == 0 else dream.like_len - 1
                    dream.dislike_len += 1

        re.save()
        dream.save()

        data = {
            "likeSum": like_sum,
            "dislikeSum": dislike_sum,
            "likeSubtract": like_subtract,
            "dislikeSubtract": dislike_subtract,
        }

        return Response(data, status=status.HTTP_200_OK)
