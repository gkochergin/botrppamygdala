import dataclasses
from typing import List
from datetime import datetime
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from rpp_bot.bot.keyboards import make_inline_kb
import emoji

router = Router()


@dataclasses.dataclass
class MealDayData:
    datetime = datetime.now()
    meal_type = {'main_meal': 'Основной приём', 'snack': 'Перекус', 'end_date': 'Завершить день'}
    messages = {
        'choose_type': 'Выберите тип приёма пищи, который вы хотите записать:',
        'main_meal': 'Вы выбрали <b>основной приём пищи</b>. Отметьте всё, что вы ели по категориям ниже.',
        'snack': 'Вы выбрали основной <b>перекус</b>. Отметьте всё, что вы ели по категориям ниже.',
        'end_date_approval': 'Вы уверены, что хотите завершить день? После этого вы не сможете больше добавить приемы пищи.',
        'end_date_saved': 'Окей, все приемы пищи (основные и перекусы) записаны. Вот ваша статистка.',
        'end_date_cancel': 'Окей, ничего не делаем.',
        'end_date_true': 'Вы завершили свой день и не можете ничего записать. До следующего дня!'
    }
    kb_meal_types_data = [
        {'name': meal_type['main_meal'], 'data': 'main_meal'},
        {'name': meal_type['snack'], 'data': 'snack'},
        {'name': meal_type['end_date'], 'data': 'end_date'}]
    kb_end_date_data = [
        {'name': 'Завершить', 'data': 'end_true'},
        {'name': 'Отменить', 'data': 'end_false'}
    ]
    cb_list_meal_type = list(meal_type.keys())
    cb_list_end_date = [data['data'] for data in kb_end_date_data]
    kb_meal_types = make_inline_kb(buttons_data=kb_meal_types_data, sizes=[1])
    kb_end_date = make_inline_kb(buttons_data=kb_end_date_data, sizes=[2])
    total_meals_count = 0
    end_date_status: bool = False


@dataclasses.dataclass
class MealNowData:
    message_text = "Что жрали-с господа?"
    kb_products_data = [
        {'name': f'{emoji.emojize(string=":hamburger:")} Булочко', 'data': 'bakery'},
        {'name': f'{emoji.emojize(string=":cut_of_meat:")} Мяско', 'data': 'meat'},
        {'name': f'{emoji.emojize(string=":ear_of_corn:")} Кукурзко', 'data': 'vegetables'},
        {'name': f'{emoji.emojize(string=":shrimp:")} Креветко', 'data': 'sea'},
        {'name': f'{emoji.emojize(string=":chocolate_bar:")} Шоколадко', 'data': 'chocolate'},
        {'name': f'{emoji.emojize(string=":floppy_disk:")} Сохранить данные', 'data': 'save_meal_data'}
    ]
    cb_list_products = [data['data'] for data in kb_products_data]
    kb_products = make_inline_kb(buttons_data=kb_products_data, sizes=[2])
    removed_buttons_list = []


meal_day = MealDayData()
meal_now = MealNowData()


def filter_buttons(buttons_list: List[dict], button_to_remove: str):
    temp = [button for button in buttons_list if button['data'] == button_to_remove]

    if meal_now.removed_buttons_list:
        if temp not in meal_now.removed_buttons_list:
            meal_now.removed_buttons_list.append(temp[0])
    else:
        meal_now.removed_buttons_list.append(temp[0])

    new_buttons_data = [button for button in buttons_list
                        if button not in meal_now.removed_buttons_list]

    return new_buttons_data


@router.message(Command(commands='harvard'))
async def harvard_command_process(message: Message):
    if not meal_day.end_date_status:
        await message.answer(
            text=meal_day.messages['choose_type'],
            reply_markup=meal_day.kb_meal_types
        )
    else:
        await message.answer(text=meal_day.messages['end_date_true'])
    # TODO: а что будет в случае, если сегодня я записал всё, а завтра обновится ли параметр end_date_status на False?
    # TODO: возможно надо каждый день в полночь пробегаться по пользователям и менять им статус, либо есть другое решение, хз какое



@router.callback_query(F.data.in_(meal_day.cb_list_meal_type))
async def meal_day_callbacks_process(callback: CallbackQuery):
    if callback.data == meal_day.cb_list_meal_type[0]:
        await callback.message.edit_text(
            text=meal_day.messages['main_meal'],
            reply_markup=meal_now.kb_products
        )
    elif callback.data == meal_day.cb_list_meal_type[1]:
        await callback.message.edit_text(
            text=meal_day.messages['snack'],
            reply_markup=meal_now.kb_products
        )
    elif callback.data == meal_day.cb_list_meal_type[2]:
        await callback.message.edit_text(
            text=meal_day.messages['end_date_approval'],
            reply_markup=meal_day.kb_end_date
        )
    await callback.answer(show_alert=False)

    @router.callback_query(F.data.in_(meal_day.cb_list_end_date))
    async def end_day_callback_process(callback: CallbackQuery):
        if callback.data == 'end_true':
            # TODO: по факту данные сохраняются при каждом создании приема пищи, устанавливаем end_date_status True
            meal_day.end_date_status = True
            await callback.message.edit_text(text=meal_day.messages['end_date_saved'], reply_markup=None)
        else:
            await callback.message.edit_text(text=meal_day.messages['end_date_cancel'], reply_markup=None)


@router.callback_query(F.data.in_(meal_now.cb_list_products))
async def meal_now_callbacks_process(callback: CallbackQuery):
    filtered_data = filter_buttons(
        buttons_list=meal_now.kb_products_data,
        button_to_remove=str(callback.data)
    )
    filtered_keyboard = make_inline_kb(buttons_data=filtered_data, sizes=[2])

    if callback.data == 'save_meal_data':
        await callback.message.edit_text("Ю-ху! Всё сохранилось!", reply_markup=None)
        meal_now.removed_buttons_list = []
    else:
        await callback.message.edit_text(
            text=f"Прекрасно! Очень важно кушать <b>{callback.data}</b>",
            reply_markup=filtered_keyboard
        )
    await callback.answer(show_alert=False)
