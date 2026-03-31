from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import (
    RegisterForm,
    LoginForm,
    AdminResetPasswordForm,
    AdminChangeRoleForm
)
from .models import User


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Регистрация прошла успешно. Теперь войдите в систему.')
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            user = authenticate(username=phone_number, password=password)

            if user is not None:
                if not user.is_active:
                    messages.error(request, 'Ваш аккаунт отключён. Обратитесь к администратору.')
                    return redirect('login')

                login(request, user)
                return redirect('dashboard')
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def user_list_view(request):
    if request.user.role not in ['admin', 'psychologist']:
        return redirect('dashboard')

    query = request.GET.get('q', '').strip()

    users = User.objects.all().order_by('id')

    if query:
        users = users.filter(
            Q(full_name__icontains=query) |
            Q(phone_number__icontains=query) |
            Q(role__icontains=query)
        )

    return render(request, 'users/user_list.html', {
        'users': users,
        'query': query
    })


@login_required
def reset_user_password_view(request, user_id):
    if request.user.role != 'admin':
        return redirect('dashboard')

    target_user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = AdminResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password1']
            target_user.set_password(new_password)
            target_user.save()

            messages.success(
                request,
                f'Пароль для пользователя "{target_user.full_name}" успешно обновлён.'
            )
            return redirect('user_list')
    else:
        form = AdminResetPasswordForm()

    return render(request, 'users/reset_user_password.html', {
        'form': form,
        'target_user': target_user
    })


@login_required
def change_user_role_view(request, user_id):
    if request.user.role != 'admin':
        return redirect('dashboard')

    target_user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = AdminChangeRoleForm(request.POST, instance=target_user)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                f'Роль пользователя "{target_user.full_name}" успешно обновлена.'
            )
            return redirect('user_list')
    else:
        form = AdminChangeRoleForm(instance=target_user)

    return render(request, 'users/change_user_role.html', {
        'form': form,
        'target_user': target_user
    })


@login_required
def toggle_user_active_view(request, user_id):
    if request.user.role != 'admin':
        return redirect('dashboard')

    target_user = get_object_or_404(User, id=user_id)

    if target_user == request.user:
        messages.error(request, 'Вы не можете отключить свой собственный аккаунт.')
        return redirect('user_list')

    if request.method == 'POST':
        target_user.is_active = not target_user.is_active
        target_user.save()

        if target_user.is_active:
            messages.success(request, f'Пользователь "{target_user.full_name}" успешно включён.')
        else:
            messages.success(request, f'Пользователь "{target_user.full_name}" успешно отключён.')

        return redirect('user_list')

    return render(request, 'users/toggle_user_active.html', {
        'target_user': target_user
    })