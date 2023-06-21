from django.contrib import admin

from customer.models import MenuItems, Carts, Category, Order, Reviews

# Register your models here.

admin.site.register(Category)
admin.site.register(MenuItems)

