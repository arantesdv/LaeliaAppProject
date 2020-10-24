from django.contrib import admin

# Register your models here.

from . import models


@admin.register(models.Patient)
class PatientAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'search_names', 'is_person_active']
	search_fields = ['search_names']


@admin.register(models.Professional)
class ProfessionalAdmin(admin.ModelAdmin):
	search_fields = ['search_names']
	list_display = ['full_name', 'is_active']


@admin.register(models.City)
class CityAdmin(admin.ModelAdmin):
	pass


@admin.register(models.Region)
class RegionAdmin(admin.ModelAdmin):
	pass

@admin.register(models.Nation)
class NationAdmin(admin.ModelAdmin):
	pass


@admin.register(models.Enterprise)
class EnterpriseAdmin(admin.ModelAdmin):
	autocomplete_fields = ['patients', 'professionals']
	search_fields = ['name']
	list_display = ['name', 'is_active']


@admin.register(models.Relation)
class RelationAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'visits_count', 'trauma_count', 'loss_count']

@admin.register(models.Employee)
class EmployeeAdmin(admin.ModelAdmin):
	search_fields = ['search_names']
	list_display = ['full_name', 'is_active']


def activate_comercial_user(modeladmin, request, queryset):
	for item in queryset:
		item.activate()
		item.save()
activate_comercial_user.short_description = 'ATIVAR CONTA'


def deactivate_comercial_user(modeladmin, request, queryset):
	for item in queryset:
		item.deactivate()
		item.save()
deactivate_comercial_user.short_description = 'DESATIVAR CONTA'


@admin.register(models.Sponsor)
class ComercialUserAdmin(admin.ModelAdmin):
	actions = [activate_comercial_user, deactivate_comercial_user]
	list_display = ['name', 'is_active']
	

@admin.register(models.Schedule)
class ScheduleAdmin(admin.ModelAdmin):
	list_display = ['date', 'hour', 'min', 'duration', 'start', 'end']


@admin.register(models.Symptom)
class SymptomAdmin(admin.ModelAdmin):
	search_fields = ['search_names']



@admin.register(models.Organ)
class OrganAdmin(admin.ModelAdmin):
	search_fields = ['search_names']




@admin.register(models.Structure)
class StructureAdmin(admin.ModelAdmin):
	search_fields = ['search_names']
