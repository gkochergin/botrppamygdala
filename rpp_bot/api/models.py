from tokenize import tokenize
import emoji
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime, timezone


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
    user_id = models.BigIntegerField(verbose_name='Tg User ID', primary_key=True, unique=True)
    chat_id = models.BigIntegerField(verbose_name='Tg Chat ID', unique=True, default=None)
    username = models.CharField(max_length=255, blank=False, default='')
    reg_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Registration date',
        help_text='Дата первой активации бота')
    timezone = models.CharField(max_length=10, help_text='Часовой пояс пользователя', default='UTC')
    marathon_completed = models.BooleanField(help_text='Статус завершения марафона', default=False)

    def __str__(self):
        return f'TG.ID > {self.user_id} | REG.DATE > {self.reg_date}'

    @property
    def days_after_reg_date(self):
        days_passed_from_now = datetime.now(timezone.utc) - self.reg_date
        number_of_days = days_passed_from_now.days
        return number_of_days


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
    LECTURE = 'LECTURE'
    QUIZ = 'QUIZ'

    MESSAGE_TYPES = [
        (ARTICLE, f'{emoji.emojize(":open_book:")} Статья'),
        (LECTURE, f'{emoji.emojize(":television:")} Лекция'),  # Лекция
        (MEDITATION, f'{emoji.emojize(":woman_in_lotus_position:")} Медитация'),  # Медитация
        (WORKOUT, f'{emoji.emojize(":woman_lifting_weights:")} Упражнение'),  # Упражнение
        (QUIZ, f'{emoji.emojize(":check_mark_button:")} Тест'),  # Упражнение
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
    short_name = models.CharField(max_length=40, default=None, help_text="Короткое название (40 символов), появится справа от emoji")

    def generate_button_data(self):
        # генерируем название для кнопок
        name = ''
        if self.short_name:
            for t in self.MESSAGE_TYPES:
                if self.message_type in t:
                    emj, _ = t[1].split(" ")
                    name = ' '.join([emj, self.short_name])
        else:
            for t in self.MESSAGE_TYPES:
                if self.message_type in t:
                    name = t[1]

        # Создаем коллбек
        prefix = self.message_type
        suffix = self.ordinal_number
        callback: str = ':'.join([str(prefix), str(suffix)])

        return name, callback.lower()

    @property
    def button_name(self) -> str:
        name, _ = self.generate_button_data()
        return name

    @property
    def button_callback(self) -> str:
        _, callback = self.generate_button_data()
        return callback

    def __str__(self):
        return f'Day: {self.day} > M-Type: {self.message_type} > C-Type: {self.content_type} > Order: {self.ordinal_number} > [{self.content[:50]}]'


class UserMessage(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
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

