from django.contrib import admin
from .models import Post, Messages


admin.site.register(Post)
admin.site.register(Messages)