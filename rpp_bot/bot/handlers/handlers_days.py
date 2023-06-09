import dataclasses
from datetime import datetime
from aiogram import Router, types, F, Bot
from aiogram.filters import Command
from typing import List

from ..admin_utils.admin_utilities import admin_access
from ..api.api import get_messages_by_day, get_daily_buttons_data, get_buttons_callback, create_user, \
    record_sent_message_event
from rpp_bot.bot.admin_utils.tools import matching_word_numeral, convert_response_dict_to_string, split_text_to_parts
from rpp_bot.bot.keyboards.keyboards import make_inline_kb

# назначаем роутер
router = Router()


class DailyTasks:
    def __init__(self, day_num: int, user_first_name: str):
        # day_num передается в бд для получения всех записей за этот день
        self.day_num = day_num
        self.tasks = get_messages_by_day(day_num)  # список заданий этого дня
        self.tasks_count = len(self.tasks)
        self.daily_greeting_template = f"{user_first_name.strip()}, приветствую тебя на {self.day_num} " \
                                       f"дне нашего марафона. Под этим сообщением есть {self.tasks_count} " \
                                       f"{matching_word_numeral(wrd='кнопка', dgt=self.tasks_count)} " \
                                       f"с твоими лекциями и заданиями. Давай начинать!"

    def get_daily_keyboard(self):
        btns_data = get_daily_buttons_data(self.day_num)
        markup = make_inline_kb(buttons_data=btns_data, sizes=[1, ])
        return markup


@dataclasses.dataclass
class DataStorage:
    btn_days_list = [f'Day {i}' for i in range(0, 13)]
    btn_back_next = [{'name': '<<<<', 'data': 'back'}, {'name': '>>>>', 'data': 'next'}]
    selected_day = int
    text_parts_list = List[str]
    text_part_num = int
    kb_back_next = make_inline_kb(buttons_data=btn_back_next)
    callback_match_list = list
    today = DailyTasks

    def get_callback_match_list(self):
        self.callback_match_list = get_buttons_callback(day=self.selected_day)
        return self.callback_match_list

    def get_parts_count(self):
        self.text_parts_count = len(self.text_parts_list)
        return self.text_parts_count


# объявляем экземпляр класса DataStorage для последующего использования в функциях
data_storage = DataStorage()


async def split_text_and_get_markup(response: list, ds=data_storage):
    # если ответ сервера (aka response) не пустой, то обрабатываем по логике
    if response:
        # превращаем ответ сервера в строку
        response_string = convert_response_dict_to_string([response])

        # разбиваем строку на элементы определенной длины
        ds.text_parts_list = split_text_to_parts(text=response_string, part_length=800)

        # выбираем кусок текста и форматируем сообщение для отправки
        if len(ds.text_parts_list) == 1:
            # если в тексте всего 1 кусок, то просто отправляем текст, без клавиатуры
            message_text = ds.text_parts_list[0]
            return message_text, None
        else:
            # Если в тексте более 1 куска, то просто отправляем первый кусок текста
            # с клавиатурой "вперёд-назад", т.е. читать дальше или вернуться назад
            ds.text_part_num = 0
            message_text = ds.text_parts_list[
                               ds.text_part_num] + f"\n\nСтраница {1} из {len(ds.text_parts_list)}"
            markup = ds.kb_back_next
            return message_text, markup
    else:
        # если ответ сервера (aka response) пустой, то сообщаем об этом и больше ничего
        message_text = "Сообщений за этот день не найдено"
        return message_text, None


@router.message(Command(commands=["start"]))
async def command_start_handler(message: types.Message) -> None:
    # Creating new user in db, skip if already exists
    create_user(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        username=message.from_user.username,
        timezone='UTC')

    # Get list of messages by day number. By default, first day number equals zero.
    messages_list = get_messages_by_day(day=0)


    # Send message to user
    await message.answer(messages_list[0]['content'])

    # Save to db "message sent to user" event
    record_sent_message_event(user_id=message.from_user.id, message_id=1, sent_at=datetime.now())


"""
Если с даты регистрации у пользователя прошло более 12 дней (т.е. фактически считаем уже >=13),
то этот пользователь получает статус "marathon_completed=True". При этом нам не важно, прочитал он свои задания
или нет. 

Как пользователю, прошедшему марафон дать возможность вернуться к информации каждого дня?

"""


@router.message(F.text.in_(data_storage.btn_days_list))
@admin_access
async def get_day_tasks_and_sent_to_user(message: types.Message, bot: Bot = None, chat_id: int = -1, day_num: int = -1,
                                         ds=data_storage):
    if day_num > -1:
        ds.selected_day = day_num
    else:
        ds.selected_day = int(message.text.removeprefix("Day "))
    ds.callback_match_list = get_buttons_callback(ds.selected_day)
    today_tasks = DailyTasks(day_num=ds.selected_day, user_first_name=message.from_user.first_name)
    if chat_id == -1:
        await message.answer(text=today_tasks.daily_greeting_template, reply_markup=today_tasks.get_daily_keyboard())
    else:
        await bot.send_message(chat_id=chat_id, text=today_tasks.daily_greeting_template,
                               reply_markup=today_tasks.get_daily_keyboard())

    @router.callback_query(F.data.in_(data_storage.callback_match_list))
    async def process_message_types_callbacks(callback: types.CallbackQuery, ds=data_storage):
        message_type, message_num = callback.data.split(":")
        ds.today = DailyTasks(day_num=ds.selected_day, user_first_name=callback.from_user.first_name)

        if message_type == 'article':
            message_text, markup = await split_text_and_get_markup(ds.today.tasks[int(message_num) - 1])
            await callback.message.answer(text=message_text, reply_markup=markup)
            await callback.answer(show_alert=False)
        elif message_type in ['meditation', 'workout', 'lecture', 'quiz']:
            await callback.message.answer(text=ds.today.tasks[int(message_num) - 1]['content'],
                                          reply_markup=None)

    @router.callback_query(F.data.in_(['back', 'next']))
    async def back_next_callback(callback_query: types.CallbackQuery, ds=data_storage) -> None:
        # counting total text parts
        total_text_parts = len(ds.text_parts_list)

        # pagination logic
        if callback_query.data == 'back':
            print(ds.text_part_num)
            if ds.text_part_num > 0:
                ds.text_part_num -= 1
            else:
                text_part_num = total_text_parts - 1
        elif callback_query.data == 'next':
            if ds.text_part_num < total_text_parts - 1:
                ds.text_part_num += 1
            elif ds.text_part_num == total_text_parts - 1:
                text_part_num = 0
        # выбираем кусок текста по его номеру в списке и форматируем сообщение для отправки
        message_text = ds.text_parts_list[
                           ds.text_part_num] + f"\n\nСтраница {ds.text_part_num + 1} из {total_text_parts}"

        await callback_query.message.edit_text(text=message_text, reply_markup=ds.kb_back_next)
        await callback_query.answer(show_alert=False)
