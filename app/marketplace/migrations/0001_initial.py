# Generated by Django 4.0.4 on 2022-07-11 21:36

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True, verbose_name='Название')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='children', to='marketplace.category', verbose_name='Подкатегория')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
                ('description', models.CharField(max_length=255, verbose_name='Описание')),
                ('amount', models.IntegerField(null=True, verbose_name='Кол-во на складе')),
                ('currency', models.CharField(max_length=3, verbose_name='Валюта')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Цена')),
                ('photo_url', models.URLField(blank=True, null=True, verbose_name='URL Изображения')),
                ('can_be_shipped', models.BooleanField(default=True, verbose_name='Есть ли доставка')),
                ('is_flexible', models.BooleanField(default=True, verbose_name='Плавающая цена')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('subcategory', mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.category', verbose_name='Подкатегория')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.CreateModel(
            name='ShippingOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Название')),
                ('type', models.CharField(max_length=50, verbose_name='Название упаковки')),
                ('price', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Стоимость')),
            ],
            options={
                'verbose_name': 'Опция доставки',
                'verbose_name_plural': 'Опции доставки',
            },
        ),
        migrations.CreateModel(
            name='TgUser',
            fields=[
                ('user_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50, verbose_name='Ник пользователя')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Зарегистрирован')),
            ],
            options={
                'verbose_name': 'Пользователь Телеграма',
                'verbose_name_plural': 'Пользователи Телеграма',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shipping_address', models.JSONField(null=True, verbose_name='Адрес доставки')),
                ('mobile_phone', models.CharField(max_length=20, null=True, verbose_name='Телефон')),
                ('receiver_name', models.CharField(max_length=100, null=True, verbose_name='Данные получателя')),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Итог')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')),
                ('item', models.ForeignKey(on_delete=models.SET('deleted_item'), to='marketplace.item', verbose_name='Товар')),
                ('shipping_option', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='marketplace.shippingoption', verbose_name='Тип доставки')),
                ('user', models.ForeignKey(on_delete=models.SET('deleted_user'), to='marketplace.tguser', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
    ]
