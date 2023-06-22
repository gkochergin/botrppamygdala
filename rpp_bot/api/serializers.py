from .models import User, UserMessage, Message, BotAdmins, QuizQuestions, QuizResults
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [f.name for f in User._meta.fields] + ['days_after_reg_date']


class UserMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMessage
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    button_name = serializers.ReadOnlyField(source='button_name')
    button_callback = serializers.CharField(source='button_callback')

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
