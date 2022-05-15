from aiogram import types
from aiogram.types import LabeledPrice, SuccessfulPayment, Message

from data.items import Item
from data.shipping_methods import REGULAR_SHIPPING, FAST_SHIPPING_DEFAULT, PICKUP_SHIPPING, FAST_SHIPPING_BOX
# from loader import dp, bot


from bot.loader import dp, bot


@dp.message_handler(commands=['catalog'])
async def get_catalog(message: types.Message):
    porshe = Item(title='Поршик',
                  description='Good car',
                  payload='anything',
                  currency='RUB',
                  prices=[LabeledPrice('BOMJ', 400_00)],
                  photo_url='https://avatars.mds.yandex.net/get-verba/787013/2a000001675ec26d44c5fc838f55f253d508/cattouchret',
                  need_name=True,
                  need_phone_number=True)
    await bot.send_invoice(chat_id=message.from_user.id, **porshe.__dict__)
    lamba = Item(title='Ламба',
                 description='Good car',
                 payload='anything',
                 currency='RUB',
                 prices=[LabeledPrice('BOMJ', 300_00)],
                 need_name=True,
                 photo_url='',
                 need_phone_number=True)
    await bot.send_invoice(chat_id=message.from_user.id, **lamba.__dict__)


@dp.shipping_query_handler
async def get_shipping_options(query: types.ShippingQuery):
    if query.shipping_address.country_code == 'RU':
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        ok=True,
                                        shipping_options=[REGULAR_SHIPPING, FAST_SHIPPING_DEFAULT,
                                                          FAST_SHIPPING_BOX, PICKUP_SHIPPING])
    else:
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        ok=False,
                                        error_message='Работаем пока только по России')


@dp.pre_checkout_query_handler
async def make_payment(query: types.ShippingQuery):
    # ! Здесь идет бронирование товара
    await bot.answer_pre_checkout_query(pre_checkout_query_id=query.id, ok=True)
    # Если есть товар, иначе отправим ok=False с объяснением
    # await bot.answer_pre_checkout_query(pre_checkout_query_id=query.id, ok=False,
    #                                     error_message='Данный товар закончился :(')
    # 1111 1111 1111 1026, 12/22, CVC 000


@dp.message_handler(content_types=SuccessfulPayment)
async def check_payment(message: Message):
    print(message.successful_payment.currency)
    print(message.successful_payment.total_amount)
    print(message.successful_payment.invoice_payload)
    print(message.successful_payment.shipping_option_id)
    print(message.successful_payment.order_info)
# @dp.register_pre_checkout_query_handler
# async def confirm_payment(query: types.ShippingQuery):
#     await bot.send_message(query.from_user.id, query)
