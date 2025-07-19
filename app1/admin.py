from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ContactSubmission,Product,Cart,CartItem,BillingAddress, ShippingAddress, Order, OrderItem


class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)

admin.site.register(User, CustomUserAdmin)
admin.site.register(ContactSubmission)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(BillingAddress)
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

