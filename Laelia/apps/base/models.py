import asyncio
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from Laelia.apps.base.functions import funcTime
from . mixins import MultiLingualNameMixin, UrlBase, CreationModificationDatesBase, PersonMixin, PhenotypeMixin, \
    EnterpriseMixin, GenderMixin, BirthDateMixin, DeathDateMixin, ProfessionMixin, SponsorMixin, ScheduleBase, \
    AddressMixin, BaseNotesMixin, PhoneMixin, RelationBase


class Facility(models.Model):
    name = models.CharField(_('Facility Name'), max_length=255)

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


class Sponsor(SponsorMixin,
              AddressMixin,
              PhoneMixin,
              BaseNotesMixin):
    class Meta:
        verbose_name = _('Comercial User')
        verbose_name_plural = _('Comercial Users')
        constraints = [models.UniqueConstraint(fields=['user', 'name'], name='unique_comercial_user')]
    
    def __str__(self):
        return f'{self.name}'
    
    def get_absolute_url(self):
        return reverse('base:comercial-detail', kwargs={'comercial_id': self.id})


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
        constraints = [models.UniqueConstraint(fields=['user', 'first_name', 'last_name', 'birth_date', 'gender'],
                                               name='unique_%(class)s')]
        
    def get_absolute_url(self):
        return reverse('base:patient-detail', kwargs={'patient_id': self.id})


class Professional(PersonMixin,
                   GenderMixin,
                   BirthDateMixin,
                   ProfessionMixin,
                   AddressMixin,
                   PhoneMixin,
                   BaseNotesMixin,
                   CreationModificationDatesBase):
    sponsor = models.ForeignKey(Sponsor, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name = _('Professional')
        verbose_name_plural = _('Professionals')
        constraints = [models.UniqueConstraint(fields=['user', 'first_name', 'last_name', 'birth_date', 'gender'],
                                               name='unique_%(class)s')]
        permissions = [
            ('inactivate_professional', 'Can inactivate the professional.'),
            ('assist_professional', 'Can assist the professional.'),
        ]
        
    def get_absolute_url(self):
        return reverse('base:professional-detail', kwargs={'professional_id': self.id})
    
    @property
    def is_active(self):
        if self.sponsor: return self.sponsor.is_active
        else: return False
        
    @property
    def patients_count(self):
        patients_count = Relation.objects.filter(professional=self).count()
        return patients_count
    

class Employee(PersonMixin,
               GenderMixin,
               BirthDateMixin,
               AddressMixin,
               PhoneMixin,
               BaseNotesMixin,
               CreationModificationDatesBase):
    sponsor = models.ForeignKey(Sponsor, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')
        constraints = [models.UniqueConstraint(fields=['user', 'first_name', 'last_name', 'birth_date', 'gender'],
                                               name='unique_%(class)s')]
        permissions = [
            ('inactivate_employee', 'Can inactivate the professional.'),
            ('can_be_assistant', 'Can assist professional.'),
        ]

    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')

    def get_absolute_url(self):
        return reverse('base:employee-detail', kwargs={'employee_id': self.id})
    
    @property
    def is_active(self):
        if self.sponsor: return self.sponsor.is_active
        else: return False


class Enterprise(EnterpriseMixin,
                 AddressMixin,
                 PhoneMixin,
                 BaseNotesMixin):
    patients = models.ManyToManyField(Patient, related_name='%(class)s_patients')
    professionals = models.ManyToManyField(Professional, related_name='%(class)s_professionals')
    sponsor = models.ForeignKey(Sponsor, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name = _('Enterprise')
        verbose_name_plural = _('Enterprises')
        
    def get_absolute_url(self):
        return reverse('base:enterprise-detail', kwargs={'enterprise_id': self.id})
    
    @property
    def is_active(self):
        if self.sponsor: return self.sponsor.is_active
        else: return False


class Relation(RelationBase):
    class Meta:
        constraints = [models.UniqueConstraint(fields=['patient', 'professional'], name='unique_relation')]
    
    def __str__(self): return f'{self.patient}: {self.professional}'
    
    def get_absolute_url(self):
        return reverse(viewname='base:relation-detail', kwargs={'relation_id': self.id, 'relation_slug': self.slug()})
    
    def slug(self):
        return slugify(f'{self.patient} xxxx {self.professional.composed_name()}').replace('-', '').replace('xxxx', '-')


class Schedule(ScheduleBase):
    
    @classmethod
    def schedule_30d_visit(cls, professional_id=0, patient_id=0):
        days = 30
        if professional_id and patient_id != 0:
            schedules = Schedule.objects.filter(professional_id=professional_id, date__day=funcTime('today') + funcTime(days))
            return cls(professional_id=professional_id, patient_id=patient_id)
    
    @staticmethod
    def next_schedule_length_days(professional_id=0, days=0):
        if professional_id != 0:
            last_date = Schedule.objects.filter(professional_id=professional_id).last()
            next_visit = last_date + days
            return next_visit
        else: return None
        
        
        
    def get_absolute_url(self):
        return reverse('base:schedule-detail', kwargs={'professional_id': self.professional.pk, 'schedule_id': self.pk})
    
    def get_success_url(self):
        return reverse('base:schedule-view', kwargs={'professional_id': self.professional.pk})


class Symptom(MultiLingualNameMixin):
    pass


class Structure(MultiLingualNameMixin):
    symptoms = models.ManyToManyField('base.Symptom', related_name='structure_symptoms', blank=True, symmetrical=True)

class Organ(MultiLingualNameMixin):
    structures = models.ManyToManyField('base.Structure', related_name='organ_structures', blank=True, symmetrical=True)
