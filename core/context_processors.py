from accounts.models import MyUser

def logged_in_user(request):
    user_id = request.session.get('user_id')
    if user_id:
        try:
            user = MyUser.objects.get(id=user_id)
            return {'logged_user': user}
        except MyUser.DoesNotExist:
            pass
    return {'logged_user': None}
