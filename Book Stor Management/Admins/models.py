from django.db import models
from django.contrib.auth.models import User

# Book model
from django.db import models

class BookModel(models.Model):
    CATEGORY_CHOICES = (
        ('Fiction', 'Fiction'),
        ('Non-Fiction', 'Non-Fiction'),
        ('Biography', 'Biography'),
        ('Science', 'Science'),
        ('Technology', 'Technology'),
        ('Other', 'Other'),
    )

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    stock = models.PositiveIntegerField()
    cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True)

    def __str__(self):
        return self.title


# Order model
class OrderModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(BookModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered')
    ], default='Pending')

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"
