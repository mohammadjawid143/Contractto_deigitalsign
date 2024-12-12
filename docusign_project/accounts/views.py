from django.shortcuts import render
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.conf import settings
from accounts.forms import RegisterForm, LoginForm
from django.views import View
from django.urls import reverse




# Create your views here.

# def my_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request=request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             if request.GET.get('next'):
#                 return HttpResponseRedirect(request.GET.get("next"))
#             return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
#         else:
#             context = {
#                 "username": username,
#                 "errorMessage": "User name by this info could't found"
#             }
#             return render(request, "accounts/login.html", context)

#     return render(request, "accounts/login.html", {})

class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        context = {'login_form': login_form}
        return render(request, 'accounts/login.html', context)

    def post(self, request: HttpRequest):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = login_form.cleaned_data.get('user_name')
            user_pass = login_form.cleaned_data.get('password')
            user: User = User.objects.filter(username__iexact=user_name).first()
            if user:
                is_password_correct = user.check_password(user_pass)
                if is_password_correct:
                    login(request, user)
                    return redirect(reverse('home'))
                else:
                    login_form.add_error('user_name', 'Incorrect password.')
            else:
                login_form.add_error('user_name', 'User not found.')

        context = {'login_form': login_form}
        return render(request, 'accounts/login.html', context)


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        context = {
            'register_form': register_form
        }
        return render(request, 'accounts/register.html', context)

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = register_form.cleaned_data.get('user_name')
            user_password = register_form.cleaned_data.get('password')
            user_exists = User.objects.filter(username__iexact=user_name).exists()
            if user_exists:
                register_form.add_error('user_name', 'This User name already exists.')
            else:
                new_user = User.objects.create_user(
                    username=user_name,
                    email=user_name,
                    password=user_password
                )
                new_user.save()
                return redirect(reverse('login_page'))

        context = {
            'register_form': register_form
        }
        return render(request, 'accounts/register.html', context)

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('login_page'))