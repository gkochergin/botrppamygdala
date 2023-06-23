from django.contrib import admin
from .models import User, UserMessage, Message, BotAdmins, QuizResults, QuizQuestions

# Register your models here.


admin.site.register(UserMessage)
admin.site.register(BotAdmins)
admin.site.register(QuizQuestions)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['day', 'ordinal_number', 'message_type', 'short_name', 'content']
    readonly_fields = ['button_name', 'button_callback']
    list_editable = ['ordinal_number', 'message_type', 'short_name']
    list_filter = ['day', 'content_type']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    readonly_fields = ['user_id', 'chat_id', 'username', 'marathon_completed', 'reg_date', 'days_after_reg_date']


@admin.register(QuizResults)
class QuizResultsAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'date', 'result']