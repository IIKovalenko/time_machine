import json
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, View
from rest_framework import generics
from targets.models import TimeTarget
from targets.serializers import TimeTargetSerializer
from times.color_generator import get_color
from times.models import TimeEntry, ActionType
from times.serializers import TimeEntrySerializer, ActionTypeSerializer
from times.utils import get_datetime_from_request


class LoginRequiredMixin(object):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class TimeEntryList(generics.ListCreateAPIView):
    queryset = TimeEntry.objects.all()
    serializer_class = TimeEntrySerializer

    def pre_save(self, obj):
        obj.user = self.request.user


class ActionTypeList(generics.ListCreateAPIView):
    queryset = ActionType.objects.all()
    serializer_class = ActionTypeSerializer

    def pre_save(self, obj):
        obj.color = get_color()

    def get_queryset(self):
        queryset = super(ActionTypeList, self).get_queryset()
        return queryset.filter(
            Q(user__isnull=True) | Q(user=self.request.user)
        )


class UserDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'times/user_detail.html'

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context['actions'] = [(a.pk, a.name, a.color) for a in ActionType.objects.all()]
        context['targets'] = TimeTargetSerializer(TimeTarget.objects.filter(user=self.request.user)).data
        return context


class UserStatisticsView(LoginRequiredMixin, View):
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
