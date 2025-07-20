def logged_in_status(request):
    status = request.session.get('user_id')
    return {'is_logged_in': status}
