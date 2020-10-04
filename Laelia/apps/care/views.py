import datetime
from django.urls import reverse_lazy
from django.shortcuts import render, reverse, get_object_or_404, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.views.generic.edit import FormView
from Laelia.apps.base.models import Relation, Professional, Patient, Schedule
from .models import Event
from .forms import TimeLineEventModelForm
from django.forms import inlineformset_factory


class RelationDetail(DetailView):
	model = Relation
	template_name = 'care/relation/relation_detail.html'
	pk_url_kwarg = 'relation_id'

	

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(**kwargs)
		context['relation'] = get_object_or_404(Relation, pk=self.kwargs.get('relation_id'))
		context['schedules'] = Schedule.objects.filter(relation=context['relation'].id)
		context['events'] = Event.objects.filter(relation=context['relation'].id)
		return context
	

class EventCreate(CreateView):
	form_class = TimeLineEventModelForm
	template_name = 'care/event/event_create.html'

	
	def get_context_data(self, **kwargs):
		context = super(EventCreate, self).get_context_data(**kwargs)
		context['relation'] = Relation.objects.get(pk=self.kwargs.get('relation_id'))
		context['form'] = TimeLineEventModelForm({'relation_id': context['relation'].id, 'event_date': datetime.date.today()})
		return context
	
	# def get_success_url(self):
	# 	return reverse('care:relation-detail', kwargs={'relation_id': self.kwargs.get('relation_id')})

class EventDetail(DetailView):
	model = Event
	template_name = 'care/event/detail.html'
	pk_url_kwarg = ['relation_id', 'event_id']
	
	
	def get_context_data(self, **kwargs):
		context = super(EventDetail, self).get_context_data(**kwargs)
		context['event'] = Event.objects.get(pk=self.kwargs.get('event_id'))
		context['relation'] = Relation.objects.get(pk=self.kwargs.get('relation_id'))
		return context


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

#
# class EventDetail(DetailView):
# 	model = Event
# 	template_name = 'care/timeline/detail.html'
# 	pk_url_kwarg = 'event_id'



class EventDelete(DeleteView):
	model = Event
	success_url = reverse_lazy('care:event-list')


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