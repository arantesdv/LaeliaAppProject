import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Prescription, ActiveCompound, CompoundSet, ComercialDrug


class ComercialDrugModelForm(forms.ModelForm):
	class Meta:
		model = ComercialDrug
		fields = ['pt_name', 'compound_sets', 'total_content', 'presentation', 'dosage_form', 'volumes', ]


class CompoundSetModelForm(forms.ModelForm):
	class Meta:
		model = CompoundSet
		fields = ['active_compound', 'strength_value', 'strength_measure_unit']


class ActiveCompoundModelForm(forms.ModelForm):
	class Meta:
		model = ActiveCompound
		fields = ['pt_name',]


class PrescriptionModelForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		self.relation_id = kwargs.pop('relation_id', None)
		super(PrescriptionModelForm, self).__init__(*args, **kwargs)
		
	class Meta:
		model = Prescription
		fields = ['relation', 'comercial_drug', 'dose', 'dosage_regimen', 'frequency','start_date', 'boxes', 'duration']
	
	def clean(self):
		cleaned_data = super().clean()
		relation = cleaned_data.get("relation")
		comercial_drug = cleaned_data.get("comercial_drug")
		dose = cleaned_data.get("dose")
		dosage_regimen = cleaned_data.get("dosage_regimen")
		frequency = cleaned_data.get("frequency")
		duration = cleaned_data.get("duration")
		boxes = cleaned_data.get("boxes")
		
		if self.request and relation:
			if relation.professional.user != self.request.user:
				msg = "The professional in relation and request user is not the same."
				self.add_error('relation', ValidationError(_(msg)))
		
		if not comercial_drug:
			msg = f"A comercial drug is necessary for prescription. If you can't find, please add what you need."
			self.add_error('comercial_drug', ValidationError(_(msg)))
		else:
			if relation:
				if comercial_drug in [drug.comercial_drug for drug in Prescription.objects.filter(relation__patient=relation.patient)]:
					print(f'{comercial_drug} already prescribed')
					raise ValidationError(_(f"{comercial_drug} is already prescribed"))
		
		if not dose:
			msg = f"Please fill the dose."
			if comercial_drug:
				msg = f"Please fill the dose. The dosage form used for {comercial_drug.pt_name} is '{comercial_drug.dosage_form.upper()}'"
			self.add_error('dose', ValidationError(_(msg)))
		
		if not dosage_regimen:
			msg = f"Please select a dosage regimem"
			self.add_error('dosage_regimen', ValidationError(_(msg)))
			
		if not frequency:
			msg = f"Please select a frequency"
			self.add_error('frequency', ValidationError(_(msg)))
			
		if not duration:
			msg = 'Duration will be set to undefined'
			self.add_error('duration', ValidationError(_(msg)))
			