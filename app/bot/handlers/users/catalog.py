from typing import Union

from aiogram import types
from aiogram.types import LabeledPrice
from aiogram.utils.exceptions import MessageCantBeEdited

from bot.loader import dp, bot
import bot.keyboards.inline as inline_keyboard
from bot.data.items import Item


@dp.message_handler(commands=['catalog'])
async def get_catalog(message: types.Message):
    await get_categories(message)


async def get_categories(message: Union[types.Message, types.CallbackQuery], **kwargs):
    keyboard = await inline_keyboard.category_keyboard()
    if isinstance(message, types.Message):
        await message.answer('Выбери категорию', reply_markup=keyboard)
    elif isinstance(message, types.CallbackQuery):
        await message.message.edit_text('Выбери категорию', reply_markup=keyboard)


async def get_subcategories(call: types.CallbackQuery, category_id: str, **kwargs):
    keyboard = await inline_keyboard.subcategory_keyboard(category_id)
    await call.message.edit_text(text='Выбери подкатегорию', reply_markup=keyboard)


async def get_items(call: types.CallbackQuery, category_id: str, page: str, **kwargs):
    keyboard = await inline_keyboard.items_keyboard(category_id, page)
    try:
        await call.message.edit_text(text='Выбери товар', reply_markup=keyboard)
    except MessageCantBeEdited:
        await call.message.delete()
        await bot.send_message(call.from_user.id, text='Выбери товар', reply_markup=keyboard)


async def get_detailed_item(call: types.CallbackQuery, item_id: str, **kwargs):
    keyboard, item_db = await inline_keyboard.detailed_item_keyboard(item_id)
    item = Item(title=item_db.title,
                description=item_db.description,
                payload=str(item_db.id),
                currency=item_db.currency,
                prices=[LabeledPrice(item_db.title, int(item_db.price * 100))],
                photo_url=item_db.photo_url,
                is_flexible=item_db.is_flexible,
                need_name=item_db.can_be_shipped,
                need_shipping_address=item_db.can_be_shipped,
                need_phone_number=item_db.can_be_shipped)

    await call.message.delete()
    await bot.send_invoice(chat_id=call.from_user.id, **item.__dict__, reply_markup=keyboard)


@dp.callback_query_handler(inline_keyboard.category_callback.filter())
async def all_queries_handler(call: types.CallbackQuery, callback_data: dict):
    stage = int(callback_data.get('stage'))
    category_id = callback_data.get('category_id')
    item_id = callback_data.get('item_id')
    page = callback_data.get('page')

    func_list = [get_categories, get_subcategories, get_items, get_detailed_item]

    on_stage_func = func_list[stage]

    await on_stage_func(call,
                        category_id=category_id,
                        item_id=item_id,
                        page=page)
