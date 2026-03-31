from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import TestResult


@login_required
def result_list_view(request):
    if request.user.role not in ['psychologist', 'admin']:
        return redirect('home')

    results = TestResult.objects.select_related('student', 'test').order_by('-created_at')

    total_results = results.count()
    green_count = results.filter(level='green').count()
    yellow_count = results.filter(level='yellow').count()
    red_count = results.filter(level='red').count()

    context = {
        'results': results,
        'total_results': total_results,
        'green_count': green_count,
        'yellow_count': yellow_count,
        'red_count': red_count,
    }

    return render(request, 'results/result_list.html', context)