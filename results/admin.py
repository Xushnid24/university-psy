from django.contrib import admin
from .models import TestResult, StudentAnswer


class StudentAnswerInline(admin.TabularInline):
    model = StudentAnswer
    extra = 0
    readonly_fields = ('question', 'selected_option')


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'test', 'total_score', 'level', 'created_at')
    list_filter = ('level', 'created_at', 'test')
    search_fields = ('student__full_name', 'test__title')
    inlines = [StudentAnswerInline]


@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'result', 'question', 'selected_option')
