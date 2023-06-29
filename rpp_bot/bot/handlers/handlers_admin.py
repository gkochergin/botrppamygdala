import logging
from aiogram import Router, types
from aiogram.filters import Command
from .handlers_days import DataStorage
from rpp_bot.bot.admin_utils.admin_utilities import admin_access
from ..keyboards import make_row_keyboard

router = Router()

data_storage = DataStorage()


@router.message(Command(commands=['admindays']))
@admin_access
async def command_day_handler(message: types.Message, ds=data_storage) -> None:
    log_text = f'User id {message.from_user.id} called {command_day_handler.__name__} function under the admin rights. '
    logging.info(log_text)
    await message.answer('Выберите нужный день',
                         reply_markup=make_row_keyboard(
                             items=ds.btn_days_list,
                             row_size=5,
                             one_time_keyboard=True)
                         )
