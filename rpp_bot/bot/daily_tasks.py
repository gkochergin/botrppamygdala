from aiogram.types import Message, CallbackQuery
from aiogram.handlers import callback_query
from aiogram import Router
from aiogram.filters import Command
import pymorphy2

import api
import emoji
from keyboards import make_inline_kb
from typing import Union

router = Router()




def matching_word_numeral(wrd: str, dgt: int):
    # Согласование слов с числительными
    # https://pymorphy2.readthedocs.io/en/latest/user/guide.html#id8
    morph = pymorphy2.MorphAnalyzer()
    word_parse = morph.parse(wrd)[0]
    return word_parse.make_agree_with_number(dgt).word


class DailyTasks:
    # я хочу, чтобы этот класс обслуживал все необходимые функции для вызова заданий каждого дня
    message_audio = None
    message_video = None
    message_text = None

    def __init__(self, day_num: int, user_first_name: str):
        # day_num передается в бд для получения всех записей за этот день
        self.day_num = day_num
        self.tasks = api.get_messages_by_day(day_num)  # список заданий этого дня
        self.tasks_count = len(self.tasks)
        self.daily_greeting_template = f"{user_first_name.strip()}, приветствую тебя на {self.day_num} " \
                                       f"дне нашего марафона. Под этим сообщением есть {self.tasks_count} " \
                                       f"{matching_word_numeral(wrd='кнопка', dgt=self.tasks_count)} " \
                                       f"с твоими лекциями и заданиями. Давай начинать!"

    def get_daily_keyboard(self):
        btns_data = api.get_daily_buttons_data(self.day_num)
        markup = make_inline_kb(buttons_data=btns_data, sizes=[1, ])
        return markup


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


@router.message(Command(commands=['startday']))
async def command_handler_startday(message: Message):
    session = UserSession(message)
    today = DailyTasks(day_num=7, user_first_name=session.first_name)
    await message.answer(text=today.daily_greeting_template, reply_markup=today.get_daily_keyboard())


