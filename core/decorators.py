from functools import wraps
from django.shortcuts import redirect


def required_login(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('accounts:login')
        return func(request, *args, **kwargs)
    return wrapper
