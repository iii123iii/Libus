from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField(max_length=50000)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    post_image = models.ImageField(upload_to="media", default="/media/Defualt")
    is_image = models.BooleanField(default=False)
    liked = models.ManyToManyField(User, blank=True, related_name="LikedUsers")

    def __str__(self):
        return self.title
    
    def delete(self, *args, **kwargs):
        if self.post_image != "/media/Defualt":
            self.post_image.delete()
        super().delete(*args, **kwargs)
    
    
class Messages(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2", blank=True)
    text = models.CharField(max_length=500)
    timestamp = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.author}:{self.user2}<{self.text}"