from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomUser, Post
from .forms import AddPostForm, RegisterUserForm, SendFeedbackForm
from .mixins import DataMixin, menu


def page_not_found(request, exception):
    return HttpResponseNotFound('<h2>Упс! Похоже такой страницы нет!</h2>')


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
    login_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавить новость')
        return {**context, **c_def}


def about(request):
    template = 'main/about.html'
    content = {'title': 'О сайте', 'menu': menu}
    return render(request, template, content)


def feedback(request):
    page = None

    if request.method == 'POST':
        form = SendFeedbackForm(request.POST)

        if form.is_valid():
            page = redirect('home')
    else:
        form = SendFeedbackForm()

    if not page:
        template = 'main/feedback.html'
        content = {'title': 'Обратная связь', 'menu': menu, 'form': form}
        page = render(request, template, content)

    return page


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'main/registration.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return {**context, **c_def}


def login(request):
    return redirect('home')


def profile(request):
    return redirect('home')
