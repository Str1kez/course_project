from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

# from loader import dp
from bot.loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Список команд: ",
            "/start - Начать диалог",
            "/help - Получить справку",
            "/catalog - Получить каталог",)
    
    await message.answer("\n".join(text))
