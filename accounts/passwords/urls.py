from django.conf.urls import re_path
from django.contrib.auth import views as auth_views


urlpatterns = [
    re_path(r'^passwords/change/$', auth_views.PasswordChangeView.as_view(),
            name='password_change'),
    re_path(r'^passwords/change/done/$',
            auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    re_path(r'^passwords/reset/$',
            auth_views.PasswordResetView.as_view(), name='password_reset'),
    re_path(r'^passwords/reset/done/$',
            auth_views.PasswordResetDoneView.as_view(),  name='password_reset_done'),
    re_path(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',
        auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    re_path(r'^passwords/reset/complete/$',
            auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
