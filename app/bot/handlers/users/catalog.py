from typing import Union

from aiogram import types


from bot.loader import dp, bot
import bot.keyboards.inline as inline_keyboard


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


async def get_items(call: types.CallbackQuery, category_id: str, subcategory_id: str, **kwargs):
    keyboard = await inline_keyboard.items_keyboard(category_id, subcategory_id)
    await call.message.edit_text(text='Выбери товар', reply_markup=keyboard)


async def get_detailed_item(call: types.CallbackQuery, category_id: str, subcategory_id: str, item_id: str):
    keyboard = await inline_keyboard.detailed_item_keyboard(category_id, subcategory_id, item_id)
    # удаляем сообщение и запускаем процесс оформления заказа
    await call.message.edit_text('НАДО СДЕЛАТЬ', reply_markup=keyboard)


@dp.callback_query_handler(inline_keyboard.category_callback.filter())
async def all_queries_handler(call: types.CallbackQuery, callback_data: dict):
    stage = int(callback_data.get('stage'))
    category_id = callback_data.get('category_id')
    subcategory_id = callback_data.get('subcategory_id')
    item_id = callback_data.get('item_id')

    func_list = [get_categories, get_subcategories, get_items, get_detailed_item]

    on_stage_func = func_list[stage]

    await on_stage_func(call,
                        category_id=category_id,
                        subcategory_id=subcategory_id,
                        item_id=item_id)
