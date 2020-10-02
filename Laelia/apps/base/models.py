from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse
from . mixins import MultiLingualNameMixin, UrlBase, CreationModificationDatesBase, PersonMixin, PhenotypeMixin, \
    EnterpriseMixin, GenderMixin, BirthDateMixin, DeathDateMixin, ProfessionMixin


class Nation(MultiLingualNameMixin):
    abrev = models.CharField(_('Nation Abreviation'), max_length=3)
    class Meta:
        verbose_name = _('Nation')
        verbose_name_plural = _('Nations')


class Region(MultiLingualNameMixin):
    nation = models.ForeignKey(Nation, on_delete=models.SET_NULL, blank=True, null=True)
    abrev = models.CharField(_('Region Abreviation'), max_length=2)
    class Meta:
        verbose_name = _('Region')
        verbose_name_plural = _('Regions')


class City(MultiLingualNameMixin):
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, blank=True, null=True)
    class Meta:
        verbose_name = _('City')
        verbose_name_plural = _('Cities')


class AddressMixin(models.Model):
    address = models.CharField(_('Address'), blank=True, null=True, max_length=255)
    neiborhood = models.CharField(_('Neiborhood'), blank=True, null=True, max_length=100)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, blank=True, null=True)
    class Meta: abstract = True


class PhoneMixin(models.Model):
    main_phone = models.CharField(_('Phone (main)'), blank=True, null=True, max_length=20)
    other_phone = models.CharField(_('Phone (other)'), blank=True, null=True, max_length=20)
    class Meta: abstract = True


class BaseNotesMixin(models.Model):
    notes = models.TextField(blank=True, null=True)
    class Meta: abstract = True


class Patient(PersonMixin,
              GenderMixin,
              BirthDateMixin,
              PhenotypeMixin,
              DeathDateMixin,
              AddressMixin,
              PhoneMixin,
              BaseNotesMixin,
              CreationModificationDatesBase):
    
    class Meta:
        verbose_name = _('Patient')
        verbose_name_plural = _('Patients')


class Professional(PersonMixin,
                   GenderMixin,
                   BirthDateMixin,
                   ProfessionMixin,
                   AddressMixin,
                   PhoneMixin,
                   BaseNotesMixin,
                   CreationModificationDatesBase):
    class Meta:
        verbose_name = _('Professional')
        verbose_name_plural = _('Professionals')


class Enterprise(EnterpriseMixin,
                 AddressMixin,
                 PhoneMixin,
                 BaseNotesMixin):
    class Meta:
        verbose_name = _('Enterprise')
        verbose_name_plural = _('Enterprises')


class Relation(UrlBase):
    patient = models.ForeignKey('base.Patient', on_delete=models.CASCADE)
    professional = models.ForeignKey('base.Professional', on_delete=models.CASCADE)
    
    def __str__(self): return f'{self.patient}: {self.professional}'
    
    
    def get_absolute_url(self):
        return reverse(viewname='base:relation-detail', kwargs={'relation_slug': self.slug(), 'relation_id': self.pk})
    
    def slug(self):
        return slugify(f'{self.patient} xxxx {self.professional.composed_name()}').replace('-', '').replace('xxxx', '-')
