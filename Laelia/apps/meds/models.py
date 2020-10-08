from django.db import models
from django.urls import reverse, reverse_lazy

from .mixins import ActiveCompoundMixin, CompoundSetMixin, ComercialDrugMixin, PrescriptionMixin


class ActiveCompound(ActiveCompoundMixin):
	class Meta:
		constraints = [models.UniqueConstraint(fields=['pt_name'], name='unique_%(class)s')]
		
		
	def get_success_url(self):
		return reverse('meds:active-detail', kwargs={'active_compound_id': self.pk})


class CompoundSet(CompoundSetMixin):
	pass


class ComercialDrug(ComercialDrugMixin):
	class Meta:
		ordering = ['pt_name']


class Prescription(PrescriptionMixin):
	
	def __str__(self):
		return f'{self.comercial_drug} {self.dose} {self.comercial_drug.dosage_form} {self.get_dosage_regimen_display()} {self.get_frequency_display()} ' \
		       f'{f"{self.duration} dias" if self.duration else ""}'
