from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


# генератор обычной клавиатуры
def make_row_keyboard(items: list[str], row_size=int, *args, **kwargs) -> ReplyKeyboardMarkup:
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

    return kb.as_markup(resize_keyboard=True, **kwargs)


def back_next():
    keyboard = InlineKeyboardBuilder()
    back_button = InlineKeyboardButton(text="<<<<", callback_data="back")
    next_button = InlineKeyboardButton(text=">>>>", callback_data="next")
    keyboard.add(back_button, next_button)
    return keyboard.as_markup()


def inline_two_buttons(btn1_text: str, btn2_text: str, btn1_data: str, btn2_data: str):
    buttons_list = [
        [InlineKeyboardButton(text=btn1_text, callback_data=btn1_data),
         InlineKeyboardButton(text=btn2_text, callback_data=btn2_data)]
    ]
    kb = InlineKeyboardBuilder(markup=buttons_list)
    return kb.as_markup()