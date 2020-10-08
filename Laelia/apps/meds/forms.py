from django import forms

from .models import Prescription, ActiveCompound, CompoundSet, ComercialDrug


class ComercialDrugModelForm(forms.ModelForm):
	class Meta:
		model = ComercialDrug
		fields = ['pt_name', 'compound_sets', 'total_content', 'presentation', 'dosage_form', 'volumes']


class CompoundSetModelForm(forms.ModelForm):
	class Meta:
		model = CompoundSet
		fields = ['active_compound', 'strength_value', 'strength_measure_unit']


class ActiveCompoundModelForm(forms.ModelForm):
	class Meta:
		model = ActiveCompound
		fields = ['pt_name',]


class PrescriptionModelForm(forms.ModelForm):
	class Meta:
		model = Prescription
		fields = ['relation', 'comercial_drug', 'dose', 'dosage_regimen', 'frequency', 'duration']
