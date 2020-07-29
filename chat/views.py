from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from .models import Room

User = get_user_model()


@login_required
def index(request):
    rooms = Room.objects.filter(participants=request.user).order_by('-date_modified')
    if rooms.exists():
        latest_room = rooms[0].id
        return redirect('chat:room', room_id=latest_room)
    else:
        return render(request, 'chat/chat.html')


def get_current_chat(room_id):
    return get_object_or_404(Room, id=room_id)


@login_required
def room(request, room_id):
    rooms = ''
    if Room.objects.filter(participants=request.user).exists():
        rooms = Room.objects.filter(participants=request.user)
    if Room.objects.filter(id=room_id).exists():
        room = Room.objects.get(id=room_id)
    return render(request, 'chat/chat.html', {
        'room': room,
        'username': request.user.username,
        'rooms': rooms

    })


def get_last_10_messages(room_id):
    room = get_object_or_404(Room, id=room_id)
    return room.messages.all()
