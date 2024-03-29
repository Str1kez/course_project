from aiogram.utils.callback_data import CallbackData


category_callback = CallbackData('get', 'stage', 'category_id', 'item_id', 'page')


def get_callback_data(stage, category_id='0', item_id='0', page='1'):
    return category_callback.new(stage, category_id, item_id, page)
