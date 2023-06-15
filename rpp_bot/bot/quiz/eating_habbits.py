import logging as log
from datetime import datetime
from aiogram import Router, types, F
from aiogram.filters import Command

import rpp_bot.bot.api as api

from rpp_bot.bot import keyboards as kb

router = Router()


class QuizSession:
    questions = api.get_quiz_question_list()
    question_count = len(questions)
    quiz_name = "<b>Тест на наличие проблем с пищевым поведением</b>"
    result_ok = "Наличие одного и более пункта говорит о проблемах пищевого поведения."
    result_bad = "Рекомендуется обратиться к специалисту за помощью. Ты всегда можешь обратится к создателям фуд-бота" \
                 " за консультацией или воспользоваться возможностью поговорить с online консультантом."

    def __init__(self, user_id, score: int, question_number: int):
        self.user_id = user_id
        self.date_time = datetime.now()
        self.question_number = question_number
        self.score = score
        self.__field_name = 'question'
        self.finished = False
        self.result_analyze = f"Это был список <b>Признаков нарушенного пищевого поведения</b>. Давай разберём твой " \
                              f"результат. Ты ответила \"Да\":"

    def add_one_to_score(self) -> None:
        self.score += 1

    def save_quiz_result(self) -> None:
        # через api создаем в бд объект с результатом прохождения теста
        try:
            api.save_quiz_result(user_id=self.user_id, result=self.score)
        except Exception as e:
            log.error(e)
            print(e)

    def get_question(self, increase: int) -> str:
        if self.question_number <= self.question_count - 1:
            question = self.questions[self.question_number][self.__field_name]
            self.question_number += increase
            return question


USER_SESSION: QuizSession
YES_NO_KB = kb.make_inline_kb_with_two_buttons(btn1_text="Да", btn2_text="Нет", btn1_data="yes", btn2_data="no")


@router.message(Command(commands='myhabbits'))
async def start_quiz(message: types.Message):
    global USER_SESSION

    # инициализируем данные сессии
    USER_SESSION = QuizSession(user_id=str(message.from_user.id), question_number=0, score=0)

    # Сообщаем пользователю, что тест начат
    await message.answer(USER_SESSION.quiz_name)
    await quiz_show_question(message=message, increase=1)


async def quiz_show_question(message: types.Message, increase: int):
    global USER_SESSION
    question_text = USER_SESSION.get_question(increase=increase)
    message_text = f"<b>Вопрос {USER_SESSION.question_number} из {USER_SESSION.question_count}</b>\n\n{question_text}"
    if USER_SESSION.question_number > 1:
        await message.edit_text(text=message_text, reply_markup=YES_NO_KB)
    else:
        await message.answer(text=message_text, reply_markup=YES_NO_KB)


@router.callback_query(F.data.in_(['yes', 'no']))
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
            result_text = USER_SESSION.result_ok
        else:
            result_text = USER_SESSION.result_bad
        if not USER_SESSION.finished:
            await callback_query.message.answer(f"{USER_SESSION.result_analyze} <b>{USER_SESSION.score}</b>\n\n{result_text}")
        USER_SESSION.save_quiz_result()
        USER_SESSION.finished = True
    await callback_query.answer(show_alert=False)
