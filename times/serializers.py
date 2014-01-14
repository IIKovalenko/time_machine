#coding: utf-8
from rest_framework import serializers
from times.models import TimeEntry


class TimeEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeEntry
        exclude = ('user', )
