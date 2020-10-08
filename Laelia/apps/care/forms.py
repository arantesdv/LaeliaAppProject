import datetime
from django import forms
from django.utils.translation import gettext_lazy as _

from . models import Event


class EventModelForm(forms.ModelForm):
	class Meta:
		model = Event
		exclude = ['created', 'visit_type']



class VisitModelForm(forms.ModelForm):
	class Meta:
		model = Event
		exclude = ['created', 'event_type', 'age_at_event']