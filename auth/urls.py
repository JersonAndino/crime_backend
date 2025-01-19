from django.urls import path
from . import views

urlpatterns = [
    path('create-user/', views.create_user, name='create_user'),
    path('edit-user/', views.edit_user, name='edit_user'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('logout/', views.logout_user, name='logout_user'),
    path('csrf-token/', views.csrf_token, name='csrf_token'),
]
