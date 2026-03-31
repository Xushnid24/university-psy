from django.urls import path
from .views import (
    register_view,
    login_view,
    logout_view,
    user_list_view,
    reset_user_password_view,
    change_user_role_view,
    toggle_user_active_view,
)

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('list/', user_list_view, name='user_list'),
    path('<int:user_id>/reset-password/', reset_user_password_view, name='reset_user_password'),
    path('<int:user_id>/change-role/', change_user_role_view, name='change_user_role'),
    path('<int:user_id>/toggle-active/', toggle_user_active_view, name='toggle_user_active'),
]