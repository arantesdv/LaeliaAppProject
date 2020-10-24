import datetime
from asgiref.sync import sync_to_async
from django.urls import reverse_lazy
from django.shortcuts import render, reverse, redirect
from django.shortcuts import get_object_or_404, get_list_or_404
from django.views.generic import ListView, DetailView, TemplateView, CreateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView, auth_login, auth_logout
from django.contrib.auth.mixins import AccessMixin
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from Laelia.apps.base.models import Relation, Patient, Professional, Enterprise, Employee, Sponsor, Schedule
from Laelia.apps.care.models import Event, Document, Visit
from Laelia.apps.care.forms import EventModelForm, VisitModelForm, ReportModelForm, ReferralModelForm, CertificateModelForm
from Laelia.apps.meds.models import Prescription
from . forms import PatientModelForm
from . functions import funcTime
from Laelia.apps.care.views import CompileContext

professional_type = ContentType.objects.get(app_label='base', model='professional')
professional_model = professional_type.model_class()


class BaseMixin:
	user_related = None
	professional = None
	patient = None
	relation = None
	relations = None
	class Meta: abstract = True
	
	def find_user_related(self, user=None):
		if user != None:
			if get_object_or_404(Professional, user=user):
				self.user_related = get_object_or_404(Professional, user=user)
				self.professional = self.user_related
			elif get_object_or_404(Patient, user=user):
				self.user_related = get_object_or_404(Patient, user=user)
			elif get_object_or_404(Employee, user=user):
				self.user_related = get_object_or_404(Employee, user=user)
			elif get_object_or_404(Sponsor, user=user):
				self.user_related = get_object_or_404(Sponsor, user=user)
			elif get_object_or_404(Enterprise, user=user):
				self.user_related = get_object_or_404(Enterprise, user=user)
		return self.user_related


	def add_to_context(self, request=None, kwargs=None, context=None):
		if kwargs:
			if kwargs.get('patient_id'):
				context['patient_id'] = kwargs.get('patient_id')
				context['patient'] = get_object_or_404(Patient, pk=kwargs['patient_id'])
				self.patient = context['patient']
			if kwargs.get('professional_id'):
				context['professional_id'] = kwargs.get('professional_id')
				context['professional'] = get_object_or_404(Professional, pk=kwargs['professional_id'])
				context['relations'] = get_list_or_404(Relation, professional=context['professional'])
				self.relations = context['relations']
				self.professional = context['professional']
			if kwargs.get('employee_id'):
				context['employee'] = get_object_or_404(Employee, pk=kwargs.get('employee_id'))
			if kwargs.get('sponsor_id'):
				context['sponsor'] = get_object_or_404(Sponsor, pk=kwargs.get('sponsor_id'))
			if kwargs.get('enterprise_id'):
				context['enterprise'] = get_object_or_404(Enterprise, pk=kwargs.get('enterprise_id'))
			if kwargs.get('relation_id'):
				context['relation_id'] = kwargs.get('relation_id')
				context['relation'] = get_object_or_404(Relation, pk=kwargs.get('relation_id'))
				context['patient'] = context['relation'].patient
				context['professional'] = context['relation'].professional
				self.patient = context['patient']
				self.professional = context['professional']
		if request:
			if request.user:
				context['user'] = request.user
				if context['user'].is_authenticated:
					context['user_related'] = self.find_user_related(user=request.user)
		return context




class Home(BaseMixin,  TemplateView):
	template_name = 'bootstrap_pages/index5.html'
	
	def get(self, request, *args, **kwargs):
		context = super().get_context_data(**kwargs)
		context = self.add_to_context(request, kwargs, context)
		return render(request, self.template_name, context)


class BaseHome(BaseMixin, AccessMixin, TemplateView):
	template_name = 'home.html'
	login_url = settings.LOGIN_URL
	
	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated: return redirect(reverse_lazy('profile'))
		else: return redirect(reverse_lazy('login'))
		
	
