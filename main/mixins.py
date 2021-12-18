user_menu = {'Войти': 'login',
             'Регистрация': 'registration', 'Выйти': 'logout'}
menu = {'На главную': 'home', 'О сайте': 'about', 'Добавить новость': 'add_post',
        'Обратная связь': 'feedback', 'Автонормы': 'autonorms'}


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context_menu = menu.copy()
        context_user_menu = user_menu.copy()

        if not self.request.user.is_authenticated:
            context_menu.pop('Обратная связь')
            context_menu.pop('Добавить новость')
            context_user_menu.pop('Выйти')
        elif not self.request.user.is_staff:
            context_menu.pop('Добавить новость')
            context_user_menu[self.request.user.email] = 'profile'
            context_user_menu.pop('Войти')
            context_user_menu.pop('Регистрация')
        else:
            context_menu.pop('Обратная связь')
            context_user_menu[self.request.user.email] = 'profile'
            context_user_menu.pop('Войти')
            context_user_menu.pop('Регистрация')

        context['user_menu'] = context_user_menu
        context['menu'] = context_menu
        return context

    def check_requests_limit(self):
        result = False
        print(
            f"{self.request.user.email} ip: {self.request.META.get('REMOTE_ADDR')}: {self.request.session['number_requests']} request in {self.request.user.request_limit}")

        if self.request.session['number_requests'] > self.request.user.request_limit:
            self.request.session['number_requests'] = 0
            result = True

        return result
