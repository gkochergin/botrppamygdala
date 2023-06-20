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
    text_parts_list = List[str]
    text_part_num = int
    kb_back_next = kb.make_inline_kb(buttons_data=btn_back_next)
    callback_match_list = list
    today = DailyTasks

    def get_callback_match_list(self):
        self.callback_match_list = api.get_buttons_callback(day=self.selected_day)
        return self.callback_match_list

    def get_parts_count(self):
        self.text_parts_count = len(self.text_parts_list)
        return self.text_parts_count


# объявляем экземпляр класса DataStorage для последующего использования в функциях
data_storage = DataStorage()


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
async def command_day_handler(message: types.Message, ds=data_storage) -> None:
    await message.answer('Выберите нужный день',
                         reply_markup=kb.make_row_keyboard(
                             items=ds.btn_days_list,
                             row_size=5,
                             one_time_keyboard=True)
                         )


async def split_text_and_get_markup(response: list, ds=data_storage):
    if response:
        # превращаем ответ сервера в строку
        response_string = tls.convert_response_dict_to_string([response])

        # разбиваем строку на элементы определенной длины
        ds.text_parts_list = tls.split_text_to_parts(text=response_string, part_length=800)

        # выбираем первый кусок текста и форматируем сообщение для отправки
        if len(ds.text_parts_list) == 1:
            message_text = ds.text_parts_list[0]
            return message_text, None
        else:
            ds.text_part_num = 0
            message_text = ds.text_parts_list[
                               ds.text_part_num] + f"\n\nСтраница {1} из {len(ds.text_parts_list)}"
            markup = ds.kb_back_next
            return message_text, markup
    else:
        message_text = "Сообщений за этот день не найдено"
        return message_text, None


@router.message(F.text.in_(data_storage.btn_days_list))
async def get_days_and_sent_to_chat(message: types.Message, ds=data_storage):
    ds.selected_day = int(message.text.removeprefix("Day "))
    ds.callback_match_list = api.get_buttons_callback(ds.selected_day)

    today_tasks = DailyTasks(day_num=ds.selected_day, user_first_name=message.from_user.first_name)

    await message.answer(text=today_tasks.daily_greeting_template, reply_markup=today_tasks.get_daily_keyboard())

    @router.callback_query(F.data.in_(data_storage.callback_match_list))
    async def process_message_types_callbacks(callback: types.CallbackQuery, ds=data_storage):
        message_type, message_num = callback.data.split(":")
        ds.today = DailyTasks(day_num=ds.selected_day, user_first_name=callback.from_user.first_name)

        if message_type == 'article':
            message_text, markup = await split_text_and_get_markup(ds.today.tasks[int(message_num) - 1])
            await callback.message.answer(text=message_text, reply_markup=markup)
            await callback.answer(show_alert=False)
        elif message_type in ['meditation', 'workout', 'lecture']:
            await callback.message.answer(text=ds.today.tasks[int(message_num) - 1]['content'],
                                          reply_markup=None)


@router.callback_query(F.data.in_(['back', 'next']))
async def back_next_callback(callback_query: types.CallbackQuery, ds=data_storage) -> None:
    # counting total text parts
    total_text_parts = len(ds.text_parts_list)

    # pagination logic
    if callback_query.data == 'back':
        if ds.text_part_num > 0:
            ds.text_part_num -= 1
        else:
            text_part_num = total_text_parts - 1
    elif callback_query.data == 'next':
        if ds.text_part_num < total_text_parts - 1:
            ds.text_part_num += 1
        elif ds.text_part_num == total_text_parts - 1:
            text_part_num = 0
    print('Expected text part number:', ds.text_part_num)
    # выбираем кусок текста по его номеру в списке и форматируем сообщение для отправки
    print('Selected text part:', ds.text_parts_list[ds.text_part_num][:300])
    message_text = ds.text_parts_list[
                       ds.text_part_num] + f"\n\nСтраница {ds.text_part_num + 1} из {total_text_parts}"

    await callback_query.message.edit_text(text=message_text, reply_markup=ds.kb_back_next)
    await callback_query.answer(show_alert=False)
