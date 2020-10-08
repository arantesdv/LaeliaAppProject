from django.contrib import admin

from .models import ActiveCompound, CompoundSet, ComercialDrug, Prescription


@admin.register(ActiveCompound)
class ActiveCompoundAdmin(admin.ModelAdmin):
	search_fields = ['_search_names']


@admin.register(CompoundSet)
class CompoundSetAdmin(admin.ModelAdmin):
	search_fields = ['active_compound__search_names']


@admin.register(ComercialDrug)
class ComercialDrugAdmin(admin.ModelAdmin):
	search_fields = ['_search_names', '_name']
	autocomplete_fields = ['compound_sets']
	
	
@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
	autocomplete_fields = ['comercial_drug']

