import requests
import datetime
import json

BASE_URL = 'http://localhost:8000/api/v1'


def create_user(user_id: str, username: str, reg_date: str, timezone: str):
    url = f'{BASE_URL}/bot-users'
    param = {'user_id': user_id}
    response = requests.get(url=url).json()
    user_exists = any(i['user_id'] == user_id for i in response)
    if not user_exists:
        # для post нужен словарь а-ля json
        data_post = {'user_id': user_id, 'username': username, 'reg_date': reg_date, 'timezone': timezone}
        requests.post(url=url, json=data_post)
        return f"Пользователь {user_id} создан."
    else:
        return f"Пользователь {user_id} существует."


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

