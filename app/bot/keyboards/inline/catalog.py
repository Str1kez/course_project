from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from asgiref.sync import sync_to_async
from django.db.models import Count, Sum

from marketplace.models import Category, Subcategory, Item
from .callbacks import get_callback_data


async def category_keyboard():
    stage = 0
    categories = await sync_to_async(Category.objects.alias(non_empty=Count('subcategory')).filter)(non_empty__gt=0)

    keyboard = InlineKeyboardMarkup()
    for cat in categories:
        callback_data = get_callback_data(stage=stage + 1, category_id=str(cat.id))
        keyboard.insert(InlineKeyboardButton(text=str(cat), callback_data=callback_data))

    return keyboard


async def subcategory_keyboard(category_id: str):
    stage = 1
    category = await sync_to_async(Category.objects.get)(id=int(category_id))
    subcategories = await sync_to_async(category.subcategory_set.
                                        alias(non_empty=Sum('item__amount')).filter)(non_empty__gt=0)

    keyboard = InlineKeyboardMarkup()
    for subcat in subcategories:
        callback_data = get_callback_data(stage=stage + 1, category_id=category_id, subcategory_id=str(subcat.id))
        keyboard.insert(InlineKeyboardButton(text=str(subcat), callback_data=callback_data))

    callback_data = get_callback_data(stage=stage - 1)
    keyboard.row(
        InlineKeyboardButton(text='Назад', callback_data=callback_data)
    )

    return keyboard


async def items_keyboard(category_id: str, subcategory_id: str):
    stage = 2
    items = await sync_to_async(Subcategory.objects.get(id=int(subcategory_id)).item_set.filter)(amount__gt=0)

    keyboard = InlineKeyboardMarkup()
    for item in items:
        callback_data = get_callback_data(stage=stage + 1, category_id=category_id,
                                          subcategory_id=subcategory_id, item_id=str(item.id))
        keyboard.insert(InlineKeyboardButton(text=str(item), callback_data=callback_data))

    callback_data = get_callback_data(stage=stage - 1, category_id=category_id)
    keyboard.row(
        InlineKeyboardButton(text='Назад', callback_data=callback_data)
    )

    return keyboard


async def detailed_item_keyboard(category_id: str, subcategory_id: str, item_id: str = '0'):
    stage = 3
    keyboard = InlineKeyboardMarkup()
    item = await sync_to_async(Item.objects.get)(id=int(item_id))
    keyboard.insert(InlineKeyboardButton(text=f'Заплатить {item.price} {item.currency}', pay=True))
    callback_data = get_callback_data(stage=stage - 1, category_id=category_id, subcategory_id=subcategory_id)
    keyboard.row(
        InlineKeyboardButton(text='Назад', callback_data=callback_data)
    )

    return keyboard, item
