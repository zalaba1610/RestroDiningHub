from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.conf import settings

import razorpay
from .models import *


# HOME
def home(request):
    restaurants = Restaurant.objects.all()
    items = Menu.objects.all()

    return render(request, 'home.html', {
        'restaurants': restaurants,
        'items': items,
    })


# RESTAURANT DETAIL
def restaurant_detail(request, id):
    restaurant = get_object_or_404(Restaurant, id=id)

    return render(request, 'restaurant_detail.html', {
        'restaurant': restaurant,
        'items': Menu.objects.filter(restaurant=restaurant),
        'reviews': Review.objects.filter(menu__restaurant=restaurant),
    })


# REGISTER
def register(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')
    return render(request, 'register.html', {'form': form})


# CART
@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(i.item.price * i.quantity for i in cart_items)

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })


@login_required
def add_to_cart(request, id):
    item = Menu.objects.get(id=id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, item=item)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('/cart/')


@login_required
def increase_quantity(request, id):
    cart = Cart.objects.get(id=id)
    cart.quantity += 1
    cart.save()
    return redirect('/cart/')


@login_required
def decrease_quantity(request, id):
    cart = Cart.objects.get(id=id)
    if cart.quantity > 1:
        cart.quantity -= 1
        cart.save()
    return redirect('/cart/')


@login_required
def remove_cart(request, id):
    Cart.objects.get(id=id).delete()
    return redirect('/cart/')


# CHECKOUT
@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)

    total = sum(i.item.price * i.quantity for i in cart_items)
    total += 50

    client = razorpay.Client(auth=(
        settings.RAZORPAY_KEY_ID,
        settings.RAZORPAY_KEY_SECRET
    ))

    payment = client.order.create({
        'amount': total * 100,
        'currency': 'INR',
        'payment_capture': 1
    })

    Order.objects.create(
        user=request.user,
        total=total,
        razorpay_order_id=payment['id'],
        status='Pending'
    )

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total': total,
        'payment': payment
    })


# ORDERS
@login_required
def orders(request):
    return render(request, 'orders.html', {
        'orders': Order.objects.filter(user=request.user)
    })


# TABLE
def select_table(request):
    return render(request, 'tables.html', {
        'tables': Table.objects.all()
    })


@login_required
def book_table(request, table_id):

    table = get_object_or_404(Table, id=table_id)

    if request.method == 'POST':

        booking_date = request.POST.get('booking_date')
        booking_time = request.POST.get('booking_time')

        # FIX: restaurant ko safe method se lo
        restaurant_id = request.POST.get('restaurant')

        restaurant = get_object_or_404(Restaurant, id=restaurant_id)

        Booking.objects.create(
            user=request.user,
            restaurant=restaurant,
            table=table,
            booking_date=booking_date,
            booking_time=booking_time
        )

        table.is_booked = True
        table.save()

        return redirect('/dashboard/')

    return render(request, 'book_table.html', {
        'table': table,
        'restaurants': Restaurant.objects.all()
    })


# REVIEW (FIXED)
@login_required
def add_review(request, id):
    if request.method == 'POST':
        menu = Menu.objects.get(id=id)

        Review.objects.create(
            user=request.user,
            menu=menu,
            rating=request.POST.get('rating'),
            comment=request.POST.get('comment')
        )

    return redirect('/')


# WISHLIST
@login_required
def wishlist(request):
    return render(request, 'wishlist.html', {
        'wishlist_items': Wishlist.objects.filter(user=request.user)
    })


@login_required
def add_to_wishlist(request, id):
    item = Menu.objects.get(id=id)
    Wishlist.objects.get_or_create(user=request.user, item=item)
    return redirect('/')


@login_required
def remove_wishlist(request, id):
    Wishlist.objects.get(id=id).delete()
    return redirect('/wishlist/')


# DASHBOARD
@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {
        'total_orders': Order.objects.count(),
        'total_revenue': Order.objects.aggregate(Sum('total'))['total__sum'] or 0,
        'total_menu': Menu.objects.count(),
        'total_reviews': Review.objects.count(),
        'recent_orders': Order.objects.order_by('-id')[:5],
        'bookings': Booking.objects.filter(user=request.user),
    })


# CANCEL BOOKING
@login_required
def cancel_booking(request, id):
    booking = get_object_or_404(Booking, id=id, user=request.user)

    booking.table.is_booked = False
    booking.table.save()

    booking.delete()

    return redirect('/dashboard/')