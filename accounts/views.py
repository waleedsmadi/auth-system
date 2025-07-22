from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import *
from .models import MyUser, AuthToken
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.conf import settings
from uuid import uuid4
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from django.contrib import messages
from core.decorators import required_login
import secrets

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
            
            token = secrets.token_urlsafe(32)
            auth_token = AuthToken(key=token, user=user)
            auth_token.save()
            response = redirect('pages:index')
            response.set_cookie('auth_token', token, httponly=True, max_age=60*60*24*30)
            return response

    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'login_form': form})



def logout(request):
    token = request.COOKIES.get('auth_token')
    if token:
        AuthToken.objects.filter(key=token).delete()
    
    response = redirect('accounts:login')
    response.delete_cookie('auth_token')
    return response




@required_login
def edit_profile(request):
    user = request.user
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

    user = request.user
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
    posts = user.posts.all()
    return render(request, 'accounts/account.html', {"user": user, 'posts': posts})




def find_account(request):
    if request.method == 'POST':
        form = FindAccountForm(data=request.POST)
        if form.is_valid():
            try:
                user = MyUser.objects.get(email=form.cleaned_data['email'])
            except MyUser.DoesNotExist:
                messages.error(request, 'No result: this email does not exists, please try with another email!')
                return redirect('accounts:find_account')
            
            reset_uuid = uuid4()
            code = uuid4().hex[:6]
            user.confirm_code = code
            user.reset_uuid = reset_uuid
            user.save()
            send_reset_password_code(user)
            return redirect('accounts:confirm_code', reset_uuid=reset_uuid)
    else:
        form = FindAccountForm()
    return render(request, 'accounts/find_account.html', {'find_account_form': form})



def confirm_code(request, reset_uuid):
    try:
        user = MyUser.objects.get(reset_uuid=reset_uuid)
    except MyUser.DoesNotExist:
        return HttpResponse('Does not exist!')
    
    if request.method == 'POST':
        form = ConfirmCodeForm(data=request.POST)
        if form.is_valid():
            if user.confirm_code == form.cleaned_data['confirm_code']:
                return redirect('accounts:reset_password', confirm_code=user.confirm_code)
            
            messages.error(request, 'error')
            return redirect('accounts:confirm_code', reset_uuid)
    else:
        form = ConfirmCodeForm()
    
    return render(request, 'accounts/confirm_code.html', {'confirm_code_form': form})




def reset_password(request, confirm_code):
    try:
        user = MyUser.objects.get(confirm_code=confirm_code)
    except MyUser.DoesNotExist:
        return HttpResponse('Invalid link!')

    if request.method == 'POST':
        form = ResetPasswordForm(data=request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']

            if confirm_password != new_password:
                messages.error(request, 'Confirm password does not match the new password!')
                return redirect('accounts:reset_password', confirm_code=user.confirm_code)
            else:
                user.password = make_password(form.cleaned_data['new_password'])
                user.reset_uuid = None
                user.confirm_code = None
                user.save()
                return redirect('accounts:login')
                
    else:
        form = ResetPasswordForm()
    return render(request, 'accounts/reset_password.html', {'reset_password_form': form})
    


    
def send_reset_password_code(user):
    subject = 'Reset Your Password'
    message = f'Hello {user.first_name}\nYour confirm code is: {user.confirm_code}'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])
