import django
import uvicorn
import asyncio
import os
from aiogram import executor
from multiprocessing import Process
from django.core.asgi import get_asgi_application

from bot.loader import dp
from bot.utils.notify_admins import on_startup_notify
from bot.utils.set_bot_commands import set_default_commands

# Настройка окружения для настроек
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webapp.settings")
django.setup()

# Создаем корутину
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


def run_server():
    app = get_asgi_application()
    config = uvicorn.Config(app=app, loop=loop, port=8001)
    server = uvicorn.Server(config=config)
    asyncio.run(server.serve())


async def on_startup(dispatcher):
    # Подключаем модули бота после установки приложений джанго
    from bot import middlewares, filters, handlers
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    # await on_startup_notify(dispatcher)


def run_bot():
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
        

if __name__ == '__main__':
    bot = Process(target=run_bot)
    server = Process(target=run_server)
    
    server.start()
    # bot.start()
