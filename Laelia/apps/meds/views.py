import datetime
from asgiref.sync import sync_to_async
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, reverse, redirect
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView
from django.views.generic.dates import YearArchiveView
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from Laelia.apps.base.models import Relation, Patient, Professional
from .models import ActiveCompound, ComercialDrug, CompoundSet, Prescription
from .forms import ActiveCompoundModelForm, ComercialDrugModelForm, CompoundSetModelForm, PrescriptionModelForm


class MedsHome(TemplateView):
	template_name = 'meds/index.html'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		if self.request.user: context['user'] = self.request.user
		else: context['user'] = None
		if context['user'] != None: context['professional'] = Professional.objects.get(user=context['user'])
		else: context['professional'] = None
		context['meds'] = ComercialDrug.objects.all()
		return context
	
	@staticmethod
	def get_professional(request):
		professional = None
		if request:
			user = request.user
			professional = Professional.objects.get(user=user)
		return professional
	
	
	@staticmethod
	def all_active_compounds():
		return ActiveCompound.objects.all()
	
	@staticmethod
	def all_professional_relations(request=None, professional_id=None):
		if professional_id != None:
			relations = Relation.objects.filter(professional_id=professional_id)
		elif request != None:
			professional = MedsHome.get_professional(request=request)
			relations = Relation.objects.filter(professional=professional)
		else:
			raise ValueError(_('You need a request or a professional_id'))
		return relations
	
	
	@staticmethod
	def patient_prescriptions(relation_id=None):
		if relation_id != None: return Prescription.objects.get(relation_id=relation_id)
		else: None



class ActiveCompoundDetail(DetailView):
	model = ActiveCompound
	template_name = 'meds/active_compound/detail.html'
	pk_url_kwarg = 'active_compound_id'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['active_compound'] = get_object_or_404(ActiveCompound, pk=self.kwargs['active_compound_id'])
		context['professional'] = MedsHome.get_professional(request=self.request)
		return context


class ComecialDrugDetail(DetailView):
	model = ComercialDrug
	template_name = 'meds/comercial_drug/detail.html'
	pk_url_kwarg = 'comercial_drug_id'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['comercial_drug'] = get_object_or_404(ActiveCompound, pk=self.kwargs['comercial_drug_id'])
		context['professional'] = MedsHome.get_professional(request=self.request)
		return context


class ComecialDrugCreate(CreateView):
	model = ComercialDrug
	template_name = 'meds/comercial_drug/create.html'
	pk_url_kwarg = 'comercial_drug_id'
	form_class = ComercialDrug
	object = None
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['today'] = datetime.date.today()
		context['professional'] = MedsHome.get_professional(request=self.request)
		return context
	
	def get(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		context['form'] = ComercialDrugModelForm()
		return render(request, self.template_name, context)
	
	def post(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		form = ComercialDrugModelForm(request.POST)
		if form.is_valid():
			object = form.save()
			object.save()
			self.object = object
			return HttpResponseRedirect(reverse_lazy('meds:active-list'))
		context['form'] = form
		return render(request, self.template_name, context)


class ActiveCompoundCreate(CreateView):
	model = ActiveCompound
	template_name = 'meds/active_compound/create.html'
	pk_url_kwarg = 'active_compound_id'
	form_class = ActiveCompoundModelForm
	object = None
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['today'] = datetime.date.today()
		context['professional'] = MedsHome.get_professional(request=self.request)
		return context
	
	def get(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		context['form'] = ActiveCompoundModelForm()
		return render(request, 'meds/active_compound/create.html', context)
	
	def post(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		form = ActiveCompoundModelForm(request.POST)
		if form.is_valid():
			active_compound = form.save()
			active_compound.save()
			self.object = active_compound
			return HttpResponseRedirect(reverse_lazy('meds:active-list'))
		context['form'] = form
		return render(request, 'meds/active_compound/create.html', context)



class ActiveCompoundList(ListView):
	model = ActiveCompound
	template_name = 'meds/active_compound/list.html'
	object_list = None
	
	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		context['professional'] = MedsHome.get_professional(request=self.request)
		context['actives'] = MedsHome.all_active_compounds()
		return context
	
	def get(self, request, *args, **kwargs):
		context = self.get_context_data()
		return render(request, 'meds/active_compound/list.html', context)



class ActiveCompoundUpdate(UpdateView):
	model = ActiveCompound
	template_name = 'meds/active_compound/update.html'
	pk_url_kwarg = 'active_compound_id'
	form_class = ActiveCompoundModelForm

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['professional'] = MedsHome.get_professional(request=self.request)
		context['actives'] = MedsHome.all_active_compounds()
		return context

	def get_success_url(self):
		return reverse('meds:active-list')


class PrescriptionCreate(CreateView):
	model = Prescription
	template_name = 'care/prescription/create.html'
	pk_url_kwarg = 'prescription_id'
	form_class = PrescriptionModelForm
	object = None
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['professional'] = MedsHome.get_professional(request=self.request)
		context['relation'] = Relation.objects.get(id=self.kwargs.get('relation_id'))
		context['prescriptions'] = Prescription.objects.filter(relation_id=self.kwargs.get('relation_id'))
		context['comercial_drugs'] = ComercialDrug.objects.all()
		return context
	
	def get(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		context['form'] = PrescriptionModelForm({'relation': context['relation']})
		return render(request, self.template_name, context)
	
	def post(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		form = PrescriptionModelForm(request.POST)
		if form.is_valid():
			object = form.save()
			object.save()
			self.object = object
			return HttpResponseRedirect(reverse_lazy('care:prescription-create', args=[self.kwargs.get('relation_id')]))
		context['form'] = form
		return render(request, self.template_name, context)


class PrescriptionList(ListView):
	model = Prescription
	template_name = 'care/prescription/list.html'
	object_list = None
	
	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		context['professional'] = MedsHome.get_professional(request=self.request)
		context['relation'] = Relation.objects.get(pk=self.kwargs.get('relation_id'))
		context['prescriptions'] = Prescription.objects.filter(relation=context['relation'])
		return context


class PrescriptionYearArchiveView(YearArchiveView):
	date_field = "created"
	make_object_list = True
	allow_future = True
	
	def get_queryset(self):
		return Prescription.objects.filter(relation_id=self.kwargs.get('relation_id'))
	
	
	
def drug_autocomplete(request):
	if request.GET.get('q'):
		q = request.GET['q']
		data = ComercialDrug.objects.using('legacy').filter(pt_name__startswith=q).values_list('pt_name',flat=True)
		json = list(data)
		return JsonResponse(json, safe=False)
	else:
		HttpResponse("No cookies")