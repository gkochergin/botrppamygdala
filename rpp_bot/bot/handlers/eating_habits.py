import logging as log
from datetime import datetime
from aiogram import Router, types, F
from aiogram.filters import Command

from rpp_bot.bot.api import api
from rpp_bot.bot.admin_utils import tools as tls
from rpp_bot.bot.keyboards import keyboards as kb


router = Router()


# ------------------------------ QUIZ EATING HABITS HANDLERS ------------------------------ #

class QuizSession:
    """
    A class representing a quiz session for a user.

    :param user_id: The Telegram ID of the user taking the quiz.
    :param score: The current quiz score of the user.
    :param question_number: The current question number.
    """
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
                              f"результат: ты ответила \"Да\""

    def add_one_to_score(self) -> None:
        """
        Increment the user's score by one.
        """
        self.score += 1

    def save_quiz_result(self) -> None:
        """
        Save the user's quiz result using the API.
        """
        # через api создаем в бд объект с результатом прохождения теста
        try:
            api.save_quiz_result(user_id=self.user_id, result=self.score)
        except Exception as e:
            log.error(e)
            print(e)

    def get_question(self, increase: int) -> str:
        """
        Get the current question and increment the question number.

        :param increase: The amount to increment the question number by.
        :return: The current question text.
        """
        if self.question_number <= self.question_count - 1:
            question = self.questions[self.question_number][self.__field_name]
            self.question_number += increase
            return question

    def keyboard(self):
        """
        Create an inline keyboard markup for the quiz.

        :return: An InlineKeyboardMarkup object representing the constructed inline keyboard markup.
        """
        btns = [{'name': 'Да', 'data': 'yes'}, {'name': 'Нет', 'data': 'no'}]
        markup = kb.make_inline_kb(buttons_data=btns)
        return markup


USER_SESSION: QuizSession


@router.message(Command(commands='myhabits'))
async def start_quiz(message: types.Message):
    """
    Start a quiz session for the user.

    :param message: The message object representing the user's message.
    """
    global USER_SESSION
    log_text = f'User {message.from_user.id} > started EATING HABITS quiz.'

    # Initialize the user's quiz session
    USER_SESSION = QuizSession(user_id=str(message.from_user.id), question_number=0, score=0)

    # Notify the user that the quiz has started
    await message.answer(USER_SESSION.quiz_name)

    # Show the first question
    await quiz_show_question(message=message, increase=1)


async def quiz_show_question(message: types.Message, increase: int):
    """
    Show the current quiz question to the user.

    :param message: The message object representing the user's message.
    :param increase: The amount to increment the question number by.
    """
    global USER_SESSION
    # Get the current question text
    question_text = USER_SESSION.get_question(increase=increase)

    # Format the message text
    message_text = f"<b>Вопрос {USER_SESSION.question_number} из {USER_SESSION.question_count}</b>\n\n{question_text}"

    # Edit or send the message
    if USER_SESSION.question_number > 1:
        await message.edit_text(text=message_text, reply_markup=USER_SESSION.keyboard())
    else:
        await message.answer(text=message_text, reply_markup=USER_SESSION.keyboard())


@router.callback_query(F.data.in_(['yes', 'no']))
async def process_callback(callback_query: types.CallbackQuery):
    """
    Process a callback query from an inline keyboard button.

    :param callback_query: The callback query object representing the user's interaction with the inline keyboard.
    """
    global USER_SESSION

    # Check if the quiz is not finished
    if not USER_SESSION.finished:
        # Update the user's score based on their answer
        if callback_query.data == "yes":
            USER_SESSION.add_one_to_score()
        elif callback_query.data == "no":
            pass

    # Check if there is a next question
    if USER_SESSION.get_question(increase=0) and not USER_SESSION.finished:
        # Show the next question
        await quiz_show_question(message=callback_query.message, increase=1)
        await callback_query.answer(show_alert=False)
    else:
        # Determine the result text based on the user's score
        if USER_SESSION.score <= 2:
            result_text = USER_SESSION.result_ok
        else:
            result_text = USER_SESSION.result_bad

        # Send the result message if the quiz is not finished
        if not USER_SESSION.finished:
            await callback_query.message.answer(
                f"{USER_SESSION.result_analyze} <b>{USER_SESSION.score}</b> "
                f"{tls.matching_word_numeral(wrd='раз', dgt=USER_SESSION.score)}.\n\n"
                f"{result_text}")

        # Save the user's quiz result and mark the quiz as finished
        USER_SESSION.save_quiz_result()
        USER_SESSION.finished = True

    await callback_query.answer(show_alert=False)
