from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from asgiref.sync import sync_to_async
from aiogram.types import CallbackQuery
from django.db.models import Count

from marketplace.models import Category
from bot.keyboards.inline.categories import get_category_keyboard

from bot.loader import dp
# from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}!")
    reply_markup = await get_category_keyboard()
    await message.answer('Категории', reply_markup=reply_markup)
    # categories = await sync_to_async(Category.objects.alias(non_empty=Count('subcategory')).filter)(non_empty__gt=0)
    # categories = await get_all_categories()
    # print(categories[0])
    # print(categories)
    # answer = await sync_to_async(Category.objects.first)()
    # await message.answer(answer)


# здесь state нужен на многоуровневую
@dp.callback_query_handler()
async def receive_category(call: CallbackQuery):
    await call.answer()
    await call.message.edit_reply_markup()
    await call.message.answer(f'Вы выбрали {call.data.split(":")[-1]}')
