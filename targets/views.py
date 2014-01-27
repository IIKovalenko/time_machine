from rest_framework import generics
from targets.models import TimeTarget
from targets.serializers import TimeTargetSerializer
from times.views import LoginRequiredMixin


class TimeTargetList(LoginRequiredMixin, generics.ListCreateAPIView):
    queryset = TimeTarget.objects.all()
    serializer_class = TimeTargetSerializer

    def pre_save(self, obj):
        obj.user = self.request.user

    def get_queryset(self):
        return super(TimeTargetList, self).get_queryset().filter(user=self.request.user)
