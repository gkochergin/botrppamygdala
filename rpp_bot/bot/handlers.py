from aiogram import Router, types, F
from aiogram.filters import Command
import rpp_bot.bot.api as api


# назначаем роутер
router = Router()


@router.message(Command(commands=["start"]))
async def command_start_handler(message: types.Message) -> None:
    messages_list = api.get_messages_by_day(day=0)
    await message.answer(f'Hello, <b>{message.from_user.full_name}</b>')
    await message.answer(messages_list[0]['content'])
    api.create_user(user_id=str(message.from_user.id), username=message.from_user.username, reg_date=str(message.date), timezone='UTC')


@router.message(Command(commands=['day']))
async def command_day_handler(message: types.Message) -> None:
    await message.answer('Sent me a day number (f.e. "0"):')

    @router.message(F.text)
    async def get_days_and_sent_to_chat(message: types.Message):
        day_num = int(message.text.strip())
        response = api.get_messages_by_day(day=day_num)
        if response:
            content_list = []
            for dictionary in response:
                concat = 'Message ' + dictionary['ordinal_number'].__str__() + ' > Type: ' + dictionary['content_type'] + '\n<b>Content:</b>\n' + dictionary['content']
                content_list.append(concat)
            result = '\n\n'.join(content_list)
            await message.answer(f"Сообщения выводятся в порядке от первого к последнему:\n\n{result}")
        else:
            await message.answer(f"Сообщений за день <b>{day_num}</b> не найдено.")

