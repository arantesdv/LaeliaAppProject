import datetime, uuid
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import ValidationError
from Laelia.apps.base.fields import MinMaxFloatField
from Laelia.apps.base.functions import funcTime
from Laelia.apps.base.mixins import UrlBase, CreationModificationDatesBase, DateTimeBase, ScheduleBase



class CareRelationMixin(UrlBase):
	relation = models.ForeignKey('base.Relation', on_delete=models.SET_NULL, blank=True, null=True)
	uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
	class Meta: abstract = True
	
	def clean(self):
		super(CareRelationMixin, self).clean()
		if not self.date: self.date = timezone.localdate()


class TimeLineMixin(CareRelationMixin, DateTimeBase):
	timeline_age = MinMaxFloatField(min_value=0, max_value=100, blank=True, null=True)
	timeline_date = models.DateField(blank=True, null=True)
	
	class Meta:
		abstract = True
	
	@staticmethod
	def age_from_date(patient, date):
		return ((date - patient.birth_date) / funcTime(365)).__round__(1)
	
	@staticmethod
	def date_from_age(patient, age=None):
		if age: return funcTime('today') - ((patient.age - age) * funcTime(365))
	
	@classmethod
	def from_age(cls, age):
		return cls(timeline_age=age)
	
	@classmethod
	def from_date(cls, date):
		return cls(timeline_date=date)
	
	@classmethod
	def from_year(cls, year):
		return cls(timeline_date=datetime.date(year=year, month=7, day=1))
	
	@classmethod
	def from_year_month(cls, year, month):
		return cls(timeline_date=datetime.date(year=year, month=month, day=1))
	
	def clean(self):
		
		if self.relation:
			if self.timeline_date:
				self.timeline_age = TimeLineMixin.age_from_date(patient=self.relation.patient, date=self.timeline_date)
			elif self.timeline_age:
				self.timeline_date = TimeLineMixin.date_from_age(patient=self.relation.patient, age=self.timeline_age)
			else:
				self.timeline_date = datetime.date.today()
				self.timeline_age = TimeLineMixin.age_from_date(patient=self.relation.patient, date=self.timeline_date)
		else:
			raise ValidationError(_('You need a relation'))

class EventBase(TimeLineMixin):
	class EventType(models.TextChoices):
		ABUSE = 'abuse', _('abuse')
		TRAUMA = 'trauma', _('trauma')
		REWARD = 'reward', _('reward')
		STRESSOR = 'stressor', _('stressor')
		ACHIEVEMENT = 'achievement', _('achievement')
		LOSS = 'loss', _('loss')
	event_type = models.CharField(blank=True, null=True, max_length=50, choices=EventType.choices)
	class ExperienceIntensity(models.IntegerChoices):
		MILD = 1, _('mild')
		MODERATE = 2, _('moderate')
		INTENSE = 3, _('intense')
	experience_intensity = models.IntegerField(choices=ExperienceIntensity.choices, blank=True, null=True)
	class SubjectiveExperience(models.IntegerChoices):
		POSITIVE = 1, _('positive')
		NEUTRAL = 0, _('neutral')
		NEGATIVE = -1, _('negative')
	subjective_experience = models.IntegerField(choices=SubjectiveExperience.choices, blank=True, null=True)
	notes = models.TextField(_('Notes'), blank=True, null=True)
	class Meta: abstract = True


class PharmacotherapyMixin(models.Model):
	class PharmacotherapyContext(models.TextChoices):
		SIDE_EFFECT = 'side effect', _('side effect')
		GOOD_RESPONSE = 'good response', _('good response')
		NO_RESPONSE = 'no response', _('no response')
	pharmaco_context = models.CharField(choices=PharmacotherapyContext.choices, blank=True, null=True, max_length=50)
	
	class Meta: abstract = True


