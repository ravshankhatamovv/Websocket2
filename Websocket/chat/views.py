from django.shortcuts import render
from django.http import HttpResponse
from chat.models import Room


def index_view_admin(request):
    return render(request, 'index.html', {
        'rooms': Room.objects.all(),
    })

def room_view_admin(request, room_name):
    try:
        chat_room = Room.objects.get(name=room_name)
        
    except Exception as e:
        return HttpResponse("Room mavjud emas")
    return render(request, 'room.html', {
        'room': chat_room,
    })

def room_view_user(request, room_name):
    chat_room,created = Room.objects.get_or_create(name=room_name)
    return render(request, 'room.html', {
        'room': chat_room,
    })

def index_view_user(request):
    return render(request, 'user_page.html', {
        'rooms': Room.objects.all(),
    })
