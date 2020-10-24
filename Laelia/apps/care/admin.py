from django.contrib import admin

from . import models


@admin.register(models.Event)
class TimeLineEventAdmin(admin.ModelAdmin):
	list_display = ['timeline_age', 'as_paragraph']
	
	
@admin.register(models.Document)
class DocumentAdmin(admin.ModelAdmin):
	list_display = ['relation', 'verbose_1']


@admin.register(models.Concept)
class ConceptAdmin(admin.ModelAdmin):
	pass

@admin.register(models.Visit)
class VisitAdmin(admin.ModelAdmin):
	pass


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
	pass


@admin.register(models.TreatmentAttendanceCertificate)
class TreatmentAttendanceCertificateAdmin(admin.ModelAdmin):
	list_display = ['relation', 'as_list_of_strings']
	
	

@admin.register(models.VisitAttendanceCertificate)
class VisitAttendanceCertificateAdmin(admin.ModelAdmin):
	list_display = ['relation', 'as_list_of_strings']
	
@admin.register(models.MedicalLicence)
class MedicalLicenceAdmin(admin.ModelAdmin):
	pass