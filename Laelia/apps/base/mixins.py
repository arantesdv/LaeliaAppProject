import datetime
from urllib.parse import urlparse, urlunparse
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.conf import settings
from .functions import funcTime





class AddressMixin(models.Model):
	address = models.CharField(_('Address'), blank=True, null=True, max_length=255)
	neiborhood = models.CharField(_('Neiborhood'), blank=True, null=True, max_length=100)
	city = models.ForeignKey('base.City', on_delete=models.SET_NULL, null=True, blank=True)
	
	class Meta:
		abstract = True
	
	@property
	def full_address(self):
		full_address = ''
		if self.address: full_address += f'{self.address}'
		if self.neiborhood: full_address += f' {self.neiborhood}'
		if self.city: full_address += f' {self.city} / {self.city.region.abrev}'
		return full_address


class PhoneMixin(models.Model):
	main_phone = models.CharField(_('Phone (main)'), blank=True, null=True, max_length=20)
	other_phone = models.CharField(_('Phone (other)'), blank=True, null=True, max_length=20)
	class Meta: abstract = True


class BaseNotesMixin(models.Model):
	notes = models.TextField(blank=True, null=True)
	class Meta: abstract = True

class MultiLingualNameMixin(models.Model):
	en_name = models.CharField(_('English Name'), max_length=255, blank=True, null=True)
	pt_name = models.CharField(_('Portuguese Name'), max_length=255, blank=True, null=True)
	es_name = models.CharField(_('Spanish Name'), max_length=255, blank=True, null=True)
	_search_names = models.CharField(max_length=255, null=True, blank=True, editable=False)
	
	class Meta:
		abstract = True
		constraints = [models.UniqueConstraint(fields=['pt_name'], name='unique_%(class)s')]
		ordering = ['pt_name']
	
	@property
	def name(self):
		name = f'{self.pt_name}'
		return name
	
	@property
	def search_names(self):
		names = f'{self.pt_name} '
		if self.en_name: names += f'; {self.en_name} '
		if self.es_name: names += f'; {self.es_name} '
		return names

	def __str__(self):
		return self.name



class UrlBase(models.Model):
	"""
	A replacement for get_absolute_url()
	Models extending this mixin should have either get_url or get_url_path implemented.
	http://code.djangoproject.com/wiki/ReplacingGetAbsoluteUrl
	"""
	
	class Meta:
		abstract = True
	
	def get_url(self):
		if hasattr(self.get_url_path, "dont_recurse"):
			raise NotImplementedError
		try:
			path = self.get_url_path()
		except NotImplementedError:
			raise
		return settings.WEBSITE_URL + path
	
	get_url.dont_recurse = True
	
	def get_url_path(self):
		if hasattr(self.get_url, "dont_recurse"):
			raise NotImplementedError
		try:
			url = self.get_url()
		except NotImplementedError:
			raise
		bits = urlparse(url)
		return urlunparse(("", "") + bits[2:])
	
	get_url_path.dont_recurse = True
	
	def get_absolute_url(self):
		return self.get_url()
	
	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		print("save() from UrlBase called")
	
	def delete(self, *args, **kwargs):
		super().delete(*args, **kwargs)
		print("delete() from UrlBase called")
	
	def test(self):
		print("test() from UrlBase called")


class CreationModificationDatesBase(models.Model):
	"""
	Abstract base class with a creation and modification date and time
	"""
	created = models.DateTimeField(_("Creation Date and Time"), auto_now_add=True, )
	modified = models.DateTimeField(_("Modification Date and Time"), auto_now=True, )
	_is_ongoing = models.BooleanField(default=True, editable=False)
	_is_protected = models.BooleanField(default=False, editable=False)
	
	class Meta: abstract = True
	
	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		print("save() from CreationModificationDatesBase called")
	
	save.alters_data = True
	
	@property
	def is_protected(self):
		return self._is_protected
	
	@property
	def is_ongoing(self):
		return self._is_ongoing
	
	def protect(self, *args, **kwargs):
		self._is_protected = True
		print('Is Protected set to TRUE')
		return super().save(*args, **kwargs)
	
	def stop(self, *args, **kwargs):
		self._is_ongoing = False
		print('Is Ongoing set to FALSE')
		return super().save(*args, **kwargs)
	
	def restart(self, *args, **kwargs):
		self._is_ongoing = True
		print('Is Ongoing set to TRUE')
		return super().save(*args, **kwargs)
	
	def delete(self, *args, **kwargs):
		if self.is_protected == True:
			print('Cannot Delete becouse the instance is protected')
			return None
		super().delete(*args, **kwargs)
	
	def test(self):
		print("test() from CreationModificationDatesBase called")


