# Telegram Marketplace 🛒
## Описание 📄
Магазин в чате telegram с админкой [django](https://www.djangoproject.com/). Основан на `django-mptt` - дереве, которое помогает представлять категории и товары в определенной иерархии. Логика работы описана с использованием [telegram bot api](https://core.telegram.org/bots/api) с библиотекой [aiogram](https://github.com/aiogram/aiogram), которая позволяет разрабатывать асинхронных ботов.
## Демо 🪧
### Начнем с админки django 👨‍💻
#### Создание категории товаров 📶
![уровни_категорий](docs/categories.png)
#### Создание товара 🚗
![создание_товара](docs/order_creating.png)
#### Создание методов доставки 🚀
![методы_доставки](docs/shipping_methods.png)
### Рассмотрим процесс заказа товара 🛍️
#### Выбор категории 📶
![категории_товара](docs/tg/categories_tg.png)
#### Выбор подкатегории 📶
![подкатегории_товара](docs/tg/subcategories_tg.png)
#### Выбор товара 🛍️
![список_товаров](docs/tg/order_list_tg.png)
#### Информация о товаре ℹ️
![инфо_о_товаре](docs/tg/order_tg.jpg)
#### Процесс оплаты 💰
![оплата](docs/tg/payment_tg.png)
#### Успешная оплата ✅
![успешная_оплата](docs/tg/successful_payment_tg.png)
#### Случай отсутствия товара на складе ❌
Если во время платежа, вдруг, не останется товара на складе, то деньги **не спишутся** и вылетит такое сообщение

![отмена_оплаты](docs/tg/order_is_upsent_tg.png)

## Запуск приложения ▶️
1. Необходимо, чтобы был установлен [Docker](https://www.docker.com/).
2. Создать `.env` файл в корневой папке с атрибутами:
    - BOT_TOKEN
    - PROVIDER_TOKEN - токен выданный платежным провайдером
    - ADMINS - id админа в телеграме
    - DJANGO_SECRET - секретный ключ для Django
    - DJANGO_SUPERUSER_PASSWORD - пароль для админа в админке
    - DJANGO_USERNAME - ник админа в админке
    - DB_URL - [postgreSQL URI](https://tableplus.com/blog/2018/08/connection-uri-syntax-in-postgresql.html#:~:text=The%20general%20form%20of%20a,param1%3Dvalue1%26...%5D&text=The%20URI%20scheme%20designator%20can%20be%20either%20postgresql%3A%2F%2F%20or%20postgres%3A%2F%2F%20.), очевидно, что все аргументы в uri должны совпадать со значениями ниже. В поле `host` написать `db`, так как Docker предоставляет локальную сеть по имени сервиса.
    - POSTGRES_DB - название для базы данных в СУБД
    - POSTGRES_USER - имя пользователя в СУБД
    - POSTGRES_PASSWORD - пароль для пользователя в СУБД
3. Выполнить в консоли `docker compose up -d`
4. Для остановки/старта использовать `docker compose stop` / `docker compose start`. Если необходимо удалить контейнеры и образ, то `docker compose down --rmi "local"`
5. Если в код были внесены изменения необходимо запускать с командой `docker compose up -d --build`, чтобы не брался кэш с прошлого билда
6. В админку можно зайти с браузера по адресу `http://localhost:8001/admin`

## Используемые технологии 🖥️
[Django](https://www.djangoproject.com/) - веб-фреймворк для поддержки orm и создания админки

[Aiogram](https://github.com/aiogram/aiogram) - асинхронный фреймворк для работы с Telegram bot api

[Uvicorn](https://www.uvicorn.org/) - ASGI сервер для работы Django в асинхронном режиме

[Docker](https://www.docker.com/) - развертывание приложения в автономных контейнерах

[Poetry](https://python-poetry.org/) - продвинутый пакетный менеджер для Python
