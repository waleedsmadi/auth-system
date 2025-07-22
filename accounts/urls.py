from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('sign_up/', views.sign_up, name='sign_up'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('find-account/', views.find_account, name='find_account'),
    path('confirm-code/<uuid:reset_uuid>/', views.confirm_code, name='confirm_code'),
    path('reset-password/<str:confirm_code>/', views.reset_password, name='reset_password'),
    path('<str:username>/', views.view_account, name='view_account'),
    path('activation/<uuid:token>/', views.active_account, name='active_account'),
    path('reactivation/<uuid:token>/', views.resend_token_email, name='reactive_account'),
]
