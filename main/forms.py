from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Post


class SimpleForm(forms.Form):
    pass


class FeedbackForm(forms.Form):
    title = forms.CharField(max_length=100, label='Заголовок', widget=forms.TextInput(attrs={'class': 'form-control'}))
    text = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10, 'class': 'form-control'}), label='Текст сообщения')
    select = forms.ChoiceField(
        choices=(
            (1, 'Безнадежно'), (2, 'Плохо'), (3, 'Сойдет'), (4, 'Хорошо, но...'),
            (5, 'Отлично! Куда деньги закинуть?')),
        label='Оценка сайта', widget=forms.Select(attrs={'class': 'form-select'}))


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        


class RegisterUserForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ('email', 'company', 'inn', 'phone')
        widgets = {'email': forms.EmailInput(attrs={'class': 'form-control'}),
                   'company': forms.TextInput(attrs={'class': 'form-control'}),
                   'inn': forms.TextInput(attrs={'class': 'form-control'}),
                   'phone': forms.TextInput(attrs={'class': 'form-control'})}


class LoginUserForm(AuthenticationForm):
    username = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    # fields = ('email', 'password')
    # widgets = {'email': forms.EmailInput(attrs={'class': 'form-input'}),
    #            'password': forms.PasswordInput(attrs={'class': 'form-input'})}
