from django import forms
from django.contrib.auth.forms import AuthenticationForm
from captcha.fields import ReCaptchaField


class SimpleForm(forms.Form):
    pass


class LoginUserForm(AuthenticationForm):
    username = forms.EmailField(label='Email',
                                widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = ReCaptchaField()
