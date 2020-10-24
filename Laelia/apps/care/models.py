import uuid, datetime
from django.db import models
from django.utils import timezone
from django.shortcuts import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from Laelia.apps.base.mixins import UrlBase, CreationModificationDatesBase
from . mixins import (TimeLineMixin,
                      PharmacotherapyMixin,
                      DocumentBase,
                      EventBase,
                      VisitBase,
                      PrescriptionBase,
                      TreatmentAttendanceBase,
                      VisitAttendanceBase,
                      MedicalLicenceBase)
from Laelia.apps.base.models import Relation
from Laelia.apps.base.mixins import MultiLingualNameMixin


class TreatmentAttendanceCertificate(TreatmentAttendanceBase):
	date = models.DateField(blank=True, null=True)
	def clean(self):
		super(TreatmentAttendanceCertificate, self).clean()


class VisitAttendanceCertificate(VisitAttendanceBase):
	def clean(self):
		super(VisitAttendanceCertificate, self).clean()

class Recipe(PrescriptionBase):
	date = models.DateField(blank=True, null=True)
	boxes = models.IntegerField(blank=True, null=True, choices=[(x, f'{x} cx') for x in range(1,21)])

class Concept(MultiLingualNameMixin):
	pass


class Event(EventBase):
	date = models.DateField(blank=True, null=True)
	concepts = models.ManyToManyField('care.Concept', blank=True)
	class Meta: ordering = ['timeline_age', 'created']
	
	def save(self, *args, **kwargs):
		return super(Event, self).save(*args, **kwargs)
	

	def get_absolute_url(self):
		return reverse('care:event-detail', kwargs={'relation_id': self.relation.pk, 'event_id': self.pk})

	@classmethod
	def create_visit(cls, relation_id=None, date=None):
		if relation_id != None: cls(relation_id=relation_id)
		if date != None: cls(event_date=datetime.date.today())
		cls(event_type=None)
		return cls
	
	@classmethod
	def add_current_from_relation(cls, relation_id=None):
		return cls(relation_id=relation_id, event_date=datetime.date.today())

	@property
	def as_list_item(self):
		if self.timeline_age:
			return f'- {self.timeline_age}: {self.notes}'
	
	@property
	def as_paragraph(self):
		if self.timeline_age:
			return f'Aos {self.timeline_age} {["anos" if self.timeline_age >= 1 else "ano"][0]}: {self.notes}'


class Document(DocumentBase):
	concepts = models.ManyToManyField('care.Concept', blank=True)

	
	def clean(self):
		super(Document, self).clean()
		if not self.relation: raise ValidationError(_('You need a relation'))

	def get_absolute_url(self):
		return reverse('care:report-detail', kwargs={'relation_id': self.relation.id, 'document_id': self.pk})
		


class Visit(VisitBase):

	
	def clean(self):
		super(Visit, self).clean()
		if not self.date: self.date = self.created.date()
		if not self.from_time: self.from_time = self.created.time()
	
	def get_absolute_url(self):
		return reverse('care:visit-detail', kwargs={'relation_id': self.relation.id, 'visit_id': self.pk})


class MedicalLicence(MedicalLicenceBase):
	reference_visit = models.ForeignKey('care.Visit', on_delete=models.SET_NULL, blank=True, null=True)