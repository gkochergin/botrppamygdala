from .models import User, UserMessage, Message, BotAdmins, QuizQuestions, QuizResults
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    days_after_reg_date = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ('user_id', 'chat_id', 'username', 'reg_date', 'timezone', 'marathon_completed', 'days_after_reg_date')


class UserMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMessage
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    button_name = serializers.ReadOnlyField()
    button_callback = serializers.CharField()

    class Meta:
        model = Message
        fields = '__all__'


class BotAdminsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotAdmins
        fields = '__all__'


class QuizQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizQuestions
        fields = '__all__'


class QuizResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizResults
        fields = '__all__'
