from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from .models import Chat, Message
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.contrib.auth import logout
from django.contrib import messages

@login_required(login_url='/login/')
def index(request):
    """
        Main chat view. Requires login to access.

        On POST request: Receives a message and saves it to the database. Returns the serialized message as JSON.
        On GET request: Retrieves all messages for a specific chat and renders them in the chat template.
    """
    if request.method == 'POST':
        print("Received data" + request.POST['textmessage'])
        myChat = Chat.objects.get(id=1)
        new_message = Message.objects.create(text=request.POST['textmessage'], chat=myChat, author=request.user, receiver=request.user)
        serialized_obj = serializers.serialize('json', [new_message, ])
        return JsonResponse(serialized_obj[1:-1], safe=False)
    
    chatMessages = Message.objects.filter(chat__id=1)
    return render(request, 'chat/index.html', {'messages': chatMessages})


def login__view(request):
    """
        Handles user login.

        On POST request: Authenticates the user and redirects to the next page or chat view.
        On GET request: Renders the login page.
    """
    redirect = request.GET.get('next', '/chat/')
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))

        if user:
            login(request, user)
            return HttpResponseRedirect(request.POST.get('redirect'))
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

        On POST request: Registers a new user and redirects to the chat view.
        On GET request: Renders the registration page.
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

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return HttpResponseRedirect('/chat/')

    return render(request, 'auth/register.html')
