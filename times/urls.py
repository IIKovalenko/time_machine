from django.conf.urls import patterns, url
from times.views import TimeEntryList

urlpatterns = patterns(
    '',
    url(r'^/api/time_entry', TimeEntryList.as_view(), name='time_entry_list'),
)
