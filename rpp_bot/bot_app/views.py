from .models import User, UserMessage, Message, BotAdmins
from .serializers import UserSerializer, UserMessageSerializer, MessageSerializer, BotAdminsSerializer
from rest_framework.generics import ListCreateAPIView, ListAPIView, CreateAPIView


class UserApiView(ListCreateAPIView):
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



