import datetime
from asgiref.sync import sync_to_async
from django.shortcuts import render, reverse, redirect
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, HttpResponseRedirect
from Laelia.apps.base.models import Relation, Patient, Professional, Enterprise, Employee, ComercialUser
from Laelia.apps.care.models import Event
from Laelia.apps.care.forms import TimeLineEventModelForm


professional_type = ContentType.objects.get(app_label='base', model='professional')
professional_model = professional_type.model_class()



class BaseHome(TemplateView):
	template_name = 'base/base_base.html'
	
	def get(self, request, *args, **kwargs):
		if request.user: user = request.user
		if user:
			kwargs['user'] = user
			patients = Patient.objects.filter(user=user)
			if len(patients) > 0: kwargs['patients'] = patients
			professionals = Professional.objects.filter(user=user)
			if len(professionals) > 0: kwargs['professionals'] = professionals
			enterprises = Enterprise.objects.filter(user=user)
			if len(enterprises) > 0: kwargs['enterprises'] = enterprises
			employees = Employee.objects.filter(user=user)
			if len(employees) > 0: kwargs['employees'] = employees
			comercials = ComercialUser.objects.filter(user=user)
			if len(comercials) > 0: kwargs['comercials'] = comercials
		return super(BaseHome, self).get(request, *args, **kwargs)
		
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context

class PatientList(ListView):
	model = Relation
	template_name = 'care/patient/list.html'
	object_list = None
	
	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		context['professional'] = get_object_or_404(professional_model, id=self.kwargs['professional_id'])
		context['patients'] = self.get_queryset()
		return context
	
	def get(self, request, *args, **kwargs):
		context = self.get_context_data()
		context['user'] = request.user
		return render(request, 'care/patient/list.html', context)
	
	def get_queryset(self):
		return Relation.objects.filter(
			professional=get_object_or_404(professional_model, id=self.kwargs['professional_id']))

class RelationDetail(DetailView):
	model = Relation
	template_name = 'relation/detail.html'
	pk_url_kwarg = 'relation_id'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['relation'] = get_object_or_404(Relation, pk=self.kwargs['relation_id'])
		context['patient_relations'] = Relation.objects.filter(patient=context['relation'].patient)
		context['events'] = Event.objects.filter(relation=context['relation'])
		return context
	
	
class EventCreate(CreateView):
	template_name = 'event/create.html'
	model = Event
	pk_url_kwarg = 'relation_id'
	form_class = TimeLineEventModelForm
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['relation'] = get_object_or_404(Relation, pk=self.kwargs['relation_id'])
		context['form'] = TimeLineEventModelForm({'relation': context['relation']})
		return context
	
	def post(self, request, *args, **kwargs):
		return super(EventCreate, self).post(request, *args, **kwargs)



class RelationCreate(CreateView):
	model = Relation
	fields = ['patient', 'professional']

	def get_object(self, queryset=None):
		return self.object

class EnterpriseDetail(DetailView):
	model = Enterprise
	template_name = 'enterprise/detail.html'
	pk_url_kwarg = 'enterprise_id'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['enterprise'] = get_object_or_404(Enterprise, pk=self.kwargs['enterprise_id'])
		return context

class ProfessionalDetail(DetailView):
	model = Professional
	template_name = 'professional/detail.html'
	pk_url_kwarg = 'professional_id'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['professional'] = get_object_or_404(Professional, pk=self.kwargs['professional_id'])
		context['relations'] = Relation.objects.filter(professional=context['professional'])
		return context

class EmployeeDetail(DetailView):
	model = Employee
	template_name = 'employee/detail.html'
	pk_url_kwarg = 'employee_id'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['employee'] = get_object_or_404(Employee, pk=self.kwargs['employee_id'])
		return context

class PatientDetail(DetailView):
	model = Patient
	template_name = 'patient/detail.html'
	pk_url_kwarg = 'patient_id'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['patient'] = get_object_or_404(Patient, pk=self.kwargs['patient_id'])
		context['professionals_list'] = [ relation.professional for relation in Relation.objects.filter(patient=context['patient']) ]
		return context


class ComercialDetail(DetailView):
	model = ComercialUser
	template_name = 'comercial/detail.html'
	pk_url_kwarg = 'comercial_id'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['comercial'] = get_object_or_404(ComercialUser, pk=self.kwargs['comercial_id'])
		return context


def user_profile_view(request):
	return render(request, 'base/user_profile.html', {'user': request.user})