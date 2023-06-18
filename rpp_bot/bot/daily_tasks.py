from aiogram.types import Message, CallbackQuery

import api
import emoji
from keyboards import make_inline_kb


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
        self.daily_greeting_template = f"{user_first_name.strip()}, приветствую тебя на {self.day_num} дне нашего марафона. " \
                                  f"Под этим сообщением есть кнопки с твоими лекциями и заданиями. Давай начинать!"



    def typical_day(self):


        # Инициализация дня
        btns_data = []



        for dictionary in self.tasks:
            btn_names.append(dictionary['message_type'])
        btn_callbacks = [str]
        match_data = [{'name': name, 'data': callback} for name, callback in zip(btn_names, btn_callbacks)]
        print(btns_data)

        # я не понимаю, как определить кол-во кнопок? я же не знаю, сколько будет всего сообщений?
        # наоборот, знаю, это кол-во записей за этот день. они уже отсортированы в нужном порядке.
        # окей, а каковы должны быть надписи на этих кнопках? а вот это уже хороший вопрос.
        # можно попробовать составить такой словарь
        buttons_quantity = self.tasks  # 3

        make_inline_kb(btns_data)

        # Вывод пользователю await message.answer или аналог
        print(self.daily_greeting_template)
        for b in btn_names:
            print([b])
        print()

        #

        # Доступ к ИИ


user_day = DailyTasks(day_num=1, user_first_name='Наташа')
# print(user_day)

print(user_day.typical_day())

b = api.get_messages_by_day(day=1)


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
