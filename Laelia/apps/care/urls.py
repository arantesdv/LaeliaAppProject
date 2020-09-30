from django.contrib import admin
from django.urls import path

from . import views

app_name = 'care'
urlpatterns = [
    path('relation/<int:relation_id>/', views.RelationView.as_view(), name='relation-view'),
]