import datetime
from asgiref.sync import sync_to_async
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.shortcuts import render, reverse,  get_object_or_404, get_list_or_404, HttpResponse
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from Laelia.apps.base.models import Relation, Patient, Professional, Enterprise, Employee, Sponsor
from Laelia.apps.care.models import Event, Document, Concept, Visit, TreatmentAttendanceCertificate, VisitAttendanceCertificate, MedicalLicence, Recipe
from Laelia.apps.care.forms import EventModelForm, VisitModelForm, CertificateModelForm, ReferralModelForm, ReportModelForm
from Laelia.apps.meds.models import Prescription
from Laelia.apps.base.functions import funcTime
from Laelia.pdf.engine import PdfCreator

professional_type = ContentType.objects.get(app_label='base', model='professional')
professional_model = professional_type.model_class()

#######################################################################################################################
# CLASS BASED VIEWS
#######################################################################################################################
class BaseMixin:
	user_related = None
	professional = None
	patient = None
	relation = None
	relations = None
	
	class Meta:
		abstract = True
	
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
				context['relations'] = get_list_or_404(Relation, professional=context['professional'])
				self.patient = context['patient']
				self.professional = context['professional']
				self.relations = context['relations']
			if kwargs.get('visit_id'):
				context['object'] = get_object_or_404(Visit, pk=kwargs.get('visit_id'))
				context['relation'] = context['object'].relation
				context['professional'] = context['relation'].professional
				context['patient'] = context['relation'].patient
				context['relations'] = get_list_or_404(Relation, professional=context['professional'])
				if Recipe.objects.filter(relation__patient=context['patient'], date=context['object'].date):
					context['prescriptions'] = Recipe.objects.filter(relation__patient=context['patient'], date=context['object'].date)
				else:
					context['prescriptions'] = None
		if request:
			if request.user:
				context['user'] = request.user
				if context['user'].is_authenticated:
					context['user_related'] = self.find_user_related(user=request.user)
		return context


class CompileContext:
	class Meta: abstract = True
	
	@staticmethod
	def add_to_context(request=None, kwargs=None, context=None):
		if kwargs:
			if kwargs.get('relation_id'):
				context['relation'] = get_object_or_404(Relation, pk=kwargs.get('relation_id'))
				context['patient'] = context['relation'].patient
				context['professional'] = context['relation'].professional
			if kwargs.get('patient_id'): context['patient'] = get_object_or_404(Patient, pk=kwargs['patient_id'])
			if kwargs.get('professional_id'): context['professional'] = get_object_or_404(Professional, pk=kwargs['professional_id'])
			if kwargs.get('visit_id'): context['visit'] = get_object_or_404(Visit, pk=kwargs.get('visit_id'))
			if kwargs.get('treatment_certificate_id'): context['treatment_certificate'] = get_object_or_404(TreatmentAttendanceCertificate, pk=kwargs.get('treatment_certificate_id'))
			if kwargs.get('attendance_certificate_id'): context['attendance_certificate'] = get_object_or_404(VisitAttendanceCertificate, pk=kwargs.get('attendance_certificate_id'))
			if kwargs.get('event_id'): context['event'] = get_object_or_404(Visit, pk=kwargs.get('event_id'))
			if kwargs.get('licence_id'): context['licence'] = get_object_or_404(MedicalLicence, pk=kwargs.get('licence_id'))
		if request:
			if request.user: context['user'] = request.user
		return context


class PatientList(BaseMixin, ListView):
	model = Relation
	template_name = 'base/professional/patient/list.html'
	object_list = None
	
	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		context['professional'] = get_object_or_404(professional_model, id=self.kwargs['professional_id'])
		context['patients'] = self.get_queryset()
		return context
	
	def get(self, request, *args, **kwargs):
		context = super().get_context_data(**kwargs)
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
		context['professional'] = context['relation'].professional
		context['patient_relations'] = Relation.objects.filter(patient=context['relation'].patient)
		context['prescriptions'] = get_list_or_404(Prescription, relation_id=self.kwargs.get('relation_id'))
		context['object'] = context['relation']
		context['patient'] = context['relation'].patient
		return render(request, self.template_name, context)


