from django.urls import path
from .views import result_list_view

urlpatterns = [
    path('', result_list_view, name='result_list'),
]