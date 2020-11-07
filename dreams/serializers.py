from rest_framework import serializers

from dreams.models import Dream, Comment


class DreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dream
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
