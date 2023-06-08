from django.urls import path
from .views import UserApiView, UserMessagesApiCreate, MessagesApiGet, BotAdminsApiView

urlpatterns = [
    path('bot-users', UserApiView.as_view(), name='bot-users'),
    path('sent-messages', UserMessagesApiCreate.as_view(), name='sent-messages'),
    path('messages', MessagesApiGet.as_view(), name='messages'),
    path('bot-admins', BotAdminsApiView.as_view(), name='bot-admins'),

]