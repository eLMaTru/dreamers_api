from django.shortcuts import render
from requests import Response
from rest_framework import views, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model, authenticate, login, logout

from account.models import UserAccount
from account.serializers import UserAccountSerializer
from account.utils import get_login_form

User = get_user_model()

# Create your views here.
class WhoAmIView(views.APIView):
    """
    Returns information about the current logged in user.
    The `user_account_id` field corresponds to the remitter id if a remitter is the logged in user.
    """
    permission_classes = (AllowAny,)

    def get(self, request):
        user = request.user
        response = {
            "whoami": None,
        }
        if user.is_authenticated:
            user_acc = UserAccount.objects.filter(user=user).first()
            if user_acc is None:
                return Response(
                    {"error": "La cuenta no es valida"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            whoami = get_user_response(user_acc)
            response["whoami"] = whoami

        return Response(response)


class CreateUser(views.APIView):
    """
    Creates a new remitter. Payload:
    ```
    {
        "first_name": string,
        "last_name": string,
        "email": string,
        "password": string,
        "type": "remitter",
        "phone_numbers": [string]
    }
    ```"""

    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data.copy()
        serializer = UserAccountSerializer(data=data)
        if serializer.is_valid():
            user_acc = serializer.save()
            login(request, user_acc.user)

            return Response(get_user_response(user_acc))
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        user_acc = UserAccount.objects.get(user=request.user)
        serializer = UserAccountSerializer(user_acc, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(get_user_response(user_acc))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_user_response(user_acc, raw=False):
    user = user_acc.user
    token, created = Token.objects.get_or_create(user=user)
    data = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "username": user.username,
        "password": None,
        "image": user_acc.image,
        "user_account_id": user_acc.id,
        "country": user_acc.country,
        "token": token
    }

    if raw:
        return data

    return UserAccountSerializer(data).data


class UserExists(views.APIView):
    permission_classes = (AllowAny,)

    def get(self, request, email):
        email = email.strip()
        user = User.objects.filter(email=email).first()
        ret = {"exists": False}
        if user is not None:
            ret["exists"] = True
        return Response(ret)


class LogoutAPIView(views.APIView):
    def get(self, request):
        """Logout the current user."""
        user = request.user
        if user.is_authenticated:
            logout(request)
        return Response({})


class LoginAPIView(views.APIView):
    """
    Logs the user in. Payload:
    ```
      username: "string",
      password: "string"
    ```
    """

    permission_classes = (AllowAny,)

    def post(self, request):
        form = get_login_form(request)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )

            user_acc = UserAccount.objects.filter(user=user).first()

            login(request, user)
            return Response(get_user_response(user_acc))

        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPITokenView(views.APIView):
    """
    Logs the user in. Payload:
    ```
      username: "string",
      password: "string"
    ```
    """

    permission_classes = (AllowAny,)

    def post(self, request):
        form = get_login_form(request)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})

        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)