from decimal import Decimal

from aiogram import types
from aiogram.types import LabeledPrice, Message, ContentType, ShippingOption
from asgiref.sync import sync_to_async

from marketplace.models import Item, TgUser, Order, ShippingOption as ShippingOptionDB
from bot.loader import dp, bot


async def get_shipping_options():
    options = await sync_to_async(ShippingOptionDB.objects.all)()
    return [ShippingOption(id=str(opt.id),
                           title=opt.title,
                           prices=[LabeledPrice(opt.type, int(opt.price * 100))]) for opt in options]


async def get_user_or_create(user_id: int, username: str):
    try:
        user = await sync_to_async(TgUser.objects.get)(user_id=user_id)
    except TgUser.DoesNotExist:
        user = TgUser(user_id=user_id, username=username)
        await sync_to_async(user.save)()

    return user


@dp.shipping_query_handler()
async def shipping(query: types.ShippingQuery):
    if query.shipping_address.country_code == 'RU':
        item = await sync_to_async(Item.objects.get)(id=int(query.invoice_payload))
        if item.can_be_shipped:
            await bot.answer_shipping_query(shipping_query_id=query.id,
                                            ok=True,
                                            shipping_options=await get_shipping_options())
        else:
            await bot.answer_shipping_query(shipping_query_id=query.id, ok=True,
                                            shipping_options=[
                                                ShippingOption('0', 'Не доставляется', [LabeledPrice('Доставка', 0)])])
    else:
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        ok=False,
                                        error_message='Работаем пока только по России')


@dp.pre_checkout_query_handler()
async def make_payment(query: types.ShippingQuery):
    # ! Здесь идет бронирование товара
    item = await sync_to_async(Item.objects.get)(id=int(query.invoice_payload))
    # Если есть товар, иначе отправим ok=False с объяснением
    if item.amount > 0:
        await bot.answer_pre_checkout_query(pre_checkout_query_id=query.id, ok=True)
    else:
        await bot.answer_pre_checkout_query(pre_checkout_query_id=query.id, ok=False,
                                            error_message='Данный товар закончился :(')
    # 1111 1111 1111 1026, 12/22, CVC 000


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def check_payment(message: Message):
    can_be_shipped = message.successful_payment.shipping_option_id != '0'
    user = await get_user_or_create(message.from_user.id, message.from_user.username)
    item = await sync_to_async(Item.objects.get)(id=int(message.successful_payment.invoice_payload))
    shipping_option = None
    if can_be_shipped:
        shipping_option = await sync_to_async(ShippingOptionDB.objects.get)(id=int(message.
                                                                                   successful_payment.
                                                                                   shipping_option_id))

    shipping_address = message.successful_payment.order_info.shipping_address.as_json() if can_be_shipped else None
    mobile_phone = message.successful_payment.order_info.phone_number if can_be_shipped else None
    receiver_name = message.successful_payment.order_info.name if can_be_shipped else None
    total_amount = message.successful_payment.total_amount / 100

    successful_order = Order(user=user,
                             item=item,
                             shipping_option=shipping_option,
                             shipping_address=shipping_address,
                             mobile_phone=mobile_phone,
                             receiver_name=receiver_name,
                             total_amount=total_amount)

    item.amount -= 1
    await sync_to_async(item.save)()
    await sync_to_async(successful_order.save)()
    await message.answer(f'Спасибо за покупку\n{item.title}')
