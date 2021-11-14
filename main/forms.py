from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Post


class SimpleForm(forms.Form):
    pass


class FeedbackForm(forms.Form):
    title = forms.CharField(max_length=100, label='Заголовок')
    text = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}), label='Текст сообщения')
    select = forms.ChoiceField(
        choices=(
            (1, 'Безнадежно'), (2, 'Плохо'), (3, 'Сойдет'), (4, 'Хорошо, но...'),
            (5, 'Отлично! Куда деньги закинуть?')),
        label='Оценка сайта')


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2', 'company', 'inn', 'phone')
        widgets = {'email': forms.EmailInput(attrs={'class': 'form-input'}),
                   'password1': forms.PasswordInput(attrs={'class': 'form-input'}),
                   'password2': forms.PasswordInput(attrs={'class': 'form-input'}),
                   'company': forms.TextInput(attrs={'class': 'form-input'}),
                   'inn': forms.TextInput(attrs={'class': 'form-input'}),
                   'phone': forms.TextInput(attrs={'class': 'form-input'})}


class LoginUserForm(AuthenticationForm):
    username = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    # fields = ('email', 'password')
    # widgets = {'email': forms.EmailInput(attrs={'class': 'form-input'}),
    #            'password': forms.PasswordInput(attrs={'class': 'form-input'})}
