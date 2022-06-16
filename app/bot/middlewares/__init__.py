# from aiogram import Dispatcher

from bot.loader import dp
# from loader import dp
from .throttling import ThrottlingMiddleware


if __name__ == "bot.middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
