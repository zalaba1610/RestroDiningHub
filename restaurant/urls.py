from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    # HOME
    path('', views.home, name='home'),

    # RESTAURANT DETAIL
    path('restaurant/<int:id>/', views.restaurant_detail, name='restaurant_detail'),

    # AUTH
    path('register/', views.register, name='register'),

    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # CART
    path('cart/', views.cart, name='cart'),

    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),

    path('increase/<int:id>/', views.increase_quantity, name='increase_quantity'),

    path('decrease/<int:id>/', views.decrease_quantity, name='decrease_quantity'),

    path('remove/<int:id>/', views.remove_cart, name='remove_cart'),

    # PAYMENT
    path('checkout/', views.checkout, name='checkout'),

    # ORDERS
    path('orders/', views.orders, name='orders'),

    # TABLE BOOKING
    path('tables/', views.select_table, name='select_table'),

    path('book-table/<int:table_id>/', views.book_table, name='book_table'),

    # REVIEW
    path('review/<int:id>/', views.add_review, name='add_review'),

    # WISHLIST
    path('wishlist/', views.wishlist, name='wishlist'),

    path('wishlist/add/<int:id>/', views.add_to_wishlist, name='add_to_wishlist'),

    path('wishlist/remove/<int:id>/', views.remove_wishlist, name='remove_wishlist'),

    # DASHBOARD
    path('dashboard/', views.dashboard, name='dashboard'),

    path('cancel-booking/<int:id>/', views.cancel_booking, name='cancel_booking'),
]