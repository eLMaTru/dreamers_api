from django.db import transaction
from rest_framework import serializers, validators
from .models import UserAccount
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAccountSerializer(serializers.Serializer):

    first_name = serializers.CharField( required=False, allow_blank=True, default="", max_length=30)
    last_name = serializers.CharField(        required=False, allow_blank=True, default="", max_length=30
)
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField()
    name = serializers.CharField(required=False, allow_blank=True, default="")
    user_account_id = serializers.CharField(allow_null=True, default="")
    is_term_condition = serializers.BooleanField(default=False)
    #country = serializers.CharField(        max_length=50, required=False, allow_null=True, allow_blank=True)
    image_url = serializers.ImageField(required=False, allow_null=True)
    token = serializers.CharField(required=False, allow_blank=True, default="")

    def validate(self, attrs):
        if User.objects.filter(username__iexact=attrs.get("username")).count() > 0:
            raise validators.ValidationError("Username already registered.")
        if User.objects.filter(email__iexact=attrs.get("email")).count() > 0:
            raise validators.ValidationError("Email already registered.")
        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            email = validated_data.get("email").strip().lower()
            user = User.objects.create(
                email=email,
                username=validated_data.get("username"),
            )
            user.set_password(validated_data.get("password"))
            user.save()
            user_acc = UserAccount.objects.create(
                user=user,
                is_term_condition=validated_data.get("is_term_condition"),
            )

            return user_acc

    def update(self, instance, validated_data):
        instance.user.first_name = validated_data["first_name"]
        instance.user.last_name = validated_data["last_name"]
        instance.image = validated_data.get("image")
        instance.user.save()
        instance.save()
        return instance

