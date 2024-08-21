from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpRequest, HttpResponseNotFound, HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm

# Create your views here.


def sign_in(request: HttpRequest):

    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'users/login.html', {'form': form})

    elif request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password_one = form.cleaned_data['password_one']
            password_two = form.cleaned_data['password_two']
            user = authenticate(request, username=username, password_one=password_one, password_two=password_two)

            # Вот здесь добавление пользователя в БД

            if user:
                login(request, user)
                messages.success(request, f'Привет, {username.title()}, добро пожаловать!')
                # return redirect('posts')
                # Вот здесь что-то другое нужно
                # здесь редирект на главную страницу

        # form is not valid or user is not authenticated
        messages.error(request, f'Неправильный логин или пароль')
        return render(request, 'users/login.html', {'form': form})


"""
Типа сначала нужно приложения создать
да, там есть логин_ин, логин аут и регистрация
но обработки нет кнопок, если неправильные символы вводятся




"""


def sign_out(request):
    logout(request)
    messages.success(request,f'Вы вышли из своего профиля')
    return redirect('login')