class RelationList(BaseMixin, ListView):
	model = Relation
	template_name = 'base/professional/patient/list.html'
	object_list = None
	
	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		context['professional'] = get_object_or_404(professional_model, id=self.kwargs['professional_id'])
		context['relations'] = self.get_queryset()
		context['relations_count'] = f'{self.get_queryset().count()} ' + ['paciente relacionado' if self.get_queryset().count() <= 1 else 'pacientes relacionados'][0]
		return context
	
	def get(self, request, *args, **kwargs):
		context = self.get_context_data()
		context = self.add_to_context(request=request, kwargs=kwargs, context=context)
		return render(request, self.template_name, context)
	
	def get_queryset(self):
		return Relation.objects.filter(
			professional=get_object_or_404(professional_model, id=self.kwargs['professional_id']))


class RelationDetail(BaseMixin, DetailView):
	model = Relation
	template_name = 'base/professional/patient/detail.html'
	pk_url_kwarg = 'relation_id'
	object = None
	
	
	def get(self, request, *args, **kwargs):
		context = super().get_context_data(**kwargs)
		context = self.add_to_context(request=request, kwargs=kwargs, context=context)
		context['relation'] = get_object_or_404(Relation, pk=self.kwargs['relation_id'])
		context['patient_relations'] = Relation.objects.filter(patient=context['relation'].patient)
		context['events'] = Event.objects.filter(relation=context['relation'])
		context['visits'] = Visit.objects.filter(relation=context['relation'])
		context['prescriptions'] = Prescription.objects.filter(relation=context['relation'])
		context['patient'] = context['relation'].patient
		context['professional'] = context['relation'].professional
		context['relations'] = get_list_or_404(Relation, professional=context['professional'])
		if self.user_related != self.professional:
			return HttpResponseRedirect(reverse_lazy('logout'))
		return render(request, self.template_name, context)


