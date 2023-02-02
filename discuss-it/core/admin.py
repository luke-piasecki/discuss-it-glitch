from django.contrib import admin

# Register your models here.
from .models import People, ChatEntry, ChatRooms

admin.site.register(People)
admin.site.register(ChatEntry)
admin.site.register(ChatRooms)

