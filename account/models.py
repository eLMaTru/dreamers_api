from django.conf import settings
from django.db import models
import hashlib

from core.models import BaseModel

# Create your models here.


class UserAccount(BaseModel):

    STATUS_ENABLED = "enabled"
    STATUS_DISABLE = "disable"
    STATUS_CHOICES = (
        (STATUS_ENABLED, STATUS_ENABLED),
        (STATUS_DISABLE, STATUS_DISABLE)
    )

    name = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(choices=STATUS_CHOICES, default='enabled', max_length=25)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_term_condition = models.BooleanField(default=False)
    image_url = models.CharField(max_length=250, blank=True, null=True)

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

    @property
    def hashed_id(self):
        encoded_id = str(self.id).encode("utf-8")
        return hashlib.sha256(encoded_id).hexdigest()

    def __str__(self):
        return self.user.username
