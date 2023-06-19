import dataclasses
from datetime import datetime
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from typing import List

import rpp_bot.bot.api as api
import tools as tls
import keyboards as kb
from daily_tasks import DailyTasks

# назначаем роутер
router = Router()


@dataclasses.dataclass
class DataStorage:
    btn_days_list = [f'Day {i}' for i in range(0, 13)]
    btn_back_next = [{'name': '<<<<', 'data': 'back'}, {'name': '>>>>', 'data': 'next'}]
    selected_day = int
    text_parts = List[str]
    text_part_num = int
    kb_back_next = kb.make_inline_kb(buttons_data=btn_back_next)
    callback_match_list = list
    today = DailyTasks


@router.message(Command(commands=["start"]))
async def command_start_handler(message: types.Message) -> None:
    messages_list = api.get_messages_by_day(day=0)

    await message.answer(messages_list[0]['content'])
    api.record_sent_message_event(user_id=message.from_user.id, message_id=1, sent_at=datetime.now())
    api.create_user(
        user_id=str(message.from_user.id),
        username=message.from_user.username,
        timezone='UTC')


@router.message(Command(commands=['admindays']))
async def command_day_handler(message: types.Message) -> None:
    await message.answer('Выберите нужный день',
                         reply_markup=kb.make_row_keyboard(
                             items=DataStorage.btn_days_list,
                             row_size=5,
                             one_time_keyboard=True)
                         )


# @router.message(F.text.in_(BTN_DAYS_LIST))
# async def get_days_and_sent_to_chat(message: types.Message):
#     DataStorage.selected_day = int(message.text.removeprefix("Day "))
#
#     # получаем данные от сервера
#     response = api.get_messages_by_day(day=DataStorage.selected_day)
#
#     if response:
#         # превращаем ответ сервера в строку
#         response_string = tls.convert_response_dict_to_string(response)
#
#         # разбиваем строку на элементы определенной длины
#         DataStorage.text_parts = tls.split_text_to_parts(text=response_string, part_length=800)
#
#         # выбираем первый кусок текста и форматируем сообщение для отправки
#         if len(DataStorage.text_parts) == 1:
#             message_text = DataStorage.text_parts[0]
#             await message.answer(message_text)
#         else:
#             DataStorage.text_part_num = 0
#             message_text = DataStorage.text_parts[DataStorage.text_part_num] + f"\n\nСтраница {1} из {len(DataStorage.text_parts)}"
#             await message.answer(message_text, reply_markup=DataStorage.kb_back_next)
#     else:
#         message_text = "Сообщений за этот день не найдено"
#         await message.answer(message_text)


async def split_text_and_get_markup(response: list):
    if response:
        # превращаем ответ сервера в строку
        response_string = tls.convert_response_dict_to_string([response])

        # разбиваем строку на элементы определенной длины
        DataStorage.text_parts = tls.split_text_to_parts(text=response_string, part_length=800)

        # выбираем первый кусок текста и форматируем сообщение для отправки
        if len(DataStorage.text_parts) == 1:
            message_text = DataStorage.text_parts[0]
            return message_text, None
        else:
            DataStorage.text_part_num = 0
            message_text = DataStorage.text_parts[DataStorage.text_part_num] + f"\n\nСтраница {1} из {len(DataStorage.text_parts)}"
            markup = DataStorage.kb_back_next
            return message_text, markup
    else:
        message_text = "Сообщений за этот день не найдено"
        return message_text, None


@router.message(F.text.in_(DataStorage.btn_days_list))
async def get_days_and_sent_to_chat(message: types.Message, state: FSMContext):
    DataStorage.selected_day = int(message.text.removeprefix("Day "))
    today = DailyTasks(day_num=DataStorage.selected_day, user_first_name=message.from_user.first_name)
    DataStorage.callback_match_list = api.get_buttons_callback(DataStorage.selected_day)

    print(DataStorage.__module__, '>',
          DataStorage.__name__, '>',
          DataStorage.__dict__['callback_match_list'], '\n')

    await message.answer(text=today.daily_greeting_template, reply_markup=today.get_daily_keyboard())
    print(today.get_daily_keyboard(), '\n')
    print(F.data.in_(DataStorage.callback_match_list))


@router.callback_query(F.data.in_(DataStorage.callback_match_list))
async def process_message_types_callbacks(callback: types.CallbackQuery):
    message_type, message_num = callback.data.split(":")
    print(DataStorage.selected_day, '\n')
    DataStorage.today = DailyTasks(day_num=DataStorage.selected_day, user_first_name=callback.from_user.first_name)

    if message_type == 'article':
        message_text, markup = await split_text_and_get_markup(DataStorage.today.tasks[int(message_num) - 1])
        await callback.message.answer(text=message_text, reply_markup=markup)
        await callback.answer(show_alert=False)
    elif message_type in ['meditation', 'workout', 'lecture']:
        await callback.message.answer(text=DataStorage.today.tasks[int(message_num) - 1]['content'], reply_markup=None)


@router.callback_query(F.data.in_(['back', 'next']))
async def back_next_callback(callback_query: types.CallbackQuery) -> None:
    print(back_next_callback.__module__, "> Мы внутри функции back_next_callback")
    print('Callback query data:', callback_query.data)

    # counting total text parts
    total_text_parts = len(DataStorage.text_parts)
    print(f'total_text_parts = {total_text_parts}')

    # pagination logic
    if callback_query.data == 'back':
        if DataStorage.text_part_num > 0:
            DataStorage.text_part_num -= 1
        else:
            text_part_num = total_text_parts - 1
    elif callback_query.data == 'next':
        if DataStorage.text_part_num < total_text_parts - 1:
            DataStorage.text_part_num += 1
        elif DataStorage.text_part_num == total_text_parts - 1:
            text_part_num = 0
    print('Expected text part number:', DataStorage.text_part_num)
    # выбираем кусок текста по его номеру в списке и форматируем сообщение для отправки
    print('Selected text part:', DataStorage.text_parts[DataStorage.text_part_num][:300])
    message_text = DataStorage.text_parts[DataStorage.text_part_num] + f"\n\nСтраница {DataStorage.text_part_num + 1} из {total_text_parts}"

    await callback_query.message.edit_text(text=message_text, reply_markup=DataStorage.kb_back_next)
    await callback_query.answer(show_alert=False)
