from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView


# Create your views here.

class RelationView(LoginRequiredMixin, DetailView):
	login_url = '/accounts/login/'
	redirect_field_name = None
