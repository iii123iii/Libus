from rest_framework import serializers

from .models import Post

class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()

    def get_author_username(self, obj):
        return obj.author.username
    
    def get_likes(self, obj):
        return obj.liked.count()
    
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'author_username', 'date_posted', 'post_image', 'is_image', 'likes')