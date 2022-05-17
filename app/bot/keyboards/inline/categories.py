from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from asgiref.sync import sync_to_async
from django.db.models import Count

from marketplace.models import Category


category_callback = CallbackData('get', 'id', 'title')


async def get_category_keyboard():
    categories = await sync_to_async(Category.objects.alias(non_empty=Count('subcategory')).filter)(non_empty__gt=0)
    # categories = await sync_to_async(Category.objects.all)()
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=str(cat),
                              callback_data=category_callback.new(id=cat.id, title=cat.title))
         for cat in categories]
    ])
