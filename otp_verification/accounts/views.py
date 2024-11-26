import random
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import CustomUser
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def generate_otp():
    return str(random.randint(100000, 999999))

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.otp = generate_otp()
            user.is_active = False
            user.save()
            send_mail(
                'Your OTP Verification Code',
                f'Your OTP is {user.otp}',
                'your_email@example.com',
                [user.email],
                fail_silently=False,
            )
            return redirect('verify_otp', user_id=user.id)
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def verify_otp(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    if request.method == 'POST':
        entered_otp = request.POST['otp']
        if user.otp == entered_otp:
            user.is_verified = True
            user.is_active = True
            user.otp = None
            user.save()
            return redirect('registration')  # Replace 'login' with your login URL name
        else:
            return render(request, 'accounts/verify_otp.html', {'error': 'Invalid OTP'})
    return render(request, 'accounts/verify_otp.html')


@login_required
def profile(request):
    print("User logged in:", request.user.is_authenticated)
    return render(request, 'accounts/profile.html')


