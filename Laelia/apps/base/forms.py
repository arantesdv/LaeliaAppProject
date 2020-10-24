from django import forms
from . import models


class CityModelForm(forms.ModelForm):
	class Meta:
		model = models.City
		fields = ['pt_name', 'region']
		
	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(CityModelForm, self).__init__(*args, **kwargs)
		
		
class ProfessionalModelForm(forms.ModelForm):
	class Meta:
		model = models.Professional
		fields = ['user', 'first_name', 'last_name', 'birth_date', 'gender', 'profession', 'specialty', 'subspecialty', 'register']
		
	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(ProfessionalModelForm, self).__init__(*args, **kwargs)


class PatientModelForm(forms.ModelForm):
	class Meta:
		model = models.Patient
		fields = ['user', 'first_name', 'last_name', 'birth_date', 'gender', 'skin_color', 'hair_color', 'main_phone', 'address', 'neiborhood', 'city']
	
	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(PatientModelForm, self).__init__(*args, **kwargs)
		
		
		
class NationModelForm(forms.ModelForm):
	class Meta:
		model = models.Nation
		fields = ['pt_name', 'abrev']
		
	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(NationModelForm, self).__init__(*args, **kwargs)
		
		
class RegionModelForm(forms.ModelForm):
	class Meta:
		model = models.Region
		fields = ['pt_name', 'abrev', 'nation']
		
	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(RegionModelForm, self).__init__(*args, **kwargs)
		
		
class ScheduleVisitModelForm(forms.ModelForm):
	class Meta:
		model = models.Schedule
		fields = ['professional','patient' ,'date', 'hour', 'min', 'duration', 'notes']



class ScheduleEventModelForm(forms.ModelForm):
	class Meta:
		model = models.Schedule
		fields = ['professional','patient' ,'date', 'hour', 'min', 'duration', 'notes']
