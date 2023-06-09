from aiogram import Router, types
from aiogram.filters import Command
import rpp_bot.bot.api as api

# назначаем роутер
router = Router()


@router.message(Command(commands=["start"]))
async def command_start_handler(message: types.Message) -> None:
    await message.answer(f'Hello, <b>{message.from_user.full_name}</b>')
    api.create_user(user_id=str(message.from_user.id), username=message.from_user.username, reg_date=str(message.date), timezone='UTC')


@router.message()
async def echo_handler(message: types.Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nic try!")
