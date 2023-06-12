# функция декоратор для перехвата ошибок и записи в лог
from typing import List
import nltk
from nltk.tokenize import sent_tokenize
import re

from rpp_bot.bot import api


def error_logger(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            with open('error.log', 'a') as f:
                f.write(f'Error: {e}\n')
            raise

    return wrapper


def split_text_to_parts(text: str, part_length: int):
    """
    Splits a given text into sentences and groups them into parts with a maximum length.

    :param text: The text to split.
    :type text: str
    :param part_length: The maximum length of each part.
    :type part_length: int
    :return: A list of strings where each string is a part of the original text with a maximum length.
    :rtype: List[str]
    """
    # Check input values
    if not text:
        raise ValueError("Input text is empty")
    if part_length <= 0:
        raise ValueError("Variable max_length can't be 0 or negative number")

    # Initialize the result list, current part list, and current length counter
    result = []
    current_part = []
    current_length = 0

    # Remove leading and trailing whitespace from the text
    text = text.strip()

    # Split the text into sentences with nltk library
    sentences = extract_strings_by_regexp(text)

    # Iterate over the sentences
    for sentence in sentences:
        # If adding the current sentence to the current part would exceed the maximum length,
        # add the current part to the "result" list and reset the "current_part" and "current_length" counters
        if current_length + len(sentence) + 1 > part_length:
            result.append('\n'.join(current_part))
            current_part = []
            current_length = 0

        # Add the current sentence to the current part and update the length counter
        current_part.append(sentence)
        current_length += len(sentence) + 1

    # If there is a non-empty current part, add it to the result list
    if current_part:
        result.append('\n'.join(current_part))

    return result


def convert_response_dict_to_string(response: list) -> str:
    """
    Converts a list of dictionaries into a string by extracting the 'content' values of dictionaries with 'content_type' equal to 'TXT'.

    :param response: A list of dictionaries containing 'content_type' and 'content' keys.
    :type response: list
    :return: A string containing the extracted 'content' values separated by two newlines.
    :rtype: str
    :raises TypeError: If the input response is not a list or if any element of the response list is not a dictionary.
    :raises KeyError: If any dictionary in the response list does not contain the required keys 'content_type' and 'content'.
    :raises ValueError: If the input response is empty.
    """
    # Check if the input response is empty and is a list
    if not response:
        raise ValueError("Input response is empty")
    elif not isinstance(response, list):
        raise TypeError(f"Expected a list, but got {type(response)}")

    # Initialize a list to store the extracted content values
    content_list = []

    # Iterate over the dictionaries in the response list
    for dictionary in response:
        # Check if the current element is a dictionary and contains the required keys
        if not isinstance(dictionary, dict):
            raise TypeError(f"Expected a dictionary, but got {type(dictionary)}")
        elif 'content_type' not in dictionary or 'content' not in dictionary:
            raise KeyError(f"Missing required keys 'content_type' and/or 'content' in dictionary:\n{dictionary}")

        # If the 'content_type' value is 'TXT', append the 'content' value to the content list
        if dictionary['content_type'] == 'TXT':
            content_list.append(dictionary['content'])

    # Join the content list with two newlines as separator and assign it to the result string
    result = '\n\n'.join(content_list)

    # Return the result string
    return result


def extract_strings_by_regexp(text: str):
    """
    Splits a given text into sentences while preserving the original new line characters.

    :param text: The text to split.
    :type text: str
    :return: A list of strings where each string is a sentence from the original text.
    :rtype: List[str]
    """
    # Define the regular expression pattern to split the text by sentences
    pattern = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s'

    # Split the text by the regular expression pattern
    sub_text = re.sub('\r\n', '\n', text)
    sentences = re.split(pattern, sub_text)

    return sentences


lorem_ipsum = "\nMessage 1 at day 3. Very very long content with lorem ipsum.\nLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.\nAliquam ultrices sagittis orci a. Sit amet commodo nulla facilisi. Eu turpis egestas pretium aenean pharetra magna. Nunc sed augue lacus viverra vitae congue eu consequat.\nDolor magna eget est lorem ipsum dolor sit amet consectetur. Sed vulputate mi sit amet. Fringilla ut morbi tincidunt augue interdum velit euismod in. Diam volutpat commodo sed egestas. Amet luctus venenatis lectus magna fringilla urna porttitor rhoncus dolor. Ipsum nunc aliquet bibendum enim facilisis gravida neque convallis a. Fringilla ut morbi tincidunt augue interdum. Eget nunc scelerisque viverra mauris in.\n"

# response = api.get_messages_by_day(day=1)
# print("RESPONSE:\n",response,'\n')
# a = convert_response_dict_to_string(response)
# b = split_text_to_parts(a, part_length=800)
# print("TEXT SPLITTED TO PARTS WITH MAX_LENGTH 800:",b,'\n')
#
# for i in b:
#     print(f'Text block length: {len(i)}\n')
#
# print('\n----------------------------------------\n')
#
# for i in b:
#     print(i)