import datetime
from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from Laelia.apps.base.models import Relation
from . models import Event, Document, Visit


class EventModelForm(forms.ModelForm):
	class Meta:
		model = Event
		exclude = ['created']
	
	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		self.relation_id = kwargs.pop('relation_id', None)
		super(EventModelForm, self).__init__(*args, **kwargs)
		
	
	def clean(self):
		cleaned_data = super().clean()
		relation = cleaned_data.get("relation")
		notes = cleaned_data.get("notes")
		age_at_event = cleaned_data.get("age_at_event")
		event_date = cleaned_data.get("event_date")
		
		if self.request and relation:
			if relation.professional.user != self.request.user:
				msg = "The professional in relation and request user is not the same."
				self.add_error('relation', ValidationError(_(msg)))
				
		if not notes:
			msg = "You should note something."
			self.add_error('notes', ValidationError(_(msg)))
			

		if not age_at_event and not event_date:
			msg = "You need to input a date or the age at event."
			self.add_error('event_date', ValidationError(_(msg)))
			self.add_error('age_at_event', ValidationError(_(msg)))


class VisitModelForm(forms.ModelForm):
	class Meta:
		model = Visit
		exclude = ['created']
	
	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		self.relation_id = kwargs.pop('relation_id', None)
		super(VisitModelForm, self).__init__(*args, **kwargs)
	
	def clean_relation(self):
		if self.request and self.relation_id != None:
			if self.cleaned_data['relation'].professional.user != self.request.user:
				raise forms.ValidationError("The name is not the same.")
		return self.cleaned_data['relation']


class ReportModelForm(forms.ModelForm):
	class Meta:
		model = Document
		exclude = ['created',]
	
	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		self.relation_id = kwargs.pop('relation_id', None)
		super(ReportModelForm, self).__init__(*args, **kwargs)

	def clean_relation(self):
		if self.request and self.relation_id != None:
			if self.cleaned_data['relation'].professional.user != self.request.user:
				raise forms.ValidationError("The name is not the same.")
		return self.cleaned_data['relation']
	
	def clean_concepts(self):
			concepts = self.cleaned_data['concepts']
			return concepts
		
		
class ReferralModelForm(forms.ModelForm):
	class Meta:
		model = Document
		exclude = ['created',]
		
	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		self.relation_id = kwargs.pop('relation_id', None)
		super(ReferralModelForm, self).__init__(*args, **kwargs)
	
	
	def clean_relation(self):
		if self.request and self.relation_id != None:
			if self.cleaned_data['relation'].professional.user != self.request.user:
				raise forms.ValidationError("The name is not the same.")
		return self.cleaned_data['relation']
		
		
class CertificateModelForm(forms.ModelForm):
	class Meta:
		model = Document
		exclude = ['created',]
		
	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		self.relation_id = kwargs.pop('relation_id', None)
		super(CertificateModelForm, self).__init__(*args, **kwargs)
	
	def clean_relation(self):
		if self.request and self.relation_id != None:
			if self.cleaned_data['relation'].professional.user != self.request.user:
				raise forms.ValidationError("The name is not the same.")
		return self.cleaned_data['relation']