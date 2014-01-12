from django.conf.urls import patterns, url
from times.views import TimeEntryList, UserDetailView

urlpatterns = patterns(
    '',
    url(r'^profile/', UserDetailView.as_view(), name='profile'),
    url(r'^api/time_entry', TimeEntryList.as_view(), name='time_entry_list'),
)
