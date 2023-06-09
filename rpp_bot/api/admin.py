from django.contrib import admin
from .models import User, UserMessage, Message, BotAdmins

# Register your models here.

admin.site.register(User)
admin.site.register(UserMessage)
admin.site.register(Message)
admin.site.register(BotAdmins)