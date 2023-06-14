import logging as log
from aiogram import Router, types, F
from aiogram.filters import Command

from rpp_bot.bot import keyboards as kb
from dataclasses import dataclass

router = Router()


@dataclass
class MyHunger:
    base_question = "Где ты чувствуешь голод?"
    head_name = "Голова"
    stomach_name = "Живот"
    head_data = "head"
    stomach_data = "stomach"
    head_result = "ЛЕЧИТЬСЯ!"
    stomach_result = "ЖРАТЬ!"

    def keyboard(self):
        return kb.inline_two_buttons(
            btn1_text=self.head_name,
            btn2_text=self.stomach_name,
            btn1_data=self.head_data, btn2_data=self.stomach_data
        )


@router.message(Command(commands='myhunger'))
async def start_hunger_test(message: types.Message):
    mhs = MyHunger()
    # Сообщаем пользователю, что тест начат
    await message.answer(
        text=f"<b>Тест на голод</b>\n\n{mhs.base_question}",
        reply_markup=mhs.keyboard())


@router.callback_query(F.text.in__([MyHunger.head_data, MyHunger.stomach_data]))
async def process_callback(callback: types.CallbackQuery):
    if callback.data == MyHunger.head_data:
        await callback.message.answer(MyHunger.head_result)
    elif callback.data == MyHunger.stomach_data:
        await callback.message.answer(MyHunger.stomach_result)
    await callback.answer(show_alert=False)
