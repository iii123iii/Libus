from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views


urlpatterns = [
    path("", views.HomeV, name="Home"),
    path("login", views.loginV, name="Login"),
    path("logout", views.logoutV, name="Logout"),
    path("register", views.registerV, name="Register"),
    path("create", views.createV, name="Create"),
    path("messages", views.messagesV, name="Messages"),
    path("messages/<slug:username2>", views.messagesWV, name="MessagesW"),
    path('get_posts/', views.posts, name="Posts"),
    path('delete/<int:id>', views.delete, name="DeletePost"),
    path('get_users/<str:username>', views.get_users, name="Users"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)