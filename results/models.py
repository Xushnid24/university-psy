from django.db import models
from django.conf import settings
from tests.models import Test, Question, AnswerOption


class TestResult(models.Model):
    LEVEL_CHOICES = [
        ('green', 'Зелёный'),
        ('yellow', 'Жёлтый'),
        ('red', 'Красный'),
    ]

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='test_results'
    )
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name='results'
    )
    total_score = models.IntegerField(default=0)
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student.full_name} - {self.test.title} - {self.level}'


class StudentAnswer(models.Model):
    result = models.ForeignKey(
        TestResult,
        on_delete=models.CASCADE,
        related_name='answers'
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )
    selected_option = models.ForeignKey(
        AnswerOption,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.result.student.full_name} - {self.question.text[:30]}'
