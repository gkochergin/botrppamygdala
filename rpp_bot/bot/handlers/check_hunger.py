import logging
from dataclasses import dataclass
from aiogram import Router, types, F
from aiogram.filters import Command
from .. import keyboards as kb

router = Router()

# ------------------------------ QUIZ CHECK HUNGER HANDLERS ------------------------------ #

@dataclass
class MyHunger:
    name = "<b>Тест на голод</b>"
    base_question = "Где ты чувствуешь голод?"
    head_name = "Голова"
    stomach_name = "Живот"
    head_data = "head"
    stomach_data = "stomach"
    head_result = "ЛЕЧИТЬСЯ!"
    stomach_result = "ЖРАТЬ!"

    def keyboard(self):
        btns = [{'name': self.head_name, 'data': self.head_data},
                {'name': self.stomach_name, 'data': self.stomach_data}]
        return kb.make_inline_kb(buttons_data=btns)

@router.message(Command(commands='myhunger'))
async def start_hunger_test(message: types.Message):
    log_text = f'User {message.from_user.id} > started CHECK HUNGER quiz.'
    logging.info(msg=log_text)
    mhs = MyHunger()
    # Сообщаем пользователю, что тест начат
    await message.answer(
        text=f"{mhs.name}\n\n{mhs.base_question}",
        reply_markup=mhs.keyboard())


@router.callback_query(F.data.in_([MyHunger.head_data, MyHunger.stomach_data]))
async def process_callback(callback: types.CallbackQuery):
    if callback.data == MyHunger.head_data:
        await callback.message.edit_text(
            text=f"{MyHunger.name}\n\n{MyHunger.head_result}",
            reply_markup=None)
    elif callback.data == MyHunger.stomach_data:
        await callback.message.edit_text(
            text=f"{MyHunger.name}\n\n{MyHunger.stomach_result}",
            reply_markup=None)
    await callback.answer(show_alert=False)
    log_text = f'User {callback.from_user.id} > finished CHECK HUNGER quiz.'
    logging.info(msg=log_text)
