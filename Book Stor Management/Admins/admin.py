from django.contrib import admin
from .models import BookModel, OrderModel

admin.site.register(BookModel)
admin.site.register(OrderModel)