class DocumentBase(DateTimeBase, UrlBase):
	uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
	relation = models.ForeignKey('base.Relation', on_delete=models.CASCADE, blank=True, null=True)
	
	class DocumentType(models.TextChoices):
		VISIT_ATTENDANCE = 'visit attendance', _('visit attendance')
		TREATMENT_ATTENDANCE = 'treatment attendance', _('treatment attendance')
		LEAVE = 'leave', _('leave')
		CAPABILITY = 'capability', _('capability')
		DISABILITY = 'disability', _('disability')
		REPORT = 'report', _('report')
		REFERRAL = 'referral', _('referral')
		RETURN = 'return', _('return')
	
	document_type = models.CharField(choices=DocumentType.choices, max_length=50, blank=True, null=True)
	document_note = models.TextField(blank=True, null=True)
	days = models.IntegerField(blank=True, null=True)

	
	class Meta:
		abstract = True
	
	def clean(self):
		super(DocumentBase, self).clean()
		if not self.relation: raise ValidationError(_("Please select a Relation"))
		if not self.document_type: raise ValidationError(_("Please select a Document Type"))
		if not self.document_date: self.document_date = datetime.date.today()
		if self.document_type == self.DocumentType.VISIT_ATTENDANCE:
			if not self.from_time or not self.to_time:
				msg = _("You need a 'from time' and 'to time' for Visit Attendance Certificate")
				raise ValidationError(msg)
		elif self.document_type == self.DocumentType.LEAVE:
			if not self.days:
				msg = _("You need a 'leave days'  for Leave Certificate")
				raise ValidationError(msg)
	
	def verbose_1(self):
		if self.document_type == self.DocumentType.VISIT_ATTENDANCE:
			title = 'ATESTADO DE COMPARECIMENTO'
			text1 = f'Certifico que {self.relation.patient} compareceu em visita com ' \
			       f'{self.relation.professional}  ' \
			       f' dia {self.document_date.strftime("%d/%m/%Y")}.'
			text2 = f'Local: {self.relation.professional.full_address}.\n Horario:  {self.from_time.strftime("%H:%M")} - {self.to_time.strftime("%H:%M")} '
		elif self.document_type == self.DocumentType.LEAVE:
			title = 'LICENÇA MÉDICA'
			text1 = f'Atesto para os devidos fins que {self.relation.patient} está em acompanhamento médico exibindo incapacidade ' \
			       f'funcional temporária decorrente de transtorno ativo. Solicito afastamento das suas atividades por {self.days} dias a ' \
			       f'partir de {self.document_date.strftime("%d/%m/%Y")}, enquando deve ficar sob supervisão. '
			text2 = 'Ao final deste período deverá comparecer em nova visita médica onde ' \
			       f'passará por avaliação da resposta, tolerabilidade e aderência ao tratamento indicado.'
		elif self.document_type == self.DocumentType.TREATMENT_ATTENDANCE:
			title = 'CERTIFICADO DE TRATAMENTO'
			text1 = f'Certifico que {self.relation.patient} esta em acompanhamento iniciado em {self.relation.start_date.strftime("%d/%m/%Y") if self.relation.start_date else self.relation.created.strftime("%d/%m/%Y")}.'
			text2 = f'Me encontro à disposição para maiores esclarecimentos caso necessário.'
		return title, text1, text2
	
	



class VisitBase(CareRelationMixin, DateTimeBase):
	urgency = models.BooleanField(_('Acute?'), default=False)
	new_complaint = models.BooleanField(_('New?'), default=False)
	complaint = models.CharField(max_length=200, blank=True, null=True)
	subjective = models.TextField(_('Subjective'), blank=True, null=True)
	objective = models.TextField(_('Objective'), blank=True, null=True)
	assessment = models.TextField(_('Assessment'), blank=True, null=True)
	plan = models.TextField(_('Plan'), blank=True, null=True)
	
	class Meta: abstract = True
	
	def clean(self):
		super(VisitBase, self).clean()
		if not self.date: self.date = timezone.now().date()
		if not self.from_date: self.from_date = self.date
		if not self.from_time: self.from_time = timezone.now().time()



class AttendanceMixin(CareRelationMixin, DateTimeBase):
	start = models.DateTimeField(blank=True, null=True)
	end = models.DateTimeField(blank=True, null=True)
	class Meta: abstract = True

class DocumentMixin(CareRelationMixin, DateTimeBase):
	introduction = models.TextField(blank=True, null=True)
	discussion = models.TextField(blank=True, null=True)
	conclusion = models.TextField(blank=True, null=True)
	class Meta: abstract = True
	
	
