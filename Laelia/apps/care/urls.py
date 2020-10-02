from django.contrib import admin
from django.urls import path

from . import views

app_name = 'care'
urlpatterns = [
    path('event/create/', views.EventCreate.as_view(), name='event-create'),
    path('relation/<slug:relation_slug>/event/update/<int:event_id>/', views.EventUpdate.as_view(), name='event-update'),
    path('event/<int:event_id>/', views.EventDetail.as_view(), name='event-detail'),
    path('event/list/<int:relation_id>/', views.EventList.as_view(), name='event-list'),
]