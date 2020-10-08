from django.contrib import admin
from django.urls import path
from Laelia.apps.meds.views import PrescriptionCreate, PrescriptionList, PrescriptionYearArchiveView
from . import views

app_name = 'care'
urlpatterns = [
	path('relation/<int:relation_id>/', views.RelationDetail.as_view(), name='relation-detail'),
	path('relation/<int:relation_id>/event/create/', views.EventCreate.as_view(), name='event-create'),
	path('relation/<int:relation_id>/event/<int:event_id>/', views.EventDetail.as_view(), name='event-detail'),
	path('relation/<int:relation_id>/visit/create/', views.VisitCreate.as_view(), name='visit-create'),
	path('relation/<int:relation_id>/prescription-create/', PrescriptionCreate.as_view(), name='prescription-create'),
	path('relation/<int:relation_id>/prescription-list/', PrescriptionList.as_view(), name='prescription-list'),
	path('relation/<int:relation_id>/prescription-year/<int:year>/', PrescriptionYearArchiveView.as_view(),
	     name='prescription-year-archive'),

]
