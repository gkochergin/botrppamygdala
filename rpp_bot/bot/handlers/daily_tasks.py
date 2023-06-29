from aiogram.types import Message, CallbackQuery
from aiogram import Router

from typing import Union

router = Router()







class UserSession:
    # а вот возможно надо создать активную сессию пользователя и хранить там данные
    # сохранять пользователя в бд

    def __init__(self, tg_bot: Union[Message, CallbackQuery]):
        # bot_access - любой объект бота, через который можно вызвать данные пользователя
        # это может быть message или callback_query
        self.first_name = tg_bot.from_user.first_name
        self.last_name = tg_bot.from_user.last_name
        self.user_id = tg_bot.from_user.id

    def save_session(self):
        pass
