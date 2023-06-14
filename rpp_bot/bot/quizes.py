from datetime import datetime
from aiogram import Router, types, F
from aiogram.filters import Command

import rpp_bot.bot.api as api
import keyboards as kb
from dataclasses import dataclass

router = Router()
global USER_SESSION


class QuizSession:
    questions = api.get_quiz_question_list()
    question_count = len(questions)

    def __init__(self, user_id, score, question_number):
        self.user_id = user_id
        self.date_time = datetime.now()
        self.question_number = question_number
        self.score = score
        self.__field_name = 'question'

    def add_one_to_score(self) -> None:
        self.score += 1

    def save_quiz_result(self) -> None:
        # через api создаем в бд объект с результатом прохождения теста
        try:
            api.save_quiz_result(user_id=self.user_id, result=QuizSession.score)
        except Exception as e:
            print(e)
        return e or None

    def get_question(self) -> str:
        if self.question_number <= QuizSession.question_count -1:
            question = QuizSession.questions[self.question_number][self.__field_name]
            self.question_number += 1
            return question
        elif self.question_number > QuizSession.question_count:
            pass


# def get_question(session: QuizSession):
#     print('session.question_number:', session.question_number)
#     print('session.question_count:', session.question_count)
#     if session.question_number <= session.question_count - 1:
#         question = session.questions[session.question_number]['question']
#         session.question_number += 1
#         return question
#     elif session.question_number > session.question_count:
#         return None


@router.message(Command(commands='startquiz'))
async def start_quiz(message: types.Message):
    global USER_SESSION

    # инициализируем данные сессии
    USER_SESSION = QuizSession(user_id=str(message.from_user.id), question_number=0, score=0)

    # Сообщаем пользователю, что тест начат
    await message.answer("<b>Тест на наличие проблем с пищевым поведением</b>")
    await quiz_show_question(session=USER_SESSION, message=message)


async def quiz_show_question(session: QuizSession, message: types.Message):
    question_text = session.get_question()
    message_text = f"Вопрос {session.question_number} из {session.question_count}\n\n{question_text}"
    await message.answer(text=message_text, reply_markup=kb.yes_no().as_markup())
    return session.question_number


@router.callback_query(lambda c: c.data.startswith('yes') or c.data.startswith('no'))
async def process_callback(callback_query: types.CallbackQuery):
    global USER_SESSION

    if callback_query.data == "yes":
        USER_SESSION.add_one_to_score()
    elif callback_query.data == "no":
        pass

    if USER_SESSION.get_question():
        await quiz_show_question(session=USER_SESSION, message=callback_query.message)
    else:
        if USER_SESSION.score <= 2:
            result_text = "Результат ваших ответов:\nУ вас всё хорошо."
        else:
            result_text = "Результат ваших ответов:\nВсё плохо, надо лечиться. Обратитесь к специалисту."

        await callback_query.message.answer(f"Кол-во 'ДА' ответов: {USER_SESSION.score}.\n\n{result_text}")
