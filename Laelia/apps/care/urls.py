from django.urls import path
from Laelia.apps.meds.views import PrescriptionCreate, PrescriptionList, PrescriptionYearArchiveView, PrescriptionDetail
from . import views


app_name = 'care'
urlpatterns = [
	path('relation/<int:relation_id>/', views.RelationDetail.as_view(), name='relation-detail'),
	path('relation/<int:relation_id>/event/create/', views.EventCreate.as_view(), name='event-create'),
	path('relation/<int:relation_id>/event/<int:event_id>/', views.EventDetail.as_view(), name='event-detail'),
	path('relation/<int:relation_id>/visit/create/', views.VisitCreate.as_view(), name='visit-create'),
	path('relation/<int:relation_id>/visit/<int:visit_id>/', views.VisitDetail.as_view(), name='visit-detail'),
	path('relation/<int:relation_id>/visit/list/', views.VisitList.as_view(), name='visit-list'),
	path('relation/<int:relation_id>/visit/<int:visit_id>/pdf/', views.build_visit, name='build-visit'),
	
	path('relation/<int:relation_id>/plan/<int:visit_id>/pdf/', views.build_visit_plan, name='build-visit-plan'),
	path('relation/<int:relation_id>/visit/<int:visit_id>/update/', views.VisitCreate.as_view(), name='visit-update'),
	path('relation/<int:relation_id>/prescription-create/', PrescriptionCreate.as_view(), name='prescription-create'),
	path('relation/<int:relation_id>/prescription-list/', PrescriptionList.as_view(), name='prescription-list'),
	path('relation/<int:relation_id>/prescription/<int:prescription_id>/', PrescriptionDetail.as_view(), name='prescription-detail'),
	path('relation/<int:relation_id>/prescription-year/<int:year>/', PrescriptionYearArchiveView.as_view(),
	     name='prescription-year-archive'),
	path('relation/<int:relation_id>/certificate/create/', views.CertificateCreate.as_view(), name='certificate-create'),
	path('relation/<int:relation_id>/report/create/', views.ReportCreate.as_view(), name='report-create'),
	path('relation/<int:relation_id>/report/<int:document_id>/', views.ReportDetail.as_view(), name='report-detail'),
	path('relation/<int:relation_id>/document/<int:document_id>/', views.DocumentDetail.as_view(),
	     name='document-detail'),
	path('relation/<int:relation_id>/licence/<int:licence_id>/', views.MedicalLicenceDetail.as_view(),  name='licence-detail'),
	path('relation/<int:relation_id>/licence/<int:licence_id>/pdf', views.medical_licence_pdf, name='medical-licence-pdf'),
]
