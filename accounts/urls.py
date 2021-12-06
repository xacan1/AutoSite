from django.conf.urls import re_path
from accounts.views import *


urlpatterns = [
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
]
