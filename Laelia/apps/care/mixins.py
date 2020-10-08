import datetime
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import ValidationError
from Laelia.apps.base.fields import MinMaxFloatField
from Laelia.apps.base.functions import funcTime


class DateOfEventMixin(models.Model):
	date_of_event = models.DateField(blank=True, null=True)
	class Meta: abstract = True
	
	
class AgeAtEventMixin(models.Model):
	age_at_event = models.IntegerField(blank=True, null=True)
	class Meta: abstract = True


class TimeLineMixin(models.Model):
	age_at_event = MinMaxFloatField(min_value=0, max_value=100, blank=True, null=True)
	event_date = models.DateField(blank=True, null=True)
	notes = models.TextField(_('Notes'), blank=True, null=True)
	
	class Meta: abstract = True
	
	@staticmethod
	def age_from_date(patient, date):
		return ((date - patient.birth_date) / funcTime(365)).__round__(1)
	
	@staticmethod
	def date_from_age(patient, age=None):
		if age: return funcTime('today') - ((patient.age - age) * funcTime(365))
	
	@classmethod
	def from_age(cls, age):
		return cls(age_at_event=age)
	
	@classmethod
	def from_date(cls, date):
		return cls(date_at_event=date)
	
	@classmethod
	def from_year(cls, year):
		return cls(date_at_event=datetime.date(year=year, month=7, day=1))
	
	@classmethod
	def from_year_month(cls, year, month):
		return cls(date_at_event=datetime.date(year=year, month=month, day=1))
	
	def clean(self):
		if self.event_date:
			if self.event_date > (funcTime('today').date() + funcTime(1)): raise ValidationError(
				_('The date cannot be greater then today'))
		if self.age_at_event != None:
			if self.relation.patient.age < self.age_at_event: raise ValidationError(
				_('The Age at Event cannot be greater then patient age'))
		if self.relation:
			if self.age_at_event and self.event_date:
				self.age_at_event = TimeLineMixin.age_from_date(patient=self.relation.patient, date=self.event_date)
			if self.event_date:
				self.age_at_event = TimeLineMixin.age_from_date(patient=self.relation.patient, date=self.event_date)


class EventTypeMixin(models.Model):
	class EventType(models.TextChoices):
		TRAUMA = 'trauma', _('trauma')
		DISEASE = 'disease', _('disease')
		POSITIVE_MARK = 'positive mark', _('positive mark')
		NEGATIVE_MARK = 'negative mark', _('negative mark')
	event_type = models.CharField(choices=EventType.choices, blank=True, null=True, max_length=50)
	class Meta: abstract = True


class VisitTypeMixin(models.Model):
	class VisitType(models.TextChoices):
		FIRST_VISIT = 'first visit', _('first visit')
		FOLLOW_UP = 'follow up', _('follow up')
		NEW_COMPLAINT = 'new complaint', _('new complaint')
		REVIST = 'revisit', _('revisit')
	visit_type = models.CharField(choices=VisitType.choices, blank=True, null=True, max_length=50)
	class Meta: abstract = True
	
	
class PharmacotherapyMixin(models.Model):
	class PharmacotherapyType(models.TextChoices):
		PRESCRIPTION = 'prescription', _('prescription')
		SIDE_EFFECT = 'side effect', _('side effect')
		GOOD_RESPONSE = 'good response', _('good response')
		NO_RESPONSE = 'no response', _('no response')
	pharmacotherapy_report_type = models.CharField(choices=PharmacotherapyType.choices, blank=True, null=True, max_length=50)
	comercial_drug = models.ForeignKey('recipe.ComercialDrug', on_delete=models.CASCADE)
	class Meta: abstract = True