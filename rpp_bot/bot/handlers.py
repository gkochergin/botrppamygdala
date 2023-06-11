from datetime import datetime
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import rpp_bot.bot.api as api
import tools as tls
import keyboards as kb

# назначаем роутер
router = Router()

# global variables
global text_part_num
global text_parts
global active_day


def record_message_event(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            with open('error.log', 'a') as f:
                f.write(f'Error: {e}\n')
            raise

    return wrapper



@router.message(Command(commands=["start"]))
async def command_start_handler(message: types.Message) -> None:
    messages_list = api.get_messages_by_day(day=0)

    await message.answer(messages_list[0]['content'])
    api.record_sent_message_event(user_id=message.from_user.id, message_id=1, sent_at=datetime.now())
    api.create_user(
        user_id=str(message.from_user.id),
        username=message.from_user.username,
        timezone='UTC')

# В БД НЕ СОХРАНЯЮТСЯ СМАЙЛИКИ!!!!!!!!!!!!!!!!!

@router.message(Command(commands=['day']))
async def command_day_handler(message: types.Message) -> None:
    await message.answer('Sent me a day number (f.e. "0"):')

    @router.message(F.text)
    async def get_days_and_sent_to_chat(message: types.Message):
        global active_day
        active_day = int(message.text.strip())
        response = api.get_messages_by_day(day=active_day)
        if response:
            content_list = []
            for dictionary in response:
                concat = 'Message ' + dictionary['ordinal_number'].__str__() + ' > Type: ' + dictionary[
                    'content_type'] + '\n<b>Content:</b>\n' + dictionary['content']
                content_list.append(concat)
            result = '\n\n'.join(content_list)
            await message.answer(f"Сообщения выводятся в порядке от первого к последнему:\n\n{result}")
        else:
            await message.answer(f"Сообщений за день <b>{active_day}</b> не найдено.")


@router.message(Command(commands=['textpages']))
async def command_textpages_handler(message: types.Message) -> None:
    global text_part_num
    global text_parts
    global active_day

    # получаем данные от сервера
    response = api.get_messages_by_day(day=active_day)

    # превращаем ответ сервера в строку
    response_string = tls.convert_response_dict_string(response)

    # разбиваем строку на элементы определенной длины
    text_parts = tls.split_text_by_sentences(text=response_string, max_length=100)

    # выбираем первый кусок текста и форматируем сообщение для отправки
    text_part_num = 0
    message_text = text_parts[0] + f"\n\nСтраница {1} из {len(text_parts)}"

    # отправляем сообщение пользователю с клавиатурой
    await message.answer(message_text, reply_markup=kb.back_next())


@router.callback_query(lambda c: c.data == 'back' or c.data == 'next')
async def back_next_callback(callback_query: types.CallbackQuery) -> None:
    global text_part_num
    global text_parts

    # counting total text parts
    total_text_parts = len(text_parts)

    # pagination logic
    if callback_query.data == 'back':
        if text_part_num > 0:
            text_part_num -= 1
        else:
            text_part_num = total_text_parts - 1
    elif callback_query.data == 'next':
        if text_part_num < total_text_parts - 1:
            text_part_num += 1
        else:
            text_part_num = 0

    # выбираем кусок текста по его номеру в списке и форматируем сообщение для отправки
    message_text = text_parts[text_part_num] + f"\n\nСтраница {text_part_num + 1} из {total_text_parts}"

    await callback_query.message.edit_text(text=message_text, reply_markup=kb.back_next())
    await callback_query.answer(show_alert=False)
