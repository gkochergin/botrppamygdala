from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

import rpp_bot.bot.api as api
import tools as tls
import keyboards as kb

router = Router()


@router.message(Command(commands='startquiz'))
async def start_quiz(message: types.Message):
    user_id = message.from_user.id
    await message.answer("Тест начат!")
    await quiz_show_question(user_id=user_id, question_number=0, score=0)


async def quiz_show_question(user_id: int, question_number: int, score: int):
    message = types.Message
    total_questions = len(api.get_quiz_question_list())
    print(total_questions)
    if question_number < total_questions:
        # получаем вопрос по номеру из бд через api
        # Question.objects.values_list('text', flat=True)[question_number]
        question_text = api.get_quiz_question_list()[question_number]

        message_text = f"Вопрос {question_number + 1} из {total_questions}\n\n{question_text}"

        # создаем специальную клавиатуру
        yes_btn_data = f"yes,{question_number + 1},{score + 1}"
        no_bt_data = f"no,{question_number + 1},{score}"
        buttons_list = [
            [InlineKeyboardButton(text="Да", callback_data=yes_btn_data),
             InlineKeyboardButton(text="Нет", callback_data=no_bt_data)]
        ]

        kb = InlineKeyboardBuilder(markup=buttons_list)

        await message.answer(text=message_text, reply_markup=kb.as_markup())
    else:
        if score <= 2:
            result_text = "Результат ваших ответов:\nУ вас всё хорошо."
        else:
            result_text = "Результат ваших ответов:\nВсё плохо, надо лечиться. Обратитесь к специалисту."
        # через api создаем в бд объект с результатом прохождения теста
        # TestResult.objects.create(user_id=user_id, result=score)

        await message.answer(f"Вы набрали {score} очков.\n\n{result_text}")


@router.callback_query(lambda c: c.data.startswith('yes') or c.data.startswith('no'))
async def process_callback(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    _, question_number, score = map(int, callback_query.data.split(','))
    await quiz_show_question(user_id, question_number, score)
