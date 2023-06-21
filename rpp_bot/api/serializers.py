from .models import User, UserMessage, Message, BotAdmins, QuizQuestions, QuizResults
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import CharField, IntegerField


class UserSerializer(ModelSerializer):
    days_after_reg_date = IntegerField()

    class Meta:
        model = User
        fields = "__all__"


class UserMessageSerializer(ModelSerializer):
    class Meta:
        model = UserMessage
        fields = "__all__"


class MessageSerializer(ModelSerializer):
    button_name = CharField()
    button_callback = CharField()

    class Meta:
        model = Message
        fields = "__all__"


class BotAdminsSerializer(ModelSerializer):
    class Meta:
        model = BotAdmins
        fields = "__all__"


class QuizQuestionsSerializer(ModelSerializer):
    class Meta:
        model = QuizQuestions
        fields = "__all__"


class QuizResultsSerializer(ModelSerializer):
    class Meta:
        model = QuizResults
        fields = "__all__"