class EventCreate(BaseMixin, CreateView):
	model = Event
	template_name = 'base/professional/patient/event/create.html'
	pk_url_kwarg = 'event_id'
	form_class = EventModelForm
	object = None
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['relation'] = get_object_or_404(Relation, pk=self.kwargs['relation_id'])
		context['professional'] = context['relation'].professional
		context['events'] = get_object_or_404(Event, relation=context['relation'])
		return context
	
	def get(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		context = self.add_to_context(request=request, kwargs=kwargs, context=context)
		context['form'] = EventModelForm({'relation': context['relation']})
		return render(request, self.template_name, context)
	
	def post(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		form = EventModelForm(request.POST)
		if form.is_valid():
			event = form.save()
			event.save()
			self.object = event
			return HttpResponseRedirect(reverse_lazy('care:event-detail', kwargs={'relation_id': self.kwargs.get('relation_id'),
		                                                                 'event_id'   : self.object.pk}))
		context['form'] = form
		return render(request, self.template_name, context)
	
	def get_success_url(self):
		return HttpResponseRedirect(reverse('care:event-detail', kwargs={'relation_id': self.kwargs.get('relation_id'),
		                                                                 'event_id'   : self.object.pk}))


class EventDetail(BaseMixin, DetailView):
	model = Event
	template_name = 'base/professional/patient/event/detail.html'
	pk_url_kwarg = 'event_id'
	object = None
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['event'] = get_object_or_404(Event, pk=self.kwargs['event_id'])
		context['relation'] = get_object_or_404(Relation, pk=self.kwargs['relation_id'])
		context['professional'] = context['relation'].professional
		context['events'] = get_object_or_404(Event, relation=context['relation'])
		return context
	
	def get_object(self, queryset=None):
		return self.object
	
	def get(self, request, *args, **kwargs):
		context = super().get_context_data(**kwargs)
		context['event'] = get_object_or_404(Event, pk=self.kwargs['event_id'])
		context['relation'] = get_object_or_404(Relation, pk=self.kwargs['relation_id'])
		context['professional'] = context['relation'].professional
		context['events'] = get_object_or_404(Event, relation=context['relation'])
		context = self.add_to_context(request=request, kwargs=kwargs, context=context)
		return render(request, self.template_name, context)



class CertificateCreate(BaseMixin, CreateView):
	model = Document
	form_class = CertificateModelForm
	template_name = 'base/professional/patient/document/certificate/create.html'
	pk_url_kwarg = 'certificate_id'
	object = None
	
	def get_context_data(self, **kwargs):
		context = super(CertificateCreate, self).get_context_data()
		context['relation'] = get_object_or_404(Relation, pk=self.kwargs['relation_id'])
		context['today'] = datetime.date.today()
		context['events'] = get_object_or_404(Event, relation=context['relation'])
		context['prescriptions'] = get_object_or_404(Prescription, relation=context['relation'])
		context['documents'] = get_object_or_404(Document, relation=context['relation'])
		context['professional'] = context['relation'].professional
		context['patient'] = context['relation'].patient
		return context
	
	def get(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		context = self.add_to_context(request=request, kwargs=kwargs, context=context)
		context['form'] = CertificateModelForm({'relation': context['relation'], 'document_date': datetime.date.today()}, request=request, relation_id=self.kwargs.get('relation_id'))
		return render(request, self.template_name, context)
	
	def post(self, request, *args, **kwargs):
		form = CertificateModelForm(request.POST)
		if form.is_valid():
			object = form.save()
			object.save()
			self.object = object
			return HttpResponseRedirect(
				reverse_lazy('care:relation-detail', kwargs={'relation_id': self.kwargs.get('relation_id')}))
		return render(request, self.template_name, {'form': form})
	
	def get_success_url(self):
		return HttpResponseRedirect(reverse('care:document-detail', kwargs={'relation_id': self.kwargs.get('relation_id'),
		                                                                 'document_id'   : self.object.pk}))


class DocumentDetail(BaseMixin, DetailView):
	model = Event
	template_name = 'base/professional/patient/document/detail.html'
	pk_url_kwarg = 'document_id'
	object = None
	
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['document'] = get_object_or_404(Document, pk=self.kwargs['document_id'])
		context['relation'] = get_object_or_404(Relation, pk=self.kwargs['relation_id'])
		context['professional'] = context['relation'].professional
		context['patient'] = context['relation'].patient
		return context
	
	def get_object(self, queryset=None):
		return self.object
	
	
	def get(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		context = self.add_to_context(request=request, kwargs=kwargs, context=context)
		return render(request, self.template_name, context)


class ReportCreate(BaseMixin, CreateView):
	template_name = 'base/professional/patient/document/report/create.html'
	model = Document
	form_class = ReportModelForm
	pk_url_kwarg = 'document_id'
	object = None
	
	def get(self, request, *args, **kwargs):
		context = super().get_context_data(**kwargs)
		context = self.add_to_context(request=request, kwargs=kwargs, context=context)
		context['relation'] = Relation.objects.get(pk=self.kwargs.get('relation_id'))
		context['professional'] = context['relation'].professional
		context['patient'] = context['relation'].patient
		context['form'] = self.form_class({
			'relation' : context['relation'],
			'document_date': funcTime('today').date(),
		})
		context['concepts'] = Concept.objects.all()
		return render(request, self.template_name, context)
	
	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			print(f'instance {instance} saved')
			return HttpResponseRedirect(instance.get_absolute_url())

class ReportDetail(BaseMixin, DetailView):
	model = Document
	template_name = 'base/professional/patient/document/detail.html'
	pk_url_kwarg = 'document_id'
	object = None
	
	
	
	def get(self, request, *args, **kwargs):
		context = super().get_context_data(**kwargs)
		context = self.add_to_context(request=self.request, kwargs=self.kwargs, context=context)
		self.object = Document.objects.get(pk=self.kwargs.get('document_id'))
		context['object'] = self.object
		return render(request, self.template_name, context)


class VisitCreate(BaseMixin, CreateView):
	model = Visit
	template_name = 'base/professional/patient/visit/create.html'
	pk_url_kwarg = 'visit_id'
	form_class = VisitModelForm
	object = None
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['relation'] = get_object_or_404(Relation, pk=self.kwargs['relation_id'])
		context['professional'] = context['relation'].professional
		return context
	
	def get(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		context = self.add_to_context(request=request, kwargs=kwargs, context=context)
		context['form'] = VisitModelForm({
			'relation': context['relation'],
			'date'    : datetime.date.today(),
		})
		return render(request, self.template_name, context)
	
	def post(self, request, *args, **kwargs):
		form = VisitModelForm(request.POST)
		if form.is_valid():
			visit = form.save()
			visit.save()
			self.object = visit
			return HttpResponseRedirect(
				reverse_lazy('care:visit-detail',
				             kwargs={'relation_id': self.kwargs.get('relation_id'), 'visit_id': self.object.pk})
			)
		return render(request, self.template_name, {'form': form})
	

	
class VisitDetail(BaseMixin, DetailView):
	pk_url_kwarg = 'visit_id'
	model = Visit
	template_name = 'base/professional/patient/visit/detail.html'
	object = None
	
	
	def get(self, request, *args, **kwargs):
		context = super().get_context_data(**kwargs)
		context = self.add_to_context(request, kwargs=kwargs, context=context)
		return render(request, self.template_name, context)




class VisitList(BaseMixin, ListView):
	template_name = 'base/professional/patient/visit/list.html'
	model = Visit
	page_kwarg = 'relation_id'
	object_list = None
	
	
	def get(self, request, *args, **kwargs):
		context = super().get_context_data(**kwargs)
		context = self.add_to_context(request=request, kwargs=kwargs, context=context)
		context['visits'] = self.model.objects.filter(relation_id=self.kwargs.get('relation_id'))
		context = CompileContext.add_to_context(request=request, kwargs=kwargs, context=context)
		return render(request, self.template_name, context)
	

class MedicalLicenceDetail(DetailView):
	template_name = 'base/professional/patient/document/licence/detail.html'
	model = MedicalLicence
	object = None
	
#######################################################################################################################
# FUNCTION VIEWS
#######################################################################################################################


def build_visit(request, relation_id=0, visit_id=0):
	context = dict()
	if visit_id != 0:
		visit = Visit.objects.get(pk=visit_id)
		patient = visit.relation.patient
		context['visit'] = visit
		context['patient'] = patient
	else:
		return None
	
	if visit.date:
		date = visit.date
	else:
		date = funcTime('today').date()
	
	context['date'] = date.strftime('%d-%m-%Y')
	context['introduction'] = ''
	context['section_1'] = visit.subjective
	context['section_2'] = visit.objective
	context['section_3'] = visit.assessment
	context['plan'] = visit.plan
	
	pdf = PdfCreator(pagesize='A4', relation_id=relation_id).create_visit(context=context)
	response = HttpResponse(content_type='application/pdf')
	patient = context['patient']
	response['Content-Disposition'] = f'attachment; filename=Visita de {patient} dia {date}.pdf'
	response.write(pdf)
	return response


def build_visit_plan(request, relation_id=0, visit_id=0):
	context = dict()
	if visit_id != 0:
		visit = Visit.objects.get(pk=visit_id)
		patient = visit.relation.patient
		context['visit'] = visit
		context['patient'] = patient
	else:
		return None
	
	if visit.date:
		date = visit.date
	else:
		date = funcTime('today').date()
	
	context['date'] = date.strftime('%d-%m-%Y')
	context['plan'] = visit.plan
	
	pdf = PdfCreator(pagesize='A5', relation_id=relation_id).create_visit(context=context)
	response = HttpResponse(content_type='application/pdf')
	patient = context['patient']
	response['Content-Disposition'] = f'attachment; filename=Visita de {patient} dia {date}.pdf'
	response.write(pdf)
	return response


def medical_licence_pdf(request, relation_id=0, licence_id=0):
	context = dict()
	if licence_id != 0:
		licence = get_object_or_404(MedicalLicence, pk=licence_id)
		context['licence'] = licence
		context['patient'] = licence.relation.patient
		context['professional'] = licence.relation.professional

	else:
		return None
	
	if licence.from_date: date = licence.from_date
	elif licence.date: date = licence.date
	else:
		date = funcTime('today').date()
	
	context['date'] = date.strftime('%d-%m-%Y')
	context['introduction'] = licence.introduction
	context['section_1'] = licence.discussion
	context['section_2'] = licence.conclusion
	context['section_3'] = f'Solicito afastamento {["temporário" if licence.disability_type == "temporary disability" else ""][0]} de {licence.relation.patient} por {licence.leave_days} dias a partir de {date.strftime("%d/%m/%Y")}.'
	context['finalization'] = f'Atenciosamente,'
	
	pdf = PdfCreator(pagesize='A5', relation_id=relation_id).create_medical_licence(context=context)
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = f'attachment; filename=Atestado Médico de {licence.relation.patient} dia {date} por {licence.leave_days} dias.pdf'
	response.write(pdf)
	return response



