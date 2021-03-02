from rest_framework import serializers

from dreams.models import Dream, Comment, Reaction


class DreamPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dream
        fields = '__all__'


class DreamGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dream
        fields = '__all__'
        depth = 2


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = '__all__'
