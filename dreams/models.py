from django.db import models
from core.models import BaseModel
from account.models import UserAccount

# Create your models here.


class Dream(BaseModel):
    STATUS_ENABLED = "enabled"
    STATUS_DISABLE = "disable"
    STATUS_DELETE = "delete"
    STATUS_EDITED = "edited"
    STATUS_CHOICES = (
        (STATUS_ENABLED, STATUS_ENABLED),
        (STATUS_DISABLE, STATUS_DISABLE),
        (STATUS_DELETE, STATUS_DELETE),
        (STATUS_EDITED, STATUS_EDITED),
    )

    status = models.CharField(choices=STATUS_CHOICES, default="enabled", max_length=25)
    name = models.CharField(max_length=101)
    description = models.TextField(blank=True, null=True)
    image = models.CharField(blank=True, null=True, max_length=500)
    is_public = models.BooleanField(default=False)
    is_favorite = models.BooleanField(default=False)
    user_account = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    is_voice = models.BooleanField(default=False)


class Comment(BaseModel):
    STATUS_ENABLED = "enabled"
    STATUS_DISABLE = "disable"
    STATUS_DELETE = "delete"
    STATUS_EDITED = "edited"
    STATUS_CHOICES = (
        (STATUS_ENABLED, STATUS_ENABLED),
        (STATUS_DISABLE, STATUS_DISABLE),
        (STATUS_DELETE, STATUS_DELETE),
        (STATUS_EDITED, STATUS_EDITED)
    )

    status = models.CharField(choices=STATUS_CHOICES, default="ENABLED", max_length=25)
    dream = models.ForeignKey(Dream, on_delete=models.CASCADE)
    user_account = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    description = models.TextField


class Reaction(BaseModel):
    like = models.BooleanField(default=False)
    dislike = models.BooleanField(default=False)
    user_account = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    dream = models.ForeignKey(Dream, on_delete=models.CASCADE)
    username = models.CharField(max_length=50)
