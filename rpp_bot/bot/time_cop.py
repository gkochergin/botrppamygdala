"""
Логика:
Процесс запускается регулярно, каждый час, например.
Процесс получает номер дня для отправки контента пользователю.
Процесс инициирует поочередно отправку заданий пользователям

"""
from rpp_bot.bot import api
from rpp_bot.bot.handlers import get_day_tasks_and_sent_to_user
from rpp_bot.bot.main import bot

"""
функция, проверяет кол-во дней с момента регистрации в чат-боте и если у пользователя >= 13 дней, проставляет
ему True для параметра marathon_completed
"""
def check_users_status():
    # получаем список всех пользователей, где days_after_reg_date >= 13
    # для каждого пользователя где days_after_reg_date >= 13
    # присваиваем значение поля marathon_completed = True
    # добавляем пользователя в новый список для массового обновления данных
    # с помощью метода bulk_update массово обновляем данные пользователей

    api.get_id_and_day_num_list()


def main():
    # по api получаем список словарей с telegram id, chat id и day number для каждого пользователя
    list_of_recipients = api.get_id_and_day_num_list()

    # для каждого получателя запускаем функцию
    for recipient in list_of_recipients:
        await get_day_tasks_and_sent_to_user(
            bot=bot,
            chat_id=recipient['chat_id'],
            day_num=recipient['days_after_reg_date'])




#
# if __name__ == '__main__':
#     pass