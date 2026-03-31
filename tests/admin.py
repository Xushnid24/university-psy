from django.contrib import admin
from .models import Test, Question, AnswerOption


class AnswerOptionInline(admin.TabularInline):
    model = AnswerOption
    extra = 2


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'is_active', 'created_at')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerOptionInline]


@admin.register(AnswerOption)
class AnswerOptionAdmin(admin.ModelAdmin):
    pass
