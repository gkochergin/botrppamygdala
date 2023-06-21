import requests
from datetime import datetime
import json
from typing import List

BASE_URL = 'http://localhost:8000/api/v1'


def create_user(user_id: int, chat_id: int, username: str, timezone: str):
    url = f'{BASE_URL}/bot-users'
    user_data = {'user_id': user_id, 'chat_id': chat_id, 'username': username, 'timezone': timezone}
    requests.post(url=url, data=user_data)

    return 'Событие Create User завершено.'


def get_user_by_id(user_id: str):
    url = f'{BASE_URL}/bot-users'
    user_data = {'user_id': user_id}
    get_user = requests.get(url=url, data=user_data).json()
    print(get_user_by_id.__module__, '>', get_user_by_id.__name__, f'> Событие Get User для user id: {user_id} завершено.')
    return get_user


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


def get_daily_buttons_data(day: int):
    url = f'{BASE_URL}/messages'
    param = {'day': day}
    response = requests.get(url=url, params=param).json()
    btn_data = [
        {'name': item['button_name'], 'data': item['button_callback']} for item in response
    ]

    print(get_buttons_callback.__name__, ">", 'btn_data', ">", btn_data, '\n')

    return btn_data


def get_buttons_callback(day: int):
    url = f'{BASE_URL}/messages'
    param = {'day': day}
    response = requests.get(url=url, params=param).json()
    print(response)
    callbacks = [item['button_callback'] for item in response]
    return callbacks


def save_user_timezone(user_id: str, timezone: str) -> None:
    url = f'{BASE_URL}/upd-user-data/{user_id}/'
    data = {'user_id': user_id, 'timezone': timezone}
    response = requests.put(url=url, data=data).json()
    return response


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


def get_id_and_day_num_list() -> List[dict]:
    url = f'{BASE_URL}/bot-users'
    response: List[dict] = requests.get(url=url).json()
    keys_to_keep = ['user_id', 'chat_id', 'days_after_reg_date']
    cleared_response = [
        {key: dictionary.get(key) for key in keys_to_keep}
        for dictionary in response if dictionary['marathon_completed'] is False
    ]
    return cleared_response


def set_marathon_completed(user_id: str, completed: bool = True):
    url = f'{BASE_URL}/upd-user-data/{user_id}/'
    data = {'user_id': user_id, 'marathon_completed': completed}
    response = requests.put(url=url, data=data).json()
    return response


print(get_buttons_callback(day=3))
print(get_id_and_day_num_list)