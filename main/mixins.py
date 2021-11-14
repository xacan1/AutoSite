menu = {'На главную': 'home', 'О сайте': 'about', 'Добавить новость': 'add_post', 'Обратная связь': 'feedback',
        'Автонормы': 'autonorms', 'Войти': 'login', 'Регистрация': 'registration', 'Выйти': 'logout'}


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        user_menu = menu.copy()

        if not self.request.user.is_authenticated:
            user_menu.pop('Обратная связь')
            user_menu.pop('Добавить новость')
            user_menu.pop('Выйти')
        elif not self.request.user.is_staff:
            user_menu.pop('Добавить новость')
            user_menu[self.request.user.email] = 'profile'
            user_menu.pop('Войти')
            user_menu.pop('Регистрация')
        else:
            user_menu.pop('Обратная связь')
            user_menu[self.request.user.email] = 'profile'
            user_menu.pop('Войти')
            user_menu.pop('Регистрация')

        context['menu'] = user_menu
        return context
