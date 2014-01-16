from django.conf.urls import patterns, url
from times.views import TimeEntryList, UserDetailView, UserStatisticsView, ActionTypeList

urlpatterns = patterns(
    '',
    url(r'^profile/', UserDetailView.as_view(), name='profile'),
    url(r'^api/time_entry', TimeEntryList.as_view(), name='time_entry_list'),
    url(r'^api/action_type', ActionTypeList.as_view(), name='action_type_list'),
    url(r'^api/profile/statistics', UserStatisticsView.as_view(), name='user_statistics_view'),
)
