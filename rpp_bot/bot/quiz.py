Да, конечно! Вот пример кода, который реализует предложенную мной логику для обработки квиза и ответов пользователя:

```python
from django.db import models

class QuizSession(models.Model):
    user_id = models.BigIntegerField()
    question_number = models.IntegerField()
    score = models.IntegerField()

class QuizResults(models.Model):
    user_id = models.BigIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    result = models.IntegerField()

@router.message(Command(commands='startquiz'))
async def start_quiz(message: types.Message):
    user_id = message.from_user.id
    # Создаем новый объект QuizSession для текущей сессии квиза
    QuizSession.objects.create(user_id=user_id, question_number=0, score=0)
    await message.answer("Тест начат!")
    await quiz_show_question(user_id=user_id, message=message)

async def quiz_show_question(user_id: int, message: types.Message):
    # Получаем текущую сессию квиза из базы данных
    quiz_session = QuizSession.objects.get(user_id=user_id)
    question_number = quiz_session.question_number
    score = quiz_session.score

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
    else:
        if score <= 2:
            result_text = "Результат ваших ответов:\nУ вас всё хорошо."
        else:
            result_text = "Результат ваших ответов:\nВсё плохо, надо лечиться. Обратитесь к специалисту."
        # Сохраняем результат в базе данных
        QuizResults.objects.create(user_id=user_id, result=score)
        # Удаляем текущую сессию квиза из базы данных
        quiz_session.delete()
        # сообщаем пользователю результат
        await message.answer(f"Кол-во 'ДА' ответов: {score}.\n\n{result_text}")

@router.callback_query(lambda c: c.data.startswith('yes') or c.data.startswith('no'))
async def process_callback(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    # Получаем текущую сессию квиза из базы данных
    quiz_session = QuizSession.objects.get(user_id=user_id)
    question_number = quiz_session.question_number
    score = quiz_session.score

    # Обновляем информацию о текущей сессии квиза в базе данных
    _, new_question_number, new_score = map(int, callback_query.data.split(','))
    quiz_session.question_number = new_question_number
    quiz_session.score = new_score
    quiz_session.save()

    await quiz_show_question(user_id=user_id, message=callback_query.message)
```
В этом примере мы создаем две новые модели `QuizSession` и `QuizResults` для хранения информации о текущей сессии квиза и результатах квиза соответственно. Мы также изменяем логику обработки команды `startquiz` и обработчика `callback_query`, чтобы использовать информацию из объектов `QuizSession` для отслеживания текущей сессии квиза и предотвращения повторного сохранения результата в базе данных после завершения квиза.

Я надеюсь, что этот код поможет вам решить проблему с повторным сохранением результата квиза в базе данных. 😊