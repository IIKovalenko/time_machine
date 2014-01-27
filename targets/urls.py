from django.conf.urls import patterns, url
from targets.views import TimeTargetList

urlpatterns = patterns(
    '',
    url(r'^api/targets', TimeTargetList.as_view(), name='targets_list'),
)
