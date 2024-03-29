# from django.shortcuts import render
# from django.http import HttpResponseNotFound
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView, UpdateView
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from main.models import CustomUser, Post
from main.forms import AddPostForm, RegisterUserForm, FeedbackForm, LoginUserForm, ProfileUserEditForm, PasswordChangeForm, SimpleForm
from main.mixins import DataMixin


class PageNotFound(FormView):
    form_class = SimpleForm
    template_name = 'main/page404.html'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        response.status_code = 404
        return response


class LoginUser(DataMixin, auth_views.LoginView):
    form_class = LoginUserForm
    template_name = 'main/login.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            title='Авторизация', form_login=LoginUserForm)
        return {**context, **c_def}

    def get_success_url(self):
        return reverse_lazy('home')


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'main/registration.html'
    success_url = reverse_lazy('registration_successful')

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            title='Регистрация', form_login=LoginUserForm)
        return {**context, **c_def}


class RegistrationSuccessful(DataMixin, FormView):
    form_class = SimpleForm
    template_name = 'main/success_registration.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Вы зарегистрировались!')
        return {**context, **c_def}


class LogoutUser(auth_views.LogoutView):
    next_page = 'home'


class MainIndex(DataMixin, FormView):
    form_class = SimpleForm
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            title='Автонормы - бесплатная база норм времени',
            form_login=LoginUserForm)
        return {**context, **c_def}


class ShowPost(DataMixin, DetailView):
    model = Post
    template_name = 'main/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            title='Новость', form_login=LoginUserForm)
        return {**context, **c_def}


class AddPost(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'main/add_post.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавить новость')
        return {**context, **c_def}


# def feedback(request):
#     page = None
#
#     if request.method == 'POST':
#         form = FeedbackForm(request.POST)
#
#         if form.is_valid():
#             page = redirect('home')
#     else:
#         form = FeedbackForm()
#
#     if not page:
#         template = 'main/feedback.html'
#         content = {'title': 'Обратная связь', 'menu': menu, 'form': form}
#         page = render(request, template, content)
#
#     return page
class FeedbackFormView(DataMixin, FormView):
    form_class = FeedbackForm
    template_name = 'main/feedback.html'
    success_url = 'home'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Сообщение')
        return {**context, **c_def}


class ProfileUser(DataMixin, DetailView):
    model = CustomUser
    template_name = 'main/profile.html'
    context_object_name = 'user_data'
    pk_url_kwarg = 'user_id'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Профиль пользователя')
        return {**context, **c_def}


class ProfileUserEdit(DataMixin, UpdateView):
    form_class = ProfileUserEditForm
    model = CustomUser
    template_name = 'main/profile_edit.html'
    pk_url_kwarg = 'user_id'
    success_url = reverse_lazy('autonorms')
    # fields = ('phone', 'cost_per_hour',)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Изменение профиля')
        return {**context, **c_def}


class About(DataMixin, FormView):
    form_class = SimpleForm
    template_name = 'main/about.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            title='О сайте', form_login=LoginUserForm)
        return {**context, **c_def}


class Features(DataMixin, FormView):
    form_class = SimpleForm
    template_name = 'main/features.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            title='Возможности', form_login=LoginUserForm)
        return {**context, **c_def}


class MyPasswordResetView(DataMixin, auth_views.PasswordResetView):
    template_name = 'main/password_reset.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            title='Сброс пароля', form_login=LoginUserForm)
        return {**context, **c_def}


class MyPasswordChangeView(DataMixin, auth_views.PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'main/password_change.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Изменение пароля')
        return {**context, **c_def}


class MyPasswordChangeDoneView(DataMixin, auth_views.PasswordChangeDoneView):
    template_name = 'main/password_change_done.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Пароль успешно изменен!')
        return {**context, **c_def}


class MyPasswordResetConfirmView(DataMixin, auth_views.PasswordResetConfirmView):
    template_name = 'main/password_reset_confirm.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            title='Установите новый пароль', form_login=LoginUserForm)
        return {**context, **c_def}


class MyPasswordResetDoneView(DataMixin, auth_views.PasswordResetDoneView):
    template_name = 'main/password_reset_done.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            title='Письмо с инструкциями по восстановлению пароля отправлено', form_login=LoginUserForm)
        return {**context, **c_def}


class MyPasswordResetCompleteView(DataMixin, auth_views.PasswordResetCompleteView):
    template_name = 'main/password_reset_complete.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            title='Восстановление пароля завершено', form_login=LoginUserForm)
        return {**context, **c_def}


# форма регистрации через админку с капчей
class MyAdminLoginView(auth_views.LoginView):
    # тут интересно, что шаблон находится вовсе не в этом приложении, до его поиска просто не доходит очередь
    # так как в settings указано, что сначала ищем все шаблоны в корне приложения: 'DIRS': [BASE_DIR / 'templates'],
    # по этому admin/login.html - это путь от корня проекта
    template_name = 'admin/login.html'
    form_class = LoginUserForm
