import uuid, datetime
from django.db import models
from django.shortcuts import reverse
from Laelia.apps.base.mixins import UrlBase
from . mixins import TimeLineMixin, EventTypeMixin
from Laelia.apps.base.models import Relation


class Event(TimeLineMixin, EventTypeMixin, UrlBase):
	relation = models.ForeignKey(Relation, on_delete=models.CASCADE, blank=True, null=True)
	uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
	
	
	def get_absolute_url(self):
		return reverse('base:event-detail', kwargs={'relation_id': self.relation.id, 'event_id': self.id })

	
	@classmethod
	def add_current_from_relation(cls, relation_id=None):
		return cls(relation_id=relation_id, event_date=datetime.date.today())

	@property
	def as_list_item(self):
		return f'- {self.age_at_event}: {self.notes}'
	
	@property
	def as_paragraph(self):
		return f'Aos {self.age_at_event} {["anos" if self.age_at_event >= 1 else "ano"][0]}: {self.notes}'


