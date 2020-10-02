from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.contenttypes.models import ContentType
from Laelia.apps.base.models import Relation


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
	template_name = 'care/patient/detail.html'
	slug_url_kwarg = 'relation_slug'
	pk_url_kwarg = 'relation_id'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['relation'] = get_object_or_404(Relation, pk=self.kwargs['relation_id'])
		context['patient_relations'] = Relation.objects.filter(patient=context['relation'].patient)
		return context


def index_view(request):
	return render(request, 'index.html', {})


def user_profile_view(request):
	return render(request, 'base/user_profile.html', {'user': request.user})