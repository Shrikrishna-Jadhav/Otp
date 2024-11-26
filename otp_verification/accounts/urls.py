from django.urls import path
from .views import register, verify_otp, profile
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
def home(request):
    return redirect('login')

urlpatterns = [
    path('', home, name='home'), 
    path('register/', register, name='register'),
    path('verify/<int:user_id>/', verify_otp, name='verify_otp'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/registration.html'), name='login'),  # Changed 'registration' to 'login'
    path('profile/', profile, name='profile'),
]
