import logging as log
from aiogram.types import Message, CallbackQuery

class DailyTasks():
    # я хочу, чтобы этот класс обслуживал все необходимые функции для вызова заданий каждого дня
    tasks = # список заданий этого дня
    message_audio = None
    message_video = None
    message_text = None


    def __init__(self, day_num: int):
        # day_num передается в бд для получения всех записей за этот день
        self.day_num = day_num
        pass



class UserSession():
    # а вот возможно надо создать активную сессию пользователя и хранить там данные
    # сохранять пользователя в бд

    def __init__(self, tg_bot: Message | CallbackQuery, ):
        # bot_access - любой объект бота, через который можно вызвать данные пользователя
        # это может быть message или callback_query
        self.first_name = tg_bot.from_user.first_name
        self.last_name = tg_bot.from_user.last_name
        self.user_id = tg_bot.from_user.id
