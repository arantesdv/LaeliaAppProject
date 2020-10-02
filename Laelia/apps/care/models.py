import uuid
from django.db import models
from django.shortcuts import reverse
from Laelia.apps.base.mixins import UrlBase
from . mixins import TimeLineMixin, EventTypeMixin
from Laelia.apps.base.models import Relation


class TimeLineEvent(TimeLineMixin, EventTypeMixin, UrlBase):
	relation = models.ForeignKey(Relation, on_delete=models.CASCADE, blank=True, null=True)
	uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

	def get_absolute_url(self):
		return reverse('care:event-detail', kwargs={'event_id': self.id})