from django.contrib import admin
from django.urls import path


from . import views

app_name = 'meds'

urlpatterns = [
    path('', views.MedsHome.as_view(), name='index'),
	path('active-create/', views.ActiveCompoundCreate.as_view(), name='active-create'),
	path('active-compound/list/', views.ActiveCompoundList.as_view(), name='active-list'),
	path('active-compound/<int:active_compound_id>/', views.ActiveCompoundDetail.as_view(), name='active-detail'),
	path('active-compound/<int:active_compound_id>/update/', views.ActiveCompoundUpdate.as_view(), name='active-update'),
	path('drug_autocomplete/', views.drug_autocomplete, name='drug_autocomplete')

]