import datetime
from asgiref.sync import sync_to_async
from django.urls import reverse_lazy
from django.shortcuts import render, reverse, redirect
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, HttpResponseRedirect
from Laelia.apps.base.models import Relation, Patient, Professional, Enterprise, Employee, ComercialUser
from Laelia.apps.care.models import Event
from Laelia.apps.care.forms import EventModelForm, VisitModelForm
from Laelia.apps.meds.models import Prescription

professional_type = ContentType.objects.get(app_label='base', model='professional')
professional_model = professional_type.model_class()



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
	template_name = 'base/relation/detail.html'
	pk_url_kwarg = 'relation_id'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['relation'] = get_object_or_404(Relation, pk=self.kwargs['relation_id'])
		context['patient_relations'] = Relation.objects.filter(patient=context['relation'].patient)
		context['events'] = Event.objects.filter(relation=context['relation'])
		context['prescriptions'] = Prescription.objects.filter(relation_id=self.kwargs.get('relation_id'))
		return context


class EventCreate(CreateView):
	model = Event
	template_name = 'care/event/create.html'
	pk_url_kwarg = 'event_id'
	form_class = EventModelForm
	object = None
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['relation'] = get_object_or_404(Relation, pk=self.kwargs['relation_id'])
		context['today'] = datetime.date.today()
		return context
	
	def get(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		context['form'] = EventModelForm({'relation': context['relation'], 'event_date': context['today']})
		return render(request, self.template_name, context)
	
	def post(self, request, *args, **kwargs):
		form = EventModelForm(request.POST)
		if form.is_valid():
			event = form.save()
			event.save()
			self.object = event
			return HttpResponseRedirect(
				reverse_lazy('base:relation-detail', kwargs={'relation_id': self.kwargs.get('relation_id')}))
		return render(request, self.template_name, {'form': form})
	
	def get_success_url(self):
		return HttpResponseRedirect(reverse('base:event-detail', kwargs={'relation_id': self.kwargs.get('relation_id'),
		                                                                 'event_id'   : self.object.pk}))


class RelationCreate(CreateView):
	model = Relation
	fields = ['patient', 'professional']
	
	def get_object(self, queryset=None):
		return self.object


class EnterpriseDetail(DetailView):
	model = Enterprise
	template_name = 'base/enterprise/detail.html'
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
		return context


class EmployeeDetail(DetailView):
	model = Employee
	template_name = 'base/employee/detail.html'
	pk_url_kwarg = 'employee_id'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['employee'] = get_object_or_404(Employee, pk=self.kwargs['employee_id'])
		return context





class EventDetail(DetailView):
	model = Event
	template_name = 'care/event/detail.html'
	pk_url_kwarg = 'event_id'
	object = None
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['event'] = get_object_or_404(Event, pk=self.kwargs['event_id'])
		context['relation'] = get_object_or_404(Relation, pk=self.kwargs['relation_id'])
		return context
	
	def get_object(self, queryset=None):
		return self.object


class VisitCreate(CreateView):
	model = Event
	template_name = 'care/visit/create.html'
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
		return render(request, 'care/visit/create.html', context)
	
	def post(self, request, *args, **kwargs):
		form = VisitModelForm(request.POST)
		if form.is_valid():
			event = form.save()
			event.save()
			self.object = event
			return HttpResponseRedirect(
				reverse_lazy('base:relation-detail', kwargs={'relation_id': self.kwargs.get('relation_id')}))
		return render(request, 'care/visit/create.html', {'form': form})
	
	def get_success_url(self):
		return HttpResponseRedirect(reverse('base:event-detail', kwargs={'relation_id': self.kwargs.get('relation_id'),
		                                                                 'event_id'   : self.object.pk}))

