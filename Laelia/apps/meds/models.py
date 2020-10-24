import datetime
from django.db import models
from django.urls import reverse, reverse_lazy

from .mixins import ActiveCompoundMixin, CompoundSetMixin, ComercialDrugMixin, PrescriptionMixin


class ActiveCompound(ActiveCompoundMixin):
	class Meta:
		constraints = [models.UniqueConstraint(fields=['pt_name'], name='unique_%(class)s')]
		
		
	def get_success_url(self):
		return reverse('meds:active-detail', kwargs={'active_compound_id': self.pk})


class CompoundSet(CompoundSetMixin):
	class Meta:
		constraints = [models.UniqueConstraint(fields=['active_compound', 'strength_value', 'strength_measure_unit'], name='unique_%(class)s')]


class ComercialDrug(ComercialDrugMixin):
	class Meta:
		ordering = ['pt_name']
		constraints = [models.UniqueConstraint(fields=['pt_name', 'total_content', 'volumes'], name='unique_%(class)s')]



class Prescription(PrescriptionMixin):
	start_date = models.DateField(blank=True, null=True)
	class Meta:
		ordering = ['-start_date']
		constraints = [models.UniqueConstraint(fields=['comercial_drug', 'relation', 'start_date'], name='unique_%(class)s')]
		
		
	def clean(self):
		super(Prescription, self).clean()
		if not self.boxes:
			if self.duration: self.boxes = int(self.duration/30)
			else: self.boxes = 1

	
	def __str__(self):
		return f'{self.comercial_drug} {self.dose} {self.comercial_drug.dosage_form} {self.get_dosage_regimen_display()} {self.get_frequency_display()} ' \
		       f'{f"{self.duration} dias" if self.duration else ""}'


	def get_absolute_url(self):
		return reverse('care:prescription-detail', kwargs={'relation_id': self.relation.pk, 'prescription_id': self.pk})