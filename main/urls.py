from django.urls import path
from .views import *

urlpatterns = [
    path('', MainIndex.as_view(), name='home'),
    path('about/', About.as_view(), name='about'),
    path('add_post', AddPost.as_view(), name='add_post'),
    path('show_post/<slug:post_slug>', ShowPost.as_view(), name='show_post'),
    path('registration/', RegisterUser.as_view(), name='registration'),
    path('feedback/', FeedbackFormView.as_view(), name='feedback'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutUser.as_view(), name='logout'),
    path('profile/<int:user_id>', ProfileUser.as_view(), name='profile'),
]
