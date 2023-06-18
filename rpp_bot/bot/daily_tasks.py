import logging as log
from aiogram.types import Message, CallbackQuery
from api import get_messages_by_day
from keyboards import make_inline_kb


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

    def typical_day(self):
        # Инициализация дня
        message_intro = "Привет! Это твой новый день под сообщением есть кнопки с твоими лекциями и заданиями. " \
                        "Нажимай, и да пребудет с тобой сила, мой юный падаван."
        btn_names = ['Лонгрид', 'Медитация', 'Упражнение']
        btn_callbacks = ['longread', 'meditation', 'workout']
        message_type = ['TXT']
        btns_data = [{'name': name, 'data': callback} for name, callback in zip(btn_names, btn_callbacks)]
        print(btns_data)

        # я не понимаю, как определить кол-во кнопок? я же не знаю, сколько будет всего сообщений?
        # наоборот, знаю, это кол-во записей за этот день. они уже отсортированы в нужном порядке.
        # окей, а каковы должны быть надписи на этих кнопках? а вот это уже хороший вопрос.
        # можно попробовать составить такой словарь
        buttons_quantity = self.tasks # 3

        make_inline_kb()


        # Вывод пользователю await message.answer или аналог
        print(message_intro)
        for b in btn_names:
            print([b])
        print()

        #



        # Доступ к ИИ


user_day = DailyTasks(day_num=1)
# print(user_day)

print(user_day.typical_day())


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
