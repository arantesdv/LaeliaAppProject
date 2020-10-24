from django.contrib import admin
from django.urls import path


from . import views

app_name = 'meds'

urlpatterns = [
    path('professional/<int:professional_id>/', views.MedsHome.as_view(), name='index'),
	path('professional/<int:professional_id>/active/create/', views.ActiveCompoundCreate.as_view(), name='active-create'),
	path('professional/<int:professional_id>/active/list/', views.ActiveCompoundList.as_view(), name='active-list'),
	path('professional/<int:professional_id>/active/<int:active_compound_id>/', views.ActiveCompoundDetail.as_view(), name='active-detail'),
	path('professional/<int:professional_id>/active/<int:active_compound_id>/update/', views.ActiveCompoundUpdate.as_view(), name='active-update'),
	path('professional/<int:professional_id>/drug/create', views.ComecialDrugCreate.as_view(), name='drug-create'),
	path('professional/<int:professional_id>/drug/<int:drug_id>/>', views.ComecialDrugDetail.as_view(), name='drug-detail'),
	path('professional/<int:professional_id>/drug/<int:drug_id>/update', views.DrugUpdate.as_view(), name='drug-update'),
	path('professional/<int:professional_id>/set/create/', views.CompoundSetCreate.as_view(), name='compoundset-create'),

]