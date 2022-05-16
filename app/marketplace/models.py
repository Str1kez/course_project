from django.db import models

# Create your models here.


class TgUser(models.Model):
    user_id = models.fields.BigIntegerField(primary_key=True)
    username = models.fields.CharField(blank=False, null=False, verbose_name='Ник пользователя')
    created_at = models.fields.DateTimeField(auto_now_add=True, verbose_name='Зарегистрирован')

    class Meta:
        verbose_name = 'Пользователь Телеграма'
        verbose_name_plural = 'Пользователи Телеграма'

    def __str__(self):
        return self.username
    
    
class Category(models.Model):
    title = models.fields.CharField(max_length=50, verbose_name='Название')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        
    def __str__(self) -> str:
        return self.title


class Subcategory(models.Model):
    title = models.fields.CharField(max_length=50, verbose_name='Название')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_pluaral = 'Подкатегории'

    def __str__(self) -> str:
        return self.title


class Item(models.Model):
    title = models.fields.CharField(max_length=100, blank=False, verbose_name='Название')
    description = models.fields.CharField(max_length=255, verbose_name='Описание')
    currency = models.fields.CharField(max_length=3, verbose_name='Валюта')
    price = models.fields.DecimalField(max_digits=8, decimal_places=2, verbose_name='Цена')
    photo_url = models.fields.URLField(verbose_name='URL Изображения', null=True)
    can_be_shipped = models.fields.BooleanField(verbose_name='Есть ли доставка', default=True)
    is_flexible = models.fields.BooleanField(verbose_name='Плавающая цена', default=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.title


class ShippingOption(models.Model):
    title = models.fields.CharField(max_length=50, blank=False, verbose_name='Название')
    type = models.fields.CharField(max_length=50, blank=False, verbose_name='Название упаковки')
    price = models.fields.DecimalField(max_digits=5, decimal_places=2, verbose_name='Стоимость')

    class Meta:
        verbose_name = 'Опция доставки'
        verbose_name_plural = 'Опции доставки'

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey(TgUser, on_delete=models.SET('deleted_user'), verbose_name='Пользователь')
    item = models.ForeignKey(Item, on_delete=models.SET('deleted_item'), verbose_name='Товар')
    shipping_option = models.ForeignKey(ShippingOption, on_delete=models.SET_NULL, verbose_name='Тип доставки', null=True)
    shipping_address = models.JSONField(verbose_name='Адрес доставки', null=True)
    mobile_phone = models.fields.CharField(max_length=20, null=True, verbose_name='Телефон')
    receiver_name = models.fields.CharField(max_length=100, null=True, verbose_name='Данные получателя')
    total_amount = models.fields.DecimalField(max_digits=8, decimal_places=2, verbose_name='Итог')
    created_at = models.fields.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return self.user.username + ' - ' + self.item.title
