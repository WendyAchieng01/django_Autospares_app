from django.contrib import admin
from orders.models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_amount', 'is_paid', 'created_at', 'updated_at']
    inlines = [OrderItemInline]

    def total_amount(self, obj):
        return obj.get_total_amount()
    total_amount.short_description = 'Total Amount'

    def is_paid(self, obj):
        return obj.is_paid
    is_paid.boolean = True
    is_paid.short_description = 'Paid'

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']