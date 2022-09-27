from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from asgiref.sync import sync_to_async
from django.core.paginator import Paginator
from django.db.models import Count, Sum, Q

from marketplace.models import Category, Item
from bot.utils.misc.logging import error_logger
from .callbacks import get_callback_data
from .custom_buttons import get_back_button, prev_page_button, next_page_button


async def category_keyboard():
    stage = 0
    categories = await sync_to_async(Category.objects.alias(non_empty=Count('children')).filter)(non_empty__gt=0,
                                                                                                 level=0)

    keyboard = InlineKeyboardMarkup()
    for cat in categories:
        callback_data = get_callback_data(stage=stage + 1, category_id=str(cat.id))
        keyboard.insert(InlineKeyboardButton(text=str(cat), callback_data=callback_data))

    return keyboard


async def subcategory_keyboard(category_id: str):
    stage = 1
    category = await sync_to_async(Category.objects.get)(id=int(category_id))
    subcategories = await sync_to_async(category.get_children)()
    items_in_category = category.item_set.exists()
    is_leaf_level = all((cat.is_leaf_node() for cat in subcategories)) and not items_in_category
    keyboard = InlineKeyboardMarkup()

    if is_leaf_level:
        subcategories = await sync_to_async(subcategories.alias(non_empty=Sum('item__amount')).filter)(non_empty__gt=0)
    else:
        if items_in_category:
            error_logger.error('Error in hierarchy of orders and categories: CATEGORY ' + str(category))
        subcategories = await sync_to_async(subcategories.alias(ne_children=Count('children'),
                                                                ne_items=Count('item__amount'))
                                            .filter)(Q(ne_children__gt=0) | Q(ne_items__gt=0))

    for subcat in subcategories:
        callback_data = get_callback_data(stage=stage + subcat.is_leaf_node(), category_id=str(subcat.id))
        keyboard.insert(InlineKeyboardButton(text=str(subcat), callback_data=callback_data))

    keyboard.row(get_back_button(category=category, stage=stage))

    return keyboard


async def items_keyboard(category_id: str, page: str):
    stage = 2
    row_width = 2
    category = await sync_to_async(Category.objects.get)(id=int(category_id))
    items = await sync_to_async(category.item_set.filter)(amount__gt=0)

    keyboard = InlineKeyboardMarkup(row_width=row_width)
    p = Paginator(items, row_width * 4)
    current_page = p.page(int(page))
    for item in current_page.object_list:
        callback_data = get_callback_data(stage=stage + 1, category_id=category_id,
                                          item_id=str(item.id))
        keyboard.insert(InlineKeyboardButton(text=str(item), callback_data=callback_data))
    pagination_buttons = []
    if current_page.has_previous():
        pagination_buttons.append(prev_page_button(stage, category_id, current_page))
    if current_page.has_next():
        pagination_buttons.append(next_page_button(stage, category_id, current_page))
    keyboard.row(*pagination_buttons)
    keyboard.row(get_back_button(category=category, stage=stage))

    return keyboard


async def detailed_item_keyboard(item_id: str = '0'):
    stage = 3
    keyboard = InlineKeyboardMarkup()
    item = await sync_to_async(Item.objects.get)(id=int(item_id))
    keyboard.insert(InlineKeyboardButton(text=f'Заплатить {item.price} {item.currency}', pay=True))

    keyboard.row(get_back_button(category=item, stage=stage))

    return keyboard, item
