from django import forms

from . models import TimeLineEvent


class TimeLineEventModelForm(forms.ModelForm):
	class Meta:
		model = TimeLineEvent
		exclude = ['created']
