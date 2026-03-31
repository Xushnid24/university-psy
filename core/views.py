from django.shortcuts import render


def home_view(request):
    return render(request, 'core/home.html')


def dashboard_view(request):
    if not request.user.is_authenticated:
        return render(request, 'core/home.html')

    if request.user.role == 'student':
        return render(request, 'core/student_dashboard.html')

    elif request.user.role == 'psychologist':
        return render(request, 'core/psychologist_dashboard.html')

    elif request.user.role == 'admin':
        return render(request, 'core/admin_dashboard.html')

    return render(request, 'core/home.html')