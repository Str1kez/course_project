from aiogram import types

from loader import dp, bot


@dp.message_handler(commands=['catalog'])
async def get_catalog(message: types.Message):
    await bot.send_invoice(chat_id=message.chat,
                           title='Поршик',
                           description='Good car',
                           )
