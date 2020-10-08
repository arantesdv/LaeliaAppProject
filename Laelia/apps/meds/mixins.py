from django.db import models
from django.utils.translation import gettext_lazy as _
from Laelia.apps.base.mixins import MultiLingualNameMixin, CreationModificationDatesBase, UrlBase
from Laelia.apps.base.fields import MinMaxFloatField
from Laelia.apps.base.models import Relation


class ActiveCompoundMixin(MultiLingualNameMixin):
	class Meta: abstract = True
	
	
class CompoundSetMixin(models.Model):
	active_compound = models.ForeignKey('meds.ActiveCompound', on_delete=models.CASCADE, blank=True, null=True)
	strength_value = MinMaxFloatField(min_value=0, blank=True, null=True)
	strength_measure_unit = models.CharField(max_length=10, blank=True, null=True)
	class Meta: abstract = True
	
	def __str__(self):
		return f'{self.active_compound} {self.strength_value} {self.strength_measure_unit}'.replace('.0', '')


class ComercialDrugMixin(MultiLingualNameMixin):
	compound_sets = models.ManyToManyField('meds.CompoundSet', related_name='%(class)s_compound_sets')
	total_content = models.FloatField(blank=True, null=True)
	presentation = models.CharField(max_length=20, blank=True, null=True)
	dosage_form = models.CharField(max_length=20, blank=True, null=True)
	volumes = models.IntegerField(blank=True, null=True, choices=[(x, f'{x}') for x in range(1,11)], default=1)
	_name = models.CharField(max_length=255, blank=True, editable=False)

	class Meta: abstract = True
	
	@property
	def name(self, *args, **kwargs):
		self._name = self.__str__()
		super(ComercialDrugMixin, self).save(*args, **kwargs)
		return self._name
	
	def __str__(self):
		return f'{self.pt_name} {self.full_set} {self.total_content if self.volumes is not None else self.total_content * self.volumes} {self.presentation}'.replace('.0', '')
	
	@property
	def full_set(self):
		total_med = len(self.compound_sets.all())
		med_list = self.compound_sets.all()
		if total_med > 0:
			if total_med == 1:
				set = med_list[0]
				full_set = f'({set.active_compound}) {set.strength_value} {set.strength_measure_unit}'
			elif total_med == 2:
				set1 = med_list[0]
				set2 = med_list[1]
				full_set = f'({set1.active_compound}/{set2.active_compound}) {set1.strength_value}{set1.strength_measure_unit}/{set2.strength_value}{set2.strength_measure_unit}'
			elif total_med == 3:
				set1 = med_list[0]
				set2 = med_list[1]
				set3 = med_list[2]
				full_set = f'({set1.active_compound}/{set2.active_compound}/{set3.active_compound}) {set1.strength_value}{set1.strength_measure_unit}/{set2.strength_value}{set2.strength_measure_unit}/{set3.strength_value}{set3.strength_measure_unit}'
			else:
				set = med_list[0]
				full_set = f'({set.active_compound}) {set.strength_value} {set.strength_measure_unit} + associações'
		return full_set
	
	

class CareRelationMixin(models.Model):
	relation = models.ForeignKey('base.Relation', on_delete=models.SET_NULL, blank=True, null=True)
	class Meta: abstract = True

	
class PrescriptionDrugMixin(models.Model):
	comercial_drug = models.ForeignKey('meds.ComercialDrug', on_delete=models.CASCADE)
	class Meta: abstract = True



class DoseMixin(models.Model):
	dose = models.FloatField()
	class Meta: abstract = True


class DosageRegimenMixin(models.Model):
	dosage_regimen = models.IntegerField(choices=[(x, f'{x}x') for x in range(1,13)], default=1)
	class Meta: abstract = True


class FrequencyMixin(models.Model):
	class FrequencyChoices(models.IntegerChoices):
		DAILY = 1, _('daily')
		WEEKLY = 7, _('weekly')
		BIWEEKLY = 14, _('biweekly')
		MONTHLY = 30, _('month')
	frequency = models.IntegerField(choices=FrequencyChoices.choices, default=FrequencyChoices.DAILY)
	class Meta: abstract = True


class DurationMixin(models.Model):
	duration = models.IntegerField(blank=True, null=True, help_text=_('Days treatment duration. Keep blank for continuous'))
	class Meta: abstract = True


class PrescriptionMixin(CareRelationMixin,
                        PrescriptionDrugMixin,
                        DoseMixin,
                        DosageRegimenMixin,
                        FrequencyMixin,
                        DurationMixin,
                        CreationModificationDatesBase,
                        UrlBase):
	class Meta: abstract = True