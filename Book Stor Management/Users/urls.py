from django.urls import path
from .views import (
    search_books, ViewMyBooks, AddToCart, ViewCart,
    CheckOut, Payment, OrdersDetails, UserLogout
)

app_name = 'users'

urlpatterns = [
    path('search/', search_books, name='search-books'),
    path('my-books/', ViewMyBooks, name='view-books'),
    path('add-to-cart/', AddToCart, name='add-to-cart'),
    path('cart/', ViewCart, name='view-cart'),
    path('checkout/', CheckOut, name='checkout'),
    path('payment/', Payment, name='payment'),
    path('orders/', OrdersDetails, name='order-details'),
    path('logout/', UserLogout, name='logout'),
]
