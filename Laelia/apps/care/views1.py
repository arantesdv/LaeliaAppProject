from django.shortcuts import render, reverse, get_object_or_404, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse_lazy
from django.forms import modelform_factory
from Laelia.apps.base.models import Relation, Professional
from .models import Event
from .forms import TimeLineEventModelForm

professional_type = ContentType.objects.get(app_label='base', model='professional')
professional_model = professional_type.model_class()


def index(request):
	user = request.user
	professional = Professional.objects.get(user=user)
	return render(request, 'care/index.html', {'professional': professional})


def patient_home(request):
	user = request.user
	professional = Professional.objects.get(user=user)
	return render(request, 'care/index.html', {'professional': professional})


def user_profile_view(request):
	return render(request, 'base/user_profile.html', {'user': request.user})


class EventCreate(CreateView):
	model = Event
	fields = ['relation', 'age_at_event', 'event_date', 'event_type', 'notes']
	template_name = 'care/timeline/create.html'


class EventUpdate(UpdateView):
	model = Event
	template_name = 'care/timeline/create.html'
	pk_url_kwarg = 'event_id'
	form_class = TimeLineEventModelForm
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['event'] = Event.objects.get(pk=self.kwargs['event_id'])
		return context
	
	def get_success_url(self):
		return reverse('care:event-list', kwargs={'event_id': self.pk})


class EventDelete(DeleteView):
	model = Event
	success_url = reverse_lazy('care:event-list')


class EventList(ListView):
	model = Event
	template_name = 'care/timeline/list.html'
	object_list = None
	
	def get_queryset(self):
		relation = self.get_context_data()['relation']
		return Event.objects.filter(relation_id=relation.id)
	
	def get_context_data(self, *, object_list=None, **kwargs):
		context = super(EventList, self).get_context_data(**kwargs)
		context['relation'] = Relation.objects.get(pk=self.kwargs['relation_id'])
		return context
	
	def get(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		return render(request, 'care/timeline/list.html', context)


class EventDetail(DetailView):
	model = Event
	template_name = 'care/timeline/detail.html'
	pk_url_kwarg = 'event_id'
