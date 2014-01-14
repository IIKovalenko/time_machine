from datetime import date
import json
from django.http import HttpResponse
from django.views.generic import TemplateView, View
from rest_framework import generics
from times.models import TimeEntry
from times.serializers import TimeEntrySerializer
from times.utils import get_datetime_from_request


class TimeEntryList(generics.ListCreateAPIView):
    queryset = TimeEntry.objects.all()
    serializer_class = TimeEntrySerializer


class UserDetailView(TemplateView):
    template_name = 'times/user_detail.html'


class UserStatisticsView(View):
    def get(self, *args, **kwargs):
        date_from = get_datetime_from_request('date_from', self.request)
        date_to = get_datetime_from_request('date_to', self.request)
        stat = TimeEntry.get_statistics(self.request.user, date_from, date_to)['actions_info']

        return HttpResponse(
            json.dumps(stat).encode('utf-8'),
            content_type='application/json'
        )
