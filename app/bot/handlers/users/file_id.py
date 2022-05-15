from aiogram.types import Message, ContentType

from data.config import ADMINS
from bot.loader import dp
# from loader import dp


@dp.message_handler(lambda message: str(message.from_user.id) in ADMINS, content_types=ContentType.PHOTO)
async def get_file_id(message: Message):
    await message.answer(message.photo[-1].file_id)
