"""Laelia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from Laelia.apps.base.views import Home, LaeliaLogin, ProfileView, LaeliaLogout

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('login/', LaeliaLogin.as_view(), name='login'),
    path('accounts/profile/', ProfileView.as_view(), name='profile'),
    path('logout/', LaeliaLogout.as_view(), name='logout'),
    path('base/', include('Laelia.apps.base.urls', namespace='base')),
    path('meds/', include('Laelia.apps.meds.urls', namespace='meds')),
    path('care/', include('Laelia.apps.care.urls', namespace='care')),
    path('core/', include('Laelia.apps.core.urls', namespace='core')),
    path('admin/', admin.site.urls),
]
