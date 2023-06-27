from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from rpp_bot.bot.keyboards import make_inline_kb
import emoji

router = Router()

btns_data = [
    {'name': emoji.emojize(string=":hamburger:"), 'data': 'bakery'},
    {'name': emoji.emojize(string=":cut_of_meat:"), 'data': 'meat'},
    {'name': emoji.emojize(string=":ear_of_corn:"), 'data': 'vegetables'},
    {'name': emoji.emojize(string=":shrimp:"), 'data': 'sea'},
]




@router.message(Command(commands='harvard'))
async def harvard_command_process(message: Message):
    emoji_keyboard = make_inline_kb(buttons_data=btns_data)
    await message.answer(text="Что жрали-с господа?", reply_markup=emoji_keyboard)
