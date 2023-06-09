# функция декоратор для перехвата ошибок и записи в лог
from typing import List
import nltk
from nltk.tokenize import sent_tokenize

nltk.download('punkt')

def error_logger(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            with open('error.log', 'a') as f:
                f.write(f'Error: {e}\n')
            raise

    return wrapper


lorem_ipsum = "\nMessage 1 at day 3. Very very long content with lorem ipsum.\nLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.\nAliquam ultrices sagittis orci a. Sit amet commodo nulla facilisi. Eu turpis egestas pretium aenean pharetra magna. Nunc sed augue lacus viverra vitae congue eu consequat.\nDolor magna eget est lorem ipsum dolor sit amet consectetur. Sed vulputate mi sit amet. Fringilla ut morbi tincidunt augue interdum velit euismod in. Diam volutpat commodo sed egestas. Amet luctus venenatis lectus magna fringilla urna porttitor rhoncus dolor. Ipsum nunc aliquet bibendum enim facilisis gravida neque convallis a. Fringilla ut morbi tincidunt augue interdum. Eget nunc scelerisque viverra mauris in.\n"


def split_text_by_paragraphs(text, max_length) -> list[str] | None:
    text = text.strip()
    if text.find('\n') == -1:
        print(text.find('\n'))
        return print("No paragraphs to split.")
    else:
        paragraphs = [p for p in text.split('\n') if p]
        print(paragraphs)

        result = []
        concat_paragraphs = []
        current_length = 0
        prev_paragraph_length = 0
        new_text_block = ''

        for paragraph in paragraphs:

            current_max_length = len(paragraph) + prev_paragraph_length

            if current_max_length < max_length:
                print(f"\nMax length: {max_length} > Paragraph length: {len(paragraph)}")
                concat_paragraphs = concat_paragraphs.append(paragraph)
                new_text_block = '\n'.join(concat_paragraphs)
                prev_paragraph_length = len(new_text_block)
            else:
                if new_text_block:
                    result.append(new_text_block)
                else:
                    result.append(paragraph)
        print(result)
        # if current_part:
        #     result.append(current_part)
        return result



def split_text_by_sentences(text, max_length):
    text = text.strip()
    sentences = sent_tokenize(text)
    result = []
    current_part = []
    current_length = 0
    for sentence in sentences:
        if current_length + len(sentence) + 1 > max_length:
            result.append(' '.join(current_part))
            current_part = []
            current_length = 0
        current_part.append(sentence)
        current_length += len(sentence) + 1
    if current_part:
        result.append(' '.join(current_part))
    return result

