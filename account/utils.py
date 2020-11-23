import string

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

User = get_user_model()


def get_login_form(request):
    username = (
        request.data.get("username").strip().lower()
        if request.data.get("username")
        else ""
    )
    request.session.set_expiry(settings.SESSION_EXPIRE_AT)
    post_data = {"username": username, "password": request.data.get("password")}
    AuthenticationForm.error_messages = {"invalid_login": "Correo username o contraseña incorrecta."}
    form = AuthenticationForm(data=post_data)
    return form


def get_current_user(request):
    user = request.user
    if not user.is_authenticated:
        user_id = request.session.get("user_id")
        if user_id:
            user = User.objects.get(id=user_id)
        else:
            user = create_anonymous_user()
            request.session["user_id"] = user.id
    return user


def create_anonymous_user(
        first_name="Guest", last_name="User", username=None, email=None, password=None
):
    if not username:
        username = "guest_{}".format(
            get_random_string(10, "abcdefghijklmnpqrstuvwxyz1234567890_")
        )
        while User.objects.filter(username=username).count() > 0:
            username = "guest_{}".format(
                get_random_string(10, "abcdefghijklmnpqrstuvwxyz1234567890_")
            )

    new_user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
    )

    return new_user

def generate_random_password():
    password = get_random_string(
        8, string.ascii_letters + string.digits + string.punctuation
    )
    return password