from django.db import models


# User Registration Model
class UserRegistrationModel(models.Model):
    name = models.CharField(max_length=100)
    loginid = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    email = models.EmailField(max_length=100, unique=True)
    locality = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Approved', 'Approved')], default='Pending')

    def __str__(self):
        return self.loginid

    class Meta:
        db_table = 'UserRegistration'


# Book Model
class BookModel(models.Model):
    bookname = models.CharField(max_length=150)
    bookid = models.CharField(max_length=100, unique=True)
    bookauthor = models.CharField(max_length=100)
    publishyear = models.IntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.TextField()
    stock = models.PositiveIntegerField()
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    status = models.CharField(max_length=50, choices=[('Available', 'Available'), ('Out of Stock', 'Out of Stock')], default='Available')

    def __str__(self):
        return f"{self.bookname} ({self.bookid})"

    class Meta:
        db_table = 'Book'


# Cart Model
class CartModel(models.Model):
    username = models.CharField(max_length=100)
    bookid = models.CharField(max_length=100)
    bookname = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def total(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.username} - {self.bookname} ({self.quantity})"

    class Meta:
        db_table = 'Cart'


# Orders Model
class OrderModel(models.Model):
    username = models.CharField(max_length=100)
    booknames = models.TextField()
    bookids = models.TextField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantities = models.CharField(max_length=255)

    delivery_address = models.TextField()
    payment_mode = models.CharField(max_length=50, choices=[('Card', 'Card'), ('Cash on Delivery', 'Cash on Delivery')])
    card_details = models.CharField(max_length=100, blank=True, null=True)

    payment_status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending')
    delivery_status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Delivered', 'Delivered')], default='Pending')

    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} - {self.order_date.strftime('%Y-%m-%d')}"

    class Meta:
        db_table = "Orders"