from django.contrib import admin
from .models import (
    RestaurantImage, Category, Menu, Cart, Order,
    Booking, Table, Review, Wishlist, Restaurant
)

# Restaurant Image
admin.site.register(RestaurantImage)

# Category
admin.site.register(Category)

# Menu
@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'category']  # category add kar diya

# Cart
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'item', 'quantity']

# Order
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total', 'status']

# Booking
# @admin.register(Booking)
# class BookingAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user', 'table', 'booking_date']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'restaurant', 'table', 'booking_date', 'booking_time']

# Table
@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ['id', 'table_number', 'seats', 'is_booked']

# Review
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'menu', 'rating']

# Wishlist
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'item']

# Restaurant
admin.site.register(Restaurant)