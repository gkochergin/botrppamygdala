from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from typing import Optional, List


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


def make_inline_kb_with_two_buttons(btn1_text: str, btn2_text: str, btn1_data: str, btn2_data: str):
    buttons_list = [
        [InlineKeyboardButton(text=btn1_text, callback_data=btn1_data),
         InlineKeyboardButton(text=btn2_text, callback_data=btn2_data)]
    ]
    kb = InlineKeyboardBuilder(markup=buttons_list)
    return kb.as_markup()


def make_inline_kb(buttons_data: List[dict], sizes: Optional[List[int]] = None,
                   repeat: bool = False) -> 'InlineKeyboardMarkup':
    """
    Create an inline keyboard markup using the specified buttons data and row sizes.

    :param buttons_data: A list of dictionaries containing the data for each button. Each dictionary must have \
        a 'name' key and a 'data' key, specifying the text and callback data for the button, respectively.
    :param sizes: An optional list of integers specifying the sizes of the rows to adjust the buttons into. \
        If not provided, no row adjustment will be performed.
    :param repeat: A boolean specifying whether to repeat the row sizes when there are more buttons than the sum of \
        the passed sizes.

    :return: An InlineKeyboardMarkup object representing the constructed inline keyboard markup.
    """
    # Check if buttons_data is a list
    if not isinstance(buttons_data, list):
        raise TypeError(
            f"Expected list of dictionaries with buttons data, received {type(buttons_data)}.\n{buttons_data}")

    # Initialize inline keyboard builder
    keyboard = InlineKeyboardBuilder()

    # Create buttons from parameter buttons_data
    for dictionary in buttons_data:
        # Check if we have data in dictionary
        if not dictionary['name'] or not dictionary["data"]:
            raise ValueError(f'No "button name" or "button callback data" in dictionary:\n{dictionary}')
        else:
            keyboard.button(text=dictionary['name'], callback_data=dictionary["data"])

    # Adjust keyboard rows sizes if sizes is provided
    if sizes:
        # Check if sizes is a list
        if not isinstance(sizes, list):
            raise TypeError(f"Expected <list> type of 'sizes' parameter, but received: {type(sizes)}")

        keyboard.adjust(*sizes, repeat=repeat)
    else:
        keyboard.adjust()

    # Get the constructed InlineKeyboardMarkup object
    markup = keyboard.as_markup()

    return markup
