from rest_framework import serializers

from .models import Post

class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    hasalike = serializers.SerializerMethodField()

    def get_author_username(self, obj):
        return obj.author.username
    
    def get_likes(self, obj):
        return obj.liked.count()
    
    def get_hasalike(self, obj):
        request = self.context.get("request")
        user = request.user if request else None
        if user and user.is_authenticated and user in obj.liked.all():
            return True
        return False
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'author_username', 'date_posted', 'post_file', 'is_file', 'likes', "hasalike")