from .models import User, UserMessage, Message, BotAdmins, QuizQuestions, QuizResults
from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("user_id", "chat_id", "reg_date", "username", "timezone", "days_after_reg_date", "marathon_completed")


class UserMessageSerializer(ModelSerializer):
    class Meta:
        model = UserMessage
        fields = ("user_id", "message_id", "sent_at")


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = ("day", "ordinal_number", "message_type", "content_type", "content", "button_name", "button_callback")


class BotAdminsSerializer(ModelSerializer):
    class Meta:
        model = BotAdmins
        fields = ("user_id", "reg_date", "first_name", "last_name", "username")


class QuizQuestionsSerializer(ModelSerializer):
    class Meta:
        model = QuizQuestions
        fields = ("question", )


class QuizResultsSerializer(ModelSerializer):
    class Meta:
        model = QuizResults
        fields = ("user_id", "date", "result")