from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from .models import Post, Messages
from django.db.models import Q
from django.contrib.auth.models import User
from .serializers import PostSerializer
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination

import json

def loginV(request):
    if(request.user.is_authenticated == True):
        return redirect('/')
    if request.method == "POST" :
        user = authenticate(request, username = request.POST['username'], password = request.POST['password'])
        if(user is not None):
            login(request, user)
            return redirect("/login")

        
    return render(request, 'login.html')

def logoutV(request):
    if(request.user.is_authenticated == True):
        logout(request)
        return redirect("/login")
        
    return redirect("/login")

def registerV(request):
    if(request.user.is_authenticated == True):
        return redirect("/")
    if(request.method == "POST"):
        if(User.objects.filter(username = request.POST['username']).exists() == False and User.objects.filter(email = request.POST['email']).exists() == False):
            user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
            user.save()
            login(request, user)
            return redirect('/')    
    
    return render(request, 'Register.html')

def HomeV(request):
    if(request.user.is_authenticated == False):
        return redirect("/login")
    context = {
        'user': request.user.username,
    }
    return render(request, 'index.html', context)

def createV(request):
    if(request.user.is_authenticated == False):
        return redirect("/login")
    
    if(request.method == "POST"):
        if(request.FILES):
            post = Post(title = request.POST['title'], content = request.POST['content'], author = request.user, post_image = request.FILES['file'], is_image = True)
            post.save()
            return redirect('/')
        else:
            post = Post(title = request.POST['title'], content = request.POST['content'], author = request.user, is_image = False)
            post.save()
            return redirect('/')
            
    return render(request, 'create.html')


def messagesV(request):
    if request.user.is_authenticated:
        context = {
            'user': request.user,
            'users' : User.objects.all(),
            'notUser': True,
        }
        return render(request, "messages.html", context)
    else:
        return redirect('login')
    
def messagesWV(request, username2):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.POST['message'] is not None:
                message = Messages(author = request.user, user2 = User.objects.get(username = username2), text = request.POST['message'])
                message.save()
                return HttpResponse(message.id, content_type="text/plain")
        
        if Messages.objects.filter(Q(author=request.user) | Q(user2=request.user)).order_by('-timestamp').first():
            context = {
                'messages': Messages.objects.filter((Q(author__username=username2) & Q(user2__username=request.user)) | (Q(author__username=request.user) & Q(user2__username=username2))).order_by('-timestamp'),
                'user': request.user,
                'first_id': Messages.objects.filter(Q(author=request.user) | Q(user2=request.user)).order_by('-timestamp').first().id,
                'users': User.objects.all(),
                'username2': username2,
                'host': request.META['HTTP_HOST'],
            }
        else:
            context = {
                'messages': Messages.objects.filter((Q(author__username=username2) & Q(user2__username=request.user)) | (Q(author__username=request.user) & Q(user2__username=username2))).order_by('-timestamp'),
                'user': request.user,
                'users': User.objects.all(),
                'username2': username2,
                'host': request.META['HTTP_HOST'],
            }   
        return render(request, "messages.html", context)
    else:
        return redirect('login')
    
    
    
@api_view(['Get'])
def posts(request):
    if(request.user.is_authenticated == False):
        return redirect("/login")
    posts = Post.objects.all()
    paginator = PageNumberPagination()
    paginator.page_size = 10
    results = paginator.paginate_queryset(posts, request)
    serializer = PostSerializer(results, many=True)
    
    return paginator.get_paginated_response(serializer.data)

def delete(request, id):
    post = Post.objects.get(id=id)
    if post.author.username == request.user.username:
        post.delete()
    return redirect('/')