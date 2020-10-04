from django import forms

from . models import Event


class TimeLineEventModelForm(forms.ModelForm):
	class Meta:
		model = Event
		exclude = ['created']
