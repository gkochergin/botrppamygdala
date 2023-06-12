from datetime import datetime
from aiogram import Router, types, F
from aiogram.filters import Command
import rpp_bot.bot.api as api
import tools as tls
import keyboards as kb

# назначаем роутер
router = Router()

# global variables
global text_parts

BTN_DAYS_LIST = [f'Day {i}' for i in range(0, 13)]


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


@router.message(Command(commands=['admindays']))
async def command_day_handler(message: types.Message) -> None:
    print(BTN_DAYS_LIST)
    await message.answer('Выберите нужный день',
                         reply_markup=kb.make_row_keyboard(
                             BTN_DAYS_LIST,
                             row_size=5,
                             one_time_keyboard=True)
                         )


@router.message(F.text.in_(BTN_DAYS_LIST))
async def get_days_and_sent_to_chat(message: types.Message):
    global text_parts

    selected_day = int(message.text.removeprefix("Day "))

    # получаем данные от сервера
    response = api.get_messages_by_day(day=selected_day)

    # превращаем ответ сервера в строку
    response_string = tls.convert_response_dict_to_string(response)

    # разбиваем строку на элементы определенной длины
    text_parts = tls.split_text_to_parts(text=response_string, part_length=800)

    # выбираем первый кусок текста и форматируем сообщение для отправки
    if len(text_parts) == 1:
        message_text = text_parts[0]
    else:
        message_text = text_parts[0] + f"\n\nСтраница {1} из {len(text_parts)}"

    # отправляем сообщение пользователю с клавиатурой
    await message.answer(message_text, reply_markup=kb.back_next())


@router.callback_query(F.data.in_(['back', 'next']))
async def back_next_callback(callback_query: types.CallbackQuery) -> None:
    global text_parts
    text_part_num = 0
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
