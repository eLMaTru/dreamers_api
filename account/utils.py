from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm


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
