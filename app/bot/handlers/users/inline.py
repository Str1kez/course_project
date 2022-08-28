from aiogram import types
from aiogram.types import LabeledPrice
from asgiref.sync import sync_to_async
from marketplace.models import Item as ItemDB

from bot.data.items import Item
from bot.loader import dp
from bot.utils.misc.throttling import rate_limit


def create_item(item: ItemDB) -> Item:
    return Item(title=item.title,
                description=item.description,
                payload=str(item.id),
                currency=item.currency,
                prices=[LabeledPrice(item.title, int(item.price * 100))],
                photo_url=item.photo_url,
                is_flexible=item.is_flexible,
                need_name=item.can_be_shipped,
                need_shipping_address=item.can_be_shipped,
                need_phone_number=item.can_be_shipped)


async def send_dummy_query(query: types.InlineQuery) -> None:
    answer = types.InlineQueryResultArticle(id='1',
                                            title='Ничего не нашел',
                                            input_message_content=types.InputTextMessageContent('Не найдено'))
    await query.answer([answer])


@rate_limit(1, key='inline')
@dp.inline_handler()
async def item_searching(query: types.InlineQuery):
    items = await sync_to_async(ItemDB.objects.filter)(title__icontains=query.query, amount__gt=0)

    if not items.exists():
        return await send_dummy_query(query)

    item_list = [create_item(item) for item in items]
    answer = []
    for i, item in enumerate(item_list):
        order_message_content = types.InputInvoiceMessageContent(**item.__dict__)
        result_article = types.InlineQueryResultArticle(id=str(i),
                                                        title=item.title,
                                                        input_message_content=order_message_content)
        answer.append(result_article)

    await query.answer(answer)
