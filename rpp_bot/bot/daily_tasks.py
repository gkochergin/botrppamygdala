import logging as log
from aiogram.types import Message, CallbackQuery
from api import get_messages_by_day
from keyboards import make_inline_kb_with_two_buttons


class DailyTasks:
    # я хочу, чтобы этот класс обслуживал все необходимые функции для вызова заданий каждого дня
    message_audio = None
    message_video = None
    message_text = None

    def __init__(self, day_num: int):
        # day_num передается в бд для получения всех записей за этот день
        self.day_num = day_num
        self.tasks = get_messages_by_day(day_num)  # список заданий этого дня
        self.tasks_count = len(self.tasks)

    def day_content(self):
        # TEXT = 'TXT'
        # VIDEO = 'VID'
        # AUDIO = 'AUD'
        # IMAGE = 'IMG'
        # GIF = 'GIF'

        for dictionary in self.tasks:
            if dictionary['content_type'] == 'TXT':
                print('TEXT')
                content = dictionary['content']
                print()
                return content
            if dictionary['content_type'] == 'VID':
                content = dictionary['content']
                return content
            if dictionary['content_type'] == 'AUD':
                print('AUDIO')
                content = dictionary['content']
                return content
            if dictionary['content_type'] == 'IMG':
                content = dictionary['content']
                return content
            if dictionary['content_type'] == 'GIF':
                content = dictionary['content']
                return content

    def day_first(self):
        main_message =




user_day = DailyTasks(day_num=1).day_content()
print(user_day)


class UserSession:
    # а вот возможно надо создать активную сессию пользователя и хранить там данные
    # сохранять пользователя в бд

    def __init__(self, tg_bot: Message or CallbackQuery):
        # bot_access - любой объект бота, через который можно вызвать данные пользователя
        # это может быть message или callback_query
        self.first_name = tg_bot.from_user.first_name
        self.last_name = tg_bot.from_user.last_name
        self.user_id = tg_bot.from_user.id

    def save_session(self):
        pass


