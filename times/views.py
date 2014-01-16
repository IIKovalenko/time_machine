import json
from django.http import HttpResponse
from django.views.generic import TemplateView, View
from rest_framework import generics
from times.models import TimeEntry, ActionType
from times.serializers import TimeEntrySerializer
from times.utils import get_datetime_from_request


class TimeEntryList(generics.ListCreateAPIView):
    queryset = TimeEntry.objects.all()
    serializer_class = TimeEntrySerializer

    def pre_save(self, obj):
        obj.user = self.request.user


class UserDetailView(TemplateView):
    template_name = 'times/user_detail.html'

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context['actions'] = [(a.pk, a.name) for a in ActionType.objects.all()]
        return context


class UserStatisticsView(View):
    def get(self, *args, **kwargs):
        date_from = get_datetime_from_request('date_from', self.request)
        date_to = get_datetime_from_request('date_to', self.request)
        if not (date_from and date_to):
            return self.json_response({'errors': ['Specify date_from and date_to GET params.']})
        stat = TimeEntry.get_statistics(self.request.user, date_from, date_to)['actions_info']
        return self.json_response(stat)

    def json_response(self, data):
        return HttpResponse(
            json.dumps(data).encode('utf-8'),
            content_type='application/json'
        )
