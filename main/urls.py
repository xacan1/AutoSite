from django.urls import path
from .views import *

urlpatterns = [
    path('', MainIndex.as_view(), name='home'),
    path('about/', about, name='about'),
    path('add_post', AddPost.as_view(), name='add_post'),
    path('show_post/<slug:post_slug>', ShowPost.as_view(), name='show_post'),
    path('registration/', RegisterUser.as_view(), name='registration'),
    path('feedback/', feedback, name='feedback'),
    path('login/', login, name='login'),
    path('profile/', profile, name='profile'),
]
