from rest_framework import serializers
from targets.models import TimeTarget


class TimeTargetSerializer(serializers.ModelSerializer):
    status = serializers.BooleanField(source='calculate_status')

    class Meta:
        model = TimeTarget
        exclude = ('user', )
