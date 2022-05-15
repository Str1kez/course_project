import logging

from aiogram import Dispatcher

# from bot.data.config import ADMINS
from data.config import ADMINS


async def on_startup_notify(dp: Dispatcher):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, "Бот Запущен", disable_notification=True)

        except Exception as err:
            logging.exception(err)
