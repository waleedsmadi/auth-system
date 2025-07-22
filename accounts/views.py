from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpModelForm, LoginForm, EditProfileModelForm, ChangePasswordForm
from .models import MyUser
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.conf import settings
from uuid import uuid4
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from django.contrib import messages
from core.decorators import required_login

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
        return render(request, 'accounts/activation_status.html', {'verified': 'The Account Is Activated'})
    
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
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']

            try:
                user = MyUser.objects.get(Q(username=username) | Q(email=username))
            except:
                messages.error(request, 'Invalid email or password!')
                return redirect('accounts:login')
            
            
            password = form.cleaned_data['password']
            if not check_password(password, user.password):
                messages.error(request, 'Invalid email or password!')
                return redirect('accounts:login')
            
            if not user.is_verified:
                messages.error(request, 'This account has not been activated yet!')
                return redirect('accounts:login')
            
            request.session['user_id'] = user.id
            return redirect('pages:index')

    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'login_form': form})



def logout(request):
    if request.session.get('user_id'):
        request.session.flush()
    return redirect('accounts:login')


@required_login
def edit_profile(request):
    user_id = request.session.get('user_id')
    user = MyUser.objects.get(id=user_id)
    if request.method == 'POST':
        form = EditProfileModelForm(data=request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('pages:index')
    else:
        form = EditProfileModelForm(instance=user)
    
    return render(request, 'accounts/edit_profile.html', {'edit_form': form})


@required_login
def change_password(request):

    user_id = request.session.get('user_id')
    user = MyUser.objects.get(id=user_id)
    if request.method == 'POST':
        form = ChangePasswordForm(data=request.POST)

        if form.is_valid():
            password = form.cleaned_data['current_password']
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']

            # Check if current password is invalid
            if not check_password(password, user.password):
                messages.error(request, 'Current password is invalid!')
                return redirect('accounts:change_password')
            
            # Check if new password and current password are similar
            elif check_password(new_password, user.password):
                messages.error(request, 'The new and current passwords are similar!')
                return redirect('accounts:change_password')
            
            # Check if confirm password and new password are not the same!
            elif new_password != confirm_password:
                messages.error(request, 'Confirm password does not match the new password!')
                return redirect('accounts:change_password')
            
            # change the password (hash)
            else:
                user.password = make_password(new_password)
                user.save()
                messages.success(request, 'Password has been changed!')
                return redirect('accounts:change_password')
    else:
        form = ChangePasswordForm()
    return render(request, 'accounts/change_password.html', {'change_password_form': form})


@required_login
def view_account(request, username):
    user = get_object_or_404(MyUser, username=username)
    return render(request, 'accounts/account.html', {"user": user})