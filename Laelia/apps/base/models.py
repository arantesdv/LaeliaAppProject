from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User
from . mixins import MultiLingualNameMixin, UrlBase, CreationModificationDatesBase, PersonMixin, PhenotypeMixin, \
    EnterpriseMixin, GenderMixin, BirthDateMixin, DeathDateMixin, ProfessionMixin, ComercialMixin, ScheduleMixin


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
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    class Meta: abstract = True
    
    @property
    def full_address(self):
        full_address = ''
        if self.address: full_address += f'{self.address}'
        elif self.city: return f'{self.city} / {self.city.region.abrev}'
        else: pass
        if self.neiborhood: full_address += f', {self.neiborhood}'
        full_address += f', {self.city} / {self.city.region.abrev}'
        return full_address


class PhoneMixin(models.Model):
    main_phone = models.CharField(_('Phone (main)'), blank=True, null=True, max_length=20)
    other_phone = models.CharField(_('Phone (other)'), blank=True, null=True, max_length=20)
    class Meta: abstract = True


class BaseNotesMixin(models.Model):
    notes = models.TextField(blank=True, null=True)
    class Meta: abstract = True


class ComercialUser(ComercialMixin,
                    AddressMixin,
                    PhoneMixin,
                    BaseNotesMixin):
    class Meta:
        verbose_name = _('Comercial User')
        verbose_name_plural = _('Comercial Users')
    
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
    sponsor = models.ForeignKey(ComercialUser, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name = _('Professional')
        verbose_name_plural = _('Professionals')
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

class Employee(PersonMixin,
               GenderMixin,
               BirthDateMixin,
               AddressMixin,
               PhoneMixin,
               BaseNotesMixin,
               CreationModificationDatesBase):
    sponsor = models.ForeignKey(ComercialUser, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')
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
    sponsor = models.ForeignKey(ComercialUser, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name = _('Enterprise')
        verbose_name_plural = _('Enterprises')
        
    def get_absolute_url(self):
        return reverse('base:enterprise-detail', kwargs={'enterprise_id': self.id})
    
    @property
    def is_active(self):
        if self.sponsor: return self.sponsor.is_active
        else: return False


class Relation(UrlBase):
    patient = models.ForeignKey('base.Patient', on_delete=models.CASCADE)
    professional = models.ForeignKey('base.Professional', on_delete=models.CASCADE)
    
    def __str__(self): return f'{self.patient}: {self.professional}'
    
    def get_absolute_url(self):
        return reverse(viewname='base:relation-detail', kwargs={'relation_id': self.id, 'relation_slug': self.slug()})
    
    def slug(self):
        return slugify(f'{self.patient} xxxx {self.professional.composed_name()}').replace('-', '').replace('xxxx', '-')


class Schedule(ScheduleMixin,
               BaseNotesMixin):
    relation = models.ForeignKey(Relation, on_delete=models.CASCADE)
    
    @staticmethod
    def next_schedule_length_days(relation_id=0, days=0):
        if relation_id != 0:
            last_date = Schedule.objects.filter(relation_id=relation_id).last()
            next_visit = last_date + days
            return next_visit
        else: return None
