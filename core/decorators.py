from functools import wraps
from django.shortcuts import redirect
from accounts.models import AuthToken


def required_login(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        token = request.COOKIES.get('auth_token')

        if not token:
            return redirect('accounts:login')
        
        try:
            user_token = AuthToken.objects.get(key=token)
            request.user = user_token.user
        except AuthToken.DoesNotExist:
            return redirect('accounts:login')
        return func(request, *args, **kwargs)
    return wrapper
