from django.contrib import admin
from django.contrib.admin import display
from mptt.admin import DraggableMPTTAdmin, ModelAdmin as MPTTAdmin

from .models import TgUser, Category, Item, ShippingOption, Order
# Register your models here.


class TgUserAdmin(admin.ModelAdmin):
    list_display = 'username', 'user_id', 'created_at'
    readonly_fields = 'username', 'user_id', 'created_at'
    search_fields = 'username', 'user_id'
    actions_on_top = True
    ordering = 'username',


class CategoryDraggableMPTTAdmin(DraggableMPTTAdmin):
    list_display = 'tree_actions', 'indented_title'
    search_fields = 'title',


class ItemMPTTAdmin(MPTTAdmin):
    list_display = 'title', 'price', 'parent', 'can_be_shipped', 'is_flexible'
    search_fields = 'title', 'parent__title'
    list_editable = 'price', 'parent', 'can_be_shipped', 'is_flexible'
    ordering = 'title', 'parent__title'


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
admin.site.register(Category, CategoryDraggableMPTTAdmin)
admin.site.register(Item, ItemMPTTAdmin)
admin.site.register(ShippingOption, ShippingOptionAdmin)
admin.site.register(Order, OrderAdmin)
