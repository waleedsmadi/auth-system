from rest_framework import serializers
from accounts.models import MyUser
from posts.models import Post


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'img']

