from django.contrib import admin
from times.models import TimeEntry, ActionType

admin.site.register(TimeEntry)
admin.site.register(ActionType)
