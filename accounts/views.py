from django.shortcuts import render
from django.contrib.auth import views as auth_views
from main.forms import LoginUserForm
from main.mixins import DataMixin


class MyPasswordChangeView(DataMixin, auth_views.PasswordChangeView):
    template_name = 'accounts/password_change.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Изменение пароля')
        return {**context, **c_def}


class MyPasswordChangeDoneView(DataMixin, auth_views.PasswordChangeDoneView):
    template_name = 'accounts/password_change_done.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Пароль успешно изменен!')
        return {**context, **c_def}


class MyPasswordResetView(DataMixin, auth_views.PasswordResetView):
    template_name = 'accounts/password_reset.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            title='Сброс пароля', form_login=LoginUserForm)
        return {**context, **c_def}


class MyPasswordResetConfirmView(DataMixin, auth_views.PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            title='Установите новый пароль', form_login=LoginUserForm)
        return {**context, **c_def}


class MyPasswordResetDoneView(DataMixin, auth_views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            title='Письмо с инструкциями по восстановлению пароля отправлено', form_login=LoginUserForm)
        return {**context, **c_def}


class MyPasswordResetCompleteView(DataMixin, auth_views.PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Восстановление пароля завершено', form_login=LoginUserForm)
        return {**context, **c_def}
