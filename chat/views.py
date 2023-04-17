from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from .models import Chat
import json


@login_required(login_url='login')
def index(request):
    user = request.user
    chat_rooms = Chat.objects.filter(members=user)
    context = {
        'chat_rooms': chat_rooms
    }
    return render(request, "chat/index.html", context=context)

@login_required()
def room(request, roomname):
    user = request.user
    chat_model = Chat.objects.filter(roomname=roomname)
    if not chat_model.exists():
        chat = Chat.objects.create(roomname=roomname)
        chat.members.add(user)
    else:
        chat_model[0].members.add(user)


    username = request.user.username
    context = {
        "room_name": roomname,
        "username": mark_safe(json.dumps(username))
    }
    return render(request, "chat/room.html", context)

