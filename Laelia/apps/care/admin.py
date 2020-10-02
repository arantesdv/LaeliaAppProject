from django.contrib import admin

from . import models


@admin.register(models.TimeLineEvent)
class TimeLineEventAdmin(admin.ModelAdmin):
	pass