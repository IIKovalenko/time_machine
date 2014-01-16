#coding: utf-8
from rest_framework import serializers
from times.models import TimeEntry, ActionType


class TimeEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeEntry
        exclude = ('user', )


class ActionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActionType
        exclude = ('color', )
