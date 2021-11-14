# from django.shortcuts import render
# from django.http import HttpResponseNotFound
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomUser, Post
from .forms import AddPostForm, RegisterUserForm, FeedbackForm, LoginUserForm, SimpleForm
from .mixins import DataMixin


class PageNotFound(FormView):
    form_class = SimpleForm
    template_name = 'main/page404.html'


class MainIndex(DataMixin, ListView):
    model = Post
    template_name = 'main/index.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        return Post.objects.filter(is_published=True).order_by('-time_create')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Автонормы')
        return {**context, **c_def}


class ShowPost(DataMixin, DetailView):
    model = Post
    template_name = 'main/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Новость')
        return {**context, **c_def}


class AddPost(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'main/add_post.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавить новость')
        return {**context, **c_def}


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'main/registration.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return {**context, **c_def}


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'main/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return {**context, **c_def}

    def get_success_url(self):
        return reverse_lazy('home')


class LogoutUser(LogoutView):
    next_page = 'home'


class ProfileUser(DataMixin, DetailView):
    model = CustomUser
    template_name = 'main/profile.html'
    context_object_name = 'user_data'
    pk_url_kwarg = 'user_id'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Профиль пользователя')
        return {**context, **c_def}


class About(DataMixin, FormView):
    form_class = SimpleForm
    template_name = 'main/about.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='О сайте')
        return {**context, **c_def}
