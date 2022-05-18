from aiogram.utils.callback_data import CallbackData


category_callback = CallbackData('get', 'stage', 'category_id', 'subcategory_id', 'item_id')


def get_callback_data(stage, category_id='0', subcategory_id='0', item_id='0'):
    return category_callback.new(stage, category_id, subcategory_id, item_id)
