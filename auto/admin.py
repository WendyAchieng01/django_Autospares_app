from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile, Category, Brand, Accessories, Product, ShippingAddress

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Accessories)
class AccessoriesAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'offer', 'category', 'brand', 'specification', 'accessories']

@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ['firstname', 'lastname', 'address', 'city', 'county', 'zipcode', 'email', 'phonenumber', 'note', 'date_added']

# Mix Profile Info and User Info
class ProfileInline(admin.StackedInline):
    model = Profile

# Extend User Model
class CustomUserAdmin(BaseUserAdmin):
    model = User
    inlines = [ProfileInline]

# Unregister the old UserAdmin
admin.site.unregister(User)
# Register the new CustomUserAdmin
admin.site.register(User, CustomUserAdmin)

