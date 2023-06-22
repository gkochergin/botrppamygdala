from django.db.models import ExpressionWrapper, F, DurationField, IntegerField
from django.db.models.functions import Cast
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.generics import ListCreateAPIView, ListAPIView, CreateAPIView
from .serializers import (
    UserSerializer, UserMessageSerializer, MessageSerializer, BotAdminsSerializer,
    QuizResultsSerializer, QuizQuestionsSerializer )

from .models import User, UserMessage, Message, BotAdmins, QuizQuestions, QuizResults


class UserApiView(ListCreateAPIView):
    queryset = User.objects.annotate(
        day_number=ExpressionWrapper(timezone.now() - F('reg_date'), output_field=DurationField())
    )

    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.query_params.get('filter_by_days'):
            max_day_number = 12
            filtered_queryset = self.queryset.filter(day_number__gte=timezone.timedelta(days=max_day_number))
            print("api.py >", "get_queryset >", "days_count >", filtered_queryset)
            return filtered_queryset
        else:
            return super().get_queryset()


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

