from rest_framework import viewsets, mixins, filters
from rest_framework.permissions import AllowAny, IsAuthenticated

from account.models import UserAccount
from account.serializers import UserAccountSerializer


#class UserAccountViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
#   pass