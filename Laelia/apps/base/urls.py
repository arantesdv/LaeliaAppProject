from django.contrib import admin
from django.urls import path, include


from . import views

app_name = 'base'
urlpatterns = [
    path('', views.BaseHome.as_view(), name='index'),
    path('relation/<int:relation_id>/', views.RelationDetail.as_view(), name='relation-detail'),
    path('relation/<int:relation_id>/event/create/', views.EventCreate.as_view(), name='event-create'),
    path('enterprise/<int:enterprise_id>/', views.EnterpriseDetail.as_view(), name='enterprise-detail'),
    path('professional/<int:professional_id>/', views.ProfessionalDetail.as_view(), name='professional-detail'),
    path('employee/<int:employee_id>/', views.EmployeeDetail.as_view(), name='employee-detail'),
    path('patient/<int:patient_id>/', views.PatientDetail.as_view(), name='patient-detail'),
    path('comercial/<int:comercial_id>/', views.ComercialDetail.as_view(), name='comercial-detail'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/<int:user_id>/', views.user_profile_view, name='user-profile'),
    path('professional/<int:professional_id>/patient-list/', views.PatientList.as_view(), name='patient-list'),


]