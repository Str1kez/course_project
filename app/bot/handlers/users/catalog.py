from aiogram import types
from aiogram.types import LabeledPrice

from bot.loader import dp, bot


@dp.message_handler(commands=['catalog'])
async def get_catalog(message: types.Message):
    await bot.send_invoice(chat_id=message.from_user.id,
                           title='Поршик',
                           description='Good car',
                           payload='PAMPARAM',
                           provider_token='381764678:TEST:37062',
                           currency='RUB',
                           prices=[LabeledPrice('BOMJ', 40000)])
