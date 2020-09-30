from django.contrib import admin
from django.urls import path, include

from . import views

app_name = 'base'
urlpatterns = [
    path('', views.index_view, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/<int:user_id>/', views.user_profile_view, name='user_profile'),
]