from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib import messages
from Users.models import UserRegistrationModel
from django.contrib.auth.views import LogoutView

class IndexView(TemplateView):
    template_name = 'base.html'

class AdminLoginView(TemplateView):
    template_name = 'AdminLogin.html'

class UserLoginView(TemplateView):
    template_name = 'UserLogin.html'

class UserRegisterView(TemplateView):
    template_name = 'UserRegister.html'

class AdminLoginAction(View):
    def post(self, request):
        admin_username = request.POST.get('loginid')
        admin_password = request.POST.get('password')

        if admin_username == 'Admin' and admin_password == 'Admin':
            return render(request, 'admins/AdminHome.html')
        else:
            messages.error(request, 'Please check your login details.')
            return redirect('AdminLogin')

class UserRegisterAction(View):
    def post(self, request):
        data = request.POST
        name = data.get('name')
        loginID = data.get('loginID')
        password = data.get('password')
        gender = data.get('gender')
        email = data.get('email')
        phoneNumber = data.get('phoneNumber')
        address = data.get('address')

        if UserRegistrationModel.objects.filter(loginID=loginID).exists():
            messages.error(request, 'Login ID already exists.')
            return redirect('UserRegister')

        if UserRegistrationModel.objects.filter(email=email).exists():
            messages.error(request, 'Email ID already exists.')
            return redirect('UserRegister')

        UserRegistrationModel.objects.create(
            name=name,
            loginID=loginID,
            password=password,
            gender=gender,
            email=email,
            phoneNumber=phoneNumber,
            address=address,
            status='Pending'
        )
        messages.success(request, 'Registration successful! Please wait for admin approval.')
        return redirect('UserRegister')

class UserLoginAction(View):
    def post(self, request):
        loginID = request.POST.get('loginID')
        password = request.POST.get('password')

        try:
            user = UserRegistrationModel.objects.get(loginID=loginID, password=password)
            if user.status == "Approved":
                request.session['userid'] = user.id
                request.session['username'] = user.name
                messages.success(request, f"Welcome {user.name}!")
                return redirect('UserHome')
            else:
                messages.error(request, "Your account is not approved yet.")
        except UserRegistrationModel.DoesNotExist:
            messages.error(request, "Invalid Login ID or Password.")

        return redirect('UserLogin')

class LogoutView(View):
    def get(self, request):
        request.session.flush()
        messages.info(request, "Logged out successfully.")
        return redirect('index')