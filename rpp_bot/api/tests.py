from django.test import TestCase


# Create your tests here.


def typical_day():
    message_intro = "Привет! Это твой новый день под сообщением есть кнопки с твоими лекциями и заданиями. " \
                    "Нажимай, и да пребудет с тобой сила, мой юный падаван."
    btn_names = ['Лонгрид', 'Медитация', 'Упражнение']
    btn_callbacks = ['longread', 'meditation', 'workout']

    btns_data = [{'name': name, 'data': callback} for name, callback in zip(btn_names, btn_callbacks) ]

    return btns_data


print(typical_day())
