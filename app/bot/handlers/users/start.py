from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
# from asgiref.sync import sync_to_async
# from django.contrib.auth.models import User

from bot.loader import dp
# from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}!")
    # answer = await sync_to_async(User.objects.first)()
    # await message.answer(answer)
