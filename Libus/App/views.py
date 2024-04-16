from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from .models import Post, Messages
from django.db.models import Q
from django.contrib.auth.models import User
from .serializers import PostSerializer
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.models import Group

import json

def loginV(request):
    if(request.user.is_authenticated == True):
        return redirect('/')
    if request.method == "POST":
        conetxt = {}
        if request.POST['username'].strip() != "" and request.POST['password'].strip() != "":
            user = authenticate(request, username = request.POST['username'], password = request.POST['password'])
            if user is not None:
                if user.groups.filter(name='BANNED').exists() == False:
                    login(request, user)
                    return redirect("/")
                else:
                    context = {
                        'error': True,
                        'e': 'The user you entered is banned.',
                    }
            else:
                context = {
                    'error': True,
                    'e': 'The username or password you entered is incorrect. Please try again.',
                }
        else:
            context = {
                'error': True,
                'e': 'The username or password you entered is incorrect. Please try again.',
            }
        
        return render(request, 'login.html', context)

    context = {
        'error': False,
    }
    return render(request, 'login.html', context)

def logoutV(request):
    if(request.user.is_authenticated == True):
        logout(request)
        return redirect("/login")
        
    return redirect("/login")

def registerV(request):
    if(request.user.is_authenticated == True):
        return redirect("/")
    context = {}
    if(request.method == "POST"):
        if request.POST['username'].strip() != "" and request.POST['email'].strip() != "" and request.POST['password'].strip() != "":
            if User.objects.filter(username = request.POST['username']).exists() == False:
                if request.POST['username'].isupper():
                    if User.objects.filter(email = request.POST['email']).exists() == False:
                        user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
                        user.save()
                        default = Group.objects.get(name='DEFAULT') 
                        default.user_set.add(user)
                        login(request, user)
                        return redirect('/')
                    else:
                        context = {
                        'error': True,
                        'e': 'The email you selected is not available. Please choose a different one.'
                        }
                        return render(request, 'Register.html', context)
                else:
                    context = {
                    'error': True,
                    'e': 'The username needs to be all upper case.'
                    }
                    return render(request, 'Register.html', context)
            else:
                context = {
                    'error': True,
                    'e': 'The username you selected is not available. Please choose a different one.'
                }
                return render(request, 'Register.html', context)
        else:
            context = {
                'error': True,
                'e': 'The email, username, or password cannot be empty or contain only spaces. Please try again.'
                }
            return render(request, 'Register.html', context)
    context = {
        'error': False,
    }
            
    
    return render(request, 'Register.html', context)

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
        return redirect('Login')
    
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
        return redirect('Login')
    
    
    
@api_view(['Get'])
def posts(request):
    if(request.user.is_authenticated == False):
        return redirect("/login")
    posts = Post.objects.all().order_by('-date_posted')
    paginator = PageNumberPagination()
    paginator.page_size = 10
    results = paginator.paginate_queryset(posts, request)
    serializer = PostSerializer(results, many=True)
    
    return paginator.get_paginated_response(serializer.data)

@api_view(['Get'])
def HasALike(request, id):
    if(request.user.is_authenticated == False):
        return redirect("/login")
    post = Post.objects.get(id=id)
    if request.user in post.liked.all():
        return HttpResponse("true")
    return HttpResponse("false")

@api_view(['Get'])
def delete(request, id):
    if(request.user.is_authenticated == False):
        return redirect("/login")
    post = Post.objects.get(id=id)
    if post.author.username == request.user.username:
        post.delete()
    return redirect('/')

@api_view(['Get'])
def get_users(request, username):
    if(request.user.is_authenticated == False):
        return redirect("/login")
    users = User.objects.filter(Q(username__startswith=username)).order_by('username')
    if len(users) > 100:
        users = users[:99]
    user_list = [{"username": user.username} for user in users]
    return HttpResponse(json.dumps(user_list), content_type="application/json")

@api_view(['Get'])
def like_or_dislike(request, id):
    if(request.user.is_authenticated == False):
        return redirect("/login")
    post = Post.objects.get(id=id)
    if request.user in post.liked.all():
        post.liked.remove(request.user)
        return HttpResponse('false')
    else:
        post.liked.add(request.user)
        return HttpResponse('true')
