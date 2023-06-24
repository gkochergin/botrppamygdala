import logging
from aiogram import Router, types, F
from aiogram.filters import Command
from .handlers_days import DataStorage
from ..admin_utilities import admin_access
from ..keyboards import make_row_keyboard

router = Router()

data_storage = DataStorage()


@router.message(Command(commands=['admindays']))
@admin_access
async def command_day_handler(message: types.Message, ds=data_storage) -> None:
    await message.answer('Выберите нужный день',
                         reply_markup=make_row_keyboard(
                             items=ds.btn_days_list,
                             row_size=5,
                             one_time_keyboard=True)
                         )
