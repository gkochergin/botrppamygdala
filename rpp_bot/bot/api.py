import requests
from datetime import datetime
import json

BASE_URL = 'http://localhost:8000/api/v1'


def create_user(user_id: str, username: str, timezone: str):
    url = f'{BASE_URL}/bot-users'
    user_data = {'user_id': user_id, 'username': username, 'timezone': timezone}
    requests.post(url=url, data=user_data)

    return 'Событие Create User завершено.'


def get_user(user_id: str):
    url = f'{BASE_URL}/bot-users'
    user_data = {'user_id': user_id}
    user = requests.get(url=url, data=user_data).json()
    print('Событие Get User завершено.')
    return user


def record_sent_message_event(user_id, message_id, sent_at):
    url = f'{BASE_URL}/sent-messages'
    param = {'user_id': user_id, 'message_id': message_id, 'sent_at': sent_at}
    requests.post(url=url, params=param)
    return 'Событие отправки данных записано.'


def get_messages_by_day(day: int) -> list:
    url = f'{BASE_URL}/messages'
    param = {'req': 'message', 'day': day}
    response = requests.get(url=url, params=param).json()
    return response

def get_messages_by_day_and_type(day: int, type: str) -> list:
    url = f'{BASE_URL}/messages'
    param = {'day': day, 'type': type}
    response = requests.get(url=url, params=param).json()
    return response


def save_user_timezone(user_id: str) -> None:
    # нужно будет сделать апдейт поля timezone конкретного юзера в базе данных
    pass


def get_quiz_question_list() -> dict:
    url = f'{BASE_URL}/quiz-question'
    response = requests.get(url).json()
    return response


def save_quiz_result(user_id: str, result: int):
    url = f'{BASE_URL}/quiz-result'
    data = {"user_id": str(user_id), "result": int(result)}
    response = requests.post(url=url, json=data)
    return response


def get_quiz_result():
    url = f'{BASE_URL}/quiz-result'
    response = requests.get(url=url)
    return response.json()
