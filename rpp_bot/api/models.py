from tokenize import tokenize

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.

class BotAdmins(models.Model):
    user_id = models.CharField(max_length=20, primary_key=True, unique=True)
    reg_date = models.DateTimeField(auto_now=True, verbose_name='Registration date')
    first_name = models.CharField(max_length=30, blank=True, help_text='Имя пользователя')
    last_name = models.CharField(max_length=30, blank=True, help_text='Фамилия пользователя')
    username = models.CharField(max_length=255, verbose_name='Telegram username', default='')

    def __str__(self):
        return f'{self.user_id} > {self.first_name} {self.last_name}'


class User(models.Model):
    user_id = models.CharField(verbose_name='Telegram ID', max_length=20, primary_key=True, unique=True)
    username = models.CharField(max_length=255, blank=False, default='')
    reg_date = models.DateTimeField(
        auto_now=True,
        editable=False,
        verbose_name='Registration date',
        help_text='Дата первой активации бота')
    timezone = models.CharField(max_length=10, help_text='Часовой пояс пользователя')

    def __str__(self):
        return f'TG.ID > {self.user_id} | REG.DATE > {self.reg_date}'


class Message(models.Model):
    TEXT = 'TXT'
    VIDEO = 'VID'
    AUDIO = 'AUD'
    IMAGE = 'IMG'
    GIF = 'GIF'

    CONTENT_TYPES = [
        (TEXT, 'Text'),
        (VIDEO, 'Video'),
        (AUDIO, 'Audio'),
        (IMAGE, 'Image'),
        (GIF, 'Gif'),
    ]

    # day 0 - это все сообщения за первый интро день, day 12 - то сообщения за последний день аутро
    day = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(12)],
        verbose_name='Sending day',
        help_text='Номер дня по счету от даты регистрации, когда отправить сообщение')
    ordinal_number = models.IntegerField(help_text='Порядковый номер отправки (уникальный)', default=1)
    content_type = models.CharField(max_length=3, choices=CONTENT_TYPES, default=TEXT)
    content = models.TextField()

    def __str__(self):
        return f'Day: {self.day} > Type: {self.content_type} > Order: {self.ordinal_number}> [{self.content[:50]}]'


class UserMessage(models.Model):
    user_id = models.ForeignKey(to='api.User', on_delete=models.CASCADE, verbose_name='Telegram ID')
    message_id = models.ForeignKey(Message, on_delete=models.CASCADE, editable=False)
    sent_at = models.DateTimeField(
        verbose_name='Sending date & time',
        editable=False,
        help_text='Дата, когда было отправлено сообщение')

    def __str__(self):
        return f'Message sent to user_id={self.user_id} at time={self.sent_at}'
