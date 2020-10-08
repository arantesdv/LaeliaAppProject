import uuid, datetime
from django.db import models
from django.shortcuts import reverse
from Laelia.apps.base.mixins import UrlBase, CreationModificationDatesBase
from . mixins import TimeLineMixin, EventTypeMixin, VisitTypeMixin
from Laelia.apps.base.models import Relation


class Event(VisitTypeMixin, TimeLineMixin, EventTypeMixin, UrlBase, CreationModificationDatesBase):
	relation = models.ForeignKey(Relation, on_delete=models.CASCADE, blank=True, null=True)
	uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
	
	class Meta:
		ordering = ['age_at_event', 'created']
	
	
	def get_absolute_url(self):
		return reverse('care:event-detail', kwargs={'relation_id': self.relation.pk, 'event_id': self.pk })

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
		if self.age_at_event:
			return f'- {self.age_at_event}: {self.notes}'
	
	@property
	def as_paragraph(self):
		if self.age_at_event:
			return f'Aos {self.age_at_event} {["anos" if self.age_at_event >= 1 else "ano"][0]}: {self.notes}'


