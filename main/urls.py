from django.urls import path, re_path
from main.views import *
from autobase import config

urlpatterns = [
    path('', MainIndex.as_view(), name='home'),
    path('features', Features.as_view(), name='features'),
    path('about', About.as_view(), name='about'),
    path('add_post', AddPost.as_view(), name='add_post'),
    path('show_post/<slug:post_slug>', ShowPost.as_view(), name='show_post'),
    path('registration/', RegisterUser.as_view(), name='registration'),
    path('registration_successful/', RegistrationSuccessful.as_view(),
         name='registration_successful'),
    path('feedback/', FeedbackFormView.as_view(), name='feedback'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutUser.as_view(), name='logout'),
    path('profile/<int:user_id>', ProfileUser.as_view(), name='profile'),
    path('profile_edit/<int:user_id>', ProfileUserEdit.as_view(), name='profile_edit'),
    re_path(r'^passwords/change/$', MyPasswordChangeView.as_view(),
            name='password_change'),
    re_path(r'^passwords/change/done/$',
            MyPasswordChangeDoneView.as_view(), name='password_change_done'),
    re_path(r'^passwords/reset/$', MyPasswordResetView.as_view(),
            name='password_reset'),
    re_path(r'^passwords/reset/done/$',
            MyPasswordResetDoneView.as_view(),  name='password_reset_done'),
    re_path(r'^passwords/reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',
            MyPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    re_path(r'^passwords/reset/complete/$',
            MyPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # Тут перехватываю url логина в админку что бы направить на форму с капчей
    path(f'{config.URL_ADMIN}/login/', MyAdminLoginView.as_view()),
]
