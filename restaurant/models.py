from django.db import models
from django.contrib.auth.models import User

# ------------------ Restaurant--------------------

class Restaurant(models.Model):

    name = models.CharField(max_length=100)

    address = models.TextField()

    image = models.ImageField(upload_to='restaurants/')

    rating = models.FloatField(default=4.0)

    delivery_time = models.CharField(
        max_length=50,
        default="30 mins"
    )

    def __str__(self):
        return self.name

# ---------------- MENU ----------------
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Menu(models.Model):
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE)

    name = models.CharField(max_length=100)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    price = models.IntegerField()

    is_veg = models.BooleanField(default=True)
    available = models.BooleanField(default=True)

    offer = models.CharField(max_length=100, blank=True, null=True)
    rating = models.FloatField(default=4.0)

    delivery_time = models.CharField(max_length=50, default="30 mins")

    description = models.TextField()
    image = models.ImageField(upload_to='menu_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
# ---------------- CART ----------------
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.item.name}"

# ---------------- TABLE ----------------
class Table(models.Model):
    table_number = models.IntegerField(unique=True)
    seats = models.IntegerField(default=4)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"Table {self.table_number}"


# ---------------- BOOKING ----------------
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    table = models.ForeignKey(Table, on_delete=models.CASCADE)

    booking_date = models.DateField()
    booking_time = models.TimeField()

    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Confirmed', 'Confirmed'),
            ('Cancelled', 'Cancelled'),
        ],
        default='Pending'
    )

    def __str__(self):
        return f"{self.user} - {self.restaurant}"


# ---------------- ORDER (RAZORPAY READY) ----------------
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.IntegerField()

    status = models.CharField(
    max_length=20,
    choices=[
        ('Pending', 'Pending'),
        ('Preparing', 'Preparing'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
    ],
    default='Pending'
)
    

    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=200, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"
    
# ---------------- REVIEWS ----------------

class Review(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)

    rating = models.IntegerField(default=5)

    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    

class Wishlist(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    item = models.ForeignKey(Menu, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
class RestaurantImage(models.Model):

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE
    )

    image = models.ImageField(
        upload_to='restaurant_gallery/'
    )

    def __str__(self):
        return self.restaurant.name
    

    


    