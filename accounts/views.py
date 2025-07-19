from django.shortcuts import render, redirect
from .forms import SignUpModelForm
from .models import MyUser
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings
from uuid import uuid4
from django.utils import timezone
from datetime import timedelta


def sign_up(request):
    if request.method == 'POST':
        form = SignUpModelForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            send_token_email(user)
            return render(request, 'accounts/activation_status.html', {'send_link': 'Activate The Account', 'user': user})
    else:
        form = SignUpModelForm()

    return render(request, 'accounts/sign_up.html', {'sign_up_form': form})



def send_token_email(user):
    link = f'http://127.0.0.1:8000/activation/{user.email_token}'
    subject = 'Active Your Account'
    message = f'Hello {user.first_name}\nPlease active your account by click the link below:\n{link}'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])



def resend_token_email(request, token):
    user = MyUser.objects.get(email_token=token)
    if user.is_verified:
        return render(request, 'accounts/activation_status.html', {'verified': 'The account is activated'})
    
    user.email_token = uuid4()
    user.creation_date = timezone.now()
    user.save()
    send_token_email(user)
    return render(request, 'accounts/activation_status.html', {'send_link': 'Activate The Account', 'user': user})



def active_account(request, token):
    try:
        user = MyUser.objects.get(email_token=token)
    except MyUser.DoesNotExist:
        return render(request, 'accounts/activation_status.html', {'invalid_token': 'Invalid Link'})
    
    if user.creation_date < (timezone.now() - timedelta(hours=1)):
        return render(request, 'accounts/activation_status.html', {'expired_time': 'Activation Time Has Expired', 'token': user.email_token})
    
    user.email_token = uuid4()
    user.is_verified = True
    user.save()
    return redirect('accounts:login')




def login(request):
    return render(request, 'accounts/login.html')
