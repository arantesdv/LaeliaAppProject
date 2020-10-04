from django.contrib import admin
from django.urls import path

from . import views

app_name = 'care'
urlpatterns = [
    path('relation/<int:relation_id>/', views.RelationDetail.as_view(), name='relation-detail'),
    path('relation/<int:relation_id>/event/create/', views.EventCreate.as_view(), name='event-create'),
    path('relation/<int:relation_id>/event/<int:event_id>/', views.EventDetail.as_view(), name='event-detail'),

]
