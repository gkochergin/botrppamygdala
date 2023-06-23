"""
Логика:
Процесс запускается регулярно, каждый час, например.
Процесс получает номер дня для отправки контента пользователю.
Процесс инициирует поочередно отправку заданий пользователям

"""
# from rpp_bot.bot.main import bot
#
#
#
# def main():
#     # по api получаем список словарей с telegram id, chat id и day number для каждого пользователя
#     list_of_recipients = api.get_id_and_day_num_list()
#
#     # для каждого получателя запускаем функцию
#     for recipient in list_of_recipients:
#         await get_day_tasks_and_sent_to_user(
#             bot=bot,
#             chat_id=recipient['chat_id'],
#             day_num=recipient['days_after_reg_date'])
#
