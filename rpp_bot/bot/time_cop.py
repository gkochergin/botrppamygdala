

"""
Логика:

Процесс запускается регулярно, каждый час, например.
Процесс проверяет какой сегодня день и сколько дней прошло с даты регистрации



"""
import datetime

from rpp_bot.bot import api
from rpp_bot.bot.handlers import get_day_tasks_and_sent_to_user

list_of_recipients = api.get_id_and_day_num_list()  # возвращает список всех user_id доступных на момент в системе

for recipient in list_of_recipients:
    print(recipient['user_id'])
    print(recipient['days_after_reg_date'])
    # для recipient нужно активировать функцию
    # await get_day_tasks_and_sent_to_user(message='', day_num=recipient[''])



    # сколько дней прошло с даты регистрации пользователя? мб это сразу считать в базе данных в виде параметра? точно!
