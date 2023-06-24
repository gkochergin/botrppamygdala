#  Copyright (c) 2023. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.

from aiogram import Router, types, html
from aiogram import F
from aiogram.filters import Command

router = Router()

admin_ids = [138405449]


def admin_access(func):
    print(func)
    async def wrapper(message: types.Message):
        user_id = message.from_user.id
        if user_id in admin_ids:
            text = f'Привет, админ! Ты получил доступ к функции {func.__name__} через команду {message.text}'
            print(text)
            await message.answer(text=text)
            return await func(message)
        else:
            text = "Ты не админ, тебе это не надо."
            await message.answer(text=text)
            print("Попытка доступа к административной функции предотвращена.")

    return wrapper


@router.message(Command('secret'))
@admin_access
async def secret_command(message: types.Message):
    await message.answer('Ты похож на админа. Функция секрет сработала.')


@router.message(Command(commands=['alluserdata']))
@admin_access
async def do_echo(message: types.Message):
    chatid = f'Чат id: {message.chat.id}'
    userid = f'Твой user id: {message.from_user.id}'
    userlang = f'Код языка: {message.from_user.language_code}'
    username = f'Пользователь: {message.from_user.username}'
    firstname = f'Имя: {message.from_user.first_name}'
    lastname = f'Фамилия: {message.from_user.last_name}'
    # userdata = {'chatid': chatid, 'userid': userid, 'userlang': userlang, 'username': username, 'firstname': firstname, 'lastname': lastname}
    userdata = (chatid, userid, userlang, username, firstname, lastname)
    text = ''
    for d in userdata:
        text += d + '\n'
    await message.answer(text)


@router.message(Command('myid'))

async def get_user_id(message: types.Message):
    user_id = message.from_user.id
    await message.answer(f'Твой id:\n{user_id}')


@router.message(Command('chatid'))
async def get_user_id(message: types.Message):
    chat_id = message.chat.id
    await message.answer(f'id этого чата:\n{chat_id}')


# утилита получения id файла, отправить боту файл, он вернет его данные
@router.message(Command('photoid'))
@admin_access
async def get_photo_id(message: types.Message):
    await message.answer('Окей, присылай фото, найду его id:')

    @router.message(F.photo)
    @admin_access
    async def message_with_text(message: types.Message):
        await message.answer("Собираю данные об изображении:")
        photoid = message.photo[-1].file_id  # -1 это самый большой файл из сета файлов
        photouniqeuid = message.photo[-1].file_unique_id
        await message.reply(f"file_id:\n{photoid}")
        await message.reply(f"file_unique_id:\n{photouniqeuid}")
