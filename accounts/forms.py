from django import forms
from .models import MyUser


class SignUpModelForm(forms.ModelForm):

    class Meta:
        model = MyUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'birth_date', 'gender']
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Username...',
                'class': 'form-control',
                'style': 'margin-bottom: 14px'
            }),

            'first_name': forms.TextInput(attrs={
                'placeholder': 'First Name...',
                'class': 'form-control',
                'style': 'margin-bottom: 14px'
            }),

            'last_name': forms.TextInput(attrs={
                'placeholder': 'Last Name...',
                'class': 'form-control',
                'style': 'margin-bottom: 14px'
            }),

            'email': forms.EmailInput(attrs={
                'placeholder': 'Email...',
                'class': 'form-control',
                'style': 'margin-bottom: 14px'
            }),

            'password': forms.PasswordInput(attrs={
                'placeholder': 'Password...',
                'class': 'form-control',
                'style': 'margin-bottom: 14px'
            }),

            'birth_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'style': 'margin-bottom: 14px'
            }),

            'gender': forms.Select(attrs={
                'class': 'form-select',
                'style': 'margin-bottom: 14px'
            }),
        }



class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'Username/Email...',
        'class': 'form-control',
        'style': 'margin-bottom: 15px',
    }))

    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={
        'placeholder': 'Password...',
        'class': 'form-control',
        'style': 'margin-bottom: 15px',
    }))