class VisitAttendanceBase(ScheduleBase, CareRelationMixin):
	class VisitReason(models.TextChoices):
		FIRST_VISIT = 'first visit', _('first visit')
		FOLLOW_UP_VISIT = 'follow up visit', _('follow up visit')
		EMERGENCY_VISIT = 'emergency visit', _('emergency visit')
		THERAPY_SESSION = 'therapy session', _('therapy session')
		DIAGNOSTIC_PROCEDURE = 'diagnostic procedure', _('diagnostic procedure')
		TREATMENT_PROCEDURE = 'treatment procedure', _('treatment procedure')
	visit_reason = models.CharField(max_length=50, choices=VisitReason.choices, blank=True, null=True)

	
	def clean(self):
		super(VisitAttendanceBase, self).clean()
		if not self.relation: raise ValidationError(_('Please select Relation'))
		if not self.date: raise ValidationError(_('Please fill Date'))
	
	@property
	def as_list_of_strings(self):
		strings, text = list(), str()
		strings.append(f'ATESTADO DE COMPARECIMENTO')
		text += f'Certifico que {self.relation.patient}'
		if self.visit_reason: text += f' compareceu em atendimento com {self.relation.professional} para {self.get_visit_reason_display()}'
		else: text += f' compareceu em atendimento com {self.relation.professional}'
		text += f' no dia {self.date.strftime("%d/%m/%Y")}'
		if self.hour and self.min: text += f' às {self.hour}:{self.min}.'
		elif self.hour: text += f' às {self.hour} h.'
		else: text += f'.'
		if self.duration:
			date_time = datetime.datetime(day=self.date.day, month=self.date.month, year=self.date.year, hour=self.hour, minute=self.min)
			duration = datetime.timedelta(minutes=self.duration)
			end = date_time + duration
			text += f' Não pode comparecer às suas atividades até {end.strftime(" às %H:%M h")}'
			if end.date() == self.date: text += ' do mesmo dia.'
			else: text += f' do dia {end.date()}.'
		strings.append(text)
		return strings

class TreatmentAttendanceBase(CareRelationMixin):
	start = models.DateField(_("Start Date"), blank=True, null=True)
	end = models.DateField(_("End Date"), blank=True, null=True)
	visits = models.IntegerField(_('Visits Completed'), help_text=_('Leave blank for auto completion'), blank=True, null=True)
	amount_paid = models.DecimalField(decimal_places=2, max_digits=7, blank=True, null=True)
	
	@property
	def as_list_of_strings(self):
		strings, text = list(), str()
		strings.append(f'CERTIFICAÇÃO DE TRATAMENTO')
		if self.relation: text += f'Certifico que {self.relation.patient}'
		if self.end != None: text += f' esteve em tratamento com {self.relation.professional} entre {self.start.strftime("%d/%m/%Y")} e {self.end.strftime("%d/%m/%Y")}.'
		else: text += f' está em tratamento com {self.relation.professional} iniciado em {self.start.strftime("%d/%m/%Y")} até o momento atual.'
		if self.visits and self.amount_paid: text += f' Compareceu ao longo deste período em {self.visits} visitas com custo total para o paciente de R$ {self.amount_paid}.'
		elif self.visits: text += f' Compareceu ao longo deste período em {self.visits} visitas no total.'
		elif self.amount_paid: text += f' O custo total ao longo deste período foi de R$ {self.amount_paid}.'
		strings.append(text)
		return strings





class PrescriptionBase(CareRelationMixin, CreationModificationDatesBase):
	comercial_drug = models.ForeignKey('meds.ComercialDrug', on_delete=models.CASCADE)
	dose = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
	dosage_regimen = models.IntegerField(choices=[(x, f'{x}x') for x in range(1, 13)], default=1, blank=True, null=True)
	class FrequencyChoices(models.IntegerChoices):
		DAILY = 1, _('daily')
		WEEKLY = 7, _('weekly')
		BIWEEKLY = 14, _('biweekly')
		MONTHLY = 30, _('month')
	frequency = models.IntegerField(choices=FrequencyChoices.choices, default=FrequencyChoices.DAILY)
	duration = models.IntegerField(blank=True, null=True,
	                               help_text=_('Days treatment duration. Keep blank for continuous'))
	class Meta: abstract = True



class MedicalLicenceBase(DocumentMixin):
	from_time = None
	to_date = None
	to_time = None
	class DisabilityType(models.TextChoices):
		PERMANENT_DISABILITY = 'permanent disability', _('permanent disability')
		TEMPORARY_DISABILITY = 'temporary disability', _('temporary disability')
	disability_type = models.CharField(choices=DisabilityType.choices, blank=True, null=True, max_length=50)
	leave_days = models.IntegerField()
	class Meta: abstract = True
	

