from django.urls import path
from .views import (
    UserApiView, UserMessagesApiCreate, MessagesApiGet,
    BotAdminsApiView, QuizResultsApiView, QuizQuestionsApiView,
    UserUpdateApiView
)

urlpatterns = [
    path('bot-users', UserApiView.as_view(), name='bot-users'),
    path('upd-user-data/<int:pk>/', UserUpdateApiView.as_view(), name='upd-user-data'),
    path('sent-messages', UserMessagesApiCreate.as_view(), name='sent-messages'),
    path('messages', MessagesApiGet.as_view(), name='messages'),
    path('bot-admins', BotAdminsApiView.as_view(), name='bot-admins'),
    path('quiz-result', QuizResultsApiView.as_view(), name='quiz-result'),
    path('quiz-question', QuizQuestionsApiView.as_view(), name='quiz-question'),

]