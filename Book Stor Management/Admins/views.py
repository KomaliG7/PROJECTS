import os, random, string
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.views import View
from Users.models import UserRegistrationModel, BookModel
from django.core.files.storage import FileSystemStorage

class IndexView(View):
    def get(self, request):
        return render(request, 'admins/Index.html')

class AdminLoginView(View):
    def get(self, request):
        return render(request, 'admins/AdminLogin.html')

class UserLoginView(View):
    def get(self, request):
        return render(request, 'admins/UserLogin.html')

class UserRegisterView(View):
    def get(self, request):
        return render(request, 'admins/UserRegister.html')

class AdminLoginAction(View):
    def post(self, request):
        username = request.POST.get('loginid', '').strip()
        pwd = request.POST.get('password', '').strip()
        if username == 'Admin' and pwd == 'Admin':
            return redirect('admins:index')
        messages.error(request, "Invalid admin credentials.")
        return redirect('admins:admin-login')

class UserRegisterAction(View):
    def post(self, request):
        loginid = request.POST.get('loginID', '').strip()
        email = request.POST.get('email', '').strip()
        if UserRegistrationModel.objects.filter(loginid=loginid).exists():
            messages.error(request, 'Login ID exists.')
            return redirect('admins:user-register')
        if UserRegistrationModel.objects.filter(email=email).exists():
            messages.error(request, 'Email exists.')
            return redirect('admins:user-register')
        UserRegistrationModel.objects.create(
            name=request.POST.get('name', '').strip(),
            loginid=loginid,
            password=request.POST.get('password', '').strip(),
            mobile=request.POST.get('mobile', '').strip(),
            email=email,
            locality=request.POST.get('locality', '').strip(),
            address=request.POST.get('address', '').strip(),
            city=request.POST.get('city', '').strip(),
            state=request.POST.get('state', '').strip(),
            status='Pending'
        )
        messages.success(request, 'User registered — pending approval.')
        return redirect('admins:user-register')

class UserLoginAction(View):
    def post(self, request):
        loginid = request.POST.get('loginID', '').strip()
        pwd = request.POST.get('password', '').strip()
        try:
            user = UserRegistrationModel.objects.get(loginid=loginid, password=pwd)
            if user.status == 'Approved':
                request.session['userid'] = user.id
                request.session['username'] = user.name
                messages.success(request, f"Welcome {user.name}")
                return redirect('users:SearchBooks')
            messages.error(request, "Account not approved yet.")
        except UserRegistrationModel.DoesNotExist:
            messages.error(request, "Invalid login ID or password.")
        return redirect('admins:user-login')

class LogoutView(View):
    def get(self, request):
        request.session.flush()
        messages.info(request, "Logged out.")
        return redirect('admins:index')

# AddBookAction, AdminHome, ViewBooks, etc. remain same if desired,
# but ensure they use proper class-based or function-based structure similarly.