class DateTimeBase(CreationModificationDatesBase):
	date = models.DateField(blank=True, null=True)
	from_date = models.DateField(blank=True, null=True)
	from_time = models.TimeField(blank=True, null=True)
	to_time = models.TimeField(blank=True, null=True)
	to_date = models.DateField(blank=True, null=True)
	class Meta: abstract = True
	
	@property
	def min_duration(self):
		if self.from_time and self.to_time:
			duration = self.from_time - self.to_time
			return duration.min


class MonthMixin(models.Model):
	class Months(models.IntegerChoices):
		JANUARY = 1, _('January')
		FEBRUARY = 2, _('February')
		MARCH = 3, _('March')
		APRIL = 4, _('April')
		MAY = 5, _('May')
		JUNE = 6, _('June')
		JULY = 7, _('July')
		AUGUST = 8, _('August')
		SEPTEMBER = 9, _('September')
		OCTOBER = 10, _('October')
		NOVEMBER = 11, _('November')
		DECEMBER = 12, _('December')
	
	month = models.PositiveSmallIntegerField(choices=Months.choices, blank=True, null=True)
	class Meta: abstract = True
	
	
class UserMixin(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
	class Meta: abstract = True
	
	
	def post_save_receiver(sender, instance, created, **kwargs):
		print(f'O usuário {instance} foi salvo')
	
	post_save.connect(post_save_receiver, sender=settings.AUTH_USER_MODEL)
	
	def post_login(sender, request, user, **kwargs):
		print(f'O usuário {user} acaba de fazer login')
	
	user_logged_in.connect(post_login)
	
	def post_logout(sender, request, user, **kwargs):
		print(f'O usuário {user} acaba de fazer logout')
	
	user_logged_out.connect(post_logout)


class PersonMixin(UserMixin):
	first_name = models.CharField(_("First name"), max_length=100)
	last_name = models.CharField(_("Last name"), max_length=150)
	_is_person_active = models.BooleanField(default=True, editable=False)
	
	class Meta:
		abstract = True

	
	@property
	def is_person_active(self):
		return self._is_person_active
	
	@property
	def search_names(self):
		return f'{self.full_name} ; {self.full_name.upper()} ; {self.full_name.lower()} ; {slugify(self.full_name).replace("-", " ")}'
	
	def composed_name(self): return '%s %s' % (self.first_name.split()[0], self.last_name.split()[-1])
	
	@property
	def full_name(self): return '%s %s' % (self.first_name, self.last_name)
	
	@property
	def short_name(self): return self.first_name.split()[0]
	
	def __str__(self): return self.full_name


class BirthDateMixin(models.Model):
	birth_date = models.DateField(_('Birth Date'))
	
	class Meta: abstract = True
	
	@property
	def age(self): return ((funcTime('today').date() - self.birth_date) / funcTime(365)).__round__(1)
	
	def age_from_date(self, date=None):
		if not date: date = datetime.date.today()
		return ((date - self.birth_date) / funcTime(365)).__round__(1)
	
	def date_from_age(self, age=None):
		if age: return funcTime('today') - ((self.age - age) * funcTime(365))


class DeathDateMixin(models.Model):
	_death_date = models.DateField(_('Death Date'), editable=False, blank=True, null=True)
	
	class Meta: abstract = True
	
	@property
	def death_date(self):
		if self._death_date: return self._death_date
		else: return None


class GenderMixin(models.Model):
	class Gender(models.TextChoices):
		MALE = 'Male', _("Male")
		FEMALE = 'Female', _("Female")
		UNDEFINED = 'Undefined', _("Undefined")
	
	gender = models.CharField(max_length=12, choices=Gender.choices, blank=True, null=True)
	
	class Meta: abstract = True
	
	def clean(self):
		super(GenderMixin, self).clean()
		if not self.gender: raise ValidationError(_('Please select an option for GENDER'))
	
	@property
	def is_male(self):
		if self.gender == self.Gender.MALE: return True
		else: return False
	
	@property
	def is_female(self):
		if self.gender == self.Gender.FEMALE: return True
		else: return False


class PhenotypeMixin(models.Model):
	class SkinColor(models.TextChoices):
		'''Reference at: http://humanphenotypes.net/metrics/skin.html'''
		PALE = 'pale', _('pale')
		FAIR = 'fair', _('fair')
		LIGHT_BROWN = 'light brown', _('light brown')
		MEDIUM_BROWN = 'medium brown', _('medium brown')
		DARK_BROWN = 'dark brown', _('dark brown')
		BLACK = 'black', _('black')
	
	skin_color = models.CharField(_('Skin Color'), max_length=25, choices=SkinColor.choices, null=True, blank=True)
	
	class HairColor(models.TextChoices):
		'''Reference at: http://humanphenotypes.net/metrics/haircol.html'''
		BLOND = 'blond', _('blond')
		RED = 'red', _('red')
		BROWN = 'brown', _('brown')
		BLACK = 'black', _('black')
	
	hair_color = models.CharField(_('Hair Color'), max_length=25, choices=HairColor.choices, null=True, blank=True,
	                              help_text=_('Natural color only'))
	
	class Meta: abstract = True


class ProfessionMixin(models.Model):
	class ProfessionType(models.TextChoices):
		MEDICAL_DOCTOR = 'medical doctor', _('medical doctor')
		NURSE = 'nurse', _('nurse')
		PSYCHOLOGIST = 'psychologist', _('psychologist')
	profession = models.CharField(_('Profession'), blank=True, null=True, max_length=50, choices=ProfessionType.choices)
	specialty = models.CharField(_('Specialty'), blank=True, null=True, max_length=255)
	subspecialty = models.CharField(_('Subspecialty'), blank=True, null=True, max_length=255)
	register = models.CharField(_('Professional Register'), blank=True, null=True, max_length=100)
	class Meta: abstract = True


class EnterpriseMixin(UserMixin):
	name = models.CharField(_('Enterprise Name'), max_length=255)
	class Meta: abstract = True
	
	def __str__(self):
		return f'{self.name}'


class SponsorMixin(UserMixin):
	name = models.CharField(max_length=200)
	_is_active = models.BooleanField(default=False, editable=False)
	class Meta: abstract = True
	
	
	@property
	def is_active(self): return self._is_active
	
	
	def activate(self):
		self._is_active = True
		return print(f'O usuário comercial {self.name} foi ativado')
	
	
	def deactivate(self):
		self._is_active = False
		return print(f'O usuário comercial {self.name} foi desativado')


class PatientMixin(models.Model):
	patient = models.ForeignKey('base.Patient', on_delete=models.SET_NULL, blank=True, null=True)
	class Meta: abstract = True
	
class ProfessionalMixin(models.Model):
	professional = models.ForeignKey('base.Professional', on_delete=models.SET_NULL, blank=True, null=True)
	class Meta: abstract = True


class ScheduleBase(ProfessionalMixin, PatientMixin, BaseNotesMixin):
	date = models.DateField()
	hour = models.IntegerField(choices=[(x, f'{x} h') for x in range(0, 24)], default=8)
	min = models.IntegerField(choices=[(x, f'{x} min') for x in range(0, 60, 15)], default=0)
	duration = models.IntegerField(choices=[(x, f'{x} h') for x in range(15, 125, 15)], default=60)
	class Meta: abstract = True
	
	@property
	def start(self):
		hour = datetime.timedelta(hours=self.hour)
		min = datetime.timedelta(minutes=self.min)
		total = hour + min
		return total
	
	@property
	def end(self):
		duration = datetime.timedelta(minutes=self.duration)
		return duration + self.start
	
	@property
	def min_duration(self):
		duration = datetime.timedelta(minutes=self.duration)
		return duration.min



class RelationBase(ProfessionalMixin, PatientMixin, CreationModificationDatesBase, UrlBase):
	enterprise = models.ForeignKey('base.Enterprise', on_delete=models.SET_NULL, blank=True, null=True)
	start_date = models.DateField(blank=True, null=True)
	class Meta: abstract = True

	def clean(self):
		super(RelationBase, self).clean()
		if not self.professional: raise ValidationError(_('You need a professional to save a relation'))
		if not self.patient: raise ValidationError(_('You need a patient to save a relation'))
	
	
	@property
	def local_site_full_address(self):
		if self.enterprise: return self.enterprise.full_address
		else: return self.professional.full_address
		
		
	@property
	def local_site_name(self):
		if self.enterprise: return self.enterprise.name
		else: return self.professional.full_name
		
	@property
	def local_site_phone(self):
		if self.enterprise: return self.enterprise.main_phone
		else: return self.professional.main_phone
		
	@property
	def visits_count(self):
		from Laelia.apps.care.models import Visit
		return Visit.objects.filter(relation=self).count()
	
	@property
	def trauma_count(self):
		from Laelia.apps.care.models import Event
		return Event.objects.filter(relation=self, event_type='trauma').count()
	
	@property
	def loss_count(self):
		from Laelia.apps.care.models import Event
		return Event.objects.filter(relation=self, event_type='loss').count()