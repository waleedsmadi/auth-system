from accounts.models import MyUser, AuthToken

def logged_in_user(request):
    token = request.COOKIES.get('auth_token')

    if token:
        try:
            user_token = AuthToken.objects.get(key=token)
            return {'logged_user': user_token.user}
        except MyUser.DoesNotExist:
            pass
    return {'logged_user': None}
