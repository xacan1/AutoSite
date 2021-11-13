from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Post


class SendFeedbackForm(forms.Form):
    title = forms.CharField(max_length=100, label='Заголовок')
    text = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}), label='Текст сообщения')
    select = forms.ChoiceField(
        choices=(
            (1, 'Безнадежно'), (2, 'Плохо'), (3, 'Пойдет'), (4, 'Хорошо, но...'),
            (5, 'Отлично! Куда деньги закинуть?')),
        label='Оценка сайта')


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2')
