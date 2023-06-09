from django.contrib import admin
from .models import User, UserMessage, Message, BotAdmins

# Register your models here.


admin.site.register(User)
admin.site.register(UserMessage)
admin.site.register(BotAdmins)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['day', 'ordinal_number', 'content_type', 'content']
    list_editable = ['ordinal_number']
    list_filter = ['day', 'content_type']

    @admin.display(description='Tokens')
    def simple_token_calc(self, cont: Message):
        tokens = cont.content.max_length
        return str(tokens)
