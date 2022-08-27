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

## Используемые технологии 🖥️
[Django](https://www.djangoproject.com/) - веб-фреймворк для поддержки orm и создания админки

[Aiogram](https://github.com/aiogram/aiogram) - асинхронный фреймворк для работы с Telegram bot api

[Uvicorn](https://www.uvicorn.org/) - ASGI сервер для работы Django в асинхронном режиме

[Docker](https://www.docker.com/) - развертывание приложения в автономных контейнерах

[Poetry](https://python-poetry.org/) - продвинутый пакетный менеджер для Python
