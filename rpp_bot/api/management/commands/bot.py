from django.core.management.base import BaseCommand
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from rpp_bot.core.config_reader import config


class Command(BaseCommand):
    help = 'Telegram bot - Amygdala RPP Bot'

    logging.basicConfig(
        level=logging.DEBUG, filename='api/logs/bot_debug.log',
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    def handle(self, *args, **options):
        # назначаем диспетчер, он же коренной роутер
        dp = Dispatcher(storage=MemoryStorage())

        # создаем объект бота, передаем токен и режим парсинга
        bot = Bot(
            token=config.tg_token.get_secret_value(),
            parse_mode='HTML'
        )
        print(bot.get_me())
        # Запускаем бота и пропускаем все накопленные входящие
        # await bot.delete_webhook(drop_pending_updates=True)
        # await dp.start_polling(bot)

