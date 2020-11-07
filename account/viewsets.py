from rest_framework import viewsets, mixins, filters
from rest_framework.permissions import AllowAny

from account.models import UserAccount
from account.serializers import UserAccountSerializer


class UserAccountViewSet(viewsets.ModelViewSet):
    serializer_class = UserAccountSerializer
    queryset = UserAccount.objects.all()
    permission_classes = (AllowAny,)
