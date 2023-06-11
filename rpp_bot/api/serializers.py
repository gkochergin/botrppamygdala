from .models import User, UserMessage, Message, BotAdmins
from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("user_id", "reg_date", "username", "timezone")


class UserMessageSerializer(ModelSerializer):
    class Meta:
        model = UserMessage
        fields = ("user_id", "message_id", "sent_at")


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = ("day", "ordinal_number", "content_type", "content")


class BotAdminsSerializer(ModelSerializer):
    class Meta:
        model = BotAdmins
        fields = ("user_id", "reg_date", "first_name", "last_name", "username")
