from rest_framework import generics
from times.models import TimeEntry
from times.serializers import TimeEntrySerializer


class TimeEntryList(generics.ListCreateAPIView):
    queryset = TimeEntry.objects.all()
    serializer_class = TimeEntrySerializer