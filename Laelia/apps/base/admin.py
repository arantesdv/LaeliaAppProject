from django.contrib import admin

# Register your models here.

from . import models


@admin.register(models.Patient)
class PatientAdmin(admin.ModelAdmin):
	pass


@admin.register(models.Professional)
class ProfessionalAdmin(admin.ModelAdmin):
	pass


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
	pass


@admin.register(models.Relation)
class RelationAdmin(admin.ModelAdmin):
	pass
