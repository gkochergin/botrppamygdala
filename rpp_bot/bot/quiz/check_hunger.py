import logging as log
from datetime import datetime
from aiogram import Router, types
from aiogram.filters import Command

import rpp_bot.bot.api as api
from rpp_bot.bot import keyboards as kb

router = Router()


class QuizSession:
    questions = api.get_quiz_question_list()
    question_count = len(questions)

    def __init__(self, user_id, score: int, question_number: int):
        self.user_id = user_id
        self.date_time = datetime.now()
        self.question_number = question_number
        self.score = score
        self.__field_name = 'question'
        self.finished = False



USER_SESSION: QuizSession


@router.message(Command(commands='myhunger'))
async def start_quiz(message: types.Message):
    global USER_SESSION

    # инициализируем данные сессии
    USER_SESSION = QuizSession(user_id=str(message.from_user.id), question_number=0, score=0)

    # Сообщаем пользователю, что тест начат
    await message.answer("<b>Тест на наличие проблем с пищевым поведением</b>")
    await quiz_show_question(message=message, increase=1)


async def quiz_show_question(message: types.Message, increase: int):
    global USER_SESSION
    question_text = USER_SESSION.get_question(increase=increase)
    message_text = f"<b>Вопрос {USER_SESSION.question_number} из {USER_SESSION.question_count}</b>\n\n{question_text}"
    if USER_SESSION.question_number > 1:
        await message.edit_text(text=message_text, reply_markup=kb.yes_no().as_markup())
    else:
        await message.answer(text=message_text, reply_markup=kb.yes_no().as_markup())


@router.callback_query(lambda c: c.data.startswith('yes') or c.data.startswith('no'))
async def process_callback(callback_query: types.CallbackQuery):
    global USER_SESSION

    if not USER_SESSION.finished:
        if callback_query.data == "yes":
            USER_SESSION.add_one_to_score()
        elif callback_query.data == "no":
            pass

    if USER_SESSION.get_question(increase=0) and not USER_SESSION.finished:
        await quiz_show_question(message=callback_query.message, increase=1)
        await callback_query.answer(show_alert=False)
    else:
        if USER_SESSION.score <= 2:
            result_text = "Наличие одного и более пункта говорит о проблемах пищевого поведения."
        else:
            result_text = "Рекомендуется обратиться к специалисту за помощью. Ты всегда можешь обратится к создателям " \
                          "фуд-бота за консультацией или воспользоваться возможностью поговорить с online " \
                          "консультантом."
        if not USER_SESSION.finished:
            await callback_query.message.answer(f"Давай разберём твой результат. "
                                                f"Это был список Признаков нарушенного пищевого поведения. "
                                                f"Ты ответила \"Да\": {USER_SESSION.score}\n\n{result_text}")
        USER_SESSION.save_quiz_result()
        USER_SESSION.finished = True
    await callback_query.answer(show_alert=False)
