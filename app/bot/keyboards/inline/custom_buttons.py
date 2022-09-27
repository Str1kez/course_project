from aiogram.types import InlineKeyboardButton

from bot.keyboards.inline.callbacks import get_callback_data
from marketplace.models import Category


def get_back_button(category: Category, stage: int) -> InlineKeyboardButton:
    if not category.get_level():
        callback_data = get_callback_data(stage=0)
    else:
        callback_data = get_callback_data(stage=stage - (stage != 1), category_id=str(category.parent.id))

    return InlineKeyboardButton(text='Назад', callback_data=callback_data)


def prev_page_button(stage: int | str, category_id: int | str, page) -> InlineKeyboardButton:
    return InlineKeyboardButton(text="⬅️",
                                callback_data=get_callback_data(stage=stage,
                                                                category_id=category_id,
                                                                page=str(
                                                                    page.previous_page_number())))


def next_page_button(stage: int | str, category_id: int | str, page) -> InlineKeyboardButton:
    return InlineKeyboardButton(text="➡️",
                                callback_data=get_callback_data(stage=stage,
                                                                category_id=category_id,
                                                                page=str(
                                                                    page.next_page_number())))
