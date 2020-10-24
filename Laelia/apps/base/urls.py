from django.contrib import admin
from django.urls import path, include

from . import views

app_name = 'base'
urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('professional/<int:professional_id>/', views.ProfessionalDetail.as_view(), name='professional-detail'),
    path('professional/<int:professional_id>/relation/list/', views.RelationList.as_view(), name='relation-list'),
    path('professional/<int:professional_id>/patient/create/', views.PatientCreate.as_view(),
         name='patient-relation-create'),
    path('professional/<int:professional_id>/schedule/create/', views.ScheduleEventCreate.as_view(),
         name='schedule-create'),
    path('professional/<int:professional_id>/schedule/visit/create/', views.ScheduleVisitCreate.as_view(),
         name='schedule-visit-create'),
    path('professional/<int:professional_id>/schedule/', views.ScheduleView.as_view(), name='schedule-view'),
    path('professional/<int:professional_id>/schedule/<int:schedule_id>/', views.ScheduleDetail.as_view(),
         name='schedule-detail'),
    path('relation/<int:relation_id>/', views.RelationDetail.as_view(), name='relation-detail'),
    path('employee/<int:employee_id>/', views.EmployeeDetail.as_view(), name='employee-detail'),
    path('patient/create/', views.PatientCreate.as_view(), name='patient-create'),
    path('patient/<int:patient_id>/', views.PatientDetail.as_view(), name='patient-detail'),
    path('comercial/<int:comercial_id>/', views.ComercialDetail.as_view(), name='comercial-detail'),
    path('enterprise/<int:enterprise_id>/', views.EnterpriseDetail.as_view(), name='enterprise-detail'),

]