class EventCreate(CreateView):
	model = Event
	template_name = 'base/professional/patient/event/create.html'
	pk_url_kwarg = 'event_id'
	form_class = EventModelForm
	object = None
	

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['relation'] = get_object_or_404(Relation, pk=self.kwargs['relation_id'])
		context['professional'] = context['relation'].professional
		context['events'] = Event.objects.filter(relation=context['relation'])
		context['today'] = datetime.date.today()
		return context
	
	def get(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		context['form'] = EventModelForm({'relation': context['relation'], 'event_date': context['today']})
		return render(request, self.template_name, context)
	
	def post(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		context['form'] = EventModelForm(request.POST)
		if context['form'].is_valid():
			event = context['form'].save()
			event.save()
			self.object = event
			return render(request, event.get_absolute_url())
			#return HttpResponseRedirect(reverse_lazy('base:relation-detail', kwargs={'relation_id': self.kwargs.get('relation_id')}))
		return render(request, self.template_name, context)


	def get_success_url(self):
		return HttpResponseRedirect(reverse('base:event-detail', kwargs={'relation_id': self.kwargs.get('relation_id'), 'event_id': self.object.pk}))



class RelationCreate(CreateView):
	model = Relation
	fields = ['patient', 'professional']

	def get_object(self, queryset=None):
		return self.object

class EnterpriseDetail(DetailView):
	model = Enterprise
	template_name = 'base/facilify/detail.html'
	pk_url_kwarg = 'enterprise_id'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['enterprise'] = get_object_or_404(Enterprise, pk=self.kwargs['enterprise_id'])
		return context

class ProfessionalDetail(DetailView):
	model = Professional
	template_name = 'base/professional/detail.html'
	pk_url_kwarg = 'professional_id'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['professional'] = get_object_or_404(Professional, pk=self.kwargs['professional_id'])
		context['relations'] = Relation.objects.filter(professional=context['professional'])
		context['visits'] = Event.objects.filter(relation__professional=context['professional']).count()
		return context

class EmployeeDetail(DetailView):
	model = Employee
	template_name = 'base/employee/detail.html'
	pk_url_kwarg = 'employee_id'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['employee'] = get_object_or_404(Employee, pk=self.kwargs['employee_id'])
		return context

class PatientDetail(BaseMixin, DetailView):
	model = Patient
	template_name = 'base/patient/detail.html'
	pk_url_kwarg = 'patient_id'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['patient'] = get_object_or_404(Patient, pk=self.kwargs['patient_id'])
		context['professionals_list'] = [relation.professional for relation in Relation.objects.filter(patient=context['patient']) ]
		context['events'] = Event.objects.filter(relation__patient=context['patient'])
		context['prescriptions'] = Prescription.objects.filter(relation__patient=context['patient'])
		return context
	
	def get(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		context = self.add_to_context(request=request, kwargs=kwargs, context=context)
		return render(request, self.template_name, context)


class ComercialDetail(DetailView):
	model = Sponsor
	template_name = 'base/sponsor/detail.html'
	pk_url_kwarg = 'comercial_id'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['comercial'] = get_object_or_404(Sponsor, pk=self.kwargs['comercial_id'])
		return context


def user_profile_view(request):
	return render(request, 'home.html', {'user': request.user})


class EventDetail(DetailView):
	model = Event
	template_name = 'base/professional/patient/event/detail.html'
	pk_url_kwarg = 'event_id'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['event'] = get_object_or_404(Event, pk=self.kwargs['event_id'])
		context['relation'] = get_object_or_404(Relation, pk=self.kwargs['relation_id'])
		context['events'] = Event.objects.filter(relation=context['relation'])
		return context


class VisitCreate(CreateView):
	model = Event
	template_name = 'base/professional/patient/visit/create.html'
	pk_url_kwarg = 'event_id'
	form_class = VisitModelForm
	object = None
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['relation'] = get_object_or_404(Relation, pk=self.kwargs['relation_id'])
		context['today'] = datetime.date.today()
		return context
	
	def get(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		context['form'] = VisitModelForm({'relation': context['relation'], 'event_date': context['today']})
		return render(request, self.template_name, context)
	
	def post(self, request, *args, **kwargs):
		form = VisitModelForm(request.POST)
		if form.is_valid():
			event = form.save()
			event.save()
			self.object = event
			return HttpResponseRedirect(
				reverse_lazy('care:visit-detail', kwargs={'relation_id': self.kwargs.get('relation_id'), 'event_id': self.object.pk}))
		return render(request, self.template_name, {'form': form})
	
	def get_success_url(self):
		return HttpResponseRedirect(reverse('base:event-detail', kwargs={'relation_id': self.kwargs.get('relation_id'),
		                                                                 'event_id'   : self.object.pk}))
	
	
class PatientCreate(BaseMixin, CreateView):
	model = Patient
	template_name = None
	pk_url_kwarg = 'patient_id'
	form_class = PatientModelForm
	object = None
	success_url = None


	def get(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		context = self.add_to_context(request=request, kwargs=kwargs, context=context)
		context['form'] = PatientModelForm(request=request)
		if isinstance(context['user_related'], Professional):
			self.template_name = 'base/professional/patient/create.html'
			context['professional'] = context['user_related']
		elif isinstance(context['user_related'], Employee):
			self.template_name = 'base/employee/patient/create.html'
			context['employee'] = context['user_related']
		return render(request, self.template_name, context)
	
	def post(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		context = self.add_to_context(request=request, kwargs=kwargs, context=context)
		context['form'] = PatientModelForm(request.POST, request.FILES, request=request)
		if context['form'].is_valid():
			self.object = context['form'].save()
			if isinstance(context['user_related'], Professional):
				relation, created = Relation.objects.get_or_create(patient=self.object, professional=context['user_related'])
				if created:
					relation.save()
					return HttpResponseRedirect(reverse_lazy('base:relation-detail', kwargs={'relation_id': relation.pk}))
				else: return HttpResponseRedirect(reverse_lazy('base:patient-detail', kwargs={'patient_id': self.object.pk}))
			else: return HttpResponseRedirect(reverse_lazy('base:patient-detail', kwargs={'patient_id': self.object.pk}))
		return render(request, self.template_name, context)


class PatientDelete(DeleteView):
	template_name = 'base/patient/delete.html'

class LaeliaLogin(LoginView):
	template_name = 'registration/login.html'


class ProfileView(BaseMixin, TemplateView):
	template_name = None


	def get(self, request, *args, **kwargs):
		context = super().get_context_data(**kwargs)
		context = self.add_to_context(request=request, kwargs=kwargs, context=context)
		if context['professional']:
			context['visits'] = Visit.objects.filter(relation__professional=context['professional'])
			self.template_name = 'base/professional/home.html'
		elif context['patient']: self.template_name = 'base/patient/home.html'
		elif context['employee']: self.template_name = 'base/employee/home.html'
		elif context['enterprise']: self.template_name = 'base/facilify/home.html'
		elif context['comercial']: self.template_name = 'base/sponsor/home.html'
		return render(request, self.template_name, context)
	


class LaeliaLogout(LogoutView):
	template_name = 'registration/logout.html'


class ScheduleVisitCreate(CreateView):
	from .forms import ScheduleVisitModelForm
	model = Schedule
	template_name = 'base/professional/schedule/visit/create.html'
	pk_url_kwarg = 'schedule_id'
	form_class = ScheduleVisitModelForm
	object = None
	
	def get(self, request, *args, **kwargs):
		context = super().get_context_data(**kwargs)
		context['professional'] = Professional.objects.get(pk=self.kwargs.get('professional_id'))
		context['form'] = self.form_class(
			{'professional': context['professional'],
			 'date': funcTime('today').date() + funcTime(30),
			 'hour': 12,
			 'min': 0,
			 'duration': 45,
			 }
		)
		return render(request, self.template_name, context)
	
	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST, request.FILES)
		if form.is_valid():
			object = form.save()
			professional = object.professional
			return HttpResponseRedirect(reverse('base:schedule-detail', kwargs={'professional_id': professional.pk, 'schedule_id': object.pk}))
		professional = Professional.objects.get(pk=self.kwargs.get('professional_id'))
		return render(request, self.template_name, {'form': form, 'professional': professional})
	
class ScheduleEventCreate(CreateView):
	from .forms import ScheduleEventModelForm
	model = Schedule
	template_name = 'base/professional/schedule/event/create.html'
	pk_url_kwarg = 'schedule_id'
	form_class = ScheduleEventModelForm
	object = None
	
	def get(self, request, *args, **kwargs):
		context = super().get_context_data(**kwargs)
		context['professional'] = Professional.objects.get(pk=self.kwargs.get('professional_id'))
		context['form'] = self.form_class({
			'professional': context['professional'],
			'date': funcTime('today').date() + funcTime(1),
			'patient_id': None,
			'hour'    : 8,
			'min'     : 0,
			'duration': 120,
		})
		return render(request, self.template_name, context)
	
	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST, request.FILES)
		if form.is_valid():
			object = form.save()
			professional = object.professional
			return HttpResponseRedirect(reverse('base:schedule-detail', kwargs={'professional_id': professional.pk, 'schedule_id': object.pk}))
		professional = Professional.objects.get(pk=self.kwargs.get('professional_id'))
		return render(request, self.template_name, {'form': form, 'professional': professional})
	
	
class ScheduleView(TemplateView, DetailView):
	template_name = 'base/professional/schedule/home.html'
	pk_url_kwarg = 'professional_id'
	object = None
	
	def get(self, request, *args, **kwargs):
		context = super().get_context_data(**kwargs)
		context['professional'] = Professional.objects.get(pk=self.kwargs.get('professional_id'))
		context['schedules'] = Schedule.objects.filter(professional=context['professional'])
		return render(request, self.template_name, context)
	


class ScheduleDetail(DetailView):
	model = Schedule
	template_name = 'base/professional/schedule/detail.html'
	pk_url_kwarg = 'schedule_id'
	object = None
	

	def get_object(self, queryset=None):
		self.object = Schedule.objects.get(pk=self.kwargs.get('schedule_id'))
		return self.object
	
	def get(self, request, *args, **kwargs):
		object = self.get_object()
		professional = object.professional
		return render(request, self.template_name, {'object': object, 'professional': professional})
	
	
	
