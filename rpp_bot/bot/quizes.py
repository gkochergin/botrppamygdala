from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

import rpp_bot.bot.api as api
import tools as tls
import keyboards as kb

router = Router()


@router.message(Command(commands='startquiz'))
async def start_quiz(message: types.Message):
    user_id = str(message.from_user.id)
    await message.answer("Тест начат!")
    await quiz_show_question(user_id=user_id, question_number=0, score=0, message=message)


async def quiz_show_question(user_id: str, question_number: int, score: int, message: types.Message):
    questions_list = api.get_quiz_question_list()
    questions_count = len(questions_list)
    if question_number < questions_count:
        question_text = api.get_quiz_question_list()[question_number]['question']
        message_text = f"Вопрос {question_number + 1} из {questions_count}\n\n{question_text}"

        # создаем специальную клавиатуру с подсчетом очков и номера вопроса
        yes_btn_data = f"yes,{question_number + 1},{score + 1}"
        no_bt_data = f"no,{question_number + 1},{score}"
        buttons_list = [
            [InlineKeyboardButton(text="Да", callback_data=yes_btn_data),
             InlineKeyboardButton(text="Нет", callback_data=no_bt_data)]
        ]

        kb = InlineKeyboardBuilder(markup=buttons_list)

        await message.answer(text=message_text, reply_markup=kb.as_markup())
    elif question_number == questions_count:
        if score <= 2:
            result_text = "Результат ваших ответов:\nУ вас всё хорошо."
        else:
            result_text = "Результат ваших ответов:\nВсё плохо, надо лечиться. Обратитесь к специалисту."
        # через api создаем в бд объект с результатом прохождения теста
        api.save_quiz_result(user_id=user_id, result=score)
        # сообщаем пользователю результат
        await message.answer(f"Кол-во 'ДА' ответов: {score}.\n\n{result_text}")



@router.callback_query(lambda c: c.data.startswith('yes') or c.data.startswith('no'))
async def process_callback(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    questions_list = api.get_quiz_question_list()
    questions_count = len(questions_list)
    _, question_number, score = map(str, callback_query.data.split(','))

    if int(question_number) <= questions_count:
        await quiz_show_question(user_id=user_id, question_number=int(question_number),
                                 score=int(score), message=callback_query.message)
        await callback_query.answer(show_alert=False)

