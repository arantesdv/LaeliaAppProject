from django.shortcuts import render
from django.contrib.auth.models import User


# Create your views here.

def index_view(request):
	return render(request, 'index.html', {})


def user_profile_view(request):
	return render(request, 'base/user_profile.html', {'user': request.user})