from django.conf.urls import patterns, url
from times.views import TimeEntryAddView

urlpatterns = patterns(
    '',
    url(r'^/api/time_entry/add$', TimeEntryAddView.as_view(), name='time_entry_add'),
)
