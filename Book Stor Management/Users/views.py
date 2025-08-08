from django.shortcuts import render, redirect
from Users.models import BookModel

def search_books(request):
    query = request.GET.get('query', '').strip()
    results = []
    if query:
        results = BookModel.objects.filter(
            bookname__icontains=query
        ) | BookModel.objects.filter(
            bookauthor__icontains=query
        ) | BookModel.objects.filter(
            bookid__icontains=query
        )
    return render(request, 'users/search_books.html', {'query': query, 'results': results})

def ViewMyBooks(request):
    return render(request, 'users/ViewMyBooks.html')

def AddToCart(request):
    # For now this is a placeholder; implement your logic here
    return redirect('users:view-cart')

def ViewCart(request):
    return render(request, 'users/ViewCart.html')

def CheckOut(request):
    return render(request, 'users/Checkout.html')

def Payment(request):
    return render(request, 'users/Payment.html')

def OrdersDetails(request):
    return render(request, 'users/ViewMyOrders.html')

def UserLogout(request):
    request.session.flush()
    return redirect('admins:index')
