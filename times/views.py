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
        context['entries'] = TimeEntry.objects.filter(user=user)
        return context
