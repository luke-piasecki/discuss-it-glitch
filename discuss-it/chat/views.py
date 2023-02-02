from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from core.views import people_view, index, home_view
from core.models import ChatEntry, ChatRooms, People
from random import randint
# Create your views here.

@login_required
def room(request, room_name):
    user = People.objects.get(username=request.user.username)
    if user.banned == True:
        return redirect(home_view)
    if request.method == 'POST':
        if 'Home' in request.POST:
            return redirect(home_view)
        else:
            if 'hostility' in request.POST:
                infraction = "hostility"
            elif 'swearing' in request.POST:
                infraction = "swearing"
            else:
                infraction = "discrimination"
            chatroom = ChatRooms.objects.get(name=room_name)
            if request.user.username != chatroom.user1:
                reporteduser = People.objects.get(username=chatroom.user1)
                if infraction == "hostility":
                    reporteduser.hostility_reports += 1
                elif infraction == "swearing":
                    reporteduser.hostility_reports += 1
                elif infraction == "discrimination":
                    reporteduser.discrimination_reports += 1
                reporteduser.save()
            else:
                if chatroom.user2 != '':
                    reporteduser = People.objects.get(username=chatroom.user2)
                    if infraction == "hostility":
                        reporteduser.hostility_reports += 1
                    elif infraction == "swearing":
                        reporteduser.hostility_reports += 1
                    elif infraction == "discrimination":
                        reporteduser.discrimination_reports += 1
                    reporteduser.save()
            return redirect(home_view)

    log = []
    for sent_item in ChatEntry.objects.filter(chatroom=ChatRooms.objects.get(name=room_name)):
        if ChatEntry.objects.filter(entry=sent_item.entry, timestamp=sent_item.timestamp).count()>1:
            sent_item.delete()
    for sent_item in ChatEntry.objects.filter(chatroom=ChatRooms.objects.get(name=room_name)):
        log.append(sent_item.entry)
    username = request.user.username
    context = {"room_name": room_name, "username": username, "log": log}
    return render(request, "chat/room.html", context)
