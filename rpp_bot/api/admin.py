from django.contrib import admin
from .models import User, UserMessage, Message, BotAdmins, QuizResults, QuizQuestions

# Register your models here.


admin.site.register(UserMessage)
admin.site.register(BotAdmins)
admin.site.register(QuizResults)
admin.site.register(QuizQuestions)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['day', 'ordinal_number', 'message_type', 'content_type', 'content']
    readonly_fields = ['button_name', 'button_callback']
    list_editable = ['ordinal_number', 'message_type']
    list_filter = ['day', 'content_type']

    @admin.display(description='Tokens')
    def simple_token_calc(self, cont: Message):
        tokens = cont.content.max_length
        return str(tokens)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    readonly_fields = ['user_id', 'chat_id', 'username', 'marathon_completed', 'reg_date', 'days_after_reg_date']