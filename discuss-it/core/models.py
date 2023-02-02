from django.db import models
from django.contrib.auth.models import User # new
from django.contrib.auth import get_user_model
from django import forms

# Create your models here.
class People(models.Model):
    politics = models.CharField(max_length=2)
    username = models.CharField(max_length=30)
    topic = models.CharField(max_length=30, default='')
    user_id = models.IntegerField(default=0)
    hostility_reports = models.IntegerField(default=0)
    swearing_reports = models.IntegerField(default=0)
    discrimination_reports = models.IntegerField(default=0)
    banned = models.BooleanField(default=False)
class ChatEntry(models.Model):
    username = models.CharField(max_length=30, default='')
    chatroom = models.ForeignKey('ChatRooms', on_delete=models.CASCADE)
    entry = models.CharField(max_length=140)
    timestamp = models.IntegerField(default='')
class ChatRooms(models.Model):
    user1 = models.CharField(max_length=30, default='')
    user2 = models.CharField(max_length=30, default='')
    name = models.IntegerField()
    topic = models.CharField(max_length=30, default='')
    user_number = models.IntegerField(default=1)
    user_politics = models.IntegerField(default=0)
    def __str__(self):
        return str(self.name)
