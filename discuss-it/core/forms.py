from django.forms import ModelForm
from core.models import People, ChatEntry
from django import forms

class PeopleForm(ModelForm):
    class Meta:
        model = People
        fields = ['politics', 'username', 'topic']
#class ChatEntryForm(ModelForm):
#    class Meta:
#        model = ChatEntry
#        fields = ['username', 'chatroom', 'entry']
