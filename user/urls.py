from django.urls import path
from user import views

from rest_framework_simplejwt.views import token_refresh

urlpatterns = [
    path('greet', views.greet, name='greet'),
    path('register', views.register, name='register'),
    path('block', views.block_user, name='block'),
    path('token', views.token_obtain_view, name='get_token'),
    path('token/refresh', token_refresh, name='refresh_token')
]
