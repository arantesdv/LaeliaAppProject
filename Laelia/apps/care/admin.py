from django.contrib import admin

from . import models


@admin.register(models.Event)
class TimeLineEventAdmin(admin.ModelAdmin):
	list_display = ['age_at_event', 'as_paragraph']