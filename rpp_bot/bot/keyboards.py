from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


# генератор обычной клавиатуры
def make_row_keyboard(items: list[str], row_size=int) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один или несколько рядов
    :type row_size: int
    :param row_size: размер клавиатуры (кол-во кнопок в ряду)
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    kb = ReplyKeyboardBuilder()
    row = [KeyboardButton(text=item) for item in items]
    for b in row:
        kb.row(b)
    kb = kb.adjust(row_size)

    return kb.as_markup(resize_keyboard=True)


