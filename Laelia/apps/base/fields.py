from functools import partial
from itertools import groupby
from operator import attrgetter

from django.db import models
from django.forms.models import ModelChoiceField, ModelChoiceIterator
from django.utils.translation import gettext_lazy as _
from . import functions


class MinMaxFloatField(models.FloatField):
	def __init__(self, min_value=None, max_value=None, *args, **kwargs):
		self.min_value, self.max_value = min_value, max_value
		super(MinMaxFloatField, self).__init__(*args, **kwargs)
	
	def formfield(self, **kwargs):
		defaults = {'min_value': self.min_value, 'max_value': self.max_value}
		defaults.update(kwargs)
		return super(MinMaxFloatField, self).formfield(**defaults)


class MinMaxIntergerField(models.IntegerField):
	def __init__(self, min_value=None, max_value=None, *args, **kwargs):
		self.min_value, self.max_value = min_value, max_value
		super(MinMaxIntergerField, self).__init__(*args, **kwargs)
	
	def formfield(self, **kwargs):
		defaults = {'min_value': self.min_value, 'max_value': self.max_value}
		defaults.update(kwargs)
		return super(MinMaxIntergerField, self).formfield(**defaults)


class GroupedModelChoiceIterator(ModelChoiceIterator):
	def __init__(self, field, groupby):
		self.groupby = groupby
		super().__init__(field)
	
	def __iter__(self):
		if self.field.empty_label is not None:
			yield ("", self.field.empty_label)
		queryset = self.queryset
		# Can't use iterator() when queryset uses prefetch_related()
		if not queryset._prefetch_related_lookups:
			queryset = queryset.iterator()
		for group, objs in groupby(queryset, self.groupby):
			yield (group, [self.choice(obj) for obj in objs])


class GroupedModelChoiceField(ModelChoiceField):
	def __init__(self, *args, choices_groupby, **kwargs):
		if isinstance(choices_groupby, str):
			choices_groupby = attrgetter(choices_groupby)
		elif not callable(choices_groupby):
			raise TypeError('choices_groupby must either be a str or a callable accepting a single argument')
		self.iterator = partial(GroupedModelChoiceIterator, groupby=choices_groupby)
		super().__init__(*args, **kwargs)