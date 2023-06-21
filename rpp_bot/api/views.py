from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.generics import ListCreateAPIView, ListAPIView, CreateAPIView
from .serializers import (
    UserSerializer, UserMessageSerializer, MessageSerializer, BotAdminsSerializer,
    QuizResultsSerializer, QuizQuestionsSerializer )

from .models import User, UserMessage, Message, BotAdmins, QuizQuestions, QuizResults


class UserApiView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdateApiView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserMessagesApiCreate(CreateAPIView):
    queryset = UserMessage.objects.all()
    serializer_class = UserMessageSerializer



class MessagesApiGet(ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        day = self.request.query_params.get('day')
        return Message.objects.filter(day=day).order_by('ordinal_number')


class BotAdminsApiView(ListCreateAPIView):
    queryset = BotAdmins.objects.all()
    serializer_class = BotAdminsSerializer



class QuizResultsApiView(ListCreateAPIView):
    queryset = QuizResults.objects.all()
    serializer_class = QuizResultsSerializer


class QuizQuestionsApiView(ListAPIView):
    queryset = QuizQuestions.objects.all()
    serializer_class = QuizQuestionsSerializer

