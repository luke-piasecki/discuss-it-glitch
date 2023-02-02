from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

#from chat.views import index
from random import randint

from .models import People, ChatRooms, ChatEntry
from .forms import PeopleForm


@login_required
def index(request):
    matched = False
    if People.objects.filter(user_id=request.user.id).exists():
        person = People.objects.get(user_id=request.user.id)
        politics = int(person.politics)
        opposite = -1*(politics-5) + 5
        lower_bound = opposite-1
        for chatroom in ChatRooms.objects.all():
            if chatroom.topic == person.topic and chatroom.user_number == 1 and chatroom.user_politics >= lower_bound and chatroom.user_politics <= lower_bound + 2:
                matched = True
                room_name = chatroom.name
                chatroom.user_number += 1
                chatroom.user2 = person.username
                chatroom.save()
                return redirect('/chat/'+str(room_name)+'/')
        if matched == False:
            new_name = randint(0,9999)
            while ChatRooms.objects.filter(name=new_name).exists():
                new_name = randint(0,9999)
            new_room = ChatRooms(name=new_name, topic=person.topic, user_number=1, user_politics=int(person.politics), user1 = person.username)
            new_room.save()
            room_name = new_name
            matched = True
            return redirect('/chat/'+str(room_name)+'/')
        context = {'room_name': room_name}
        return render(request, "chat/index.html")


    else:
        return redirect(people_view)


def home_view(request):
    if request.method == 'POST':
        if 'Chat' in request.POST:
            if request.user.is_authenticated:
                if People.objects.filter(user_id=request.user.id).exists():
                    return redirect(topic_view)
                else:
                    return redirect(people_view)
            else:
                return redirect('sign_up')
        if 'Account' in request.POST:
            return redirect(account_view)
    return render(request, "core/home.html")
def login_view(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user =  auth.authenticate(request, username=username, password=password)

      # Check if a user is verified and authenticated
        if user is not None:
        # Use the returned user object in login()
            login(request, user)

        # Redirect to home page after logging in
            return redirect(home_view)
        else:
            return render(request, "registration/signup.html")
    return render(request, 'registration/login.html')
def logout_view(request):
    logout(request)
    #return render(request, "Disquss/home.html")

class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


#class PeopleCreate(CreateView, LoginRequiredMixin):
#    model = People
#    template_name = 'core/politics.html'
#    form_class = PeopleForm

@login_required
def people_view(request):
    if People.objects.filter(user_id=request.user.id).exists() == False:
        problem = False
        name = str(request.user.username)
        id = request.user.id
        if request.method == 'POST':
            new_entry = People()
            if request.POST["politics"].isnumeric():
                if int(request.POST["politics"]) <= 10:
                    new_entry.politics = request.POST["politics"]
                    new_entry.username = name
                    new_entry.user_id = id
                    new_entry.choice = request.POST["politics"]
                    new_entry.save()
                    problem = False
                    return redirect(topic_view)
                else:
                    #return redirect(people_view)
                    problem = True
            else:
                problem = True
                #return redirect(people_view)

        context = {'problem': problem}
        return render(request, 'core/politics.html', context)
    else:
        return redirect(topic_view)
@login_required
def topic_view(request):
    if People.objects.filter(user_id=request.user.id).exists():
        person = People.objects.get(user_id=request.user.id)
        topic = ''
        if request.method == 'POST':
            if 'abortion' in request.POST:
                topic = 'abortion'
            elif 'immigration' in request.POST:
                topic = 'immigration'
            person.topic = topic
            person.save()
            return redirect(index)

        context = {'topic': topic}
        return render(request, 'core/topics.html', context)
    else:
        return redirect(index)
@login_required
def account_view(request):
    if People.objects.filter(user_id=request.user.id).exists():
        id = request.user.id
        username = request.user.username
        user = User.objects.get(username=username)
        person = People.objects.get(username=username)
        if request.method == 'POST':
            if 'new_username' in request.POST:
                request.user.username = request.POST["new_username"]
                person.username = request.POST["new_username"]
            if 'new_password' in request.POST:
                user.password = request.POST["new_password"]
    else:
        return redirect(people_view)
    context = {'username': user.username}
    return render(request, 'core/account.html', context)
