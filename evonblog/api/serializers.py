from rest_framework.serializers import ModelSerializer
from evonblog.models import User, Comment, Post


class SaveUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class GetUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "id")

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"