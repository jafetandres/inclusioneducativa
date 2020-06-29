import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe

User = get_user_model()


def index(request):
    return render(request, 'chat/ca.html')


@login_required
def room(request, room_name):
    return render(request, 'chat/ca.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'username': mark_safe(json.dumps(request.user.username)),
    })
