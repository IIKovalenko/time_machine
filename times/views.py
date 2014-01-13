from datetime import date
from django.views.generic import TemplateView
from rest_framework import generics
from times.models import TimeEntry
from times.serializers import TimeEntrySerializer


class TimeEntryList(generics.ListCreateAPIView):
    queryset = TimeEntry.objects.all()
    serializer_class = TimeEntrySerializer


class UserDetailView(TemplateView):
    template_name = 'times/user_detail.html'

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        user = self.request.user
        context['statistics'] = TimeEntry.get_statistics(user, date(2014, 1, 1), date(2014, 1, 20))
        return context
