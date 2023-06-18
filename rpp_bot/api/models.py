from tokenize import tokenize
import emoji
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.

class BotAdmins(models.Model):
    user_id = models.BigIntegerField(primary_key=True, unique=True)
    reg_date = models.DateTimeField(auto_now=True, verbose_name='Registration date')
    first_name = models.CharField(max_length=30, blank=True, help_text='Имя пользователя')
    last_name = models.CharField(max_length=30, blank=True, help_text='Фамилия пользователя')
    username = models.CharField(max_length=255, verbose_name='Telegram username', default='')

    def __str__(self):
        return f'{self.user_id} > {self.first_name} {self.last_name}'


class User(models.Model):
    user_id = models.BigIntegerField(verbose_name='Telegram ID', primary_key=True, unique=True)
    username = models.CharField(max_length=255, blank=False, default='')
    reg_date = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name='Registration date',
        help_text='Дата первой активации бота')
    timezone = models.CharField(max_length=10, help_text='Часовой пояс пользователя')

    def __str__(self):
        return f'TG.ID > {self.user_id} | REG.DATE > {self.reg_date}'


class Message(models.Model):
    # content types
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

    # message types
    ARTICLE = 'ARTICLE'
    MEDITATION = 'MEDITATION'
    WORKOUT = 'WORKOUT'

    MESSAGE_TYPES = [
        (ARTICLE, f'{emoji.emojize(":open_book:")} Статья'),
        (MEDITATION, f'{emoji.emojize(":woman_in_lotus_position:")} Медитация'),
        (WORKOUT, f'{emoji.emojize(":woman_lifting_weights:")} Упражнение'),
    ]

    # day 0 - это все сообщения за первый интро день, day 12 - то сообщения за последний день аутро
    day = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(12)],
        verbose_name='Sending day',
        help_text='Номер дня по счету от даты регистрации, когда отправить сообщение')
    ordinal_number = models.IntegerField(help_text='Порядковый номер отправки (уникальный)', default=1)
    content_type = models.CharField(max_length=3, choices=CONTENT_TYPES, default=TEXT)
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES, default=ARTICLE)
    content = models.TextField()

    def __str__(self):
        return f'Day: {self.day} > M-Type: {self.message_type} > C-Type: {self.content_type} > Order: {self.ordinal_number} > [{self.content[:50]}]'


class UserMessage(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Telegram ID')
    message_id = models.ForeignKey(Message, on_delete=models.CASCADE)
    sent_at = models.DateTimeField(
        verbose_name='Sending date & time',
        help_text='Дата, когда было отправлено сообщение')

    def __str__(self):
        return f'Message sent to user_id={self.user_id} at time={self.sent_at}'


class QuizQuestions(models.Model):
    question = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.pk} > {self.question}"


class QuizResults(models.Model):
    # Хранятся все результаты для всех тестов ?
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Telegram ID')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Quiz date', help_text='Дата прохождения квиза')
    result = models.IntegerField()

    def __str__(self):
        return f"User: {self.user_id.user_id} > Quiz date: {self.date} > Result: {self.result}"

