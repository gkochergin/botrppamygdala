from django.core.management.base import BaseCommand
import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from rpp_bot.config_reader import config

# инициализация sentry
# sentry_sdk.init(
#     dsn=config.sentry_dsn.get_secret_value(),
#
#     # Set traces_sample_rate to 1.0 to capture 100%
#     # of transactions for performance monitoring.
#     # We recommend adjusting this value in production.
#     traces_sample_rate=1.0
# )

async def main():

    logging.basicConfig(
        level=logging.DEBUG, filename='bot_app/logs/bot_debug.log',
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


if __name__ == "__main__":
    asyncio.run(main())
