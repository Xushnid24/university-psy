from django.urls import path
from .views import (
    test_list_view,
    create_test_view,
    edit_test_view,
    delete_test_view,
    add_question_view,
    edit_question_view,
    delete_question_view,
    add_answer_option_view,
    edit_answer_option_view,
    delete_answer_option_view,
    pass_test_view,
    test_result_view,
)

urlpatterns = [
    path('', test_list_view, name='test_list'),
    path('create/', create_test_view, name='create_test'),

    path('<int:test_id>/edit/', edit_test_view, name='edit_test'),
    path('<int:test_id>/delete/', delete_test_view, name='delete_test'),

    path('<int:test_id>/add-question/', add_question_view, name='add_question'),
    path('question/<int:question_id>/edit/', edit_question_view, name='edit_question'),
    path('question/<int:question_id>/delete/', delete_question_view, name='delete_question'),

    path('question/<int:question_id>/add-answer/', add_answer_option_view, name='add_answer_option'),
    path('answer/<int:option_id>/edit/', edit_answer_option_view, name='edit_answer_option'),
    path('answer/<int:option_id>/delete/', delete_answer_option_view, name='delete_answer_option'),

    path('<int:test_id>/pass/', pass_test_view, name='pass_test'),
    path('result/<int:result_id>/', test_result_view, name='test_result'),
]