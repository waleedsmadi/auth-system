from django.shortcuts import render, redirect
from .forms import SignUpModelForm
from .models import MyUser
from django.contrib.auth.hashers import make_password


def sign_up(request):
    if request.method == 'POST':
        form = SignUpModelForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            return redirect('accounts:login')
    else:
        form = SignUpModelForm()

    return render(request, 'accounts/sign_up.html', {'sign_up_form': form})


def login(request):
    return render(request, 'accounts/login.html')