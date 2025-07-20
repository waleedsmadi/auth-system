from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('sign_up/', views.sign_up, name='sign_up'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('activation/<uuid:token>/', views.active_account, name='active_account'),
    path('reactivation/<uuid:token>/', views.resend_token_email, name='reactive_account'),
]
