from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from .models import Chat, Message
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.contrib.auth import logout
from django.db import transaction
from django.contrib import messages

@login_required(login_url='/login/')
def index(request):
    """
        Main chat view. Requires login to access.
        On POST request: Receives a message and saves it to the database.
        On GET request: Retrieves all messages for the chat and renders them in the chat template.
    """
    chat = Chat.objects.first() 

    if request.method == 'POST':
        new_message = Message.objects.create(
            text=request.POST['textmessage'], 
            chat=chat, 
            author=request.user, 
            receiver=request.user
        )
        serialized_obj = serializers.serialize('json', [new_message, ])
        return JsonResponse(serialized_obj[1:-1], safe=False)
    
    chatMessages = Message.objects.filter(chat=chat)
    return render(request, 'chat/index.html', {'messages': chatMessages})

def login__view(request):
    """
        Handles user login.
    """
    redirect = request.GET.get('next', '/chat/')
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return HttpResponseRedirect(redirect)
        else:
            return render(request, 'auth/login.html', {'wrongPassword': True, 'redirect': redirect})
    return render(request, 'auth/login.html', {'redirect': redirect})

def logout_view(request):
    """
        Handles user logout and redirects to the login page.
    """
    logout(request)
    return HttpResponseRedirect('/login/')

def register__view(request):
    """
        Handles new user registration.
        Create a new Chat when none exists
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'auth/register.html')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'auth/register.html')

        with transaction.atomic():
            user = User.objects.create_user(username=username, email=email, password=password)
            if not Chat.objects.exists():
                Chat.objects.create()
        login(request, user)
        return HttpResponseRedirect('/chat/')

    return render(request, 'auth/register.html')