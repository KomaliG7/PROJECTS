from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'pages/home.html')
def about(request):
    return render(request,'pages/about.html')
def contact(request):
    return render(request,'pages/contact.html')
def feedback(request):
    success=False
    if request.method =='POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'Feedback from {name} ({email}):{message}')
        success = True
        return render(request, 'pages/feedback.html', {'success': success})
    return render(request, 'pages/feedback.html', {'success': success})
