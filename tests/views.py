from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Test, Question, AnswerOption
from .forms import TestForm, QuestionForm, AnswerOptionForm
from results.models import TestResult, StudentAnswer


@login_required
def test_list_view(request):
    tests = Test.objects.filter(is_active=True).order_by('-created_at')

    passed_test_ids = []
    if request.user.role == 'student':
        passed_test_ids = list(
            TestResult.objects.filter(student=request.user).values_list('test_id', flat=True)
        )

    return render(request, 'tests/test_list.html', {
        'tests': tests,
        'passed_test_ids': passed_test_ids
    })


@login_required
def create_test_view(request):
    if request.user.role not in ['psychologist', 'admin']:
        return redirect('home')

    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            test.created_by = request.user
            test.save()
            return redirect('test_list')
    else:
        form = TestForm()

    return render(request, 'tests/create_test.html', {'form': form})


@login_required
def edit_test_view(request, test_id):
    if request.user.role not in ['psychologist', 'admin']:
        return redirect('home')

    test = get_object_or_404(Test, id=test_id)

    if request.user.role == 'psychologist' and test.created_by != request.user:
        return redirect('test_list')

    if request.method == 'POST':
        form = TestForm(request.POST, instance=test)
        if form.is_valid():
            form.save()
            return redirect('test_list')
    else:
        form = TestForm(instance=test)

    return render(request, 'tests/edit_test.html', {
        'form': form,
        'test': test
    })


@login_required
def delete_test_view(request, test_id):
    if request.user.role not in ['psychologist', 'admin']:
        return redirect('home')

    test = get_object_or_404(Test, id=test_id)

    if request.user.role == 'psychologist' and test.created_by != request.user:
        return redirect('test_list')

    if request.method == 'POST':
        test.delete()
        return redirect('test_list')

    return render(request, 'tests/delete_test.html', {'test': test})


@login_required
def add_question_view(request, test_id):
    if request.user.role not in ['psychologist', 'admin']:
        return redirect('home')

    test = get_object_or_404(Test, id=test_id)

    if request.user.role == 'psychologist' and test.created_by != request.user:
        return redirect('test_list')

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.test = test
            question.save()
            return redirect('test_list')
    else:
        form = QuestionForm()

    return render(request, 'tests/add_question.html', {
        'form': form,
        'test': test
    })


@login_required
def edit_question_view(request, question_id):
    if request.user.role not in ['psychologist', 'admin']:
        return redirect('home')

    question = get_object_or_404(Question, id=question_id)

    if request.user.role == 'psychologist' and question.test.created_by != request.user:
        return redirect('test_list')

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('test_list')
    else:
        form = QuestionForm(instance=question)

    return render(request, 'tests/edit_question.html', {
        'form': form,
        'question': question
    })


@login_required
def delete_question_view(request, question_id):
    if request.user.role not in ['psychologist', 'admin']:
        return redirect('home')

    question = get_object_or_404(Question, id=question_id)

    if request.user.role == 'psychologist' and question.test.created_by != request.user:
        return redirect('test_list')

    if request.method == 'POST':
        question.delete()
        return redirect('test_list')

    return render(request, 'tests/delete_question.html', {'question': question})


@login_required
def add_answer_option_view(request, question_id):
    if request.user.role not in ['psychologist', 'admin']:
        return redirect('home')

    question = get_object_or_404(Question, id=question_id)

    if request.user.role == 'psychologist' and question.test.created_by != request.user:
        return redirect('test_list')

    if request.method == 'POST':
        form = AnswerOptionForm(request.POST)
        if form.is_valid():
            answer_option = form.save(commit=False)
            answer_option.question = question
            answer_option.save()
            return redirect('test_list')
    else:
        form = AnswerOptionForm()

    return render(request, 'tests/add_answer_option.html', {
        'form': form,
        'question': question
    })


@login_required
def edit_answer_option_view(request, option_id):
    if request.user.role not in ['psychologist', 'admin']:
        return redirect('home')

    option = get_object_or_404(AnswerOption, id=option_id)

    if request.user.role == 'psychologist' and option.question.test.created_by != request.user:
        return redirect('test_list')

    if request.method == 'POST':
        form = AnswerOptionForm(request.POST, instance=option)
        if form.is_valid():
            form.save()
            return redirect('test_list')
    else:
        form = AnswerOptionForm(instance=option)

    return render(request, 'tests/edit_answer_option.html', {
        'form': form,
        'option': option
    })


@login_required
def delete_answer_option_view(request, option_id):
    if request.user.role not in ['psychologist', 'admin']:
        return redirect('home')

    option = get_object_or_404(AnswerOption, id=option_id)

    if request.user.role == 'psychologist' and option.question.test.created_by != request.user:
        return redirect('test_list')

    if request.method == 'POST':
        option.delete()
        return redirect('test_list')

    return render(request, 'tests/delete_answer_option.html', {'option': option})


@login_required
def pass_test_view(request, test_id):
    if request.user.role != 'student':
        return redirect('home')

    test = get_object_or_404(Test, id=test_id, is_active=True)

    already_passed = TestResult.objects.filter(student=request.user, test=test).exists()
    if already_passed:
        return redirect('home')

    questions = test.questions.all().order_by('order')

    if request.method == 'POST':
        total_score = 0

        result = TestResult.objects.create(
            student=request.user,
            test=test,
            total_score=0,
            level='green'
        )

        for question in questions:
            option_id = request.POST.get(f'question_{question.id}')
            if option_id:
                selected_option = get_object_or_404(
                    AnswerOption,
                    id=option_id,
                    question=question
                )
                total_score += selected_option.score

                StudentAnswer.objects.create(
                    result=result,
                    question=question,
                    selected_option=selected_option
                )

        if total_score <= 5:
            level = 'green'
        elif total_score <= 10:
            level = 'yellow'
        else:
            level = 'red'

        result.total_score = total_score
        result.level = level
        result.save()

        return redirect('home')

    return render(request, 'tests/pass_test.html', {
        'test': test,
        'questions': questions
    })


@login_required
def test_result_view(request, result_id):
    result = get_object_or_404(TestResult, id=result_id)

    if request.user.role not in ['psychologist', 'admin']:
        return redirect('home')

    return render(request, 'tests/test_result.html', {
        'result': result
    })