from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

# from loader import dp
from bot.loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Список команд: ",
            "/start - Начать диалог",
            "/help - Получить справку",
            "/catalog - Получить каталог",
            "@MarketplaceCWBot <b>название</b> $price<i><b>от</b></i>,<i><b>до</b></i>",
            "Позволяет искать товар по названию или описанию",
            "Опционально: фильтр цены с нижним и верхним пределом цены")
    
    await message.answer("\n".join(text))
