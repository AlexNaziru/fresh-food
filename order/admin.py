from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['first_name', 'last_name', 'address']
    inlines = [OrderItemInline]


# Showing the orders from the clients in the admin panel and conneciting ordered items to Order
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
