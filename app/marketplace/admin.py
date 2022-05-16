from django.contrib import admin
from django.contrib.admin import display

from .models import TgUser, Category, Subcategory, Item, ShippingOption, Order
# Register your models here.


class TgUserAdmin(admin.ModelAdmin):
    list_display = 'username', 'user_id', 'created_at'
    readonly_fields = 'username', 'user_id', 'created_at'
    search_fields = 'username', 'user_id'
    actions_on_top = True
    ordering = 'username',


class CategoryAdmin(admin.ModelAdmin):
    list_display = 'title',
    search_fields = 'title',
    ordering = 'title',


class SubcategoryAdmin(admin.ModelAdmin):
    list_display = 'title', 'category'
    search_fields = 'title', 'category__title'
    list_editable = 'category',
    ordering = 'category__title', 'title'


class ItemAdmin(admin.ModelAdmin):
    list_display = 'title', 'price', 'subcategory', 'get_category', 'can_be_shipped', 'is_flexible'
    search_fields = 'title', 'subcategory__title'
    list_editable = 'price', 'subcategory', 'can_be_shipped', 'is_flexible'
    ordering = 'title', 'subcategory__title'

    @display(ordering='subcategory__category', description='Категория')
    def get_category(self, obj):
        return obj.subcategory.category


class ShippingOptionAdmin(admin.ModelAdmin):
    list_display = 'title', 'type', 'price'
    list_editable = 'type', 'price'
    ordering = 'price', 'title'


class OrderAdmin(admin.ModelAdmin):
    list_display = '__str__', 'get_item', 'get_username', 'total_amount', 'created_at'
    ordering = '-created_at',
    readonly_fields = 'user', 'item', 'shipping_option', 'shipping_address', 'mobile_phone', 'receiver_name', \
                      'total_amount', 'created_at'

    @display(description='Товар')
    def get_item(self, obj):
        return obj.item.title

    @display(description='Покупатель')
    def get_username(self, obj):
        return obj.user.username


admin.site.register(TgUser, TgUserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(ShippingOption, ShippingOptionAdmin)
admin.site.register(Order, OrderAdmin)
