from django.contrib import admin
from django.urls import path, include

from . import views

app_name = 'base'
urlpatterns = [
    path('', views.index_view, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/<int:user_id>/', views.user_profile_view, name='user-profile'),
    path('professional/<int:professional_id>/patient/list/', views.PatientList.as_view(), name='patient-list'),
    path('relation/<slug:relation_slug>/<int:relation_id>/', views.RelationDetail.as_view(), name='relation-detail'),
]