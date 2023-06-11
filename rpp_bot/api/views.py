from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, ListAPIView, CreateAPIView
from .serializers import UserSerializer, UserMessageSerializer, MessageSerializer, BotAdminsSerializer

from .models import User, UserMessage, Message, BotAdmins


class UserApiView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # переопределяем стандартный метод post
    def post(self, request, *args, **kwargs):
        # создается новый объект сериализатора с данными из запроса
        serializer = self.get_serializer(data=request.data)

        # Проверяется валидность данных. Если данные не валидны, то будет выброшено исключение
        # с информацией об ошибках валидации.
        serializer.is_valid(raise_exception=True)

        # получаем объект или создаём новый
        user, created = User.objects.get_or_create(**serializer.validated_data)

        # Получаем заголовки ответа
        headers = self.get_success_headers(serializer.data)

        # возвращаем ответ с сериализованными данными объекта и соответствующим статусом
        # (201, если был создан новый объект, иначе 200).
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK, headers=headers)


class UserMessagesApiCreate(CreateAPIView):
    queryset = UserMessage.objects.all()
    serializer_class = UserMessageSerializer

    # def perform_create(self, serializer):
    #     user_id = self.request.data.get('user_id')
    #     message_id = self.request.data.get('message_id')
    #     sent_at = self.request.data.get('sent_at')
    #
    #     user = User.objects.get(id=user_id)
    #     message = Message.objects.get(id=message_id)
    #
    #     serializer.save(user_id=user, message_id=message, sent_at=sent_at)

class MessagesApiGet(ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        day = self.request.query_params.get('day')
        return Message.objects.filter(day=day).order_by('ordinal_number')


class BotAdminsApiView(ListCreateAPIView):
    queryset = BotAdmins.objects.all()
    serializer_class = BotAdminsSerializer



