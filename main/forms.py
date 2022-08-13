from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import *


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        widgets = {
            'first_name': forms.TextInput(attrs={'required': True, 'pattern': '[A-Za-zА-Яа-яЁё]{3,20}'}),
            'last_name': forms.TextInput(attrs={'required': True, 'pattern': '[A-Za-zА-Яа-яЁё]{3,20}'}),
            'email': forms.EmailInput(attrs={'required': True, 'onfocus': "this.type='email'", 'onblur':
                "var re = /[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?/;"
                "if (!re.test(String(this.value).toLowerCase())) {this.value=''}"})
        }